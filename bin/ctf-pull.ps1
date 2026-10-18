# Windows port of bin/ctf-pull. Talks to CTFd through the external `ctfd` CLI
# (CTFD_BIN env -> `ctfd` on PATH -> `python -m ctfd`) and drives the local
# helper scripts/ctf-pipeline.py.
$ErrorActionPreference = 'Stop'

$CTF_HOME = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$env:CTF_HOME = $CTF_HOME
$PY = if ($env:CTF_PYTHON) { $env:CTF_PYTHON } else { 'python' }
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONPATH = $CTF_HOME + $(if ($env:PYTHONPATH) { ';' + $env:PYTHONPATH } else { '' })
$PIPE = $CTF_HOME
$HELPER = Join-Path $PIPE 'scripts\ctf-pipeline.py'
$BASE_ROOT = if ($env:CTF_PROFILES_ROOT) { $env:CTF_PROFILES_ROOT } else { Join-Path $CTF_HOME 'ctfs' }
$CTFD_BIN = if ($env:CTFD_BIN) { $env:CTFD_BIN } else { '' }
$LOGDIR = Join-Path $CTF_HOME 'logs\sync'

$Argv = @($args)
if ($Argv.Count -lt 1) { $MODE = 'help' }
elseif ($Argv.Count -eq 1) { $MODE = [string]$Argv[0]; $Argv = @() }
else { $MODE = [string]$Argv[0]; $Argv = $Argv[1..($Argv.Count - 1)] }

$PROFILE = ''
$DRY_RUN = $false
$CHALLENGE = ''
$STATUS_VALUE = ''
$POSITIONAL = New-Object System.Collections.Generic.List[string]

$i = 0
while ($i -lt $Argv.Count) {
  $a = [string]$Argv[$i]
  if ($a -eq '--name' -or $a -eq '-n') {
    if ($i + 1 -ge $Argv.Count) { Write-Error 'Missing profile name'; exit 2 }
    $PROFILE = [string]$Argv[$i + 1]; $i += 2
  } elseif ($a -eq '--dry-run') { $DRY_RUN = $true; $i += 1 }
  elseif ($a -eq '--challenge') {
    if ($i + 1 -ge $Argv.Count) { Write-Error 'Missing challenge name'; exit 2 }
    $CHALLENGE = [string]$Argv[$i + 1]; $i += 2
  } elseif ($a -eq '--status') {
    if ($i + 1 -ge $Argv.Count) { Write-Error 'Missing status value'; exit 2 }
    $STATUS_VALUE = [string]$Argv[$i + 1]; $i += 2
  } else { $POSITIONAL.Add($a); $i += 1 }
}

function Show-Usage {
  @"
Usage:
  ctf-pull init --name NAME --url URL     Create a named CTF profile (prompts for token)
  ctf-pull sync --name NAME              Refresh one profile's metadata
  ctf-pull pull --name NAME              Sync one profile and download everything
  ctf-pull resync --name NAME            Force-refresh one profile
  ctf-pull resync --name NAME --dry-run  Preview metadata changes only
  ctf-pull status --name NAME            Show one profile's status
  ctf-pull list                          List all configured CTF profiles

Local folders work/, notes/ and flag_output_dir/ are preserved during resync.
"@
}

New-Item -ItemType Directory -Force -Path $BASE_ROOT, $LOGDIR | Out-Null

$validModes = 'init', 'sync', 'pull', 'resync', 'status', 'list', 'doctor', 'set-status', 'open', 'git-init'
if ($MODE -notin $validModes) {
  if ($MODE -in 'help', '-h', '--help') { Show-Usage; exit 0 }
  Write-Error "Unknown mode: $MODE"
  Show-Usage
  exit 2
}

function Get-EventSlug([string]$Value) {
  $code = @'
import re, sys, unicodedata
s = unicodedata.normalize('NFKD', sys.argv[1]).encode('ascii', 'ignore').decode()
s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
print(s or 'ctf-event')
'@
  $out = $code | & $PY - $Value
  if ($LASTEXITCODE -ne 0) { throw 'event_slug failed' }
  return ($out | Out-String).Trim()
}

function Get-ProfileRoots {
  @(Get-ChildItem -Path $BASE_ROOT -Recurse -Depth 2 -Filter 'config.json' -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Directory.Name -eq '.ctfd' } |
    ForEach-Object { $_.Directory.Parent.FullName } |
    Sort-Object -Unique)
}

function Resolve-Root {
  if ([string]::IsNullOrEmpty($PROFILE)) {
    $found = Get-ProfileRoots
    if ($found.Count -ne 1) { Write-Error 'Specify --name NAME (or use ctf-pull list).'; exit 2 }
    $script:ROOT = $found[0]
  } else {
    $PROFILE = Get-EventSlug $PROFILE
    $script:ROOT = Join-Path $BASE_ROOT $PROFILE
  }
  New-Item -ItemType Directory -Force -Path $ROOT | Out-Null
  $script:CONFIG = Join-Path $ROOT '.ctfd\config.json'
  $script:LOGDIR = Join-Path (Join-Path $CTF_HOME 'logs\sync') $PROFILE
  New-Item -ItemType Directory -Force -Path $LOGDIR | Out-Null
  $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
  $script:LOG = Join-Path $LOGDIR "$stamp-$MODE.log"
}

function Invoke-Helper([string[]]$HelperArgs) {
  & $PY $HELPER @HelperArgs
}

function Invoke-Ctfd([string[]]$CtfdArgs) {
  if ($null -eq $CtfdArgs) { $CtfdArgs = @() }
  Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $env:TEMP '.ctfd.cache')
  if ($CTFD_BIN) { $exe = $CTFD_BIN; $pre = @() }
  elseif (Get-Command ctfd -ErrorAction SilentlyContinue) { $exe = 'ctfd'; $pre = @() }
  else { $exe = $PY; $pre = @('-m', 'ctfd') }
  $run = @($pre) + @('-d', $ROOT) + @($CtfdArgs)
  for ($attempt = 1; $attempt -le 3; $attempt++) {
    $ep = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try { $out = & $exe @run 2>&1 } finally { $ErrorActionPreference = $ep }
    $code = $LASTEXITCODE
    $out | ForEach-Object { $_.ToString() } | Tee-Object -FilePath $LOG -Append
    Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $env:TEMP '.ctfd.cache')
    if ($code -eq 0) { return }
    "Retrying CTFd command ($attempt/3)..." | Tee-Object -FilePath $LOG -Append
    Start-Sleep -Seconds ($attempt * 2)
  }
  throw 'CTFd command failed after 3 attempts'
}

function Export-Metadata {
  if (-not (Test-Path $CONFIG)) { return }
  $code = @'
import json, sys
from pathlib import Path
root, config_path = map(Path, sys.argv[1:])
config = json.loads(config_path.read_text())
details = config.get('Challenges', [])
summary = []
for challenge in details:
    summary.append({
        'name': challenge.get('name', ''),
        'category': challenge.get('category', ''),
        'type': challenge.get('type', ''),
        'is_downloaded': bool(challenge.get('is_downloaded', False)),
        'id': challenge.get('id', ''),
    })
for name, data in (('challenges-detailed.json', details), ('challenges.json', summary)):
    (root / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
'@
  $code | & $PY - $ROOT $CONFIG
  if ($LASTEXITCODE -ne 0) { throw 'export_metadata failed' }
}

function Write-EventInfo {
  if (-not (Test-Path $CONFIG)) { return }
  $code = @'
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path
root, config_path = map(Path, sys.argv[1:])
d = json.loads(config_path.read_text())
url = d.get('CTFD', {}).get('URL', '').rstrip('/')
title = 'CTF Event'
try:
    import requests
    html = requests.get(url + '/', timeout=15).text
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    if m: title = re.sub(r'\s+', ' ', m.group(1)).strip()
except Exception:
    pass
chals = d.get('Challenges', [])
counts = {}
for c in chals: counts[c.get('category', 'Unknown')] = counts.get(c.get('category', 'Unknown'), 0) + 1
lines = [f'# {title}', '', '## CTF Information', '', '- **Platform:** CTFd', f'- **URL:** {url}',
         f'- **Last sync:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}',
         f'- **Total challenges:** {len(chals)}', '', '## Challenge Summary', '', '| Category | Count |', '|---|---:|']
lines += [f'| {k} | {v} |' for k, v in sorted(counts.items())]
lines += ['', '## Resync', '', 'Run `ctf-pull resync` to refresh challenge metadata and attachments.', '',
          'Local `work/`, `notes/` and `flag_output_dir/` folders are preserved.']
(root / '_ctf-info.md').write_text('\n'.join(lines) + '\n')
'@
  $code | & $PY - $ROOT $CONFIG
}

function Normalize-Categories {
  if (-not (Test-Path $ROOT)) { return }
  $map = [ordered]@{
    'Cryptography' = 'crypto'; 'Web' = 'web'; 'Binary' = 'pwn'; 'Reverse' = 'reverse'
    'Forensics' = 'forensics'; 'Mobile' = 'mobile'; 'OSINT' = 'osint'; 'Misc' = 'misc'
    'Boot2Root' = 'boot2root'; 'Selamat' = 'welcome'
  }
  Get-ChildItem -Path $ROOT -Directory -Force | Where-Object { $_.Name -ne '.ctfd' } | ForEach-Object {
    $dir = $_
    $name = $null
    foreach ($k in $map.Keys) { if ($dir.Name -like "*$k*") { $name = $map[$k]; break } }
    if (-not $name) { return }
    $target = Join-Path $ROOT $name
    if ($dir.FullName -ne $target) {
      New-Item -ItemType Directory -Force -Path $target | Out-Null
      Get-ChildItem -Path $dir.FullName -Force | ForEach-Object { Move-Item -Force -Path $_.FullName -Destination $target }
      Remove-Item -Force -Recurse -Path $dir.FullName
    }
  }
}

function Invoke-Organize {
  $detailed = Join-Path $ROOT 'challenges-detailed.json'
  if (-not (Test-Path $detailed)) { return }
  $code = @'
import json, re, sys
from pathlib import Path
root, detailed = map(Path, sys.argv[1:])
items = json.loads(detailed.read_text())

def slug(value, fallback='challenge'):
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()
    return value or fallback

def category(value):
    v = value.lower()
    names = [('cryptography','crypto'),('web exploitation','web'),('binary exploitation','pwn'),
             ('reverse engineering','reverse'),('digital forensics','forensics'),
             ('mobile exploitation','mobile'),('osint','osint'),('miscellaneous','misc'),
             ('boot2root','boot2root'),('selamat','welcome')]
    for needle, short in names:
        if needle in v: return short
    return slug(value, 'other')

for item in items:
    cat = root / category(item.get('category', 'Other'))
    chal = cat / slug(item.get('name', 'challenge'))
    cat.mkdir(parents=True, exist_ok=True)
    if not chal.exists():
        old = cat / item.get('name', '').replace(' ', '-')
        if old.exists(): old.rename(chal)
    chal.mkdir(exist_ok=True)
    (chal / 'work').mkdir(exist_ok=True)
    (chal / 'notes').mkdir(exist_ok=True)
    (chal / 'flag_output_dir').mkdir(exist_ok=True)
    readme = chal / 'README.md'
    if not readme.exists():
        desc = (item.get('description') or 'No description provided.').replace('\r', '')
        hints = item.get('hints') or []
        lines = [f"# {item.get('name','Challenge')}", '', f"- **ID:** {item.get('id','')}",
                 f"- **Category:** {item.get('category','')}", f"- **Type:** {item.get('type','')}",
                 f"- **Points:** {item.get('value','')}", '', '## Description', '', desc]
        if item.get('connection_info'): lines += ['', '## Connection', '', str(item['connection_info'])]
        if hints:
            lines += ['', '## Hints', ''] + [f"- {h.get('content', h) if isinstance(h, dict) else h}" for h in hints]
        files = item.get('files') or []
        if files: lines += ['', '## Files', ''] + [f"- {Path(str(f)).name}" for f in files]
        readme.write_text('\n'.join(lines) + '\n')
'@
  $code | & $PY - $ROOT $detailed
  if ($LASTEXITCODE -ne 0) { throw 'organize_from_json failed' }
}

function Ensure-Layout {
  if (-not (Test-Path $ROOT)) { return }
  $template = @"
# Solution

## Summary

<!-- Describe the intended vulnerability or solving idea. -->

## Analysis

<!-- Record the important observations and commands. -->

## Exploitation / Solving Steps

<!-- Add reproducible steps here. -->

## Flag Validation

<!-- Record how the flag was verified by the challenge platform/artifact. -->

"@
  Get-ChildItem -Path $ROOT -Directory -Force | Where-Object { $_.Name -ne '.ctfd' } | ForEach-Object {
    $cat = $_
    Get-ChildItem -Path $cat.FullName -Directory -Force | ForEach-Object {
      foreach ($sub in 'work', 'notes', 'writeup', 'flag_output_dir') {
        New-Item -ItemType Directory -Force -Path (Join-Path $_.FullName $sub) | Out-Null
      }
      $sol = Join-Path $_.FullName 'writeup\solution.md'
      if (-not (Test-Path $sol)) { Set-Content -Path $sol -Value $template -Encoding UTF8 }
    }
  }
}

if ($MODE -ne 'list') {
  Resolve-Root
  try {
    $script:LOCK = [System.IO.File]::Open((Join-Path $ROOT '.pipeline.lock'),
      [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
  } catch {
    Write-Error "Pipeline is already running for profile: $PROFILE"
    exit 1
  }
}

switch ($MODE) {
  'init' {
    if ([string]::IsNullOrEmpty($PROFILE)) { Write-Error 'Usage: ctf-pull init --name NAME --url URL'; exit 2 }
    Invoke-Ctfd (@('init') + $POSITIONAL.ToArray())
    Write-EventInfo
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $CONFIG) | Out-Null
  }
  'sync' {
    if ($DRY_RUN) { Invoke-Helper @('dry-run', $ROOT); break }
    Invoke-Helper @('snapshot', $ROOT)
    Invoke-Ctfd @('sync', '--force')
    Export-Metadata
    Normalize-Categories
    Invoke-Organize
    Invoke-Helper @('diff', $ROOT)
    Invoke-Helper @('generate', $ROOT)
    Write-EventInfo
    Ensure-Layout
  }
  { $_ -eq 'pull' -or $_ -eq 'resync' } {
    if ($DRY_RUN) { Invoke-Helper @('dry-run', $ROOT); break }
    Invoke-Helper @('snapshot', $ROOT)
    Invoke-Helper @('archive', $ROOT)
    Invoke-Ctfd @('sync', '--force')
    Export-Metadata
    Invoke-Ctfd @('challenges', '--force')
    Export-Metadata
    Normalize-Categories
    Invoke-Organize
    Invoke-Helper @('diff', $ROOT)
    Invoke-Helper @('generate', $ROOT)
    Write-EventInfo
    Ensure-Layout
  }
  'status' {
    if (-not (Test-Path $CONFIG)) { Write-Error "Not initialized: $CONFIG"; exit 1 }
    $code = @'
import json, os, sys
p = sys.argv[1]
d = json.load(open(p))
print('URL:', d.get('CTFD', {}).get('URL', ''))
print('CTF root:', os.path.dirname(os.path.dirname(os.path.abspath(p))))
print('Challenges cached:', len(d.get('Challenges', [])))
'@
    $code | & $PY - $CONFIG
  }
  'list' {
    '{0,-24} {1}' -f 'PROFILE', 'ROOT'
    Get-ProfileRoots | ForEach-Object { '{0,-24} {1}' -f (Split-Path -Leaf $_), $_ }
  }
  'doctor' { Invoke-Helper @('doctor', $ROOT) }
  'set-status' {
    if ([string]::IsNullOrEmpty($CHALLENGE) -or [string]::IsNullOrEmpty($STATUS_VALUE)) {
      Write-Error 'Usage: ctf-pull set-status --name PROFILE --challenge CHALLENGE --status STATUS'; exit 2
    }
    Invoke-Helper @('set-status', $ROOT, $CHALLENGE, $STATUS_VALUE)
  }
  'open' {
    if ([string]::IsNullOrEmpty($CHALLENGE)) {
      Write-Error 'Usage: ctf-pull open --name PROFILE --challenge CHALLENGE'; exit 2
    }
    Invoke-Helper @('open', $ROOT, $CHALLENGE)
  }
  'git-init' { Invoke-Helper @('git-init', $ROOT) }
}

if ($MODE -ne 'list' -and $script:LOCK) { $script:LOCK.Dispose() }

if ($MODE -ne 'list') {
  "Workspace: $ROOT"
  "Log: $LOG"
}
