# Windows port of bin/ctf-install-tools.
# There is no apt on Windows: this installs the Python toolchain with pip and
# reports the optional packages, leaving native binaries to winget/manual setup.
param([switch]$DryRun, [switch]$Extras)

$CTF_HOME = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$PY = if ($env:CTF_PYTHON) { $env:CTF_PYTHON } else { 'python' }
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

function Invoke-Step([string]$Exe, [string[]]$Params) {
  Write-Host ("+ {0} {1}" -f $Exe, ($Params -join ' '))
  if ($DryRun) { return $true }
  & $Exe @Params
  if ($LASTEXITCODE -ne 0) { return $false }
  return $true
}

Invoke-Step $PY @('-m', 'pip', 'install', '--upgrade', 'pip') | Out-Null

if (-not (Invoke-Step $PY @('-m', 'pip', 'install', 'requests'))) {
  Write-Error 'Failed to install requests (required by scripts/ctf-pipeline.py)'
  exit 1
}

$req = Join-Path $CTF_HOME 'config\requirements-ctf.txt'
Write-Host '[INFO] Installing the Python CTF packages. Some Linux-only packages (fpylll, angr, pwntools, ...) may fail on Windows; that does not stop the pipeline.'
if ($DryRun) {
  Write-Host ("+ {0} -m pip install -r {1}" -f $PY, $req)
} else {
  try {
    & $PY -m pip install -r $req
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Some packages did not install; the core pipeline still works.' }
  } catch { Write-Warning "requirements install error: $_" }
}

if ($Extras) {
  if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
    Invoke-Step $PY @('-m', 'pip', 'install', '--user', 'pipx') | Out-Null
    Invoke-Step $PY @('-m', 'pipx', 'ensurepath') | Out-Null
  }
  # `pipx install --force` fails with the uv backend when the venv already
  # exists, so upgrade installed tools and only install the missing ones.
  $installed = @()
  if (-not $DryRun) {
    $installed = (& $PY -m pipx list --short 2>$null) |
      ForEach-Object { ($_ -split '\s+')[0] }
  }
  $pipxFailures = 0
  foreach ($pkg in 'objection', 'msoffcrypto-tool', 'name-that-hash', 'xortool', 'oletools', 'volatility3', 'pytesseract') {
    if ($installed -contains $pkg) {
      $ok = Invoke-Step $PY @('-m', 'pipx', 'upgrade', $pkg)
    } else {
      $ok = Invoke-Step $PY @('-m', 'pipx', 'install', $pkg)
    }
    if (-not $ok) {
      Write-Warning "pipx failed for $pkg; continuing."
      $pipxFailures++
    }
  }
  if ($pipxFailures -gt 0) { Write-Warning "$pipxFailures pipx tool(s) failed." }
}

$tools = Join-Path $CTF_HOME 'config\tools.json'
if (-not (Test-Path $tools)) {
  Write-Host "Initializing local tool inventory: $tools"
  if (-not $DryRun) { Copy-Item (Join-Path $CTF_HOME 'config\tools.example.json') $tools }
}

if (-not $DryRun) {
  & $PY (Join-Path $CTF_HOME 'scripts\refresh-tools-json.py')
  & (Join-Path $CTF_HOME 'bin\ctf-doctor.ps1')
}
Write-Host 'CTF tool installation completed.'
