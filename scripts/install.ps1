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

.EXAMPLE
  powershell -File scripts\install.ps1 -Action install
#>
[CmdletBinding()]
param(
  [ValidateSet('install', 'uninstall', 'status')]
  [string]$Action = 'status',
  [string]$CubaseDir = 'E:\Steinberg\Cubase 15',
  [string]$Built = ''
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $Built) { $Built = Join-Path $RepoRoot 'build\translation_vi.xml' }

# Candidate search directories, most likely first.
$Targets = @(
  (Join-Path $CubaseDir 'translation.xml'),
  (Join-Path $env:APPDATA 'Steinberg\Cubase 15_64\translation.xml')
)

function Assert-CubaseClosed {
  $running = Get-Process -Name 'Cubase*' -ErrorAction SilentlyContinue
  if ($running) {
    Write-Warning "Cubase is still running (PID $($running.Id -join ', ')). Close it first, or the file may be locked."
  }
}

function Show-Status {
  Write-Host "Cubase dir : $CubaseDir" -ForegroundColor Cyan
  if (Test-Path $Built) {
    Write-Host ("Built      : {0}  ({1:N0} bytes)" -f $Built, (Get-Item $Built).Length)
  } else {
    Write-Host "Built      : $Built  (MISSING - run: python tools\build.py)" -ForegroundColor Yellow
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
}

switch ($Action) {
  'install' {
    if (-not (Test-Path $Built)) { throw "missing build output: $Built  (run: python tools\build.py)" }
    try { [xml]$null = Get-Content $Built -Raw } catch { throw "not valid XML: $_" }
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
  }

  'status' { Show-Status }
}
