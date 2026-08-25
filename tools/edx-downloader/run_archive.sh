#!/usr/bin/env bash
#
# One-command archive of an edX course (Linux / WSL / macOS).
#
# Sets up the virtual environment, installs dependencies and Chromium, makes
# sure you are signed in to edX, then archives the whole course: per-unit
# screenshots, text, videos, transcripts and a single Word document.
#
# Safe to re-run -- the archive is resumable and skips finished work.
#
# Usage:
#   ./run_archive.sh                    # full archive
#   ./run_archive.sh --no-videos --limit 3
#   ./run_archive.sh --dry-run
#   ./run_archive.sh --out /some/where --folder-name my-archive
#
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
COURSE_ID="course-v1:KingsCollegeLondon+SSPP_STCx4+1T2025"
FOLDER_NAME="01_course-archive"
OUT=""
SKIP_INSTALL=0
PASSTHROUGH=()

START_TS=$(date +%s)

# Colours only when attached to a terminal.
if [[ -t 1 ]]; then
    C_STEP=$'\033[1;36m'; C_OK=$'\033[0;32m'; C_WARN=$'\033[0;33m'
    C_ERR=$'\033[0;31m';  C_OFF=$'\033[0m'
else
    C_STEP=""; C_OK=""; C_WARN=""; C_ERR=""; C_OFF=""
fi

step() { printf '\n%s==> %s%s\n' "$C_STEP" "$1" "$C_OFF"; }
ok()   { printf '    %s%s%s\n'   "$C_OK"   "$1" "$C_OFF"; }
warn() { printf '    %s%s%s\n'   "$C_WARN" "$1" "$C_OFF"; }
err()  { printf '    %s%s%s\n'   "$C_ERR"  "$1" "$C_OFF" >&2; }
die()  { err "$1"; exit "${2:-1}"; }

trap 'err "Aborted at line $LINENO."' ERR

# ---------------------------------------------------------------------------
# Are we in WSL?
# ---------------------------------------------------------------------------
IS_WSL=0
if grep -qi microsoft /proc/version 2>/dev/null; then
    IS_WSL=1
fi

# Default destination: the Windows Downloads folder when running under WSL,
# otherwise the user's home directory.
if [[ $IS_WSL -eq 1 ]]; then
    WIN_USER="$(cmd.exe /c 'echo %USERNAME%' 2>/dev/null | tr -d '\r\n' || true)"
    [[ -n "$WIN_USER" ]] || WIN_USER="$USER"
    OUT="/mnt/c/Users/${WIN_USER}/Downloads/Learning/China-West Relations - Dilemmas and Lessons (KCL)"
else
    OUT="$HOME/Learning/China-West Relations - Dilemmas and Lessons (KCL)"
fi

# ---------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------
usage() {
    sed -n '3,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --out)          OUT="$2"; shift 2 ;;
        --folder-name)  FOLDER_NAME="$2"; shift 2 ;;
        --course-id)    COURSE_ID="$2"; shift 2 ;;
        --skip-install) SKIP_INSTALL=1; shift ;;
        -h|--help)      usage ;;
        # A bare "--" ends this script's own options; the rest goes to the archiver.
        --)             shift; PASSTHROUGH+=("$@"); break ;;
        # Everything else is handed straight to the Python archiver.
        *)              PASSTHROUGH+=("$1"); shift ;;
    esac
done

DESTINATION="${OUT}/${FOLDER_NAME}"

# ---------------------------------------------------------------------------
# 1. Virtual environment
# ---------------------------------------------------------------------------
step "Preparing the Python environment"

VENV_PY="$SCRIPT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
    warn "No .venv found - creating one."
    BOOTSTRAP=""
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then BOOTSTRAP="$candidate"; break; fi
    done
    [[ -n "$BOOTSTRAP" ]] || die "No Python interpreter found. Try: sudo apt install python3 python3-venv"

    if ! "$BOOTSTRAP" -m venv .venv 2>/dev/null; then
        die "Could not create the virtual environment. Try: sudo apt install python3-venv"
    fi
    ok "Created .venv"
else
    ok "Using existing .venv"
fi

# ---------------------------------------------------------------------------
# 2. Dependencies
# ---------------------------------------------------------------------------
if [[ $SKIP_INSTALL -eq 0 ]]; then
    step "Installing dependencies (skip next time with --skip-install)"

    "$VENV_PY" -m pip install --upgrade pip --quiet
    "$VENV_PY" -m pip install -r requirements.txt --quiet
    ok "Python packages installed"

    # --with-deps needs sudo for the system libraries Chromium links against.
    if "$VENV_PY" -m playwright install --with-deps chromium 2>/dev/null; then
        ok "Chromium installed (with system libraries)"
    else
        warn "Could not install system libraries automatically."
        warn "If Chromium fails to start, run:"
        warn "    sudo $VENV_PY -m playwright install-deps chromium"
        "$VENV_PY" -m playwright install chromium
        ok "Chromium installed"
    fi
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
    warn "ffmpeg not found - HLS-only videos will be skipped."
    warn "Install it with:  sudo apt install ffmpeg"
fi

# ---------------------------------------------------------------------------
# 3. Dependency check
# ---------------------------------------------------------------------------
step "Checking dependencies"
if ! "$VENV_PY" ./edx_course_downloader.py --check; then
    die "Dependency check failed - see the list above." 2
fi

# ---------------------------------------------------------------------------
# 4. Destination sanity
# ---------------------------------------------------------------------------
step "Destination"
if [[ $IS_WSL -eq 1 && "$OUT" == /mnt/* ]]; then
    MOUNT_ROOT="/$(echo "$OUT" | cut -d/ -f2-3)"
    [[ -d "$MOUNT_ROOT" ]] || die "$MOUNT_ROOT is not mounted. Is that drive available in WSL?"
    warn "Writing to a Windows drive from WSL is slower than the Linux filesystem."
fi
ok "$DESTINATION"

COMMON_ARGS=(--course-id "$COURSE_ID" --out "$OUT" --folder-name "$FOLDER_NAME")

# ---------------------------------------------------------------------------
# 5. edX session
# ---------------------------------------------------------------------------
step "Checking your edX session"

PROBE=0
"$VENV_PY" ./edx_course_downloader.py --dry-run "${COMMON_ARGS[@]}" || PROBE=$?

if [[ $PROBE -eq 2 ]]; then
    die "The archiver could not start - see the error above." 2
fi

if [[ $PROBE -ne 0 ]]; then
    warn "Not signed in. A Chromium window will open - log in to edX there."
    warn "Your password is typed only into that window; this script never sees it."

    if [[ $IS_WSL -eq 1 && -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
        err "No display detected. The sign-in step needs a visible browser window."
        err "On Windows 11, WSLg provides this - try 'wsl --update' from PowerShell."
        die "Alternatively, sign in on Windows and pass --cookie-file cookies.txt." 1
    fi

    "$VENV_PY" ./edx_course_downloader.py --login || die "Sign-in did not complete."
    "$VENV_PY" ./edx_course_downloader.py --dry-run "${COMMON_ARGS[@]}" \
        || die "Still cannot read the course after signing in." 1
fi
ok "Signed in and the course outline is readable"

# A bare --dry-run request stops here; the probe above already printed it.
for arg in "${PASSTHROUGH[@]:-}"; do
    if [[ "$arg" == "--dry-run" ]]; then
        step "Dry run only - nothing downloaded."
        exit 0
    fi
done

# ---------------------------------------------------------------------------
# 6. Archive
# ---------------------------------------------------------------------------
step "Archiving the course (Ctrl+C is safe - progress is saved)"

ARCHIVE_EXIT=0
"$VENV_PY" ./edx_course_downloader.py "${COMMON_ARGS[@]}" "${PASSTHROUGH[@]:-}" || ARCHIVE_EXIT=$?

ELAPSED=$(( $(date +%s) - START_TS ))
printf '\n'

case $ARCHIVE_EXIT in
    0)
        printf '%s%s%s\n' "$C_OK" "$(printf '=%.0s' {1..74})" "$C_OFF"
        ok "Finished in $((ELAPSED / 60))m $((ELAPSED % 60))s"
        ok "Folder    : $DESTINATION"
        ok "Word file : $DESTINATION/course.docx"
        printf '%s%s%s\n' "$C_OK" "$(printf '=%.0s' {1..74})" "$C_OFF"
        if [[ $IS_WSL -eq 1 ]] && command -v explorer.exe >/dev/null 2>&1; then
            explorer.exe "$(wslpath -w "$DESTINATION" 2>/dev/null)" >/dev/null 2>&1 || true
        fi
        ;;
    130)
        warn "Stopped by you. Re-run this script to resume where it left off."
        ;;
    *)
        err "The archive finished with errors (exit $ARCHIVE_EXIT)."
        err "Full detail: $DESTINATION/archive.log"
        ;;
esac

exit $ARCHIVE_EXIT
