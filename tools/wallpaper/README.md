# wallpaper.py

Generates a photorealistic 4K desktop wallpaper from `prompt.txt` using the
OpenAI Images API. Stdlib only for the API call; Pillow only for resizing.

```bash
python -m pip install -r requirements.txt   # Pillow, only needed for --fit pad/cover
export OPENAI_API_KEY=sk-...

python wallpaper.py --dry-run                        # print the plan and prompt, no API call
python wallpaper.py -n 3 --contact-sheet --out ./out # three candidates plus a montage to pick from
python wallpaper.py --variant winter -n 3            # a different take on the same scene
python test_wallpaper.py                             # offline test suite, no key needed
```

## Scenes

`prompt.txt` is the default scene: a log cabin at golden hour, porch and flag,
eagle in flight, dog and horse, river in the foreground, peaks behind. Three
variants of the same location ship in `variants/` and are selected by name with
`--variant` (`--list-variants` to see them):

| variant | what changes |
|---|---|
| `dawn-mist` | first light, layered valley mist, lamplit window, frost and breath |
| `winter` | deep snow, icicles, long blue shadows, partly frozen river |
| `storm-break` | sunlit subjects against a retreating storm wall, wet everything, faint rainbow |

All four keep the same framing discipline: the eagle is placed low in the upper
half with sky above it, and the dog's feet and the horse's hooves are called out
as fully in frame. That matters because of the crop arithmetic below.

## The framing problem this script exists to handle

Neither model renders 16:9, so something has to give between the model output
and a 3840x2160 wallpaper:

| model | native size | aspect | lost to a centre cover-crop |
|---|---|---|---|
| `gpt-image-1` | 1536x1024 | 1.500 | **7.8% off the top and 7.8% off the bottom** (200px each at 4K) |
| `dall-e-3` | 1792x1024 | 1.750 | 0.8% off each side |

For this prompt those two bands are exactly where the eagle and the horse's
hooves live, so a silent centre crop clips them. Three ways out:

- **`--fit pad` (default)** — scale to fit and fill the bars with a blurred,
  cover-scaled copy of the same frame. Nothing is cropped; the bars read as
  continued sky and ground rather than black letterboxing. Use `--no-blur-fill`
  for plain black bars.
- **`--fit cover --crop-anchor top`** — keep the old crop behaviour but choose
  which edge survives. The script prints the exact pixel loss and warns when the
  crop is large.
- **`--model dall-e-3`** — widest native frame, near-lossless crop, but weaker
  material rendering and it rewrites your prompt server-side.

`--model auto` picks whichever model loses least, given the chosen fit.

The prompt sent to the API also gets a framing guard appended (subjects kept in
the central band, upper-left third left uncluttered for desktop icons). Disable
with `--no-compose-guard`.

## Behaviour worth knowing

- **`revised_prompt` is surfaced.** `dall-e-3` silently rewrites prompts. Any
  returned revision is printed and saved next to the image as
  `<name>.revised_prompt.txt`, so scene drift is traceable.
- **`-n` is clamped per model.** `gpt-image-1` accepts up to 10 per request,
  `dall-e-3` exactly 1. Over-asking warns and clamps instead of erroring out.
- **Retries actually back off.** Exponential growth with full jitter, capped at
  60s, honouring `Retry-After`; only retryable statuses (408/409/425/429/5xx)
  and transport errors are retried.
- **Exit codes are real.** `0` success, `2` usage/config, `3` API failure after
  retries, `4` local I/O or image-processing failure, `130` interrupt. A run
  that writes no image never exits `0`.

## Picking a keeper

`--contact-sheet` writes a labelled montage alongside the full-size files
whenever more than one image is produced. Candidates differ in details you have
to compare side by side — whether the eagle is clipped, whether the flag came
out right — and that is tedious to do by flipping between 4K files.

## Tests

`python test_wallpaper.py` runs the whole suite with no API key and no network;
it also works under `pytest` if you have it. The crop arithmetic is pinned to
exact pixel values, and the render tests use a synthetic source with marker
bands on the extreme top and bottom rows to prove `pad` keeps them and `cover`
does not. Render tests self-skip if Pillow is missing.

## Expected failure modes for this prompt

Firearms are often softened or dropped, and models routinely get US flag star
and stripe counts wrong. Generate `-n 3` and expect to discard some runs on
those two details.
