<#
.SYNOPSIS
    Rebuilds both Python environments after a fresh clone or git pull.

.DESCRIPTION
    Virtualenvs are not tracked in git, so they must be rebuilt locally.
    This repo has two independent environments:

      1. Root project      - Mason/BSH test framework, managed by Poetry,
                             needs Python >=3.13.1,<3.14, installs into .venv
      2. AUTO ROBOT FORCE TEST - standalone UR robot scripts, plain pip,
                             needs ur_rtde, installs into its own .venv

    Safe to re-run; existing environments are reused unless -Clean is passed.

.PARAMETER Only
    Build just one environment: 'root' or 'force'. Default builds both.

.PARAMETER Clean
    Delete existing virtualenvs before building.

.EXAMPLE
    .\bootstrap.ps1
    .\bootstrap.ps1 -Only force
    .\bootstrap.ps1 -Clean
#>
[CmdletBinding()]
param(
    [ValidateSet('root', 'force', 'both')]
    [string]$Only = 'both',

    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
$RepoRoot   = $PSScriptRoot
$ForceDir   = Join-Path $RepoRoot 'AUTO ROBOT FORCE TEST'
$failures   = @()

function Write-Step { param($Text) Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Ok   { param($Text) Write-Host "    OK  $Text" -ForegroundColor Green }
function Write-Warn { param($Text) Write-Host "    !   $Text" -ForegroundColor Yellow }
function Write-Fail { param($Text) Write-Host "    X   $Text" -ForegroundColor Red }

# Finds an interpreter satisfying a major.minor requirement via the py launcher,
# falling back to whatever `python` is on PATH.
function Find-Python {
    param([string]$MajorMinor)

    if (Get-Command py -ErrorAction SilentlyContinue) {
        $exe = & py "-$MajorMinor" -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $exe) { return $exe.Trim() }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $ver = & python -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
        if ($ver -and $ver.Trim() -eq $MajorMinor) { return (Get-Command python).Source }
    }
    return $null
}

function Remove-Venv {
    param([string]$Path)
    if (Test-Path $Path) {
        Write-Warn "removing existing $(Split-Path $Path -Leaf)"
        Remove-Item -Recurse -Force $Path
    }
}

# ---------------------------------------------------------------- root project
function Build-RootEnv {
    Write-Step 'Root project (Poetry, Python 3.13)'

    $py = Find-Python '3.13'
    if (-not $py) {
        Write-Fail 'Python 3.13 not found. pyproject.toml requires >=3.13.1,<3.14.'
        Write-Host '        Install it from https://www.python.org/downloads/ then re-run.' -ForegroundColor DarkGray
        if (Get-Command py -ErrorAction SilentlyContinue) {
            Write-Host '        Currently installed:' -ForegroundColor DarkGray
            & py -0p 2>&1 | ForEach-Object { Write-Host "          $_" -ForegroundColor DarkGray }
        }
        $script:failures += 'root (no Python 3.13)'
        return
    }
    Write-Ok "interpreter $py"

    if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
        Write-Fail 'poetry not on PATH.'
        Write-Host '        Install:  py -3.13 -m pip install --user poetry' -ForegroundColor DarkGray
        $script:failures += 'root (no poetry)'
        return
    }
    Write-Ok "poetry $((& poetry --version) -replace '[^\d.]', '')"

    if ($Clean) { Remove-Venv (Join-Path $RepoRoot '.venv') }

    # poetry.toml sets virtualenvs.in-project=true, so this lands in .venv/
    Write-Host '    installing dependencies (Bosch Artifactory, may take a while)...'
    Push-Location $RepoRoot
    try {
        & poetry env use $py | Out-Null
        & poetry install
        if ($LASTEXITCODE -ne 0) { throw "poetry install exited $LASTEXITCODE" }
        Write-Ok 'root environment ready  ->  .venv'
    } catch {
        Write-Fail $_.Exception.Message
        Write-Host '        Dependencies come from artifactory-04.boschdevcloud.com;' -ForegroundColor DarkGray
        Write-Host '        this needs VPN plus valid Artifactory credentials.' -ForegroundColor DarkGray
        $script:failures += 'root (poetry install failed)'
    } finally {
        Pop-Location
    }
}

# ------------------------------------------------------- AUTO ROBOT FORCE TEST
function Build-ForceEnv {
    Write-Step 'AUTO ROBOT FORCE TEST (pip, Python 3.11+)'

    if (-not (Test-Path $ForceDir)) {
        Write-Warn 'folder not present, skipping'
        return
    }

    # The scripts only need ur_rtde; any reasonably modern Python works.
    $py = $null
    foreach ($v in '3.11', '3.12', '3.13', '3.10') {
        $py = Find-Python $v
        if ($py) { break }
    }
    if (-not $py) {
        Write-Fail 'no suitable Python found (tried 3.10-3.13)'
        $script:failures += 'force (no Python)'
        return
    }
    Write-Ok "interpreter $py"

    $venv = Join-Path $ForceDir '.venv'
    if ($Clean) { Remove-Venv $venv }

    if (-not (Test-Path $venv)) {
        Write-Host '    creating virtualenv...'
        & $py -m venv $venv
        if ($LASTEXITCODE -ne 0) { Write-Fail 'venv creation failed'; $script:failures += 'force (venv)'; return }
    }

    $venvPy = Join-Path $venv 'Scripts\python.exe'
    Write-Host '    installing dependencies...'
    & $venvPy -m pip install --quiet --upgrade pip
    & $venvPy -m pip install --quiet -r (Join-Path $ForceDir 'requirements.txt')
    if ($LASTEXITCODE -ne 0) {
        Write-Fail 'pip install failed'
        $script:failures += 'force (pip)'
        return
    }

    # ur_rtde ships prebuilt wheels for most platforms but can fall back to a
    # source build that needs Boost + CMake, so confirm it actually imports.
    & $venvPy -c "import rtde_control, rtde_receive" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warn 'ur_rtde installed but failed to import - check for a compiler/Boost issue'
        $script:failures += 'force (ur_rtde import)'
        return
    }
    Write-Ok 'force test environment ready  ->  AUTO ROBOT FORCE TEST\.venv'
}

# ------------------------------------------------------------------------ main
Write-Host 'TST_NBN_ROBOT environment bootstrap' -ForegroundColor White

if ($Only -in 'root', 'both')  { Build-RootEnv }
if ($Only -in 'force', 'both') { Build-ForceEnv }

Write-Host ''
if ($failures.Count -eq 0) {
    Write-Host 'All requested environments built.' -ForegroundColor Green
    Write-Host ''
    Write-Host '  Run the Mason tests:   poetry run pytest' -ForegroundColor DarkGray
    Write-Host '  Run a force test:      & ".\AUTO ROBOT FORCE TEST\.venv\Scripts\python.exe" ".\AUTO ROBOT FORCE TEST\arm_code.py"' -ForegroundColor DarkGray
    exit 0
} else {
    Write-Host "Incomplete: $($failures -join ', ')" -ForegroundColor Red
    Write-Host 'See the messages above for what to install.' -ForegroundColor DarkGray
    exit 1
}
