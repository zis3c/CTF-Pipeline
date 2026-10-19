# Windows equivalent of activate-ctf.sh. Dot-source it:
#   . "$CTF_HOME\config\activate-ctf.ps1"
if (-not $env:CTF_HOME) {
  $env:CTF_HOME = Split-Path -Parent $PSScriptRoot
}
if (-not $env:CTF_PYTHON) {
  $cmd = Get-Command python -ErrorAction SilentlyContinue
  $env:CTF_PYTHON = if ($cmd) { $cmd.Source } else { 'python' }
}
$env:CTF_GLOBAL_EVIDENCE_DIR = Join-Path $env:CTF_HOME 'evidence'
$env:PATH = (Join-Path $env:CTF_HOME 'bin') + ';' + $env:PATH
# Windows Python defaults to the locale (cp1252) encoding; force UTF-8 so the
# helper scripts read/write the generated JSON consistently.
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
# Expose the bundled `ctfd` module so `python -m ctfd` works.
$env:PYTHONPATH = $env:CTF_HOME + $(if ($env:PYTHONPATH) { ';' + $env:PYTHONPATH } else { '' })

function ctf-update { & (Join-Path $env:CTF_HOME 'bin\ctf-update-all.ps1') @args }
function ctf-pull { & (Join-Path $env:CTF_HOME 'bin\ctf-pull.ps1') @args }

Write-Host "CTF environment: $env:CTF_PYTHON"
Write-Host "Global evidence directory: $env:CTF_GLOBAL_EVIDENCE_DIR"
