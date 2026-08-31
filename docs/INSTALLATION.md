# Installation Guide

## Requirements

- Kali Linux, Debian or Ubuntu recommended.
- Bash, Git, Python 3.12 and a compatible virtual environment.
- `ctfd-player-cli` installed in the selected Python environment.
- Optional Podman for `run-isolated` and Chrome DevTools MCP for browser work.

## Install

```bash
git clone <private-repository-url> /home/zisec/ctf
source /home/zisec/ctf/config/activate-ctf.sh
```

The current scripts assume `/home/zisec/ctf`. Portability requires replacing hardcoded paths with a configurable `CTF_HOME`.

## Python dependencies

```bash
/home/zisec/.venvs/ctf-dev/bin/python -m pip install -r /home/zisec/ctf/config/requirements-ctf.txt
/home/zisec/ctf/bin/ctf-doctor
```

## Configure a CTF profile

```bash
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull pull --name example-ctf
```

Enter the token interactively. Never place it in command history, documentation or Git.

## Verify development fixtures

```bash
/home/zisec/ctf/test-corpus/smoke-test.sh
/home/zisec/ctf/test-corpus/ctfd-integration-test.py
```
