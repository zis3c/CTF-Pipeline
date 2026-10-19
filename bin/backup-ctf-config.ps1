# Windows port of bin/backup-ctf-config.
$CTF_HOME = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$dest = Join-Path (Join-Path $CTF_HOME 'backups') $stamp
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$files = @(
  'config\tools.json', 'config\requirements-ctf.txt', 'config\requirements-ctf.lock',
  'config\activate-ctf.ps1', 'bin\ctf-doctor.ps1'
)
foreach ($f in $files) {
  $src = Join-Path $CTF_HOME $f
  if (Test-Path $src) { Copy-Item -Force -Path $src -Destination $dest }
}

Write-Output $dest
