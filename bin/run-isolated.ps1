# Windows port of bin/run-isolated.
# Prefers a container runtime (Docker/Podman) when installed; otherwise falls
# back to Windows Sandbox with the folder mounted read-only and networking off.
if ($args.Count -lt 1) { Write-Error 'usage: run-isolated <directory> [command...]'; exit 2 }
$target = [string]$args[0]
$rest = if ($args.Count -gt 1) { $args[1..($args.Count - 1)] } else { @() }
if (-not (Test-Path -LiteralPath $target -PathType Container)) { Write-Error "directory not found: $target"; exit 1 }
$full = (Resolve-Path -LiteralPath $target).Path

$runtime = $null
if (Get-Command podman -ErrorAction SilentlyContinue) { $runtime = 'podman' }
elseif (Get-Command docker -ErrorAction SilentlyContinue) { $runtime = 'docker' }

if ($runtime) {
  $cmd = if ($rest.Count -eq 0) { @('/bin/bash') } else { $rest }
  $runArgs = @('run', '--rm', '--network=none', '--cap-drop=ALL', '--security-opt=no-new-privileges',
               '--read-only', '--tmpfs', '/tmp:rw,noexec,nosuid,size=256m',
               '-v', "${full}:/work:ro", 'docker.io/library/debian:bookworm-slim') + $cmd
  & $runtime @runArgs
  exit $LASTEXITCODE
}

$sandbox = Get-Command WindowsSandbox.exe -ErrorAction SilentlyContinue
if ($sandbox) {
  $wsb = Join-Path $env:TEMP ("ctf-isolated-{0}.wsb" -f [guid]::NewGuid().ToString('N'))
  $xml = @"
<Configuration>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>$full</HostFolder>
      <SandboxFolder>C:\Users\WDAGUtilityAccount\Desktop\work</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <Networking>Disable</Networking>
</Configuration>
"@
  [System.IO.File]::WriteAllText($wsb, $xml, (New-Object System.Text.UTF8Encoding($false)))
  Write-Host "Launching Windows Sandbox (mounted read-only at Desktop\work, networking disabled): $wsb"
  & $sandbox.Source $wsb
  exit 0
}

Write-Error 'No isolation runtime found. Install Docker/Podman, enable Windows Sandbox (Windows Pro/Enterprise), or run the attachment in a separate VM.'
exit 1
