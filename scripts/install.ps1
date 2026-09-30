<#
.SYNOPSIS
  Install / uninstall the Vietnamese UI translation for Cubase.

.DESCRIPTION
  Cubase reads its UI strings from a plain-text XML database. The loader first
  tries '<dir>\translation.xml' on disk and only falls back to the copy embedded
  in Cubase15.exe, so dropping a file in the right directory overrides it - no
  need to patch the executable.

  This script installs to every plausible search directory. If "Vietnamese" does
  not show up in Edit > Preferences > General > Language, remove one of the
  installed files and start Cubase again to find which directory the loader uses.

.PARAMETER Action
  install | uninstall | status

.PARAMETER Variant
  en     - English and Vietnamese only.  THE DEFAULT, and the one in use.
  full   - the whole translation.xml, all nine languages plus Vietnamese

  Both are built by tools\build.py and both are kept. The default is "en"
  because Cubase reads it correctly - verified on 10,737 entries, no <us> and no
  <vi> lost, and not one Vietnamese value differing from the map - and it is
  1,449,424 bytes against 5,328,470.

  "full" is the file shape Steinberg ships: the original has all nine language
  elements in all 10,737 entries, so it is worth keeping as the fallback.

    - install.ps1 writes a .bak beside every file it overwrites
    - -Action uninstall puts the .bak back
    - keys\translation_original.xml is the source both are built from, and is
      in git

.PARAMETER NoScore
  Skip the Score Editor file instrumentnames_vi.xml.  The Score Editor is a
  separate engine (ScoringEngine.dll, Steinberg's Dorico core) with its own
  catalogue under Components\ScoringEngine\l10n, and it globs that folder -
  so unlike translation.xml there is exactly one place to put the file and no
  need to guess.  -NoScore installs the DAW translation alone.

.EXAMPLE
  powershell -File scripts\install.ps1 -Action install

.EXAMPLE
  powershell -File scripts\install.ps1 -Action install -Variant full

.EXAMPLE
  powershell -File scripts\install.ps1 -Action install -NoScore
#>
[CmdletBinding()]
param(
  [ValidateSet('install', 'uninstall', 'status')]
  [string]$Action = 'status',
  [ValidateSet('en', 'full')]
  [string]$Variant = 'en',
  [switch]$NoScore,
  [string]$CubaseDir = 'E:\Steinberg\Cubase 15',
  [string]$Built = ''
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $Built) {
  $Built = if ($Variant -eq 'en') {
    Join-Path $RepoRoot 'build\translation_vi_en.xml'
  } else {
    Join-Path $RepoRoot 'build\translation_vi.xml'
  }
}

# Candidate search directories, most likely first.
$Targets = @(
  (Join-Path $CubaseDir 'translation.xml'),
  (Join-Path $env:APPDATA 'Steinberg\Cubase 15_64\translation.xml')
)

# The Score Editor is a different engine with a different catalogue, and it
# globs one known folder, so this target is certain rather than a candidate.
$ScoreBuilt  = Join-Path $RepoRoot 'build\instrumentnames_vi.xml'
$ScoreTarget = Join-Path $CubaseDir 'Components\ScoringEngine\l10n\instrumentnames_vi.xml'

function Assert-CubaseClosed {
  $running = Get-Process -Name 'Cubase*' -ErrorAction SilentlyContinue
  if ($running) {
    Write-Warning "Cubase is still running (PID $($running.Id -join ', ')). Close it first, or the file may be locked."
  }
}

function Show-Status {
  Write-Host "Cubase dir : $CubaseDir" -ForegroundColor Cyan
  foreach ($v in @('full', 'en')) {
    $f = if ($v -eq 'en') { Join-Path $RepoRoot 'build\translation_vi_en.xml' }
         else { Join-Path $RepoRoot 'build\translation_vi.xml' }
    if (Test-Path $f) {
      Write-Host ("  {0,-5}  {1,12:N0} bytes  {2}" -f $v, (Get-Item $f).Length, (Split-Path -Leaf $f))
    } else {
      Write-Host ("  {0,-5}  {1,12}  {2}  (MISSING - run: python tools\build.py)" -f $v, '-', (Split-Path -Leaf $f)) -ForegroundColor Yellow
    }
  }
  Write-Host ''
  foreach ($t in $Targets) {
    $dir = Split-Path $t -Parent
    $state = if (Test-Path $t) { 'INSTALLED' } else { 'absent   ' }
    $color  = if (Test-Path $t) { 'Green' } else { 'DarkGray' }
    Write-Host ("  [{0}] {1}" -f $state, $t) -ForegroundColor $color
    if (-not (Test-Path (Split-Path $t -Parent))) {
      Write-Host ("             (thư mục cha chưa tồn tại: {0})" -f $dir) -ForegroundColor DarkGray
    }
    if (Test-Path "$t.bak") { Write-Host "             backup: $t.bak" -ForegroundColor DarkYellow }
  }

  Write-Host ''
  Write-Host 'Score Editor (ScoringEngine.dll, separate engine)' -ForegroundColor Cyan
  if (Test-Path $ScoreBuilt) {
    Write-Host ("  built    {0,12:N0} bytes  {1}" -f (Get-Item $ScoreBuilt).Length, (Split-Path -Leaf $ScoreBuilt))
  } else {
    Write-Host ("  built    {0,12}  {1}  (MISSING - run: python tools\score_instruments.py build)" -f '-', (Split-Path -Leaf $ScoreBuilt)) -ForegroundColor Yellow
  }
  $scoreState = if (Test-Path $ScoreTarget) { 'INSTALLED' } else { 'absent   ' }
  $scoreColor = if (Test-Path $ScoreTarget) { 'Green' } else { 'DarkGray' }
  Write-Host ("  [{0}] {1}" -f $scoreState, $ScoreTarget) -ForegroundColor $scoreColor
  if (Test-Path "$ScoreTarget.bak") { Write-Host "          backup: $ScoreTarget.bak" -ForegroundColor DarkYellow }
}

switch ($Action) {
  'install' {
    if (-not (Test-Path $Built)) { throw "missing build output: $Built  (run: python tools\build.py)" }
    try { [xml]$null = Get-Content $Built -Raw } catch { throw "not valid XML: $_" }
    Write-Host ("variant    : {0}   ({1:N0} bytes)" -f $Variant, (Get-Item $Built).Length) -ForegroundColor Cyan
    Assert-CubaseClosed

    foreach ($t in $Targets) {
      $dir = Split-Path $t -Parent
      if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
      if (Test-Path $t) { Copy-Item $t "$t.bak" -Force; Write-Host "backed up -> $t.bak" -ForegroundColor DarkYellow }
      Copy-Item $Built $t -Force
      Write-Host "installed -> $t" -ForegroundColor Green
    }
    Write-Host ''
    Write-Host 'Next: start Cubase -> Edit > Preferences > General > Language -> Vietnamese -> restart Cubase' -ForegroundColor Cyan
    Write-Host 'If "Vietnamese" is not listed, run -Action uninstall and try only one target at a time.' -ForegroundColor DarkGray

    if (-not $NoScore) {
      if (-not (Test-Path $ScoreBuilt)) {
        Write-Host ''
        Write-Host ("Score Editor skipped: {0} not built  (run: python tools\score_instruments.py build)" -f (Split-Path -Leaf $ScoreBuilt)) -ForegroundColor Yellow
      } else {
        try { [xml]$null = Get-Content $ScoreBuilt -Raw } catch { throw "not valid XML: $_" }
        $sdir = Split-Path $ScoreTarget -Parent
        if (-not (Test-Path $sdir)) { New-Item -ItemType Directory -Force -Path $sdir | Out-Null }
        if (Test-Path $ScoreTarget) { Copy-Item $ScoreTarget "$ScoreTarget.bak" -Force; Write-Host "backed up -> $ScoreTarget.bak" -ForegroundColor DarkYellow }
        Copy-Item $ScoreBuilt $ScoreTarget -Force
        Write-Host ("installed -> {0}  ({1:N0} bytes)" -f $ScoreTarget, (Get-Item $ScoreBuilt).Length) -ForegroundColor Green
      }
    }
  }

  'uninstall' {
    Assert-CubaseClosed
    foreach ($t in $Targets) {
      if (Test-Path "$t.bak") {
        Move-Item "$t.bak" $t -Force
        Write-Host "restored -> $t" -ForegroundColor Green
      } elseif (Test-Path $t) {
        Remove-Item $t -Force
        Write-Host "removed  -> $t" -ForegroundColor Green
      }
    }
    if (-not $NoScore) {
      if (Test-Path "$ScoreTarget.bak") {
        Move-Item "$ScoreTarget.bak" $ScoreTarget -Force
        Write-Host "restored -> $ScoreTarget" -ForegroundColor Green
      } elseif (Test-Path $ScoreTarget) {
        Remove-Item $ScoreTarget -Force
        Write-Host "removed  -> $ScoreTarget" -ForegroundColor Green
      }
    }
  }

  'status' { Show-Status }
}
