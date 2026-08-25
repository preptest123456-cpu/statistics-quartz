#Requires -Version 5.1
<#
.SYNOPSIS
    One-command archive of an edX course into a local folder.

.DESCRIPTION
    Sets up the virtual environment, installs dependencies and Chromium, makes sure
    you are signed in to edX, then archives the whole course: per-unit screenshots,
    text, videos, transcripts and a single Word document.

    Safe to re-run. The archive is resumable, so a second run picks up where the
    last one stopped and skips everything already downloaded.

.EXAMPLE
    .\run_archive.ps1
    Full archive into the default folder.

.EXAMPLE
    .\run_archive.ps1 -NoVideos -Limit 3
    Quick check: first 3 units, text and screenshots only.

.EXAMPLE
    .\run_archive.ps1 -Out "D:\Archive" -FolderName "kcl-china"
    Archive somewhere else.
#>
[CmdletBinding()]
param(
    [string] $Out        = "C:\Users\fbous\Downloads\Learning\China-West Relations - Dilemmas and Lessons (KCL)",
    [string] $FolderName = "01_course-archive",
    [string] $CourseId   = "course-v1:KingsCollegeLondon+SSPP_STCx4+1T2025",

    [switch] $NoVideos,          # skip video downloads
    [int]    $Limit      = 0,    # stop after N units (0 = no limit)
    [switch] $Force,             # re-capture and re-download everything
    [switch] $SkipInstall,       # assume the venv is already set up
    [switch] $DryRun             # print the outline and exit
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$script:Started = Get-Date

function Write-Step   { param([string] $Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Ok     { param([string] $Text) Write-Host "    $Text" -ForegroundColor Green }
function Write-Warn   { param([string] $Text) Write-Host "    $Text" -ForegroundColor Yellow }
function Write-Err    { param([string] $Text) Write-Host "    $Text" -ForegroundColor Red }

function Stop-WithError {
    param([string] $Message, [int] $Code = 1)
    Write-Err $Message
    exit $Code
}

# ---------------------------------------------------------------------------
# 1. Locate or create the virtual environment
# ---------------------------------------------------------------------------
Write-Step "Preparing the Python environment"

$VenvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $VenvPython)) {
    Write-Warn "No .venv found - creating one."

    $bootstrap = $null
    foreach ($candidate in @('py', 'python', 'python3')) {
        $found = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($found) { $bootstrap = $found.Source; break }
    }
    if (-not $bootstrap) {
        Stop-WithError "No Python interpreter found on PATH. Install Python 3.9+ from python.org and re-run."
    }

    if ((Split-Path $bootstrap -Leaf) -ieq 'py.exe') {
        & $bootstrap -3 -m venv .venv
    } else {
        & $bootstrap -m venv .venv
    }
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $VenvPython)) {
        Stop-WithError "Could not create the virtual environment (exit $LASTEXITCODE)."
    }
    Write-Ok "Created .venv"
} else {
    Write-Ok "Using existing .venv"
}

# ---------------------------------------------------------------------------
# 2. Dependencies
# ---------------------------------------------------------------------------
if (-not $SkipInstall) {
    Write-Step "Installing dependencies (skip next time with -SkipInstall)"

    & $VenvPython -m pip install --upgrade pip --quiet
    & $VenvPython -m pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "pip install failed (exit $LASTEXITCODE). Run it by hand to see the full error."
    }
    Write-Ok "Python packages installed"

    & $VenvPython -m playwright install chromium
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "Could not install Chromium (exit $LASTEXITCODE)."
    }
    Write-Ok "Chromium installed"
}

# ---------------------------------------------------------------------------
# 3. Dependency preflight
# ---------------------------------------------------------------------------
Write-Step "Checking dependencies"

& $VenvPython .\edx_course_downloader.py --check
if ($LASTEXITCODE -ne 0) {
    Stop-WithError "Dependency check failed (exit $LASTEXITCODE). See the list above." $LASTEXITCODE
}

# ---------------------------------------------------------------------------
# 4. Build the argument list
# ---------------------------------------------------------------------------
$CommonArgs = @(
    '--course-id', $CourseId,
    '--out',       $Out,
    '--folder-name', $FolderName
)

$RunArgs = $CommonArgs
if ($NoVideos)  { $RunArgs += '--no-videos' }
if ($Force)     { $RunArgs += '--force' }
if ($Limit -gt 0) { $RunArgs += @('--limit', "$Limit") }

# ---------------------------------------------------------------------------
# 5. Make sure we are signed in (a dry run needs a valid session)
# ---------------------------------------------------------------------------
Write-Step "Checking your edX session"

& $VenvPython .\edx_course_downloader.py --dry-run @CommonArgs
$probe = $LASTEXITCODE

if ($probe -eq 2) {
    Stop-WithError "The archiver could not start - see the error above." 2
}

if ($probe -ne 0) {
    Write-Warn "Not signed in. A Chromium window will open - log in to edX there."
    Write-Warn "Your password is typed only into that window; this script never sees it."

    & $VenvPython .\edx_course_downloader.py --login
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "Sign-in did not complete (exit $LASTEXITCODE)."
    }

    & $VenvPython .\edx_course_downloader.py --dry-run @CommonArgs
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "Still not able to read the course after signing in (exit $LASTEXITCODE)." $LASTEXITCODE
    }
}
Write-Ok "Signed in and the course outline is readable"

if ($DryRun) {
    Write-Step "Dry run only - nothing downloaded."
    exit 0
}

# ---------------------------------------------------------------------------
# 6. Archive
# ---------------------------------------------------------------------------
Write-Step "Archiving the course (Ctrl+C is safe - progress is saved)"

& $VenvPython .\edx_course_downloader.py @RunArgs
$archiveExit = $LASTEXITCODE

$Destination = Join-Path $Out $FolderName
$elapsed = (Get-Date) - $script:Started

Write-Host ""
if ($archiveExit -eq 0) {
    Write-Host ("=" * 74) -ForegroundColor Green
    Write-Ok "Finished in $([int]$elapsed.TotalMinutes)m $($elapsed.Seconds)s"
    Write-Ok "Folder    : $Destination"
    Write-Ok "Word file : $(Join-Path $Destination 'course.docx')"
    Write-Host ("=" * 74) -ForegroundColor Green

    if (Test-Path -LiteralPath $Destination) {
        Start-Process explorer.exe -ArgumentList "`"$Destination`""
    }
} elseif ($archiveExit -eq 130) {
    Write-Warn "Stopped by you. Re-run this script to resume where it left off."
} else {
    Write-Err "The archive finished with errors (exit $archiveExit)."
    Write-Err "Full detail: $(Join-Path $Destination 'archive.log')"
}

exit $archiveExit
