# Windows port of bin/ctf-doctor. Checks the Python CTF environment and the
# tools reachable on Windows; Linux-only binaries are reported as warnings.
$ErrorActionPreference = 'Continue'

$CTF_ROOT = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$env:CTF_HOME = $CTF_ROOT
$PY = if ($env:CTF_PYTHON) { $env:CTF_PYTHON } else { 'python' }
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$errors = 0
function Pass($m) { Write-Host "[OK] $m" }
function Warn($m) { Write-Host "[WARN] $m" }
function Fail($m) { Write-Host "[FAIL] $m"; $script:errors++ }

if (Get-Command $PY -ErrorAction SilentlyContinue) { Pass "Python executable ($PY)" } else { Fail "Python executable missing ($PY)" }

$ver = (& $PY -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>$null | Out-String).Trim()
$verOk = $false
if ($LASTEXITCODE -eq 0 -and $ver) { try { $verOk = ([version]$ver -ge [version]'3.10') } catch { $verOk = $false } }
if ($verOk) { Pass "Python $ver" } else { Fail "Python version (need >= 3.10)" }

& $PY -m pip check *> $null
if ($LASTEXITCODE -eq 0) { Pass "Python dependencies" } else { Fail "Python dependency check" }

$modules = 'pwn', 'Crypto', 'gmpy2', 'fpylll', 'angr', 'qiling', 'frida', 'uncompyle6', 'keystone', 'elftools',
'volatility3', 'yara', 'pefile', 'oletools', 'flask_unsign', 'dnslib', 'shodan', 'scapy', 'capstone', 'lief', 'z3'
foreach ($m in $modules) {
  & $PY -c "import $m" *> $null
  if ($LASTEXITCODE -eq 0) { Pass "import $m" } else { Fail "import $m" }
}

foreach ($x in 'git', 'curl', 'python', 'pip') {
  if (Get-Command $x -ErrorAction SilentlyContinue) { Pass "command $x" } else { Warn "command $x not found" }
}
foreach ($x in 'gdb', 'checksec', 'ROPgadget', 'ghidra', 'nmap', 'tshark', 'binwalk', 'exiftool', 'steghide', 'docker', 'podman', 'vol', 'one_gadget', 'zsteg') {
  if (Get-Command $x -ErrorAction SilentlyContinue) { Pass "command $x" } else { Warn "command $x not found (Linux-only or optional)" }
}

$tools = Join-Path $CTF_ROOT 'config\tools.json'
$toolsOk = $false
if (Test-Path $tools) {
  & $PY -m json.tool $tools *> $null
  if ($LASTEXITCODE -eq 0) { $toolsOk = $true }
}
if ($toolsOk) { Pass 'tools.json valid' } else { Fail 'tools.json invalid or missing' }

try {
  $driveRoot = [System.IO.Path]::GetPathRoot((Resolve-Path $CTF_ROOT).Path)
  $freeGb = (New-Object System.IO.DriveInfo($driveRoot)).AvailableFreeSpace / 1GB
  if ($freeGb -gt 10) { Pass ("disk space {0:N1} GiB free" -f $freeGb) } else { Warn ("disk space below 10 GiB ({0:N1} GiB)" -f $freeGb) }
} catch { Warn 'disk space check failed' }

Write-Host "Doctor result: $errors error(s)"
exit $errors
