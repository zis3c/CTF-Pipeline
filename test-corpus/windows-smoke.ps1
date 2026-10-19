# Offline smoke test for the Windows pipeline: no CTFd server required.
# Exercises ctf-pull.ps1 set-status/open against a throwaway profile.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$env:CTF_HOME = $repo
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$tmp = Join-Path $env:TEMP ("ctf-smoke-" + [guid]::NewGuid().ToString('N'))
$env:CTF_PROFILES_ROOT = $tmp
$root = Join-Path $tmp 'demo'
New-Item -ItemType Directory -Force -Path (Join-Path $root '.ctfd') | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)
$chal = '[{"id":1,"name":"Fixture Chal","category":"Cryptography","type":"standard","value":100,"description":"x","files":[],"hints":[]}]'
[System.IO.File]::WriteAllText((Join-Path $root 'challenges-detailed.json'), $chal, $utf8)
[System.IO.File]::WriteAllText((Join-Path $root '.ctfd\config.json'), '{"CTFD":{"URL":"http://127.0.0.1:9","TOKEN":"x"},"Challenges":[]}', $utf8)

$pull = Join-Path $repo 'bin\ctf-pull.ps1'
try {
  $out = & $pull set-status --name demo --challenge 'Fixture Chal' --status in_progress
  if (($out -join "`n") -notmatch 'Status updated') { throw 'set-status failed' }

  $chalDir = Join-Path $root 'crypto\fixture-chal'
  if (-not (Test-Path (Join-Path $chalDir 'attachment-manifest.json'))) { throw 'manifest missing' }
  if ((Get-Content (Join-Path $root 'INDEX.md') -Raw) -notmatch '\[~\]') { throw 'INDEX status missing' }

  $path = (& $pull open --name demo --challenge 'Fixture Chal' | Select-Object -First 1).Trim()
  # Compare by shape, not exact string: the tool canonicalizes the path (8.3 short
  # names, drive case), so it can differ from the caller-built $chalDir.
  if (-not (Test-Path -LiteralPath $path -PathType Container)) { throw "open returned a missing directory: $path" }
  if ($path -notmatch '[\\/]crypto[\\/]fixture-chal$') { throw "open returned: $path (expected ...\crypto\fixture-chal)" }
} finally {
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
Write-Host 'windows pipeline smoke test: OK'
