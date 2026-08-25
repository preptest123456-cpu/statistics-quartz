#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edX course archiver
===================

Downloads a complete edX course that *you are enrolled in* into a local folder
(by default inside your OneDrive folder so it syncs to the cloud), producing:

    <OneDrive>/edex_China-West Relations - Dilemmas and Lessons/
        course.docx              <- Word document: all text + every screenshot
        manifest.json            <- resume/state file
        archive.log              <- run log
        01 - Section name/
            01 - Subsection name/
                01 - Unit name/
                    unit.png         <- full-page screenshot of the unit
                    unit.html        <- raw rendered HTML of the unit
                    unit.txt         <- plain-text extraction
                    Lecture 1.mp4    <- video(s)
                    Lecture 1.en.srt <- transcript(s)

Design notes
------------
* Authentication is done by *you*, interactively, in a real Chromium window the
  first time you run the script (``--login``).  The browser profile is kept in
  ``~/.edx_archiver/profile`` so later runs are silent.  The script never asks
  for, stores, or transmits your password.
* Course structure comes from the official ``/api/courses/v1/blocks/`` endpoint;
  if that is unavailable it falls back to walking the learning MFE with the
  browser.
* Videos come from ``student_view_data.encoded_videos`` (direct MP4 when edX
  offers one, HLS via ffmpeg otherwise, yt-dlp as a last resort).
* Everything is resumable: re-running skips work already recorded in
  ``manifest.json`` and resumes half-finished downloads with HTTP Range.

Please only use this on courses you are enrolled in, keep the output for your
own study, and stay within the edX terms of service and the course licence.

Usage
-----
    python edx_course_downloader.py --login          # one-time sign-in
    python edx_course_downloader.py                  # archive the default course
    python edx_course_downloader.py --url "<any course URL>" --out ~/Desktop
    python edx_course_downloader.py --no-videos --limit 5     # quick dry run

Requirements: see requirements.txt (playwright, requests, python-docx,
beautifulsoup4, lxml, tqdm; ffmpeg on PATH for HLS videos).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import dataclasses
import datetime as _dt
import html as _html
import importlib
import json
import logging
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple
from urllib.parse import quote, urljoin, urlparse

# --------------------------------------------------------------------------------------
# Optional third-party dependencies -- imported lazily/defensively so that ``--help`` and
# the dependency checker still work on a bare interpreter.
# --------------------------------------------------------------------------------------

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:  # pragma: no cover
    BeautifulSoup = None  # type: ignore[assignment]
    NavigableString = Tag = object  # type: ignore[assignment,misc]

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None  # type: ignore[assignment]


LOG = logging.getLogger("edx")

# --------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------

#: The course this script was written for.  Override with --course-id / --url.
DEFAULT_COURSE_ID = "course-v1:KingsCollegeLondon+SSPP_STCx4+1T2025"

#: Folder name requested by the user.  ``:`` is illegal on Windows/OneDrive, so the
#: sanitiser rewrites it to " -" at runtime.
DEFAULT_FOLDER_NAME = "edex_China-West Relations: Dilemmas and Lessons"

LMS_BASE = "https://courses.edx.org"
MFE_BASE = "https://learning.edx.org"
STATE_DIR = Path.home() / ".edx_archiver"
PROFILE_DIR = STATE_DIR / "profile"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

#: Block categories that carry content we care about.
CONTAINER_TYPES = {"course", "chapter", "sequential", "vertical"}
VIDEO_TYPES = {"video"}
TEXT_TYPES = {"html", "problem", "drag-and-drop-v2", "openassessment", "discussion", "lti_consumer"}

#: Preference order when several encodings of the same video exist.
VIDEO_PROFILE_PREFERENCE = (
    "desktop_mp4",
    "fallback",
    "desktop_webm",
    "mobile_high",
    "mobile_low",
    "hls",
)

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


# --------------------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------------------


class ArchiveError(RuntimeError):
    """Fatal, user-facing error."""


def sanitize_component(name: str, maxlen: int = 90) -> str:
    """Make ``name`` safe as a single path component on Windows, macOS and Linux."""
    name = unicodedata.normalize("NFKC", _html.unescape(name or "")).strip()
    name = name.replace(":", " -").replace("/", "-").replace("\\", "-")
    name = re.sub(r'[<>"|?*\x00-\x1f]', "", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if not name:
        name = "untitled"
    if name.split(".")[0].upper() in WINDOWS_RESERVED:
        name = f"_{name}"
    if len(name) > maxlen:
        name = name[:maxlen].rstrip(" .-")
    return name


def human_size(num: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} PB"


def human_duration(seconds: float) -> str:
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


def which(binary: str) -> Optional[str]:
    return shutil.which(binary)


def retry(
    attempts: int = 4,
    base_delay: float = 2.0,
    exceptions: Tuple[type, ...] = (Exception,),
    label: str = "operation",
) -> Callable:
    """Exponential-backoff retry decorator (2s, 4s, 8s, ...)."""

    def decorator(fn: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last: Optional[BaseException] = None
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:  # noqa: PERF203
                    last = exc
                    if attempt == attempts:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    LOG.warning(
                        "%s failed (attempt %d/%d): %s -- retrying in %.0fs",
                        label, attempt, attempts, exc, delay,
                    )
                    time.sleep(delay)
            raise ArchiveError(f"{label} failed after {attempts} attempts: {last}") from last

        wrapper.__name__ = getattr(fn, "__name__", "wrapped")
        return wrapper

    return decorator


class RateLimiter:
    """Minimum wall-clock gap between requests, shared across threads."""

    def __init__(self, min_interval: float) -> None:
        self.min_interval = max(0.0, min_interval)
        self._lock = threading.Lock()
        self._last = 0.0

    def wait(self) -> None:
        if not self.min_interval:
            return
        with self._lock:
            gap = time.monotonic() - self._last
            if gap < self.min_interval:
                time.sleep(self.min_interval - gap)
            self._last = time.monotonic()


def setup_logging(logfile: Optional[Path], verbose: bool) -> None:
    LOG.setLevel(logging.DEBUG)
    LOG.handlers.clear()

    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.DEBUG if verbose else logging.INFO)
    stream.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(message)s", "%H:%M:%S"))
    LOG.addHandler(stream)

    if logfile:
        logfile.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(name)s  %(message)s"))
        LOG.addHandler(fh)

    logging.getLogger("urllib3").setLevel(logging.WARNING)


# --------------------------------------------------------------------------------------
# OneDrive / output location
# --------------------------------------------------------------------------------------


def find_onedrive_root() -> Optional[Path]:
    """Best-effort discovery of the local OneDrive sync root on any OS."""
    candidates: List[Path] = []

    for var in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial", "ONEDRIVE"):
        value = os.environ.get(var)
        if value:
            candidates.append(Path(value))

    home = Path.home()
    candidates += [home / "OneDrive", home / "One Drive", home / "onedrive"]

    system = platform.system()
    if system == "Darwin":
        candidates += sorted((home / "Library" / "CloudStorage").glob("OneDrive*"))
    elif system == "Windows":
        candidates += sorted(home.glob("OneDrive - *"))
    else:
        candidates += sorted(home.glob("OneDrive*"))

    for candidate in candidates:
        with contextlib.suppress(OSError):
            if candidate.is_dir():
                return candidate.resolve()
    return None


def resolve_output_root(explicit: Optional[str], folder_name: str) -> Path:
    """Return (and create) the course folder, preferring OneDrive."""
    folder = sanitize_component(folder_name, maxlen=120)

    if explicit:
        base = Path(os.path.expandvars(explicit)).expanduser()
    else:
        onedrive = find_onedrive_root()
        if onedrive:
            LOG.info("OneDrive detected at %s", onedrive)
            base = onedrive
        else:
            base = Path.home() / "Documents"
            LOG.warning(
                "No OneDrive folder found -- falling back to %s. "
                "Pass --out to choose a different location.", base,
            )

    root = base / folder
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------


@dataclasses.dataclass
class Config:
    course_id: str = DEFAULT_COURSE_ID
    start_url: Optional[str] = None
    folder_name: str = DEFAULT_FOLDER_NAME
    out: Optional[str] = None
    lms_base: str = LMS_BASE
    mfe_base: str = MFE_BASE

    login: bool = False
    headful: bool = False
    profile_dir: Path = PROFILE_DIR
    cookie_file: Optional[str] = None
    cookies_from_browser: Optional[str] = None

    want_videos: bool = True
    want_screenshots: bool = True
    want_docx: bool = True
    want_transcripts: bool = True
    want_html: bool = True
    want_images: bool = True
    export_quartz: Optional[str] = None

    video_workers: int = 3
    quality: str = "best"           # best | worst | <profile name>
    screenshot_width: int = 1280
    screenshot_scale: float = 1.5
    screenshot_mode: str = "xblock"  # xblock | mfe
    page_timeout: int = 60_000       # ms
    settle_ms: int = 1_200

    limit: Optional[int] = None
    only: Optional[str] = None       # regex filter on section/subsection titles
    force: bool = False
    dry_run: bool = False
    rate_limit: float = 0.4
    verbose: bool = False

    # populated at runtime
    root: Path = dataclasses.field(default=Path("."), init=False)
    username: Optional[str] = dataclasses.field(default=None, init=False)


# --------------------------------------------------------------------------------------
# Course / block model
# --------------------------------------------------------------------------------------


@dataclasses.dataclass
class Block:
    """One node of the edX course tree."""

    block_id: str
    block_type: str
    display_name: str
    children: List["Block"] = dataclasses.field(default_factory=list)
    student_view_data: Dict[str, Any] = dataclasses.field(default_factory=dict)
    lms_web_url: str = ""
    graded: bool = False
    parent: Optional["Block"] = dataclasses.field(default=None, repr=False)
    index: int = 0  # 1-based position among siblings

    # ---- convenience ------------------------------------------------------------
    @property
    def is_container(self) -> bool:
        return self.block_type in CONTAINER_TYPES

    @property
    def short_id(self) -> str:
        return self.block_id.rsplit("@", 1)[-1]

    @property
    def title(self) -> str:
        return self.display_name or self.block_type.title()

    def folder_name(self) -> str:
        return sanitize_component(f"{self.index:02d} - {self.title}")

    def walk(self) -> Iterator["Block"]:
        yield self
        for child in self.children:
            yield from child.walk()

    def descendants_of_type(self, types: Iterable[str]) -> List["Block"]:
        wanted = set(types)
        return [b for b in self.walk() if b.block_type in wanted]

    def breadcrumb(self) -> str:
        parts, node = [], self
        while node is not None:
            if node.block_type != "course":
                parts.append(node.title)
            node = node.parent
        return " / ".join(reversed(parts))


def build_tree(blocks: Dict[str, Dict[str, Any]], root_id: str) -> Block:
    """Turn the flat ``blocks`` map from the API into a parent/child tree."""
    made: Dict[str, Block] = {}

    def make(block_id: str, parent: Optional[Block], index: int) -> Block:
        raw = blocks.get(block_id, {})
        node = Block(
            block_id=block_id,
            block_type=raw.get("type", "unknown"),
            display_name=raw.get("display_name") or "",
            student_view_data=raw.get("student_view_data") or {},
            lms_web_url=raw.get("lms_web_url") or "",
            graded=bool(raw.get("graded")),
            parent=parent,
            index=index,
        )
        made[block_id] = node
        for i, child_id in enumerate(raw.get("children") or [], start=1):
            if child_id in made:      # defensive: the API should never produce cycles
                continue
            node.children.append(make(child_id, node, i))
        return node

    return make(root_id, None, 1)


# --------------------------------------------------------------------------------------
# Authentication + HTTP
# --------------------------------------------------------------------------------------


class BrowserSession:
    """A persistent Chromium context plus a ``requests`` session sharing its cookies."""

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._pw = None
        self._context = None
        self._page = None
        self.http: "requests.Session" = self._new_http()

    # ---- lifecycle --------------------------------------------------------------
    def _new_http(self) -> "requests.Session":
        if requests is None:
            raise ArchiveError("The 'requests' package is required (pip install -r requirements.txt)")
        s = requests.Session()
        s.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-GB,en;q=0.9",
            "Referer": self.cfg.mfe_base + "/",
        })
        return s

    def start(self, headless: Optional[bool] = None) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:  # pragma: no cover
            raise ArchiveError(
                "Playwright is required. Install it with:\n"
                "    pip install -r requirements.txt\n"
                "    python -m playwright install chromium"
            ) from exc

        if headless is None:
            headless = not (self.cfg.headful or self.cfg.login)

        self.cfg.profile_dir.mkdir(parents=True, exist_ok=True)
        self._pw = sync_playwright().start()
        LOG.debug("Launching Chromium (headless=%s, profile=%s)", headless, self.cfg.profile_dir)
        self._context = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self.cfg.profile_dir),
            headless=headless,
            viewport={"width": self.cfg.screenshot_width, "height": 1400},
            device_scale_factor=self.cfg.screenshot_scale,
            user_agent=USER_AGENT,
            locale="en-GB",
            args=["--disable-blink-features=AutomationControlled", "--mute-audio"],
        )
        self._context.set_default_timeout(self.cfg.page_timeout)
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()

    def close(self) -> None:
        for closer in (
            lambda: self._context and self._context.close(),
            lambda: self._pw and self._pw.stop(),
        ):
            with contextlib.suppress(Exception):
                closer()
        self._context = self._pw = self._page = None

    def __enter__(self) -> "BrowserSession":
        self.start()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    @property
    def page(self):  # noqa: ANN201 - playwright Page
        if self._page is None:
            raise ArchiveError("Browser is not started")
        return self._page

    def new_page(self):  # noqa: ANN201
        if self._context is None:
            raise ArchiveError("Browser is not started")
        return self._context.new_page()

    # ---- cookies ----------------------------------------------------------------
    def sync_cookies_to_http(self) -> None:
        """Copy Chromium's edX cookies into the requests session."""
        if self._context is None:
            return
        count = 0
        for c in self._context.cookies():
            domain = c.get("domain", "")
            if "edx.org" not in domain:
                continue
            self.http.cookies.set(c["name"], c["value"], domain=domain, path=c.get("path", "/"))
            count += 1
        LOG.debug("Imported %d edX cookies into the HTTP session", count)
        csrf = self.http.cookies.get("csrftoken")
        if csrf:
            self.http.headers["X-CSRFToken"] = csrf

    def load_cookie_file(self, path: str) -> None:
        """Load a Netscape-format cookies.txt (e.g. exported by a browser add-on)."""
        jar_path = Path(path).expanduser()
        if not jar_path.is_file():
            raise ArchiveError(f"Cookie file not found: {jar_path}")
        loaded = 0
        for line in jar_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, _flag, cookie_path, _secure, _expiry, name, value = parts[:7]
            self.http.cookies.set(name, value, domain=domain, path=cookie_path)
            loaded += 1
        LOG.info("Loaded %d cookies from %s", loaded, jar_path)

    def load_browser_cookies(self, browser: str) -> None:
        try:
            import browser_cookie3
        except ImportError as exc:
            raise ArchiveError(
                "--cookies-from-browser needs the browser_cookie3 package "
                "(pip install browser-cookie3)"
            ) from exc
        getter = getattr(browser_cookie3, browser, None)
        if getter is None:
            raise ArchiveError(f"Unsupported browser for cookie import: {browser}")
        jar = getter(domain_name="edx.org")
        for cookie in jar:
            self.http.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
        LOG.info("Imported edX cookies from %s", browser)

    # ---- interactive login ------------------------------------------------------
    def interactive_login(self) -> None:
        """Open the sign-in page and wait until the user is authenticated."""
        page = self.page
        page.goto(f"{self.cfg.mfe_base}/", wait_until="domcontentloaded")
        print("\n" + "=" * 78)
        print("  A Chromium window has opened.  Sign in to edX there (SSO/2FA are fine).")
        print("  This window is the ONLY place your password is typed -- the script")
        print("  never sees it.  The session is cached in:")
        print(f"      {self.cfg.profile_dir}")
        print("  Waiting for sign-in ... (Ctrl+C to abort)")
        print("=" * 78 + "\n")

        deadline = time.monotonic() + 900  # 15 minutes
        while time.monotonic() < deadline:
            self.sync_cookies_to_http()
            if self.whoami(quiet=True):
                LOG.info("Signed in as %s", self.cfg.username)
                return
            time.sleep(3)
        raise ArchiveError("Timed out waiting for sign-in")

    # ---- API helpers ------------------------------------------------------------
    def whoami(self, quiet: bool = False) -> Optional[str]:
        """Return the logged-in username, or None."""
        url = f"{self.cfg.lms_base}/api/user/v1/me"
        try:
            resp = self.http.get(url, timeout=30)
        except Exception as exc:  # noqa: BLE001
            if not quiet:
                LOG.debug("whoami failed: %s", exc)
            return None
        if resp.status_code == 200:
            with contextlib.suppress(ValueError, KeyError):
                self.cfg.username = resp.json()["username"]
                return self.cfg.username
        if not quiet:
            LOG.debug("whoami -> HTTP %s", resp.status_code)
        return None

    @retry(label="GET")
    def get(self, url: str, **kwargs: Any) -> "requests.Response":
        kwargs.setdefault("timeout", 60)
        resp = self.http.get(url, **kwargs)
        if resp.status_code in (401, 403):
            raise ArchiveError(
                f"Not authorised for {url} (HTTP {resp.status_code}). "
                "Run with --login to refresh your edX session."
            )
        if resp.status_code >= 500:
            raise IOError(f"HTTP {resp.status_code} for {url}")
        return resp

    def get_json(self, url: str, **kwargs: Any) -> Any:
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        return resp.json()


# --------------------------------------------------------------------------------------
# Course discovery
# --------------------------------------------------------------------------------------


COURSE_ID_RE = re.compile(r"(course-v1:[^/?#+]+\+[^/?#+]+\+[^/?#]+)")


def course_id_from_url(url: str) -> Optional[str]:
    """Pull ``course-v1:Org+Number+Run`` out of any edX URL."""
    match = COURSE_ID_RE.search(url)
    if match:
        return match.group(1)
    # legacy slash-separated ids: /courses/Org/Number/Run/
    legacy = re.search(r"/courses/([^/]+/[^/]+/[^/]+)/", url)
    return legacy.group(1) if legacy else None


class CourseFetcher:
    """Fetches the course block tree."""

    def __init__(self, session: BrowserSession, cfg: Config) -> None:
        self.s = session
        self.cfg = cfg

    def fetch_tree(self) -> Block:
        try:
            return self._fetch_via_blocks_api()
        except ArchiveError:
            raise
        except Exception as exc:  # noqa: BLE001
            LOG.warning("Blocks API failed (%s) -- falling back to the course outline API", exc)
        return self._fetch_via_outline_api()

    # -- primary: /api/courses/v1/blocks/ -----------------------------------------
    def _fetch_via_blocks_api(self) -> Block:
        params = {
            "course_id": self.cfg.course_id,
            "depth": "all",
            "all_blocks": "false",
            "requested_fields": "children,display_name,type,graded,student_view_data,student_view_multi_device,format",
            "student_view_data": "video,html,discussion",
            "nav_depth": "4",
        }
        if self.cfg.username:
            params["username"] = self.cfg.username
        url = f"{self.cfg.lms_base}/api/courses/v1/blocks/?" + "&".join(
            f"{k}={quote(str(v), safe='')}" for k, v in params.items()
        )
        LOG.debug("Blocks API: %s", url)
        data = self.s.get_json(url)
        blocks = data.get("blocks") or {}
        root_id = data.get("root")
        if not blocks or not root_id:
            raise IOError("Blocks API returned no usable data")
        tree = build_tree(blocks, root_id)
        if not tree.display_name:
            tree.display_name = self._course_title() or self.cfg.course_id
        LOG.info("Course structure: %d blocks", sum(1 for _ in tree.walk()))
        return tree

    # -- fallback: /api/course_home/outline/ --------------------------------------
    def _fetch_via_outline_api(self) -> Block:
        url = f"{self.cfg.lms_base}/api/course_home/outline/{quote(self.cfg.course_id, safe='')}"
        data = self.s.get_json(url)
        outline = (data.get("course_blocks") or {}).get("blocks") or {}
        if not outline:
            raise ArchiveError(
                "Could not read the course structure. Are you enrolled, and is the "
                "course id correct? Try --login."
            )
        root_id = next(
            (bid for bid, b in outline.items() if b.get("type") == "course"),
            next(iter(outline)),
        )
        tree = build_tree(outline, root_id)
        LOG.info("Course structure (outline API): %d blocks", sum(1 for _ in tree.walk()))
        return tree

    def _course_title(self) -> Optional[str]:
        with contextlib.suppress(Exception):
            url = f"{self.cfg.lms_base}/api/courses/v1/courses/{quote(self.cfg.course_id, safe='')}"
            return self.s.get_json(url).get("name")
        return None


# --------------------------------------------------------------------------------------
# Manifest (resume state)
# --------------------------------------------------------------------------------------


class Manifest:
    """Small JSON state file so re-runs skip finished work."""

    VERSION = 2

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self.data: Dict[str, Any] = {
            "version": self.VERSION,
            "created": _dt.datetime.now().isoformat(timespec="seconds"),
            "course_id": None,
            "items": {},
        }
        if path.is_file():
            with contextlib.suppress(Exception):
                loaded = json.loads(path.read_text(encoding="utf-8"))
                if loaded.get("version") == self.VERSION:
                    self.data = loaded
                else:
                    LOG.info("Manifest version changed -- starting a fresh one")

    def done(self, key: str, kind: str) -> bool:
        entry = self.data["items"].get(key, {})
        return entry.get(kind, {}).get("status") == "ok"

    def record(self, key: str, kind: str, **fields: Any) -> None:
        with self._lock:
            entry = self.data["items"].setdefault(key, {})
            entry[kind] = {"status": "ok", "at": _dt.datetime.now().isoformat(timespec="seconds"), **fields}

    def fail(self, key: str, kind: str, error: str) -> None:
        with self._lock:
            entry = self.data["items"].setdefault(key, {})
            entry[kind] = {"status": "error", "error": error[:500],
                           "at": _dt.datetime.now().isoformat(timespec="seconds")}

    def save(self) -> None:
        with self._lock:
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
            tmp.replace(self.path)


# --------------------------------------------------------------------------------------
# Unit rendering: screenshots + text extraction
# --------------------------------------------------------------------------------------


@dataclasses.dataclass
class UnitCapture:
    """What we extracted from one vertical (unit)."""

    block: Block
    directory: Path
    screenshot: Optional[Path] = None
    html_path: Optional[Path] = None
    text_path: Optional[Path] = None
    html: str = ""
    text: str = ""
    videos: List["VideoAsset"] = dataclasses.field(default_factory=list)
    images: List[Path] = dataclasses.field(default_factory=list)


class UnitRenderer:
    """Loads a unit in Chromium, screenshots it and extracts its content."""

    #: Selectors hidden before screenshotting so the page looks clean.
    HIDE_SELECTORS = (
        "#cookie-policy-banner", ".cookie-banner", "#consent_blackbar",
        ".notification-banner", "#footer-edx-v3", "footer", ".sock",
        "[data-testid='course-tabs-navigation']",
    )

    def __init__(self, session: BrowserSession, cfg: Config) -> None:
        self.s = session
        self.cfg = cfg

    # ---- URLs -------------------------------------------------------------------
    def xblock_url(self, block: Block) -> str:
        return (
            f"{self.cfg.lms_base}/xblock/{block.block_id}"
            "?show_title=1&show_bookmark_button=0&recheck_access=1&view=student_view"
        )

    def mfe_url(self, block: Block) -> str:
        parent = block.parent.block_id if block.parent else ""
        return f"{self.cfg.mfe_base}/course/{self.cfg.course_id}/{parent}/{block.block_id}"

    # ---- main entry -------------------------------------------------------------
    def capture(self, block: Block, directory: Path) -> UnitCapture:
        capture = UnitCapture(block=block, directory=directory)
        directory.mkdir(parents=True, exist_ok=True)

        page = self.s.page
        url = self.mfe_url(block) if self.cfg.screenshot_mode == "mfe" else self.xblock_url(block)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=self.cfg.page_timeout)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("Could not open %s (%s) -- trying the xblock view", block.title, exc)
            page.goto(self.xblock_url(block), wait_until="domcontentloaded",
                      timeout=self.cfg.page_timeout)

        self._settle(page)
        self._prepare_for_capture(page)

        if self.cfg.want_screenshots:
            shot = directory / "unit.png"
            with contextlib.suppress(Exception):
                page.screenshot(path=str(shot), full_page=True, animations="disabled")
                capture.screenshot = shot
                LOG.debug("  screenshot -> %s (%s)", shot.name, human_size(shot.stat().st_size))

        raw_html = page.content()
        capture.html = self._extract_unit_html(raw_html)
        capture.text = html_to_text(capture.html)

        if self.cfg.want_html and capture.html:
            capture.html_path = directory / "unit.html"
            capture.html_path.write_text(
                f"<!doctype html><meta charset='utf-8'><title>{_html.escape(block.title)}</title>\n"
                f"{capture.html}",
                encoding="utf-8",
            )
        if capture.text:
            capture.text_path = directory / "unit.txt"
            capture.text_path.write_text(capture.text, encoding="utf-8")

        return capture

    # ---- helpers ----------------------------------------------------------------
    def _settle(self, page) -> None:  # noqa: ANN001
        """Wait for lazy content, expand collapsibles, stop media."""
        with contextlib.suppress(Exception):
            page.wait_for_load_state("networkidle", timeout=15_000)

        # Expand anything collapsed so the screenshot shows the full text.
        with contextlib.suppress(Exception):
            page.evaluate(
                """
                () => {
                  document.querySelectorAll('details').forEach(d => d.open = true);
                  document.querySelectorAll(
                    '.collapsible-body, .hideshowbottom, .longform, .shortform'
                  ).forEach(el => { el.style.display = 'block'; el.style.height = 'auto'; });
                  document.querySelectorAll('[aria-expanded="false"]').forEach(el => {
                    try { el.click(); } catch (e) {}
                  });
                  document.querySelectorAll('video, audio').forEach(m => {
                    try { m.pause(); m.currentTime = 0; } catch (e) {}
                  });
                }
                """
            )
        page.wait_for_timeout(self.cfg.settle_ms)

        # Scroll through the page so lazy images load, then return to the top.
        with contextlib.suppress(Exception):
            page.evaluate(
                """
                async () => {
                  const step = window.innerHeight;
                  for (let y = 0; y < document.body.scrollHeight; y += step) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 120));
                  }
                  window.scrollTo(0, 0);
                }
                """
            )
        page.wait_for_timeout(300)

    def _prepare_for_capture(self, page) -> None:  # noqa: ANN001
        with contextlib.suppress(Exception):
            page.add_style_tag(content="""
                * { animation: none !important; transition: none !important; }
                %s { display: none !important; }
            """ % ", ".join(self.HIDE_SELECTORS))

    def _extract_unit_html(self, raw_html: str) -> str:
        """Reduce a full page down to the xblock content."""
        if BeautifulSoup is None:
            return raw_html
        soup = BeautifulSoup(raw_html, "lxml")
        for junk in soup.select("script, style, noscript, iframe.xblock-init, .cookie-banner"):
            junk.decompose()

        containers = soup.select(
            ".vert-mod, .xblock-student_view, [data-block-type='vertical'], "
            "main .course-content, #seq_content"
        )
        if containers:
            biggest = max(containers, key=lambda c: len(c.get_text(strip=True)))
            return str(biggest)
        body = soup.body
        return str(body) if body else raw_html


def html_to_text(html_fragment: str) -> str:
    """Readable plain text from an HTML fragment."""
    if not html_fragment:
        return ""
    if BeautifulSoup is None:
        text = re.sub(r"<[^>]+>", " ", html_fragment)
        return re.sub(r"\s+", " ", _html.unescape(text)).strip()

    soup = BeautifulSoup(html_fragment, "lxml")
    for junk in soup.select("script, style, noscript"):
        junk.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for block in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr"]):
        block.append("\n")
    text = soup.get_text()
    lines = [re.sub(r"[ \t\xa0]+", " ", line).strip() for line in text.splitlines()]
    out: List[str] = []
    for line in lines:
        if line or (out and out[-1]):
            out.append(line)
    return "\n".join(out).strip()


# --------------------------------------------------------------------------------------
# Videos and transcripts
# --------------------------------------------------------------------------------------


@dataclasses.dataclass
class VideoAsset:
    block: Block
    url: str
    profile: str
    path: Path
    size: int = 0
    duration: float = 0.0
    transcripts: Dict[str, str] = dataclasses.field(default_factory=dict)
    transcript_paths: Dict[str, Path] = dataclasses.field(default_factory=dict)
    downloaded: bool = False
    note: str = ""


class VideoDownloader:
    """Resolves the best source for a video block and downloads it."""

    def __init__(self, session: BrowserSession, cfg: Config, manifest: Manifest) -> None:
        self.s = session
        self.cfg = cfg
        self.manifest = manifest
        self.limiter = RateLimiter(cfg.rate_limit)
        self._ffmpeg = which("ffmpeg")
        self._ytdlp = which("yt-dlp") or which("youtube-dl")

    # ---- source selection --------------------------------------------------------
    def resolve(self, block: Block, directory: Path) -> Optional[VideoAsset]:
        data = block.student_view_data or {}
        encoded: Dict[str, Any] = data.get("encoded_videos") or {}
        candidates: List[Tuple[str, str, int]] = []  # (profile, url, size)

        for profile, info in encoded.items():
            url = (info or {}).get("url")
            if url:
                candidates.append((profile, url, int((info or {}).get("file_size") or 0)))

        for source in data.get("all_sources") or []:
            if source and source not in [c[1] for c in candidates]:
                candidates.append(("source", source, 0))

        if not candidates:
            LOG.debug("  no downloadable source for %s", block.title)
            return None

        def rank(candidate: Tuple[str, str, int]) -> Tuple[int, int]:
            profile, url, size = candidate
            try:
                pref = VIDEO_PROFILE_PREFERENCE.index(profile)
            except ValueError:
                pref = len(VIDEO_PROFILE_PREFERENCE)
            if url.endswith(".m3u8"):          # HLS needs ffmpeg -> least preferred
                pref += 10
            return (pref, -size)

        if self.cfg.quality in {c[0] for c in candidates}:
            profile, url, size = next(c for c in candidates if c[0] == self.cfg.quality)
        elif self.cfg.quality == "worst":
            profile, url, size = sorted(candidates, key=rank, reverse=True)[0]
        else:
            profile, url, size = sorted(candidates, key=rank)[0]

        suffix = ".mp4"
        path_part = urlparse(url).path.lower()
        for ext in (".mp4", ".webm", ".m3u8", ".mov"):
            if path_part.endswith(ext):
                suffix = ".mp4" if ext == ".m3u8" else ext
                break

        filename = sanitize_component(f"{block.index:02d} - {block.title}") + suffix
        return VideoAsset(
            block=block,
            url=url,
            profile=profile,
            path=directory / filename,
            size=size,
            duration=float(data.get("duration") or 0),
            transcripts=dict(data.get("transcripts") or {}),
        )

    # ---- download ---------------------------------------------------------------
    def download(self, asset: VideoAsset) -> VideoAsset:
        key = asset.block.block_id
        if not self.cfg.force and self.manifest.done(key, "video") and asset.path.is_file():
            asset.downloaded = True
            asset.note = "already downloaded"
            LOG.info("  = video already present: %s", asset.path.name)
            return asset

        asset.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if asset.url.endswith(".m3u8"):
                self._download_hls(asset)
            else:
                self._download_direct(asset)
            asset.downloaded = True
            asset.size = asset.path.stat().st_size
            self.manifest.record(
                key, "video", path=str(asset.path), bytes=asset.size, profile=asset.profile
            )
        except Exception as exc:  # noqa: BLE001
            LOG.error("  ! video failed for %s: %s", asset.block.title, exc)
            asset.note = str(exc)
            self.manifest.fail(key, "video", str(exc))
        return asset

    @retry(label="video download", exceptions=(IOError, OSError))
    def _download_direct(self, asset: VideoAsset) -> None:
        """Streamed download with HTTP Range resume."""
        target, part = asset.path, asset.path.with_suffix(asset.path.suffix + ".part")
        existing = part.stat().st_size if part.is_file() else 0
        headers = {"Range": f"bytes={existing}-"} if existing else {}

        self.limiter.wait()
        with self.s.http.get(asset.url, headers=headers, stream=True, timeout=(30, 120)) as resp:
            if resp.status_code == 416 and existing:      # already complete
                part.replace(target)
                return
            if existing and resp.status_code != 206:      # server ignored the range
                LOG.debug("  server ignored Range -- restarting %s", target.name)
                existing = 0
                part.unlink(missing_ok=True)
            if resp.status_code not in (200, 206):
                raise IOError(f"HTTP {resp.status_code} while fetching {asset.url}")

            total = int(resp.headers.get("Content-Length") or 0) + existing
            mode = "ab" if existing else "wb"
            bar = None
            if tqdm is not None and total:
                bar = tqdm(total=total, initial=existing, unit="B", unit_scale=True,
                           unit_divisor=1024, desc=target.name[:38], leave=False)
            try:
                with open(part, mode) as fh:
                    for chunk in resp.iter_content(chunk_size=1 << 18):
                        if chunk:
                            fh.write(chunk)
                            if bar:
                                bar.update(len(chunk))
            finally:
                if bar:
                    bar.close()

        if total and part.stat().st_size < total * 0.98:
            raise IOError(
                f"short read for {target.name}: {human_size(part.stat().st_size)} of {human_size(total)}"
            )
        part.replace(target)
        LOG.info("  + video %s (%s)", target.name, human_size(target.stat().st_size))

    def _download_hls(self, asset: VideoAsset) -> None:
        """Remux an HLS playlist into MP4 with ffmpeg (yt-dlp as a fallback)."""
        if self._ffmpeg:
            cmd = [
                self._ffmpeg, "-y", "-loglevel", "warning",
                "-user_agent", USER_AGENT,
                "-i", asset.url,
                "-c", "copy", "-bsf:a", "aac_adtstoasc",
                str(asset.path),
            ]
        elif self._ytdlp:
            cmd = [self._ytdlp, "--no-warnings", "-o", str(asset.path), asset.url]
        else:
            raise ArchiveError(
                f"{asset.block.title} is HLS-only; install ffmpeg (or yt-dlp) to download it."
            )
        LOG.info("  > %s via %s", asset.path.name, Path(cmd[0]).name)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0 or not asset.path.is_file():
            raise IOError((proc.stderr or proc.stdout or "converter failed").strip()[:400])

    # ---- transcripts -------------------------------------------------------------
    def fetch_transcripts(self, asset: VideoAsset) -> None:
        if not self.cfg.want_transcripts:
            return
        urls = dict(asset.transcripts)
        if not urls:
            urls = {
                "en": f"{self.cfg.lms_base}/courses/{self.cfg.course_id}"
                      f"/xblock/{asset.block.block_id}/handler/transcript/download"
            }
        for lang, url in urls.items():
            full = url if url.startswith("http") else urljoin(self.cfg.lms_base, url)
            try:
                self.limiter.wait()
                resp = self.s.http.get(full, timeout=60)
                if resp.status_code != 200 or not resp.content.strip():
                    LOG.debug("  no %s transcript (HTTP %s)", lang, resp.status_code)
                    continue
                body = resp.text
                ext = ".srt" if "-->" in body else ".txt"
                if body.lstrip().startswith("{"):     # edX sometimes serves sjson
                    body, ext = sjson_to_srt(body), ".srt"
                out = asset.path.with_suffix(f".{lang}{ext}")
                out.write_text(body, encoding="utf-8")
                asset.transcript_paths[lang] = out
                LOG.info("  + transcript %s", out.name)
            except Exception as exc:  # noqa: BLE001
                LOG.debug("  transcript %s failed: %s", lang, exc)


def sjson_to_srt(payload: str) -> str:
    """Convert edX's ``{"start": [...], "end": [...], "text": [...]}`` sjson to SRT."""
    def stamp(ms: int) -> str:
        s, ms = divmod(max(0, int(ms)), 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    try:
        data = json.loads(payload)
    except ValueError:
        return payload
    starts, ends, texts = data.get("start", []), data.get("end", []), data.get("text", [])
    chunks = []
    for i, (start, end, text) in enumerate(zip(starts, ends, texts), start=1):
        if not (text or "").strip():
            continue
        chunks.append(f"{i}\n{stamp(start)} --> {stamp(end)}\n{text.strip()}\n")
    return "\n".join(chunks)


# --------------------------------------------------------------------------------------
# Inline images
# --------------------------------------------------------------------------------------


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}

CONTENT_TYPE_EXTENSION = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "image/bmp": ".bmp",
    "image/avif": ".avif",
}


class AssetDownloader:
    """Pulls the images a unit references and rewrites the HTML to point at local copies.

    Runs against the saved ``unit.html``, so it also works on units captured by an
    earlier run -- no need to re-screenshot anything.
    """

    def __init__(self, session: BrowserSession, cfg: Config, manifest: Manifest) -> None:
        self.s = session
        self.cfg = cfg
        self.manifest = manifest
        self.limiter = RateLimiter(cfg.rate_limit)

    def harvest(self, capture: UnitCapture) -> int:
        """Download every referenced image. Returns how many were saved."""
        if not capture.html or BeautifulSoup is None:
            return 0

        key = capture.block.block_id
        if not self.cfg.force and self.manifest.done(key, "images"):
            existing = sorted((capture.directory / "images").glob("*"))
            capture.images = [p for p in existing if p.is_file()]
            return 0

        soup = BeautifulSoup(capture.html, "lxml")
        targets = self._collect(soup)
        if not targets:
            self.manifest.record(key, "images", count=0)
            return 0

        image_dir = capture.directory / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        saved = 0
        used_names: Dict[str, int] = {}
        for tag, attr, url in targets:
            local = self._fetch(url, image_dir, used_names)
            if local is None:
                continue
            tag[attr] = f"images/{local.name}"
            capture.images.append(local)
            saved += 1

        if saved:
            capture.html = str(soup)
            if capture.html_path:
                capture.html_path.write_text(
                    f"<!doctype html><meta charset='utf-8'>"
                    f"<title>{_html.escape(capture.block.title)}</title>\n{capture.html}",
                    encoding="utf-8",
                )
            LOG.info("      + %d image(s)", saved)

        self.manifest.record(key, "images", count=saved)
        return saved

    # ---- helpers ----------------------------------------------------------------
    def _collect(self, soup: Any) -> List[Tuple[Any, str, str]]:
        """Find every image reference worth downloading."""
        found: List[Tuple[Any, str, str]] = []
        seen: set = set()

        def add(tag: Any, attr: str, raw: str) -> None:
            if not raw or raw.startswith("data:"):
                return                      # already inline
            absolute = urljoin(self.cfg.lms_base, raw)
            if not absolute.startswith(("http://", "https://")):
                return
            if absolute in seen:
                return
            seen.add(absolute)
            found.append((tag, attr, absolute))

        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            add(img, "src", src)

        # Links that point straight at an image (diagrams, figures, charts).
        for anchor in soup.find_all("a"):
            href = anchor.get("href") or ""
            if Path(urlparse(href).path).suffix.lower() in IMAGE_EXTENSIONS:
                add(anchor, "href", href)

        return found

    def _fetch(self, url: str, image_dir: Path, used_names: Dict[str, int]) -> Optional[Path]:
        try:
            self.limiter.wait()
            resp = self.s.http.get(url, timeout=60)
            if resp.status_code != 200 or not resp.content:
                LOG.debug("      image %s -> HTTP %s", url, resp.status_code)
                return None

            name = self._filename(url, resp.headers.get("Content-Type", ""), used_names)
            path = image_dir / name
            path.write_bytes(resp.content)
            return path
        except Exception as exc:  # noqa: BLE001 - one bad image must not stop the archive
            LOG.debug("      image %s failed: %s", url, exc)
            return None

    def _filename(self, url: str, content_type: str, used_names: Dict[str, int]) -> str:
        raw = Path(urlparse(url).path).name or "image"
        stem, suffix = os.path.splitext(raw)
        suffix = suffix.lower()

        if suffix not in IMAGE_EXTENSIONS:
            suffix = CONTENT_TYPE_EXTENSION.get(content_type.split(";")[0].strip(), ".png")

        stem = sanitize_component(stem, maxlen=60) or "image"
        candidate = f"{stem}{suffix}"

        count = used_names.get(candidate, 0)
        used_names[candidate] = count + 1
        if count:
            candidate = f"{stem}-{count + 1}{suffix}"
        return candidate


# --------------------------------------------------------------------------------------
# Markdown / Quartz export
# --------------------------------------------------------------------------------------


def html_to_markdown(fragment: str) -> str:
    """Convert a unit's HTML into Markdown suitable for Quartz or Obsidian."""
    if not fragment:
        return ""
    if BeautifulSoup is None:
        return html_to_text(fragment)

    soup = BeautifulSoup(fragment, "lxml")
    for junk in soup.select("script, style, noscript, button, .sr, .sr-only"):
        junk.decompose()

    def inline(node: Any) -> str:
        if isinstance(node, NavigableString):
            return re.sub(r"\s+", " ", str(node))
        if not isinstance(node, Tag):
            return ""
        name = (node.name or "").lower()
        inner = "".join(inline(c) for c in node.children)

        if name in {"strong", "b"}:
            return f"**{inner.strip()}**" if inner.strip() else ""
        if name in {"em", "i"}:
            return f"*{inner.strip()}*" if inner.strip() else ""
        if name == "code":
            return f"`{inner.strip()}`" if inner.strip() else ""
        if name == "br":
            return "\n"
        if name == "a":
            href = node.get("href", "")
            text = inner.strip() or href
            return f"[{text}]({href})" if href else text
        if name == "img":
            src = node.get("src", "")
            alt = (node.get("alt") or "").replace("]", "")
            return f"\n\n![{alt}]({src})\n\n" if src else ""
        return inner

    lines: List[str] = []

    def block(node: Any, depth: int = 0) -> None:
        if isinstance(node, NavigableString):
            text = str(node).strip()
            if text:
                lines.append(text)
            return
        if not isinstance(node, Tag):
            return

        name = (node.name or "").lower()

        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = node.get_text(" ", strip=True)
            if text:
                level = min(6, int(name[1]) + 1)   # page title owns h1
                lines.append(f"\n{'#' * level} {text}\n")
            return

        if name in {"p", "div", "section", "article"}:
            if node.find(["p", "ul", "ol", "table", "h1", "h2", "h3", "h4", "div", "blockquote"]):
                for child in node.children:
                    block(child, depth)
                return
            text = "".join(inline(c) for c in node.children).strip()
            if text:
                lines.append(f"\n{text}\n")
            return

        if name in {"ul", "ol"}:
            ordered = name == "ol"
            for i, item in enumerate(node.find_all("li", recursive=False), start=1):
                nested = item.find_all(["ul", "ol"], recursive=False)
                for tag in nested:
                    tag.extract()
                text = "".join(inline(c) for c in item.children).strip()
                bullet = f"{i}." if ordered else "-"
                lines.append(f"{'  ' * depth}{bullet} {text}")
                for tag in nested:
                    block(tag, depth + 1)
            lines.append("")
            return

        if name == "blockquote":
            text = node.get_text(" ", strip=True)
            if text:
                lines.append(f"\n> {text}\n")
            return

        if name == "pre":
            text = node.get_text()
            if text.strip():
                lines.append(f"\n```\n{text.rstrip()}\n```\n")
            return

        if name == "table":
            rows = node.find_all("tr")
            if not rows:
                return
            lines.append("")
            for index, row in enumerate(rows):
                cells = [c.get_text(" ", strip=True).replace("|", "\\|")
                         for c in row.find_all(["td", "th"])]
                if not cells:
                    continue
                lines.append("| " + " | ".join(cells) + " |")
                if index == 0:
                    lines.append("|" + "|".join(" --- " for _ in cells) + "|")
            lines.append("")
            return

        if name == "img":
            rendered = inline(node).strip()
            if rendered:
                lines.append(rendered)
            return

        if name == "hr":
            lines.append("\n---\n")
            return

        for child in node.children:
            block(child, depth)

    root = soup.body or soup
    for child in root.children:
        block(child)

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class QuartzExporter:
    """Writes the archive out as Markdown notes for Quartz (or Obsidian)."""

    def __init__(self, cfg: Config, course: Block, captures: List[UnitCapture]) -> None:
        self.cfg = cfg
        self.course = course
        self.captures = captures

    def export(self, target: Path) -> Path:
        target.mkdir(parents=True, exist_ok=True)
        LOG.info("Exporting Markdown notes to %s", target)

        sections: Dict[str, List[UnitCapture]] = {}
        section_titles: Dict[str, str] = {}

        for capture in self.captures:
            sequential = capture.block.parent
            chapter = sequential.parent if sequential else None
            if chapter is None:
                continue
            slug = self._slug(chapter)
            sections.setdefault(slug, []).append(capture)
            section_titles[slug] = chapter.title

        for slug, items in sections.items():
            folder = target / slug
            folder.mkdir(parents=True, exist_ok=True)
            for capture in items:
                self._write_unit(folder, capture)
            self._write_section_index(folder, section_titles[slug], items)

        self._write_course_index(target, sections, section_titles)
        LOG.info("Markdown export complete: %d sections, %d notes",
                 len(sections), len(self.captures))
        return target

    # ---- pieces ------------------------------------------------------------------
    def _slug(self, block: Block) -> str:
        text = unicodedata.normalize("NFKD", f"{block.index:02d}-{block.title}")
        text = text.encode("ascii", "ignore").decode()
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[\s_]+", "-", text)[:70] or f"block-{block.index:02d}"

    def _frontmatter(self, title: str, extra: Dict[str, Any]) -> str:
        def quote(value: Any) -> str:
            return '"' + str(value).replace('"', "'") + '"'

        lines = ["---", f"title: {quote(title)}"]
        for key, value in extra.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                lines.extend(f"  - {quote(v)}" for v in value)
            elif value not in (None, ""):
                lines.append(f"{key}: {quote(value)}")
        lines.append("---")
        return "\n".join(lines)

    def _write_unit(self, folder: Path, capture: UnitCapture) -> None:
        block = capture.block
        note = folder / f"{self._slug(block)}.md"

        body = html_to_markdown(capture.html) or capture.text

        # Point image links at the copies inside the archive folder.
        if capture.images:
            relative = os.path.relpath(capture.directory, note.parent).replace(os.sep, "/")
            body = body.replace("](images/", f"]({relative}/images/")

        parts = [
            self._frontmatter(block.title, {
                "course": self.course.title,
                "section": block.parent.parent.title if block.parent and block.parent.parent else "",
                "subsection": block.parent.title if block.parent else "",
                "archived": _dt.datetime.now().strftime("%Y-%m-%d"),
                "tags": ["edx", "course-archive"],
            }),
            "",
            f"# {block.title}",
            "",
            f"*{block.breadcrumb()}*",
            "",
            body,
        ]

        if capture.videos:
            parts += ["", "## Videos", ""]
            for video in capture.videos:
                rel = os.path.relpath(video.path, note.parent).replace(os.sep, "/")
                detail = human_duration(video.duration) if video.duration else ""
                parts.append(f"- [{video.path.name}]({rel})" + (f" — {detail}" if detail else ""))
                for lang, path in video.transcript_paths.items():
                    trel = os.path.relpath(path, note.parent).replace(os.sep, "/")
                    parts.append(f"  - [Transcript ({lang})]({trel})")

        if capture.screenshot:
            rel = os.path.relpath(capture.screenshot, note.parent).replace(os.sep, "/")
            parts += ["", "## Screenshot", "", f"![{block.title}]({rel})"]

        note.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")

    def _write_section_index(self, folder: Path, title: str, items: List[UnitCapture]) -> None:
        parts = [
            self._frontmatter(title, {
                "course": self.course.title,
                "tags": ["edx", "course-archive", "section"],
            }),
            "",
            f"# {title}",
            "",
        ]
        for capture in items:
            parts.append(f"- [[{self._slug(capture.block)}|{capture.block.title}]]")
        (folder / "index.md").write_text("\n".join(parts) + "\n", encoding="utf-8")

    def _write_course_index(
        self, target: Path, sections: Dict[str, List[UnitCapture]], titles: Dict[str, str]
    ) -> None:
        total_videos = sum(len(c.videos) for c in self.captures)
        parts = [
            self._frontmatter(self.course.title, {
                "course_id": self.cfg.course_id,
                "archived": _dt.datetime.now().strftime("%Y-%m-%d"),
                "tags": ["edx", "course-archive", "index"],
            }),
            "",
            f"# {self.course.title}",
            "",
            f"Archived {_dt.datetime.now().strftime('%d %B %Y')} — "
            f"{len(sections)} sections, {len(self.captures)} units, {total_videos} videos.",
            "",
            "## Contents",
            "",
        ]
        for slug, items in sections.items():
            parts.append(f"### [[{slug}/index|{titles[slug]}]]")
            parts.append("")
            for capture in items:
                parts.append(f"- [[{slug}/{self._slug(capture.block)}|{capture.block.title}]]")
            parts.append("")
        (target / "index.md").write_text("\n".join(parts) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------------------
# Word document
# --------------------------------------------------------------------------------------


class DocxBuilder:
    """Builds one Word document containing every unit's text and screenshot."""

    MAX_IMAGE_HEIGHT_IN = 8.0

    def __init__(self, cfg: Config, course: Block) -> None:
        try:
            import docx
            from docx.enum.section import WD_SECTION
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.shared import Inches, Pt, RGBColor
        except ImportError as exc:  # pragma: no cover
            raise ArchiveError(
                "python-docx is required for the Word output (pip install python-docx), "
                "or run with --no-docx."
            ) from exc

        self._docx = docx
        self._Inches, self._Pt, self._RGB = Inches, Pt, RGBColor
        self._ALIGN = WD_ALIGN_PARAGRAPH
        self._SECTION = WD_SECTION

        self.cfg = cfg
        self.course = course
        self.doc = docx.Document()
        self._page_width_in = 6.5
        self._configure_styles()
        self._cover()

    # ---- setup -------------------------------------------------------------------
    def _configure_styles(self) -> None:
        section = self.doc.sections[0]
        usable = section.page_width - section.left_margin - section.right_margin
        self._page_width_in = max(3.0, usable / 914400)  # EMU -> inches

        normal = self.doc.styles["Normal"]
        normal.font.name = "Calibri"
        normal.font.size = self._Pt(11)
        normal.paragraph_format.space_after = self._Pt(6)

        with contextlib.suppress(KeyError):
            self.doc.styles["Title"].font.color.rgb = self._RGB(0x1F, 0x3B, 0x63)

    def _cover(self) -> None:
        title = self.doc.add_heading(self.course.title or self.cfg.course_id, level=0)
        title.alignment = self._ALIGN.CENTER

        subtitle = self.doc.add_paragraph("Course archive")
        subtitle.alignment = self._ALIGN.CENTER
        subtitle.runs[0].italic = True

        meta = self.doc.add_paragraph()
        meta.alignment = self._ALIGN.CENTER
        run = meta.add_run(
            f"Course ID: {self.cfg.course_id}\n"
            f"Archived: {_dt.datetime.now().strftime('%d %B %Y, %H:%M')}\n"
            f"Source: {self.cfg.mfe_base}/course/{self.cfg.course_id}"
        )
        run.font.size = self._Pt(9)
        run.font.color.rgb = self._RGB(0x60, 0x60, 0x60)

        note = self.doc.add_paragraph()
        note.alignment = self._ALIGN.CENTER
        note_run = note.add_run(
            "Personal study copy. Course content remains the property of its authors "
            "and is subject to the edX terms of service and the course licence."
        )
        note_run.font.size = self._Pt(8)
        note_run.italic = True
        note_run.font.color.rgb = self._RGB(0x80, 0x80, 0x80)

        self.doc.add_page_break()
        self.doc.add_heading("Contents", level=1)
        self._toc_field()
        self.doc.add_page_break()

    def _toc_field(self) -> None:
        """Insert a real Word TOC field (press F9 in Word to populate it)."""
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn

        paragraph = self.doc.add_paragraph()
        run = paragraph.add_run()

        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = r'TOC \o "1-3" \h \z \u'
        separate = OxmlElement("w:fldChar")
        separate.set(qn("w:fldCharType"), "separate")
        placeholder = OxmlElement("w:t")
        placeholder.text = "Right-click here and choose 'Update Field' to build the contents."
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")

        for element in (begin, instr, separate, placeholder, end):
            run._r.append(element)

    # ---- content -----------------------------------------------------------------
    def add_section(self, block: Block) -> None:
        self.doc.add_page_break()
        self.doc.add_heading(block.title, level=1)

    def add_subsection(self, block: Block) -> None:
        self.doc.add_heading(block.title, level=2)

    def add_unit(self, capture: UnitCapture) -> None:
        block = capture.block
        self.doc.add_heading(block.title, level=3)

        crumb = self.doc.add_paragraph()
        crumb_run = crumb.add_run(block.breadcrumb())
        crumb_run.font.size = self._Pt(8)
        crumb_run.italic = True
        crumb_run.font.color.rgb = self._RGB(0x70, 0x70, 0x70)

        if capture.html:
            self._render_html(capture.html)
        elif capture.text:
            for para in capture.text.split("\n\n"):
                if para.strip():
                    self.doc.add_paragraph(para.strip())

        for video in capture.videos:
            self._add_video_entry(video)

        if capture.screenshot and capture.screenshot.is_file():
            caption = self.doc.add_paragraph()
            caption_run = caption.add_run("Screenshot of this unit as it appears on edX:")
            caption_run.font.size = self._Pt(9)
            caption_run.italic = True
            self._add_image(capture.screenshot)

    def _add_video_entry(self, video: VideoAsset) -> None:
        paragraph = self.doc.add_paragraph()
        label = paragraph.add_run("Video: ")
        label.bold = True
        name = paragraph.add_run(video.path.name)
        name.font.size = self._Pt(10)

        details = []
        if video.duration:
            details.append(human_duration(video.duration))
        if video.size:
            details.append(human_size(video.size))
        if not video.downloaded:
            details.append(video.note or "not downloaded")
        if details:
            extra = paragraph.add_run(f"  ({', '.join(details)})")
            extra.font.size = self._Pt(9)
            extra.font.color.rgb = self._RGB(0x70, 0x70, 0x70)

        for lang, path in video.transcript_paths.items():
            transcript = self.doc.add_paragraph(style="List Bullet")
            run = transcript.add_run(f"Transcript ({lang}): {path.name}")
            run.font.size = self._Pt(9)

    def _add_image(self, path: Path) -> None:
        width_in = self._page_width_in
        try:
            from PIL import Image  # noqa: PLC0415

            with Image.open(path) as img:
                w, h = img.size
            if w and h:
                projected_height = width_in * (h / w)
                if projected_height > self.MAX_IMAGE_HEIGHT_IN:
                    # Tall full-page screenshot: slice it so nothing is shrunk to nothing.
                    self._add_sliced_image(path, w, h)
                    return
        except Exception:  # noqa: BLE001 - Pillow is optional
            pass
        with contextlib.suppress(Exception):
            self.doc.add_picture(str(path), width=self._Inches(width_in))

    def _add_sliced_image(self, path: Path, width: int, height: int) -> None:
        """Split a very tall screenshot into page-sized slices so text stays legible."""
        from PIL import Image  # noqa: PLC0415

        slice_height = int(width * (self.MAX_IMAGE_HEIGHT_IN / self._page_width_in))
        slices = max(1, -(-height // slice_height))
        if slices > 12:  # absurdly long page -- just insert it scaled down
            with contextlib.suppress(Exception):
                self.doc.add_picture(str(path), width=self._Inches(self._page_width_in))
            return

        with Image.open(path) as img:
            for i in range(slices):
                top = i * slice_height
                box = (0, top, width, min(height, top + slice_height))
                part_path = path.with_name(f"{path.stem}.part{i + 1:02d}.png")
                img.crop(box).save(part_path)
                with contextlib.suppress(Exception):
                    self.doc.add_picture(str(part_path), width=self._Inches(self._page_width_in))
                with contextlib.suppress(OSError):
                    part_path.unlink()

    # ---- HTML -> docx ------------------------------------------------------------
    def _render_html(self, fragment: str) -> None:
        if BeautifulSoup is None:
            self.doc.add_paragraph(html_to_text(fragment))
            return
        soup = BeautifulSoup(fragment, "lxml")
        for junk in soup.select("script, style, noscript, button, .sr, .sr-only"):
            junk.decompose()
        root = soup.body or soup
        for child in root.children:
            self._render_node(child, list_level=0)

    def _render_node(self, node: Any, list_level: int) -> None:
        if isinstance(node, NavigableString):
            text = str(node).strip()
            if text:
                self.doc.add_paragraph(text)
            return
        if not isinstance(node, Tag):
            return

        name = (node.name or "").lower()

        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = node.get_text(" ", strip=True)
            if text:
                self.doc.add_heading(text, level=min(6, int(name[1]) + 3))
            return

        if name in {"p", "div", "section", "article", "span"}:
            if node.find(["p", "ul", "ol", "table", "h1", "h2", "h3", "h4", "img", "div"]):
                for child in node.children:
                    self._render_node(child, list_level)
                return
            text = node.get_text(" ", strip=True)
            if text:
                paragraph = self.doc.add_paragraph()
                self._render_inline(node, paragraph)
            return

        if name in {"ul", "ol"}:
            style_base = "List Number" if name == "ol" else "List Bullet"
            for item in node.find_all("li", recursive=False):
                style = style_base if list_level == 0 else f"{style_base} {min(3, list_level + 1)}"
                try:
                    paragraph = self.doc.add_paragraph(style=style)
                except KeyError:
                    paragraph = self.doc.add_paragraph(style=style_base)
                self._render_inline(item, paragraph, skip=("ul", "ol"))
                for nested in item.find_all(["ul", "ol"], recursive=False):
                    self._render_node(nested, list_level + 1)
            return

        if name == "blockquote":
            text = node.get_text(" ", strip=True)
            if text:
                try:
                    self.doc.add_paragraph(text, style="Intense Quote")
                except KeyError:
                    paragraph = self.doc.add_paragraph(text)
                    paragraph.paragraph_format.left_indent = self._Inches(0.5)
            return

        if name in {"pre", "code"} and node.parent and node.parent.name != "pre":
            text = node.get_text()
            if text.strip():
                paragraph = self.doc.add_paragraph()
                run = paragraph.add_run(text.rstrip())
                run.font.name = "Consolas"
                run.font.size = self._Pt(9)
            return

        if name == "table":
            self._render_table(node)
            return

        if name in {"hr"}:
            self.doc.add_paragraph("_" * 60)
            return

        if name in {"br"}:
            return

        for child in node.children:
            self._render_node(child, list_level)

    def _render_inline(self, node: Any, paragraph: Any, skip: Tuple[str, ...] = ()) -> None:
        """Walk inline children, preserving bold/italic/links."""

        def walk(element: Any, bold: bool, italic: bool) -> None:
            if isinstance(element, NavigableString):
                text = re.sub(r"\s+", " ", str(element))
                if text.strip():
                    run = paragraph.add_run(text)
                    run.bold = bold or None
                    run.italic = italic or None
                return
            if not isinstance(element, Tag):
                return
            name = (element.name or "").lower()
            if name in skip:
                return
            if name == "br":
                paragraph.add_run("\n")
                return
            if name == "a":
                text = element.get_text(" ", strip=True)
                href = element.get("href", "")
                if text:
                    run = paragraph.add_run(text)
                    run.font.color.rgb = self._RGB(0x0B, 0x5C, 0xAB)
                    run.underline = True
                    if href and href.startswith("http") and href not in text:
                        note = paragraph.add_run(f" <{href}>")
                        note.font.size = self._Pt(8)
                        note.font.color.rgb = self._RGB(0x80, 0x80, 0x80)
                return
            is_bold = bold or name in {"b", "strong", "th"}
            is_italic = italic or name in {"i", "em"}
            for child in element.children:
                walk(child, is_bold, is_italic)

        for child in node.children:
            walk(child, False, False)

    def _render_table(self, table_tag: Any) -> None:
        rows = table_tag.find_all("tr")
        if not rows:
            return
        width = max(len(r.find_all(["td", "th"])) for r in rows)
        if not width:
            return
        try:
            table = self.doc.add_table(rows=0, cols=width)
            table.style = "Light Grid Accent 1"
        except Exception:  # noqa: BLE001
            table = self.doc.add_table(rows=0, cols=width)
        for row in rows:
            cells = row.find_all(["td", "th"])
            docx_row = table.add_row().cells
            for i, cell in enumerate(cells[:width]):
                docx_row[i].text = cell.get_text(" ", strip=True)

    # ---- output ------------------------------------------------------------------
    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.doc.save(str(path))
        except PermissionError as exc:
            alt = path.with_name(f"{path.stem}-{_dt.datetime.now():%Y%m%d-%H%M%S}.docx")
            LOG.warning("%s is locked (%s) -- saving as %s", path.name, exc, alt.name)
            self.doc.save(str(alt))
            return alt
        return path


# --------------------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------------------


@dataclasses.dataclass
class Stats:
    sections: int = 0
    subsections: int = 0
    units: int = 0
    screenshots: int = 0
    images: int = 0
    videos_ok: int = 0
    videos_failed: int = 0
    videos_skipped: int = 0
    transcripts: int = 0
    bytes: int = 0
    started: float = dataclasses.field(default_factory=time.monotonic)

    def elapsed(self) -> str:
        return human_duration(time.monotonic() - self.started)


class Archiver:
    """Ties everything together."""

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.stats = Stats()
        self.session = BrowserSession(cfg)
        self.manifest = Manifest(cfg.root / "manifest.json")
        self.renderer = UnitRenderer(self.session, cfg)
        self.videos = VideoDownloader(self.session, cfg, self.manifest)
        self.assets = AssetDownloader(self.session, cfg, self.manifest)
        self.captures: List[UnitCapture] = []
        self._interrupted = False

    # ---- run ---------------------------------------------------------------------
    def run(self) -> int:
        self._install_signal_handler()
        cfg = self.cfg

        self.session.start()
        try:
            self._authenticate()
            course = CourseFetcher(self.session, cfg).fetch_tree()
            self.manifest.data["course_id"] = cfg.course_id
            self.manifest.data["course_title"] = course.title
            self.manifest.save()

            self._print_outline(course)
            if cfg.dry_run:
                LOG.info("Dry run -- nothing was downloaded.")
                return 0

            self._walk_course(course)

            if cfg.want_videos and self.captures:
                self._download_all_videos()

            if cfg.want_docx:
                self._build_docx(course)

            if cfg.export_quartz and self.captures:
                self._export_markdown(course)
        finally:
            self.manifest.save()
            self.session.close()

        self._summarise()
        return 1 if self._interrupted else 0

    # ---- steps -------------------------------------------------------------------
    def _install_signal_handler(self) -> None:
        def handler(signum: int, _frame: Any) -> None:
            self._interrupted = True
            LOG.warning("Interrupted (signal %s) -- saving progress; run again to resume.", signum)
            self.manifest.save()
            raise KeyboardInterrupt

        with contextlib.suppress(ValueError):  # not the main thread
            signal.signal(signal.SIGINT, handler)

    def _authenticate(self) -> None:
        cfg = self.cfg
        if cfg.cookie_file:
            self.session.load_cookie_file(cfg.cookie_file)
        if cfg.cookies_from_browser:
            self.session.load_browser_cookies(cfg.cookies_from_browser)

        self.session.sync_cookies_to_http()
        if self.session.whoami(quiet=True):
            LOG.info("Signed in as %s", cfg.username)
            return

        if cfg.login or cfg.headful:
            self.session.close()
            self.session.start(headless=False)
            self.session.interactive_login()
            return

        raise ArchiveError(
            "You are not signed in to edX in this browser profile.\n"
            "Run once with --login to sign in (a Chromium window opens), then re-run normally."
        )

    def _print_outline(self, course: Block) -> None:
        LOG.info("=" * 74)
        LOG.info("Course : %s", course.title)
        LOG.info("ID     : %s", self.cfg.course_id)
        LOG.info("Output : %s", self.cfg.root)
        chapters = [b for b in course.children if b.block_type == "chapter"]
        units = course.descendants_of_type(["vertical"])
        videos = course.descendants_of_type(VIDEO_TYPES)
        LOG.info("Content: %d sections, %d units, %d videos", len(chapters), len(units), len(videos))
        LOG.info("=" * 74)
        for chapter in chapters:
            LOG.debug("  %s", chapter.title)
            for seq in chapter.children:
                LOG.debug("    %s (%d units)", seq.title, len(seq.children))

    def _selected(self, block: Block) -> bool:
        if not self.cfg.only:
            return True
        pattern = re.compile(self.cfg.only, re.IGNORECASE)
        node: Optional[Block] = block
        while node is not None:
            if pattern.search(node.title or ""):
                return True
            node = node.parent
        return False

    def _walk_course(self, course: Block) -> None:
        cfg = self.cfg
        chapters = [b for b in course.children if b.block_type in {"chapter", "sequential", "vertical"}]

        for chapter in chapters:
            if not self._selected(chapter) and not any(
                self._selected(s) for s in chapter.walk()
            ):
                LOG.debug("Skipping section %s (filtered out)", chapter.title)
                continue

            chapter_dir = cfg.root / chapter.folder_name()
            LOG.info("")
            LOG.info("## %s", chapter.title)
            self.stats.sections += 1

            for sequential in chapter.children:
                if not self._selected(sequential) and not any(
                    self._selected(v) for v in sequential.walk()
                ):
                    continue
                seq_dir = chapter_dir / sequential.folder_name()
                LOG.info("  # %s", sequential.title)
                self.stats.subsections += 1

                verticals = [v for v in sequential.children if v.block_type == "vertical"] or [sequential]
                for vertical in verticals:
                    if cfg.limit is not None and self.stats.units >= cfg.limit:
                        LOG.info("Reached --limit of %d units", cfg.limit)
                        return
                    try:
                        self._process_unit(vertical, seq_dir / vertical.folder_name())
                    except KeyboardInterrupt:
                        raise
                    except Exception as exc:  # noqa: BLE001
                        LOG.error("  ! unit '%s' failed: %s", vertical.title, exc)
                        self.manifest.fail(vertical.block_id, "unit", str(exc))
                    finally:
                        self.manifest.save()

    def _process_unit(self, vertical: Block, directory: Path) -> None:
        cfg = self.cfg
        already = self.manifest.done(vertical.block_id, "unit")
        LOG.info("    - %s", vertical.title)
        self.stats.units += 1

        if already and not cfg.force and (directory / "unit.png").exists():
            LOG.info("      = already captured; reusing")
            capture = UnitCapture(block=vertical, directory=directory)
            capture.screenshot = directory / "unit.png"
            html_path, text_path = directory / "unit.html", directory / "unit.txt"
            if html_path.is_file():
                capture.html = html_path.read_text(encoding="utf-8", errors="replace")
                capture.html_path = html_path
            if text_path.is_file():
                capture.text = text_path.read_text(encoding="utf-8", errors="replace")
                capture.text_path = text_path
        else:
            capture = self.renderer.capture(vertical, directory)
            self.manifest.record(
                vertical.block_id, "unit",
                title=vertical.title,
                path=str(directory),
                screenshot=bool(capture.screenshot),
                chars=len(capture.text),
            )

        if capture.screenshot and capture.screenshot.is_file():
            self.stats.screenshots += 1

        if cfg.want_images:
            try:
                self.assets.harvest(capture)
            except Exception as exc:  # noqa: BLE001 - images are a bonus, never fatal
                LOG.warning("      ! images failed for %s: %s", vertical.title, exc)
            self.stats.images += len(capture.images)

        if cfg.want_videos:
            for video_block in vertical.descendants_of_type(VIDEO_TYPES):
                asset = self.videos.resolve(video_block, directory)
                if asset is None:
                    self.stats.videos_skipped += 1
                    LOG.info("      ~ no downloadable source: %s", video_block.title)
                    continue
                capture.videos.append(asset)

        self.captures.append(capture)

    def _download_all_videos(self) -> None:
        assets = [a for capture in self.captures for a in capture.videos]
        if not assets:
            LOG.info("No videos to download.")
            return

        LOG.info("")
        LOG.info("Downloading %d video(s) with %d worker(s) ...", len(assets), self.cfg.video_workers)
        workers = max(1, self.cfg.video_workers)

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(self._download_one, a): a for a in assets}
            try:
                for future in concurrent.futures.as_completed(futures):
                    future.result()
            except KeyboardInterrupt:
                LOG.warning("Cancelling remaining downloads ...")
                for future in futures:
                    future.cancel()
                raise
        self.manifest.save()

    def _download_one(self, asset: VideoAsset) -> None:
        self.videos.download(asset)
        if asset.downloaded:
            self.stats.videos_ok += 1
            self.stats.bytes += asset.size
        else:
            self.stats.videos_failed += 1
        self.videos.fetch_transcripts(asset)
        self.stats.transcripts += len(asset.transcript_paths)

    def _build_docx(self, course: Block) -> None:
        LOG.info("")
        LOG.info("Building Word document ...")
        builder = DocxBuilder(self.cfg, course)

        by_block = {c.block.block_id: c for c in self.captures}
        seen_sections: set = set()
        seen_subsections: set = set()

        for capture in self.captures:
            vertical = capture.block
            sequential = vertical.parent
            chapter = sequential.parent if sequential else None

            if chapter is not None and chapter.block_id not in seen_sections:
                builder.add_section(chapter)
                seen_sections.add(chapter.block_id)
            if sequential is not None and sequential.block_id not in seen_subsections:
                builder.add_subsection(sequential)
                seen_subsections.add(sequential.block_id)

            builder.add_unit(by_block.get(vertical.block_id, capture))

        target = builder.save(self.cfg.root / "course.docx")
        LOG.info("Word document: %s (%s)", target, human_size(target.stat().st_size))

    def _export_markdown(self, course: Block) -> None:
        target = Path(os.path.expandvars(str(self.cfg.export_quartz))).expanduser()
        try:
            QuartzExporter(self.cfg, course, self.captures).export(target)
        except Exception as exc:  # noqa: BLE001 - the archive itself is already safe
            LOG.error("Markdown export failed: %s", exc)

    def _summarise(self) -> None:
        s = self.stats
        LOG.info("")
        LOG.info("=" * 74)
        LOG.info("Done in %s", s.elapsed())
        LOG.info("  sections     : %d", s.sections)
        LOG.info("  subsections  : %d", s.subsections)
        LOG.info("  units        : %d", s.units)
        LOG.info("  screenshots  : %d", s.screenshots)
        LOG.info("  images       : %d", s.images)
        LOG.info("  videos       : %d ok, %d failed, %d without a download source",
                 s.videos_ok, s.videos_failed, s.videos_skipped)
        LOG.info("  transcripts  : %d", s.transcripts)
        LOG.info("  downloaded   : %s", human_size(s.bytes))
        LOG.info("  folder       : %s", self.cfg.root)
        LOG.info("=" * 74)


# --------------------------------------------------------------------------------------
# Dependency check
# --------------------------------------------------------------------------------------


SAC_PREFLIGHT_MODULES: Tuple[Tuple[str, str], ...] = (
    ("lxml.etree", "lxml"),
    ("charset_normalizer", "charset-normalizer"),
)


def preflight_compiled_dependencies(
    importer: Callable[[str], Any] = importlib.import_module,
) -> None:
    """Fail early when Windows blocks a compiled dependency used by the archive."""
    failures: List[Tuple[str, BaseException]] = []
    for module, _label in SAC_PREFLIGHT_MODULES:
        try:
            importer(module)
        except Exception as exc:  # noqa: BLE001 - any import failure must stop the archive
            failures.append((module, exc))

    if not failures:
        return

    details = "\n".join(f"  - {module}: {exc}" for module, exc in failures)
    raise ArchiveError(
        "Startup preflight failed; a compiled Python dependency could not load:\n"
        f"{details}\n\n"
        "On Windows, Smart App Control can block wheel .pyd files, especially in a "
        "virtual environment created from a relocatable or bundled Python runtime. "
        "Do not disable Smart App Control.\n\n"
        "Temporary workaround for a trusted bundled runtime: recreate the environment "
        "with `python -m venv --system-site-packages .venv`, or set "
        "`include-system-site-packages = true` in `.venv\\pyvenv.cfg`, then rerun this "
        "preflight. The durable fix is to use a standard user-installed CPython and "
        "recreate `.venv`."
    )


def check_dependencies(strict: bool = False) -> bool:
    """Report which optional/required pieces are installed."""
    rows: List[Tuple[str, bool, str]] = []

    def probe(module: str, label: str, hint: str) -> None:
        try:
            __import__(module)
            rows.append((label, True, ""))
        except (ImportError, OSError):
            rows.append((label, False, hint))

    probe("requests", "requests", "pip install requests")
    probe("playwright", "playwright", "pip install playwright && python -m playwright install chromium")
    probe("bs4", "beautifulsoup4", "pip install beautifulsoup4 lxml")
    probe("lxml.etree", "lxml", "pip install lxml")
    probe("charset_normalizer", "charset-normalizer", "pip install charset-normalizer")
    probe("docx", "python-docx", "pip install python-docx")
    probe("PIL", "Pillow (image slicing)", "pip install Pillow")
    probe("tqdm", "tqdm (progress bars)", "pip install tqdm")

    rows.append(("ffmpeg (HLS videos)", bool(which("ffmpeg")), "https://ffmpeg.org/download.html"))
    rows.append(("yt-dlp (fallback)", bool(which("yt-dlp")), "pip install yt-dlp"))

    print("\nDependency check")
    print("-" * 60)
    for label, ok, hint in rows:
        mark = "ok  " if ok else "MISSING"
        print(f"  [{mark}] {label}" + (f"   -> {hint}" if not ok else ""))
    onedrive = find_onedrive_root()
    print(f"  [{'ok  ' if onedrive else 'none'}] OneDrive folder"
          + (f"   -> {onedrive}" if onedrive else "   -> not found; use --out"))
    print("-" * 60)

    required = {"requests", "playwright"}
    missing_required = [label for label, ok, _ in rows if not ok and label in required]
    if strict and missing_required:
        return False
    return not missing_required


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def parse_args(argv: Optional[Sequence[str]] = None) -> Config:
    parser = argparse.ArgumentParser(
        prog="edx_course_downloader.py",
        description="Archive an edX course you are enrolled in (screenshots, text, videos, Word doc).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python edx_course_downloader.py --login\n"
            "  python edx_course_downloader.py\n"
            "  python edx_course_downloader.py --url 'https://learning.edx.org/course/course-v1:Org+X+1T2025/...'\n"
            "  python edx_course_downloader.py --no-videos --limit 3 --verbose\n"
        ),
    )

    where = parser.add_argument_group("course + destination")
    where.add_argument("--url", help="Any URL from the course (the course id is parsed out of it)")
    where.add_argument("--course-id", default=None, help=f"Course id (default: {DEFAULT_COURSE_ID})")
    where.add_argument("--out", default=None,
                       help="Parent folder for the archive (default: your OneDrive folder)")
    where.add_argument("--folder-name", default=DEFAULT_FOLDER_NAME,
                       help="Name of the course folder created inside --out")
    where.add_argument("--lms-base", default=LMS_BASE, help="LMS origin (default: %(default)s)")
    where.add_argument("--mfe-base", default=MFE_BASE, help="Learning MFE origin (default: %(default)s)")

    auth = parser.add_argument_group("authentication")
    auth.add_argument("--login", action="store_true",
                      help="Open a browser window and wait while you sign in to edX")
    auth.add_argument("--headful", action="store_true", help="Show the browser window while working")
    auth.add_argument("--profile-dir", default=str(PROFILE_DIR),
                      help="Where the browser profile (your session) is cached")
    auth.add_argument("--cookie-file", help="Netscape cookies.txt to import instead of using the profile")
    auth.add_argument("--cookies-from-browser",
                      choices=["chrome", "firefox", "edge", "brave", "chromium", "safari", "opera"],
                      help="Import edX cookies straight from an installed browser")

    what = parser.add_argument_group("what to archive")
    what.add_argument("--no-videos", action="store_true", help="Skip video downloads")
    what.add_argument("--no-screenshots", action="store_true", help="Skip screenshots")
    what.add_argument("--no-docx", action="store_true", help="Skip the Word document")
    what.add_argument("--no-transcripts", action="store_true", help="Skip subtitle files")
    what.add_argument("--no-html", action="store_true", help="Do not save per-unit unit.html")
    what.add_argument("--no-images", action="store_true",
                      help="Do not download images embedded in the course pages")
    what.add_argument("--export-quartz", metavar="DIR",
                      help="Also write the course out as Markdown notes for Quartz/Obsidian")
    what.add_argument("--only", metavar="REGEX",
                      help="Only archive sections/units whose title matches this regex")
    what.add_argument("--limit", type=int, help="Stop after N units (handy for a test run)")

    how = parser.add_argument_group("tuning")
    how.add_argument("--quality", default="best",
                     help="best | worst | a profile name such as desktop_mp4, mobile_low")
    how.add_argument("--video-workers", type=int, default=3, help="Parallel video downloads")
    how.add_argument("--screenshot-mode", choices=["xblock", "mfe"], default="xblock",
                     help="xblock = clean content only (default); mfe = the full course page")
    how.add_argument("--screenshot-width", type=int, default=1280, help="Browser viewport width")
    how.add_argument("--screenshot-scale", type=float, default=1.5, help="Device pixel ratio")
    how.add_argument("--timeout", type=int, default=60, help="Per-page timeout in seconds")
    how.add_argument("--settle", type=int, default=1200, help="Milliseconds to wait after load")
    how.add_argument("--rate-limit", type=float, default=0.4,
                     help="Minimum seconds between HTTP requests (be kind to edX)")
    how.add_argument("--force", action="store_true", help="Re-download and re-capture everything")
    how.add_argument("--dry-run", action="store_true", help="Show the course outline and exit")
    how.add_argument("--check", action="store_true", help="Check dependencies and exit")
    how.add_argument("-v", "--verbose", action="store_true", help="Debug logging")

    args = parser.parse_args(argv)

    if args.check:
        sys.exit(0 if check_dependencies() else 2)

    course_id = args.course_id
    if not course_id and args.url:
        course_id = course_id_from_url(args.url)
        if not course_id:
            parser.error(f"Could not find a course id in --url {args.url!r}")
    course_id = course_id or DEFAULT_COURSE_ID

    return Config(
        course_id=course_id,
        start_url=args.url,
        folder_name=args.folder_name,
        out=args.out,
        lms_base=args.lms_base.rstrip("/"),
        mfe_base=args.mfe_base.rstrip("/"),
        login=args.login,
        headful=args.headful,
        profile_dir=Path(args.profile_dir).expanduser(),
        cookie_file=args.cookie_file,
        cookies_from_browser=args.cookies_from_browser,
        want_videos=not args.no_videos,
        want_screenshots=not args.no_screenshots,
        want_docx=not args.no_docx,
        want_transcripts=not args.no_transcripts,
        want_html=not args.no_html,
        want_images=not args.no_images,
        export_quartz=args.export_quartz,
        video_workers=max(1, args.video_workers),
        quality=args.quality,
        screenshot_width=args.screenshot_width,
        screenshot_scale=args.screenshot_scale,
        screenshot_mode=args.screenshot_mode,
        page_timeout=args.timeout * 1000,
        settle_ms=args.settle,
        limit=args.limit,
        only=args.only,
        force=args.force,
        dry_run=args.dry_run,
        rate_limit=args.rate_limit,
        verbose=args.verbose,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    cfg = parse_args(argv)

    try:
        preflight_compiled_dependencies()
    except ArchiveError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    cfg.root = resolve_output_root(cfg.out, cfg.folder_name)
    setup_logging(cfg.root / "archive.log", cfg.verbose)

    LOG.info("edX course archiver")
    LOG.debug("Config: %s", {k: str(v) for k, v in dataclasses.asdict(cfg).items()})

    if not check_dependencies(strict=True):
        LOG.error("Missing required dependencies -- see the list above.")
        return 2

    try:
        return Archiver(cfg).run()
    except KeyboardInterrupt:
        LOG.warning("Stopped by user. Re-run the same command to resume.")
        return 130
    except ArchiveError as exc:
        LOG.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        LOG.exception("Unexpected failure: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
