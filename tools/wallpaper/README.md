# wallpaper.py

Generates a photorealistic 4K desktop wallpaper from `prompt.txt` using the
OpenAI Images API. Stdlib only for the API call; Pillow only for resizing.

```bash
python -m pip install -r requirements.txt   # Pillow, only needed for --fit pad/cover
export OPENAI_API_KEY=sk-...

python wallpaper.py --dry-run               # print the plan and prompt, no API call
python wallpaper.py -n 3 --out ./out        # generate three candidates
```

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

## Expected failure modes for this prompt

Firearms are often softened or dropped, and models routinely get US flag star
and stripe counts wrong. Generate `-n 3` and expect to discard some runs on
those two details.
