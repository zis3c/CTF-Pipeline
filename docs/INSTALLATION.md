# Installation Guide

## Requirements

- Kali Linux, Debian or Ubuntu recommended.
- Bash, Git, Python 3.12 and a compatible virtual environment.
- `ctfd-player-cli` installed in the selected Python environment.
- Optional Podman for `run-isolated` and Chrome DevTools MCP for browser work.

## Install

```bash
export CTF_HOME="$HOME/ctf-pipeline"
git clone <private-repository-url> "$CTF_HOME"
source "$CTF_HOME/config/activate-ctf.sh"
```

All scripts derive their repository root automatically. Set `CTF_HOME` when the repository is stored outside its default location. Set `CTF_PYTHON` when Python is not on `PATH` or when a dedicated virtual environment is preferred.

## Python dependencies

```bash
"$CTF_PYTHON" -m pip install -r "$CTF_HOME/config/requirements-ctf.txt"
"$CTF_HOME/bin/ctf-doctor"
```

## Configure a CTF profile

```bash
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull pull --name example-ctf
```

Enter the token interactively. Never place it in command history, documentation or Git.

## Verify development fixtures

```bash
"$CTF_HOME/test-corpus/smoke-test.sh"
"$CTF_HOME/test-corpus/ctfd-integration-test.py"
```
