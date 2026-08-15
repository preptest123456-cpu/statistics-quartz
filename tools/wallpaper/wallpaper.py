#!/usr/bin/env python3
"""Generate a photorealistic desktop wallpaper from a text prompt.

Talks to the OpenAI Images API over plain HTTPS (stdlib only), then fits the
returned image to the requested wallpaper resolution.

Why this exists in its current shape — the source models do not render 16:9:

    gpt-image-1  ->  1536x1024  (1.500)  vs 3840x2160 (1.778)
    dall-e-3     ->  1792x1024  (1.750)  vs 3840x2160 (1.778)

A naive "scale to cover, then center-crop" pipeline therefore deletes 7.8% of
the frame off the top *and* the bottom of a gpt-image-1 render — which is
exactly where wallpaper prompts tend to put a soaring bird, a horse's hooves,
or a porch floor. This script never crops silently: it defaults to --fit pad
(nothing is lost), prints the exact pixel loss for any lossy fit, and can pick
the model whose native aspect ratio is closest to the target.

Exit codes:
    0   success
    2   usage / configuration error
    3   API error (after retries)
    4   local I/O or image-processing error
    130 interrupted
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_API = 3
EXIT_IO = 4
EXIT_INTERRUPT = 130

API_URL = "https://api.openai.com/v1/images/generations"

# Sizes each model can actually return, plus its per-request image cap.
MODELS: dict[str, dict[str, Any]] = {
    "gpt-image-1": {
        "sizes": [(1024, 1024), (1536, 1024), (1024, 1536)],
        "max_n": 10,
        "revises_prompt": False,
        "note": "best material rendering (fur, feathers, leather); most literal prompt following",
    },
    "dall-e-3": {
        "sizes": [(1024, 1024), (1792, 1024), (1024, 1792)],
        "max_n": 1,
        "revises_prompt": True,
        "note": "widest native frame (1.75); rewrites the prompt server-side",
    },
}

# Appended to the prompt unless --no-compose-guard. Keeps subjects out of the
# bands a wide crop would eat, and out of the corner the OS puts icons in.
COMPOSE_GUARD = (
    "Composition: frame this for a wide {aspect} crop. Leave generous empty "
    "headroom above the highest subject and generous empty ground below the "
    "lowest subject; keep every important subject entirely within the central "
    "horizontal band of the frame, well clear of the top and bottom edges. "
    "Keep the upper-left third of the image relatively uncluttered and low in "
    "detail so desktop icons remain legible over it."
)

RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FitPlan:
    src: tuple[int, int]
    dst: tuple[int, int]
    fit: str
    scale: float
    scaled: tuple[int, int]
    crop_box: tuple[int, int, int, int] | None
    pad: tuple[int, int]  # (bar_w each side, bar_h each side)
    lost_px: tuple[int, int]  # (per-side x, per-side y) cropped, in target pixels
    lost_frac: float  # fraction of the source frame discarded

    def describe(self) -> str:
        sw, sh = self.src
        dw, dh = self.dst
        lines = [
            f"source {sw}x{sh} ({sw / sh:.3f})  ->  target {dw}x{dh} ({dw / dh:.3f})",
            f"fit={self.fit}  scale={self.scale:.4f}  scaled={self.scaled[0]}x{self.scaled[1]}",
        ]
        if self.fit == "cover":
            assert self.crop_box is not None
            left, top, right, bottom = self.crop_box
            nw, nh = self.scaled
            lines.append(
                f"crop discards {top}px top / {nh - bottom}px bottom and "
                f"{left}px left / {nw - right}px right, in target pixels "
                f"({self.lost_frac * 100:.1f}% of the source frame)"
            )
        elif self.fit == "pad":
            pw, ph = self.pad
            lines.append(f"pad adds {pw}px side bars and {ph}px top/bottom bars (nothing cropped)")
        else:
            lines.append("no resampling; the raw model output is written as-is")
        return "\n".join("  " + line for line in lines)


def plan_fit(
    src: tuple[int, int], dst: tuple[int, int], fit: str, anchor: float
) -> FitPlan:
    sw, sh = src
    dw, dh = dst

    if fit == "none":
        return FitPlan(src, src, fit, 1.0, src, None, (0, 0), (0, 0), 0.0)

    if fit == "cover":
        scale = max(dw / sw, dh / sh)
        nw, nh = max(dw, round(sw * scale)), max(dh, round(sh * scale))
        off_x = int(round((nw - dw) * 0.5))
        off_y = int(round((nh - dh) * anchor))
        box = (off_x, off_y, off_x + dw, off_y + dh)
        lost_x = (nw - dw) // 2
        lost_y = (nh - dh) // 2
        kept = (dw / scale) * (dh / scale)
        lost_frac = max(0.0, 1.0 - kept / (sw * sh))
        return FitPlan(src, dst, fit, scale, (nw, nh), box, (0, 0), (lost_x, lost_y), lost_frac)

    if fit == "pad":
        scale = min(dw / sw, dh / sh)
        nw, nh = min(dw, round(sw * scale)), min(dh, round(sh * scale))
        return FitPlan(
            src, dst, fit, scale, (nw, nh), None, ((dw - nw) // 2, (dh - nh) // 2), (0, 0), 0.0
        )

    raise ValueError(f"unknown fit mode: {fit}")


def aspect_penalty(size: tuple[int, int], dst: tuple[int, int]) -> float:
    """How far a source size is from the target aspect, in log space."""
    return abs(math.log((size[0] / size[1]) / (dst[0] / dst[1])))


def choose_size(model: str, dst: tuple[int, int], requested: str | None) -> tuple[int, int]:
    sizes = MODELS[model]["sizes"]
    if requested:
        try:
            w, h = (int(part) for part in requested.lower().split("x", 1))
        except ValueError:
            raise ValueError(f"--size must look like 1536x1024, got {requested!r}") from None
        if (w, h) not in sizes:
            offered = ", ".join(f"{a}x{b}" for a, b in sizes)
            raise ValueError(f"{model} does not offer {requested}; it offers {offered}")
        return (w, h)
    return min(sizes, key=lambda s: aspect_penalty(s, dst))


def choose_model(dst: tuple[int, int], fit: str) -> str:
    """Pick the model whose best native size loses the least to a cover crop.

    Only consulted for --model auto. With --fit pad nothing is ever cropped, so
    quality wins and we stay on gpt-image-1.
    """
    if fit != "cover":
        return "gpt-image-1"
    return min(
        MODELS,
        key=lambda m: aspect_penalty(choose_size(m, dst, None), dst),
    )


def report_model_tradeoff(dst: tuple[int, int], anchor: float, out=sys.stderr) -> None:
    print("model frame trade-off for this target:", file=out)
    for model, spec in MODELS.items():
        size = choose_size(model, dst, None)
        plan = plan_fit(size, dst, "cover", anchor)
        print(
            f"  {model:<12} {size[0]}x{size[1]} ({size[0] / size[1]:.3f})"
            f"  cover-crop loses {plan.lost_frac * 100:5.1f}%"
            f"  ({plan.lost_px[1]}px per side vertically)"
            f"  — {spec['note']}",
            file=out,
        )


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------


class ApiError(RuntimeError):
    pass


def _sleep_for(attempt: int, base: float, retry_after: float | None) -> float:
    if retry_after is not None:
        return min(retry_after, 60.0)
    # Real exponential growth plus full jitter. The delay must be recomputed
    # every attempt — a fixed sleep inside the loop is not a backoff.
    return min(base * (2**attempt), 60.0) * (0.5 + random.random() * 0.5)


def request_images(
    *,
    api_key: str,
    model: str,
    prompt: str,
    size: tuple[int, int],
    n: int,
    quality: str | None,
    retries: int,
    backoff: float,
    timeout: float,
    verbose: bool,
) -> list[dict[str, Any]]:
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": f"{size[0]}x{size[1]}",
    }
    if quality:
        payload["quality"] = quality
    if model == "dall-e-3":
        # dall-e-3 returns URLs unless told otherwise; b64 keeps it one round trip.
        payload["response_format"] = "b64_json"

    body = json.dumps(payload).encode("utf-8")
    last: Exception | None = None

    for attempt in range(retries + 1):
        req = urllib.request.Request(
            API_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
            data = parsed.get("data")
            if not data:
                raise ApiError(f"response contained no images: {parsed!r}")
            return data
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:800]
            last = ApiError(f"HTTP {exc.code}: {detail}")
            if exc.code not in RETRY_STATUS or attempt == retries:
                break
            header = exc.headers.get("Retry-After") if exc.headers else None
            try:
                retry_after = float(header) if header else None
            except ValueError:
                retry_after = None
            delay = _sleep_for(attempt, backoff, retry_after)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = ApiError(f"{type(exc).__name__}: {exc}")
            if attempt == retries:
                break
            delay = _sleep_for(attempt, backoff, None)

        if verbose:
            print(
                f"  attempt {attempt + 1}/{retries + 1} failed ({last}); "
                f"retrying in {delay:.1f}s",
                file=sys.stderr,
            )
        time.sleep(delay)

    raise last if last else ApiError("request failed for an unknown reason")


# --------------------------------------------------------------------------
# image output
# --------------------------------------------------------------------------


def load_pillow():
    try:
        from PIL import Image, ImageFilter  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "Pillow is required for --fit pad/cover. Install it with "
            "`python -m pip install Pillow`, or pass --fit none to write the "
            "raw model output."
        ) from exc
    return Image, ImageFilter


def feather_mask(size: tuple[int, int], pad: tuple[int, int], feather: int):
    """Alpha mask that fades the sharp image out over the edges facing a bar.

    Without it the pasted image meets its own blurred continuation at a hard
    line, which reads as a visible rectangle on a wallpaper.
    """
    from PIL import Image, ImageDraw  # noqa: PLC0415

    w, h = size
    mask = Image.new("L", size, 255)
    draw = ImageDraw.Draw(mask)
    feather = max(1, min(feather, w // 2, h // 2))
    for i in range(feather):
        value = int(255 * (i + 1) / (feather + 1))
        if pad[0] > 0:
            draw.line([(i, 0), (i, h - 1)], fill=value)
            draw.line([(w - 1 - i, 0), (w - 1 - i, h - 1)], fill=value)
        if pad[1] > 0:
            draw.line([(0, i), (w - 1, i)], fill=value)
            draw.line([(0, h - 1 - i), (w - 1, h - 1 - i)], fill=value)
    return mask


def render(raw: bytes, plan: FitPlan, dest: Path, *, blur_fill: bool) -> None:
    if plan.fit == "none":
        dest.write_bytes(raw)
        return

    import io  # noqa: PLC0415

    Image, ImageFilter = load_pillow()
    with Image.open(io.BytesIO(raw)) as src_img:
        img = src_img.convert("RGB")

        if plan.fit == "cover":
            scaled = img.resize(plan.scaled, Image.LANCZOS)
            out = scaled.crop(plan.crop_box)
        else:  # pad
            dw, dh = plan.dst
            sharp = img.resize(plan.scaled, Image.LANCZOS)
            if blur_fill:
                # Fill the bars with a blurred copy of the same frame stretched
                # to the target, so the extension reads as continued sky and
                # ground instead of black letterboxing. Stretching (rather than
                # cover-scaling) keeps the horizon at the same height as the
                # sharp image, so the join has nothing to line up wrongly.
                bg = img.resize((dw, dh), Image.LANCZOS)
                out = bg.filter(ImageFilter.GaussianBlur(radius=max(dw, dh) / 90))
                mask = feather_mask(plan.scaled, plan.pad, feather=max(8, min(dw, dh) // 40))
                out.paste(sharp, plan.pad, mask)
            else:
                out = Image.new("RGB", (dw, dh), (0, 0, 0))
                out.paste(sharp, plan.pad)

        params: dict[str, Any] = {}
        if dest.suffix.lower() in {".jpg", ".jpeg"}:
            params = {"quality": 95, "subsampling": 0}
        out.save(dest, **params)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_resolution(text: str) -> tuple[int, int]:
    try:
        w, h = (int(part) for part in text.lower().split("x", 1))
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected WIDTHxHEIGHT, got {text!r}") from None
    if w <= 0 or h <= 0:
        raise argparse.ArgumentTypeError("resolution must be positive")
    return (w, h)


def parse_anchor(text: str) -> float:
    named = {"top": 0.0, "center": 0.5, "centre": 0.5, "middle": 0.5, "bottom": 1.0}
    if text.lower() in named:
        return named[text.lower()]
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "expected top/center/bottom or a float in [0, 1]"
        ) from None
    if not 0.0 <= value <= 1.0:
        raise argparse.ArgumentTypeError("anchor must be within [0, 1]")
    return value


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="wallpaper.py",
        description="Generate a photorealistic wallpaper at a target resolution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  wallpaper.py --dry-run\n"
            "  wallpaper.py -n 3 --out ./out\n"
            "  wallpaper.py --fit cover --crop-anchor top   # crop, protect the sky\n"
            "  wallpaper.py --model dall-e-3                # widest native frame\n"
        ),
    )
    src = p.add_mutually_exclusive_group()
    src.add_argument(
        "--prompt-file",
        type=Path,
        default=Path(__file__).with_name("prompt.txt"),
        help="file holding the scene prompt (default: prompt.txt beside this script)",
    )
    src.add_argument("--prompt", help="inline prompt text, overrides --prompt-file")

    p.add_argument(
        "--model",
        choices=[*MODELS, "auto"],
        default="gpt-image-1",
        help="image model (default: gpt-image-1)",
    )
    p.add_argument("--size", help="force a source size, e.g. 1536x1024")
    p.add_argument("--quality", help="model quality hint, e.g. high / hd")
    p.add_argument(
        "--resolution",
        type=parse_resolution,
        default=(3840, 2160),
        help="target wallpaper resolution (default: 3840x2160)",
    )
    p.add_argument(
        "--fit",
        choices=["pad", "cover", "none"],
        default="pad",
        help=(
            "pad: scale to fit, fill the bars with a blurred continuation, lose "
            "nothing (default). cover: scale and crop to fill, loses edges. "
            "none: write the raw model output."
        ),
    )
    p.add_argument(
        "--crop-anchor",
        type=parse_anchor,
        default=0.5,
        metavar="POS",
        help="for --fit cover: top/center/bottom or 0..1, which edge to protect",
    )
    p.add_argument(
        "--no-blur-fill",
        action="store_true",
        help="for --fit pad: use black bars instead of a blurred continuation",
    )
    p.add_argument("-n", "--count", type=int, default=1, help="images to request (default: 1)")
    p.add_argument("--out", type=Path, default=Path("."), help="output directory (default: .)")
    p.add_argument("--basename", default="wallpaper", help="output filename stem")
    p.add_argument(
        "--format", choices=["png", "jpg"], default="png", help="output format (default: png)"
    )
    p.add_argument(
        "--keep-original", action="store_true", help="also save the unmodified model output"
    )
    p.add_argument(
        "--no-compose-guard",
        action="store_true",
        help="do not append the framing/uncluttered-corner instructions to the prompt",
    )
    p.add_argument("--retries", type=int, default=4, help="retry attempts (default: 4)")
    p.add_argument("--backoff", type=float, default=2.0, help="base backoff seconds (default: 2)")
    p.add_argument("--timeout", type=float, default=300.0, help="per-request timeout seconds")
    p.add_argument(
        "--dry-run", action="store_true", help="print the plan and prompt; make no API call"
    )
    p.add_argument("-v", "--verbose", action="store_true", help="log retries and payload details")
    return p


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        text = args.prompt
    else:
        if not args.prompt_file.is_file():
            raise FileNotFoundError(f"prompt file not found: {args.prompt_file}")
        text = args.prompt_file.read_text(encoding="utf-8")
    text = text.strip()
    if not text:
        raise ValueError("prompt is empty")
    return text


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dst = args.resolution

    try:
        prompt = load_prompt(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    model = choose_model(dst, args.fit) if args.model == "auto" else args.model
    spec = MODELS[model]

    if args.count < 1:
        print("error: -n must be at least 1", file=sys.stderr)
        return EXIT_USAGE
    count = args.count
    if count > spec["max_n"]:
        print(
            f"warning: {model} accepts at most n={spec['max_n']} per request; "
            f"clamping -n {count} to {spec['max_n']}",
            file=sys.stderr,
        )
        count = spec["max_n"]

    try:
        size = choose_size(model, dst, args.size)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if not args.no_compose_guard:
        aspect = f"{dst[0] // math.gcd(*dst)}:{dst[1] // math.gcd(*dst)}"
        prompt = f"{prompt}\n\n{COMPOSE_GUARD.format(aspect=aspect)}"

    plan = plan_fit(size, dst, args.fit, args.crop_anchor)

    print(f"model: {model} (n={count}, size={size[0]}x{size[1]})", file=sys.stderr)
    print(plan.describe(), file=sys.stderr)
    if args.fit == "cover" and plan.lost_frac > 0.02:
        print(
            "warning: this crop deletes a meaningful band of the frame. Anything "
            "the prompt places near the top or bottom edge (birds in flight, "
            "hooves, foreground floor) can be cut. Use --fit pad, --crop-anchor, "
            "or --model dall-e-3 for a wider native frame.",
            file=sys.stderr,
        )
    if args.verbose or args.model == "auto":
        report_model_tradeoff(dst, args.crop_anchor)

    if args.dry_run:
        print("\n--- prompt as sent ---", file=sys.stderr)
        print(prompt, file=sys.stderr)
        print("--- end prompt ---", file=sys.stderr)
        print("dry run: no API call made", file=sys.stderr)
        return EXIT_OK

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("error: OPENAI_API_KEY is not set", file=sys.stderr)
        return EXIT_USAGE

    try:
        data = request_images(
            api_key=api_key,
            model=model,
            prompt=prompt,
            size=size,
            n=count,
            quality=args.quality,
            retries=args.retries,
            backoff=args.backoff,
            timeout=args.timeout,
            verbose=args.verbose,
        )
    except ApiError as exc:
        print(f"error: image request failed: {exc}", file=sys.stderr)
        return EXIT_API

    try:
        args.out.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory: {exc}", file=sys.stderr)
        return EXIT_IO

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    written = 0
    for index, item in enumerate(data, start=1):
        suffix = f"-{index}" if len(data) > 1 else ""
        stem = f"{args.basename}-{stamp}{suffix}"

        b64 = item.get("b64_json")
        if not b64:
            print(
                f"error: image {index} carried no b64_json "
                f"(keys: {sorted(item)}); nothing written",
                file=sys.stderr,
            )
            continue
        try:
            raw = base64.b64decode(b64)
        except (ValueError, TypeError) as exc:
            print(f"error: image {index} was not valid base64: {exc}", file=sys.stderr)
            continue

        # dall-e-3 silently rewrites the prompt. Surface and persist it, or the
        # scene drifts with no record of how.
        revised = item.get("revised_prompt")
        if revised:
            sidecar = args.out / f"{stem}.revised_prompt.txt"
            try:
                sidecar.write_text(revised + "\n", encoding="utf-8")
            except OSError as exc:
                print(f"warning: could not write {sidecar}: {exc}", file=sys.stderr)
            print(f"\n[{index}] model-revised prompt (saved to {sidecar.name}):", file=sys.stderr)
            print(revised, file=sys.stderr)
        elif spec["revises_prompt"]:
            print(f"[{index}] warning: no revised_prompt returned", file=sys.stderr)

        try:
            if args.keep_original:
                original = args.out / f"{stem}-original.png"
                original.write_bytes(raw)
                print(f"[{index}] wrote {original}", file=sys.stderr)
            dest = args.out / f"{stem}.{args.format}"
            render(raw, plan, dest, blur_fill=not args.no_blur_fill)
        except (OSError, RuntimeError) as exc:
            print(f"error: could not write image {index}: {exc}", file=sys.stderr)
            continue

        written += 1
        print(f"[{index}] wrote {dest} ({dst[0]}x{dst[1]})", file=sys.stderr)

    if written == 0:
        print("error: no images were written", file=sys.stderr)
        return EXIT_IO
    if written < len(data):
        print(f"warning: only {written} of {len(data)} images were written", file=sys.stderr)
        return EXIT_IO
    return EXIT_OK


if __name__ == "__main__":
    try:
        # The process must exit with main()'s status; `main()` alone (or
        # sys.exit() with no argument) always reports success.
        sys.exit(main())
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        sys.exit(EXIT_INTERRUPT)
