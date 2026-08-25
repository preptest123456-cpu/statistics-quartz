# edX course archiver

Downloads an edX course **you are enrolled in** into a local folder — by default
inside your OneDrive folder, so it syncs to the cloud — capturing:

- **Screenshots** — a full-page PNG of every unit, exactly as it looks on edX
- **Images** — every picture embedded in the page, saved locally, with `unit.html`
  rewritten to point at the local copies so it still renders after your access ends
- **Text** — every unit's content, saved as `unit.txt` / `unit.html`
- **Videos** — the best MP4 edX offers (HLS is remuxed with ffmpeg)
- **Transcripts** — subtitle files (`.srt`) for each video
- **`course.docx`** — one Word document with the whole course: headings per
  section/subsection/unit, the extracted text, the screenshots embedded inline,
  and a table of contents

Default output folder:

```
<OneDrive>/edex_China-West Relations - Dilemmas and Lessons/
```

(`:` is not a legal character in Windows/OneDrive filenames, so the script
rewrites it to ` -` automatically.)

## Install

```bash
cd tools/edx-downloader
python -m pip install -r requirements.txt
python -m playwright install chromium
```

`ffmpeg` on your PATH is optional but recommended — a few edX videos are only
published as HLS streams and need it. Check everything at once:

```bash
python edx_course_downloader.py --check
```

## Quick start (Windows, one command)

`run_archive.ps1` does the whole thing: creates the virtual environment, installs
the dependencies and Chromium, prompts you to sign in if needed, then archives the
course and opens the folder when it's done.

```powershell
cd tools\edx-downloader
.\run_archive.ps1
```

Re-running is safe — the archive resumes and skips whatever is already downloaded.

| Switch | |
| --- | --- |
| `-NoVideos` | Text and screenshots only |
| `-Limit 3` | Stop after 3 units (quick test) |
| `-DryRun` | Print the outline, download nothing |
| `-Force` | Re-capture and re-download everything |
| `-SkipInstall` | Skip the dependency step on later runs |
| `-Out` / `-FolderName` / `-CourseId` | Override the destination or course |

If PowerShell blocks the script, allow it for that one session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Everything below is the manual equivalent.

## Quick start (Linux, WSL or macOS)

`run_archive.sh` is the same thing for a shell:

```bash
cd tools/edx-downloader
./run_archive.sh
```

Under WSL it detects your Windows username and defaults to
`/mnt/c/Users/<you>/Downloads/Learning/...`, then opens the folder in Explorer
when it finishes. Options are passed straight through:

```bash
./run_archive.sh --no-videos --limit 3
./run_archive.sh --dry-run
./run_archive.sh --out ~/archive --folder-name kcl-china
./run_archive.sh --skip-install          # later runs
```

First-time WSL setup, if you haven't got these already:

```bash
sudo apt update && sudo apt install -y python3-venv ffmpeg
```

Two WSL-specific notes: signing in needs a visible browser window, which WSLg
provides on Windows 11 (`wsl --update` if Chromium won't open); and writing to
`/mnt/c` is slower than the Linux filesystem, so archive to `~` and copy
afterwards if it drags.


## Use

**1. Sign in once.** A real Chromium window opens; log in to edX there (SSO and
2FA both work). The session is cached in `~/.edx_archiver/profile`, so you only
do this once. The script never sees, asks for, or stores your password.

```bash
python edx_course_downloader.py --login
```

**2. Archive the course.**

```bash
python edx_course_downloader.py
```

That defaults to the China–West Relations course
(`course-v1:KingsCollegeLondon+SSPP_STCx4+1T2025`). For any other course, paste
any URL from it:

```bash
python edx_course_downloader.py --url "https://learning.edx.org/course/course-v1:Org+Number+Run/..."
```

### Try it small first

```bash
python edx_course_downloader.py --dry-run             # print the outline, download nothing
python edx_course_downloader.py --no-videos --limit 3 # first 3 units, text + screenshots only
```

## Output layout

```
edex_China-West Relations - Dilemmas and Lessons/
├── course.docx                 <- the Word document
├── manifest.json               <- resume state
├── archive.log                 <- full run log
└── 01 - Week 1 Foundations/
    └── 01 - Lecture block/
        └── 01 - Introduction/
            ├── unit.png        <- screenshot
            ├── unit.html       <- rendered HTML
            ├── unit.txt        <- plain text
            ├── 02 - Welcome.mp4
            └── 02 - Welcome.en.srt
```

## Useful options

| Option | What it does |
| --- | --- |
| `--out PATH` | Put the archive somewhere other than OneDrive |
| `--folder-name NAME` | Rename the course folder |
| `--only REGEX` | Only sections/units whose title matches, e.g. `--only "Week [12]"` |
| `--limit N` | Stop after N units |
| `--no-videos` / `--no-screenshots` / `--no-docx` / `--no-transcripts` / `--no-images` | Skip a stage |
| `--export-quartz DIR` | Also write Markdown notes for Quartz or Obsidian |
| `--quality` | `best` (default), `worst`, or a profile like `desktop_mp4`, `mobile_low` |
| `--video-workers N` | Parallel video downloads (default 3) |
| `--screenshot-mode mfe` | Screenshot the full course page instead of just the unit content |
| `--screenshot-width` / `--screenshot-scale` | Viewport width and pixel density (default 1280 @ 1.5×) |
| `--force` | Re-capture and re-download everything |
| `--rate-limit SECONDS` | Minimum gap between requests (default 0.4s) |
| `--headful` | Watch the browser work |
| `-v` | Debug logging |

## How it works

1. **Auth** — Playwright keeps a persistent Chromium profile; its edX cookies are
   copied into a `requests` session for the API and file downloads.
   Alternatives: `--cookie-file cookies.txt` or `--cookies-from-browser chrome`.
2. **Structure** — the official `/api/courses/v1/blocks/` endpoint returns the
   whole course tree with `student_view_data`; the course-home outline API is the
   fallback.
3. **Units** — each vertical is opened in the browser, collapsibles are expanded,
   the page is scrolled to trigger lazy images, then screenshotted full-page and
   its HTML reduced to just the content.
4. **Videos** — sources are ranked (`desktop_mp4` > `fallback` > … > HLS) and
   downloaded with HTTP Range resume; HLS goes through ffmpeg, with yt-dlp as a
   last resort.
5. **Word doc** — `python-docx` renders headings, paragraphs, bold/italic, links,
   lists, tables and blockquotes, then embeds each screenshot. Screenshots taller
   than a page are sliced so the text stays readable.

Everything is **resumable**: state lives in `manifest.json`, and re-running the
same command picks up where it stopped (partial video downloads resume mid-file).
Press Ctrl+C any time — progress is saved.

## Publishing to Quartz or Obsidian

`--export-quartz` writes the archive a second time as Markdown notes:

```bash
./run_archive.sh --skip-install -- --export-quartz ../../content/china-west-relations
```

You get one note per unit, an index per section, and a course index — all with
Quartz frontmatter (`title`, `course`, `section`, `tags`) and `[[wikilinks]]`
between them. Headings, lists, tables, bold/italic, links and images all survive
the HTML-to-Markdown conversion.

Inline images are **copied** into `assets/` beside each note and referenced with a
content-relative path, because Quartz only serves files under its content root —
a link back into the archive folder would 404. Videos and the full-page screenshots
are far too large to duplicate into a notes tree, so they are cited as filesystem
paths instead of links a browser cannot follow. Use `--no-quartz-assets` to skip
copying and keep archive paths throughout.

Pointed at this repo's `content/` directory, `npx quartz build --serve` renders the
whole course as a browsable site. The same files open directly as an Obsidian vault.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `You are not signed in to edX` | `python edx_course_downloader.py --login` |
| `Not authorised … HTTP 403` | Session expired — run `--login` again |
| `Could not read the course structure` | Check you're enrolled and the course id is right; try `--dry-run -v` |
| HLS videos fail | Install ffmpeg, or `pip install yt-dlp` |
| Blank/short screenshots | Raise `--settle 3000`, or try `--screenshot-mode mfe` |
| `course.docx` is locked | Close it in Word; the script saves a timestamped copy instead |
| No OneDrive folder found | Pass `--out "C:\Users\you\OneDrive"` |

## Tests

Offline tests (no browser or edX account needed) covering path sanitising, URL
parsing, tree building, video-source selection, sjson→SRT, HTML→text, the Word
builder and the manifest:

```bash
python test_smoke.py
```

## Please note

Use this only on courses you are enrolled in, keep the output for your own
study, and don't redistribute it — the material stays the property of King's
College London and edX, under the edX terms of service and the course licence.
The polite defaults (rate limiting, 3 download workers) are there for a reason;
please don't crank them up.
