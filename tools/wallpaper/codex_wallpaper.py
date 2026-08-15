#!/usr/bin/env python3
"""Single-file photorealistic wallpaper generator — paste-and-run.

    pip install Pillow
    export OPENAI_API_KEY=sk-...
    python codex_wallpaper.py -n 3

Everything is in this one file: the scene prompt, the API call (stdlib only),
and the resize. Pillow is the sole dependency, and only for the resize.

Why the fitting is not a plain centre crop
------------------------------------------
Neither model renders 16:9. gpt-image-1 returns 1536x1024 (1.500) against a
3840x2160 target (1.778), so "scale to cover, then centre crop" silently
deletes 200px off the top AND 200px off the bottom — 7.8% at each edge, which
is exactly where this scene puts the soaring eagle and the horse's hooves.
dall-e-3's 1792x1024 loses only 17px per edge but renders materials worse and
rewrites your prompt server-side.

So --fit pad (the default) scales to fit and fills the side bars with a
blurred copy of the same frame, losing nothing. --fit cover still crops, but
prints exactly what it removed and takes --anchor top to protect the sky.

Exit codes: 0 ok, 2 usage, 3 API failure, 4 local I/O, 130 interrupt.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROMPT = """\
A photorealistic wide landscape photograph of a hand-hewn log cabin at golden
hour in the northern Rocky Mountains, shot on a full-frame camera with a 35mm
lens at f/8, natural light, no lens flare, no text, no watermark.

The cabin sits right of centre on a low rise, weathered logs and chinking, a
stone chimney with a thin line of woodsmoke. A covered porch runs across its
front: rough-sawn planks, a split-log bench, a lever-action hunting rifle
resting against the porch post, and a US flag hanging from a bracket on the
porch beam, moving slightly in the breeze.

A bald eagle soars in front of and above the cabin, wings fully spread, banking
slightly toward the camera, sunlit from behind so the white head and tail read
clearly against the sky. Keep the eagle low in the upper half of the frame with
open sky above it — do not let the wingtips approach the top edge.

A German shepherd stands alert on the grass at the foot of the porch steps, full
body visible including all four feet. A chestnut quarter horse stands a few
paces to its right, saddled, head slightly lowered, with its legs and hooves
fully in frame and clear of the bottom edge.

A shallow river runs across the foreground from left to right, catching warm
low-angle light on the ripples, with round river stones along the near bank.
Pine and aspen fill the middle distance; snow-dusted peaks rise behind under a
clear late-afternoon sky with a few high cirrus clouds.

Composition: frame this for a wide 16:9 crop. Leave generous empty sky above the
eagle and generous empty ground below the porch; keep every important subject
entirely within the central horizontal band, well clear of the top and bottom
edges. Keep the upper-left third relatively uncluttered and low in detail so
desktop icons remain legible over it.

Render every element with photographic realism: individual feathers on the
eagle, coarse guard hairs in the dog's coat, the sheen on the horse's flank,
grain and cracks in the porch timber, and the correct US flag with thirteen
stripes beginning and ending in red and a fifty-star canton.
"""

API_URL = "https://api.openai.com/v1/images/generations"
SIZES = {"gpt-image-1": (1536, 1024), "dall-e-3": (1792, 1024)}
MAX_N = {"gpt-image-1": 10, "dall-e-3": 1}
RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}


def call_api(key, model, prompt, n, quality, retries, timeout, verbose):
    payload = {"model": model, "prompt": prompt, "n": n,
               "size": "{}x{}".format(*SIZES[model])}
    if quality:
        payload["quality"] = quality
    if model == "dall-e-3":
        payload["response_format"] = "b64_json"
    body = json.dumps(payload).encode()
    last = None

    for attempt in range(retries + 1):
        req = urllib.request.Request(
            API_URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode()).get("data")
            if not data:
                raise RuntimeError("response contained no images")
            return data
        except urllib.error.HTTPError as exc:
            last = RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:400]}")
            if exc.code not in RETRY_STATUS or attempt == retries:
                break
            header = exc.headers.get("Retry-After") if exc.headers else None
            wait = float(header) if header and header.isdigit() else None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            last = RuntimeError(f"{type(exc).__name__}: {exc}")
            if attempt == retries:
                break
            wait = None
        # Real exponential backoff with jitter — recomputed every attempt.
        delay = min(wait, 60.0) if wait else min(2.0 * 2**attempt, 60.0) * (0.5 + random.random() / 2)
        if verbose:
            print(f"  attempt {attempt + 1} failed ({last}); retrying in {delay:.1f}s", file=sys.stderr)
        time.sleep(delay)

    raise last or RuntimeError("request failed")


def fit_image(raw, dst, fit, anchor, dest):
    from PIL import Image, ImageDraw, ImageFilter
    import io

    dw, dh = dst
    with Image.open(io.BytesIO(raw)) as src:
        img = src.convert("RGB")
        sw, sh = img.size

        if fit == "cover":
            scale = max(dw / sw, dh / sh)
            nw, nh = max(dw, round(sw * scale)), max(dh, round(sh * scale))
            off_y = int(round((nh - dh) * anchor))
            print(f"  cover: discarding {off_y}px top / {nh - dh - off_y}px bottom", file=sys.stderr)
            out = img.resize((nw, nh), Image.LANCZOS).crop(((nw - dw) // 2, off_y,
                                                           (nw - dw) // 2 + dw, off_y + dh))
        else:  # pad — nothing is cropped
            scale = min(dw / sw, dh / sh)
            nw, nh = min(dw, round(sw * scale)), min(dh, round(sh * scale))
            pad = ((dw - nw) // 2, (dh - nh) // 2)
            print(f"  pad: {pad[0]}px side bars, {pad[1]}px top/bottom bars, nothing cropped",
                  file=sys.stderr)
            sharp = img.resize((nw, nh), Image.LANCZOS)
            # Stretch (not cover-scale) the fill so the horizon stays at the
            # same height across the join, then feather the seam.
            out = img.resize((dw, dh), Image.LANCZOS).filter(
                ImageFilter.GaussianBlur(radius=max(dw, dh) / 90))
            feather = max(8, min(dw, dh) // 40)
            mask = Image.new("L", (nw, nh), 255)
            draw = ImageDraw.Draw(mask)
            for i in range(min(feather, nw // 2, nh // 2)):
                value = int(255 * (i + 1) / (feather + 1))
                if pad[0] > 0:
                    draw.line([(i, 0), (i, nh - 1)], fill=value)
                    draw.line([(nw - 1 - i, 0), (nw - 1 - i, nh - 1)], fill=value)
                if pad[1] > 0:
                    draw.line([(0, i), (nw - 1, i)], fill=value)
                    draw.line([(0, nh - 1 - i), (nw - 1, nh - 1 - i)], fill=value)
            out.paste(sharp, pad, mask)

        out.save(dest)


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate a photorealistic 4K wallpaper.")
    p.add_argument("--model", choices=list(SIZES), default="gpt-image-1")
    p.add_argument("-n", "--count", type=int, default=1)
    p.add_argument("--fit", choices=["pad", "cover", "none"], default="pad")
    p.add_argument("--anchor", choices=["top", "center", "bottom"], default="center",
                   help="for --fit cover: which edge to protect")
    p.add_argument("--width", type=int, default=3840)
    p.add_argument("--height", type=int, default=2160)
    p.add_argument("--quality", help="model quality hint, e.g. high / hd")
    p.add_argument("--out", type=Path, default=Path("."))
    p.add_argument("--retries", type=int, default=4)
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--prompt-file", type=Path, help="use this file instead of the built-in scene")
    p.add_argument("--from-file", type=Path, metavar="IMAGE",
                   help="skip the API and just fit an image you already have (no key needed)")
    p.add_argument("--dry-run", action="store_true", help="print the plan, make no API call")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    dst = (args.width, args.height)
    anchor = {"top": 0.0, "center": 0.5, "bottom": 1.0}[args.anchor]
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else PROMPT

    n = max(1, args.count)
    if n > MAX_N[args.model]:
        print(f"warning: {args.model} caps n at {MAX_N[args.model]}; clamping from {n}",
              file=sys.stderr)
        n = MAX_N[args.model]

    sw, sh = SIZES[args.model]
    print(f"{args.model}: {sw}x{sh} ({sw / sh:.3f}) -> {dst[0]}x{dst[1]} "
          f"({dst[0] / dst[1]:.3f}), fit={args.fit}, n={n}", file=sys.stderr)

    # Fit an image you already have (e.g. downloaded from a chat UI). No key needed.
    if args.from_file:
        if not args.from_file.is_file():
            print(f"error: no such file: {args.from_file}", file=sys.stderr)
            return 2
        try:
            args.out.mkdir(parents=True, exist_ok=True)
            dest = args.out / f"{args.from_file.stem}-{dst[0]}x{dst[1]}.png"
            fit_image(args.from_file.read_bytes(), dst, args.fit, anchor, dest)
        except (OSError, ImportError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 4
        print(f"wrote {dest}", file=sys.stderr)
        return 0

    if args.dry_run:
        print("\n--- prompt ---\n" + prompt + "--- end ---\ndry run: no API call", file=sys.stderr)
        return 0

    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        print("error: OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    try:
        data = call_api(key, args.model, prompt, n, args.quality,
                        args.retries, args.timeout, args.verbose)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    try:
        args.out.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    written = 0
    for i, item in enumerate(data, 1):
        if not item.get("b64_json"):
            print(f"error: image {i} had no b64_json", file=sys.stderr)
            continue
        raw = base64.b64decode(item["b64_json"])
        stem = f"wallpaper-{stamp}" + (f"-{i}" if len(data) > 1 else "")

        # dall-e-3 rewrites prompts silently; surface it or the scene drifts unseen.
        if item.get("revised_prompt"):
            (args.out / f"{stem}.revised_prompt.txt").write_text(item["revised_prompt"] + "\n")
            print(f"[{i}] model-revised prompt:\n{item['revised_prompt']}", file=sys.stderr)

        dest = args.out / f"{stem}.png"
        try:
            if args.fit == "none":
                dest.write_bytes(raw)
            else:
                fit_image(raw, dst, args.fit, anchor, dest)
        except (OSError, ImportError) as exc:
            print(f"error: image {i}: {exc}", file=sys.stderr)
            continue
        written += 1
        print(f"[{i}] wrote {dest}", file=sys.stderr)

    if written < len(data):
        return 4  # never report success when an image was lost
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())  # exit with main()'s status, not an implicit 0
    except KeyboardInterrupt:
        sys.exit(130)
