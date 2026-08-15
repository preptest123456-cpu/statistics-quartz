"""Offline tests for wallpaper.py — no API key and no network required.

Run with `python -m pytest test_wallpaper.py`, or plainly with
`python test_wallpaper.py`.
"""

from __future__ import annotations

import io
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import wallpaper as w  # noqa: E402

UHD = (3840, 2160)


# --- geometry ------------------------------------------------------------


def test_cover_crop_from_gpt_image_1_loses_200px_per_edge():
    """The bug this tool exists to prevent, pinned to exact numbers."""
    plan = w.plan_fit((1536, 1024), UHD, "cover", 0.5)
    assert plan.scale == 2.5
    assert plan.scaled == (3840, 2560)
    assert plan.crop_box == (0, 200, 3840, 2360)
    assert plan.lost_px == (0, 200)
    assert round(plan.lost_frac * 100, 1) == 15.6


def test_cover_crop_from_dall_e_3_is_nearly_lossless():
    plan = w.plan_fit((1792, 1024), UHD, "cover", 0.5)
    assert plan.crop_box == (0, 17, 3840, 2177)
    assert plan.lost_frac < 0.02


def test_crop_anchor_moves_the_whole_loss_to_one_edge():
    top = w.plan_fit((1536, 1024), UHD, "cover", 0.0)
    bottom = w.plan_fit((1536, 1024), UHD, "cover", 1.0)
    assert top.crop_box == (0, 0, 3840, 2160)  # sky survives intact
    assert bottom.crop_box == (0, 400, 3840, 2560)  # ground survives intact


def test_pad_never_crops_and_fills_the_target():
    plan = w.plan_fit((1536, 1024), UHD, "pad", 0.5)
    assert plan.scaled == (3240, 2160)
    assert plan.pad == (300, 0)
    assert plan.lost_frac == 0.0
    assert plan.scaled[0] + 2 * plan.pad[0] == UHD[0]
    assert plan.scaled[1] + 2 * plan.pad[1] == UHD[1]


def test_portrait_target_pads_top_and_bottom():
    plan = w.plan_fit((1536, 1024), (1440, 2560), "pad", 0.5)
    assert plan.pad[0] == 0 and plan.pad[1] > 0


def test_fit_none_is_a_passthrough():
    plan = w.plan_fit((1536, 1024), UHD, "none", 0.5)
    assert plan.scale == 1.0 and plan.crop_box is None and plan.lost_frac == 0.0


# --- model and size selection --------------------------------------------


def test_auto_size_picks_the_widest_offered_frame_for_a_16_9_target():
    assert w.choose_size("gpt-image-1", UHD, None) == (1536, 1024)
    assert w.choose_size("dall-e-3", UHD, None) == (1792, 1024)


def test_auto_model_prefers_the_wider_frame_only_when_cropping():
    assert w.choose_model(UHD, "cover") == "dall-e-3"
    assert w.choose_model(UHD, "pad") == "gpt-image-1"


def test_unsupported_size_is_rejected_with_the_offered_list():
    try:
        w.choose_size("gpt-image-1", UHD, "999x999")
    except ValueError as exc:
        assert "1536x1024" in str(exc)
    else:
        raise AssertionError("expected ValueError")


# --- retry backoff -------------------------------------------------------


def test_backoff_grows_and_stays_capped():
    random.seed(1)
    delays = [w._sleep_for(attempt, 2.0, None) for attempt in range(8)]
    assert delays[0] < delays[4]
    assert all(d <= 60.0 for d in delays)


def test_retry_after_header_wins_but_is_capped():
    assert w._sleep_for(0, 2.0, 12.0) == 12.0
    assert w._sleep_for(0, 2.0, 900.0) == 60.0


# --- CLI -----------------------------------------------------------------


def run_cli(args: list[str]) -> tuple[int, str]:
    """Run main() with its (deliberately chatty) reporting captured."""
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
        code = w.main(args)
    return code, buf.getvalue()


def test_n_is_clamped_to_the_model_cap_rather_than_erroring():
    assert w.MODELS["dall-e-3"]["max_n"] == 1
    assert w.MODELS["gpt-image-1"]["max_n"] == 10
    code, out = run_cli(["--dry-run", "--model", "dall-e-3", "-n", "5"])
    assert code == w.EXIT_OK
    assert "clamping -n 5 to 1" in out


def test_large_cover_crop_warns_loudly():
    code, out = run_cli(["--dry-run", "--fit", "cover"])
    assert code == w.EXIT_OK
    assert "200px top" in out and "warning:" in out


def test_compose_guard_is_appended_and_can_be_disabled():
    _, with_guard = run_cli(["--dry-run"])
    _, without = run_cli(["--dry-run", "--no-compose-guard"])
    assert "central horizontal band" in with_guard
    assert "central horizontal band" not in without


def test_dry_run_needs_no_api_key():
    assert run_cli(["--dry-run"])[0] == w.EXIT_OK


def test_unknown_variant_is_a_usage_error():
    assert run_cli(["--dry-run", "--variant", "no-such-scene"])[0] == w.EXIT_USAGE


def test_shipped_variants_all_load():
    names = w.list_variants()
    assert names, "expected scene variants to ship with the tool"
    for name in names:
        assert run_cli(["--dry-run", "--variant", name])[0] == w.EXIT_OK


def test_empty_prompt_is_a_usage_error():
    assert run_cli(["--dry-run", "--prompt", "   "])[0] == w.EXIT_USAGE


# --- rendering (skipped without Pillow) ----------------------------------


def _sample_source():
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (1536, 1024), (120, 160, 220))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 1535, 40], fill=(255, 0, 0))  # stands in for the eagle
    draw.rectangle([0, 983, 1535, 1023], fill=(0, 255, 0))  # stands in for the hooves
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def test_pad_keeps_both_edge_bands_and_cover_does_not(tmp_path=None):
    try:
        from PIL import Image
    except ImportError:
        print("skipped render tests: Pillow not installed")
        return

    out = Path(tmp_path) if tmp_path else Path(__file__).parent / ".test-out"
    out.mkdir(parents=True, exist_ok=True)
    raw = _sample_source()

    def corners(name, fit, anchor):
        dest = out / name
        w.render(raw, w.plan_fit((1536, 1024), UHD, fit, anchor), dest, blur_fill=True)
        with Image.open(dest) as im:
            px = im.load()
            assert im.size == UHD
            return px[im.width // 2, 2], px[im.width // 2, im.height - 3]

    assert corners("pad.png", "pad", 0.5) == ((255, 0, 0), (0, 255, 0))
    top, bottom = corners("cover.png", "cover", 0.5)
    assert top != (255, 0, 0) and bottom != (0, 255, 0)
    assert corners("cover_top.png", "cover", 0.0)[0] == (255, 0, 0)


def test_contact_sheet_tiles_every_candidate(tmp_path=None):
    try:
        from PIL import Image
    except ImportError:
        print("skipped contact sheet test: Pillow not installed")
        return

    out = Path(tmp_path) if tmp_path else Path(__file__).parent / ".test-out"
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(3):
        path = out / f"cand{i}.png"
        Image.new("RGB", (960, 540), (40 * i, 80, 120)).save(path)
        paths.append(path)

    sheet = out / "contact.jpg"
    w.contact_sheet(paths, sheet, sheet_width=960)
    with Image.open(sheet) as im:
        assert im.width == 960 and im.height > 540


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"FAIL {name}: {type(exc).__name__}: {exc}")
            else:
                print(f"ok   {name}")
    print("\n" + ("all tests passed" if not failures else f"{failures} test(s) failed"))
    sys.exit(1 if failures else 0)
