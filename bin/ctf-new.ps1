# Windows port of bin/ctf-new: scaffold a manual challenge workspace.
if ($args.Count -lt 1) { Write-Error 'usage: ctf-new <challenge-name>'; exit 2 }
$name = [string]$args[0]
$safe = $name.ToLower() -replace '[^a-z0-9._-]+', '-'

$CTF_HOME = if ($env:CTF_HOME) { $env:CTF_HOME } else { Split-Path -Parent $PSScriptRoot }
$env:PYTHONUTF8 = '1'
$root = Join-Path $CTF_HOME "ctfs\manual\$safe"
if (Test-Path $root) { Write-Error "exists: $root"; exit 1 }

foreach ($sub in 'files', 'work', 'notes', 'writeup', 'flag_output_dir') {
  New-Item -ItemType Directory -Force -Path (Join-Path $root $sub) | Out-Null
}

$noBom = New-Object System.Text.UTF8Encoding($false)
function Write-Text($path, $text) { [System.IO.File]::WriteAllText($path, $text, $noBom) }

$agent = @'
# Agent Context

This is a manually created challenge. Inspect the category and choose the appropriate CTF skill.

- Work: `work/`
- Notes: `notes/`
- Writeup: `writeup/solution.md`
- Evidence: `flag_output_dir/`
'@

$safety = @'
# Execution Safety

Treat supplied files as untrusted. Use `CTF_HOME/bin/run-isolated` before executing unknown code.
'@

$solution = @'
# Solution

## Summary

## Analysis

## Solving Steps

## Flag Validation
'@

Write-Text (Join-Path $root '.solver-status') "not_started`n"
Write-Text (Join-Path $root 'AGENT.md') ($agent + "`n")
Write-Text (Join-Path $root 'EXECUTION-SAFETY.md') ($safety + "`n")
Write-Text (Join-Path $root 'attachment-manifest.json') (@{ challenge = $name; files = @() } | ConvertTo-Json)
Write-Text (Join-Path $root 'writeup\solution.md') ($solution + "`n")
Write-Text (Join-Path $root 'README.md') "# $name`n`nCategory:`nTarget:`nFlag format:`n`nEvidence and solver output belong in flag_output_dir/.`n"

Write-Host "created $root"
