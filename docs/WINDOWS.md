# Windows (native PowerShell)

Native Windows support is provided by PowerShell ports of the Bash scripts. No
WSL, MSYS2 or container runtime is required for the core pipeline.

## Requirements

- Windows 10/11 with PowerShell 5.1 (bundled) or PowerShell 7+.
- Python 3.10+ on PATH (`python`). Python 3.13 is tested.
- Git (only needed for `ctf-pull git-init` and `ctf-update-all`).
- The `ctfd` CLI. A minimal one is **bundled** as the `ctfd` Python package at
  the repository root and is used via `python -m ctfd`. An external CLI on
  `PATH` or `CTFD_BIN` still takes precedence if you prefer the upstream tool.

## Authentication

The bundled client reads `.ctfd/config.json` and authenticates in this order:

1. `Authorization: Token <token>` with the configured token (or `CTFD_TOKEN`).
2. If the token is rejected (or empty), it logs in with a session using
   `CTFD_USERNAME`/`CTFD_PASSWORD` (aliases `CTF_USERNAME`/`CTF_PASSWORD`).

```powershell
# token-based instance
$env:CTFD_TOKEN = "ctfd_..."
.\bin\ctf-pull.ps1 init --name event --url https://ctf.example.com

# instance that only accepts a logged-in session
$env:CTF_USERNAME = "user"; $env:CTF_PASSWORD = "pass"
.\bin\ctf-pull.ps1 init --name event --url https://ctf.example.com
```

`init` never prompts; it stores whatever token is available (possibly empty, to
use the session fallback). Token values are written only to `.ctfd/config.json`,
which is git-ignored.

## Setup

```powershell
$env:CTF_HOME = "C:\Users\<you>\ctf-pipeline"
. "$env:CTF_HOME\config\activate-ctf.ps1"   # dot-source to set CTF_HOME/PYTHON/PATH

.\bin\ctf-install-tools.ps1 -DryRun
.\bin\ctf-install-tools.ps1
.\bin\ctf-doctor.ps1
```

Only `requests` is strictly required by the pipeline. Many packages in
`config/requirements-ctf.txt` (fpylll, angr, qiling, volatility3, ...) are
Linux-oriented and may fail to build on Windows; that does not stop the
pipeline. Install the specific tools you need individually.

## Quick start

```powershell
.\bin\ctf-pull.ps1 init  --name example-ctf --url https://ctf.example.com
.\bin\ctf-pull.ps1 pull  --name example-ctf   # sync metadata + download attachments
.\bin\ctf-pull.ps1 resync --name example-ctf --dry-run
.\bin\ctf-pull.ps1 resync --name example-ctf
.\bin\ctf-pull.ps1 list
```

All commands from `docs/COMMANDS.md` are available with the same flags; replace
`ctf-pull` with `.\bin\ctf-pull.ps1` (or dot-source `activate-ctf.ps1` and use
the `ctf-pull` function).

## Environment variables

- `CTF_HOME` — pipeline checkout (defaults to the script's parent folder).
- `CTF_PYTHON` — Python executable (defaults to `python`; point it at a venv).
- `CTF_PROFILES_ROOT` — where profiles live (defaults to `$CTF_HOME\ctfs`).
- `CTFD_BIN` — explicit path/command for the CTFd CLI.

## Differences from Linux

- File permissions (`chmod 600/700`) are Linux concepts and are skipped on
  Windows; use NTFS ACLs or BitLocker if you need to protect tokens/evidence.
- `bin\run-isolated.ps1` uses Docker/Podman if present, otherwise Windows
  Sandbox (Pro/Enterprise) with the folder mounted read-only and networking
  disabled. Without any of these it reports that no runtime is available.
- `ctf-install-tools` and `ctf-update-all` install Python packages with pip and
  pull the repository with git. The apt/gem/cmake toolchain from Linux is not
  replicated; install native tools with winget or manually.
- `ctf-install-tools.ps1 -Extras` runs `python -m pipx`, upgrades tools that
  already exist and installs only the missing ones. The Windows extras list is
  smaller than the Linux one and does not include `paramspider`, `flare-capa`,
  `slither-analyzer` or `pcodedmp`.
- Foundry, the web3 Python environment and Linux-only gems are not managed on
  Windows. The `--with-foundry` and `--with-web3` update flags are Linux-only.

## Verify

```powershell
.\test-corpus\windows-smoke.ps1      # offline pipeline smoke test
python .\test-corpus\ctfd-integration-test.py
```
