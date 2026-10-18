# Windows port of bin/ctf-update-all.
# No apt/gem on Windows: this updates the Python environment and pulls the
# pipeline repository. Native tools are left to winget/manual updates.
$ErrorActionPreference = 'Continue'

$ROOT = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$PY = if ($env:CTF_PYTHON) { $env:CTF_PYTHON } else { 'python' }
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$CFG = Join-Path $ROOT 'config'
$LOGDIR = Join-Path $ROOT 'logs\update'
New-Item -ItemType Directory -Force -Path $LOGDIR | Out-Null
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$LOG = Join-Path $LOGDIR "$stamp.log"
Start-Transcript -Path $LOG | Out-Null

Write-Host "=== CTF update started: $stamp ==="
Write-Host "Log: $LOG"

Write-Host '[1/5] Backup current configuration'
& (Join-Path $ROOT 'bin\backup-ctf-config.ps1')

Write-Host '[2/5] Update Python CTF environment'
& $PY -m pip install --upgrade pip
& $PY -m pip install --upgrade -r (Join-Path $CFG 'requirements-ctf.in')
& $PY -m pip freeze --local | Sort-Object | Set-Content (Join-Path $CFG 'requirements-ctf.lock')

Write-Host '[3/5] Update pipeline repository'
$dirty = git -C $ROOT status --porcelain
if (-not (Test-Path (Join-Path $ROOT '.git'))) {
  Write-Host "SKIP missing repo: $ROOT"
} elseif ($dirty) {
  Write-Host "SKIP dirty repo (local changes preserved): $ROOT"
} else {
  git -C $ROOT pull --ff-only
}

Write-Host '[4/5] Refresh inventory and verify'
& $PY (Join-Path $ROOT 'scripts\refresh-tools-json.py')
& (Join-Path $ROOT 'bin\ctf-doctor.ps1')

Write-Host '[5/5] Save post-update backup'
& (Join-Path $ROOT 'bin\backup-ctf-config.ps1')

Write-Host "=== CTF update completed: $((Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')) ==="
Stop-Transcript | Out-Null
