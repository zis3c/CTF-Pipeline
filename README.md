# CTF Pipeline

A local, multi-CTF workflow for retrieving CTFd challenges, organizing artifacts, tracking solving progress, and giving an AI agent reliable context.

## Repository scope

This repository contains the reusable pipeline, documentation, scripts, and safe test fixtures. Real CTF profiles, challenge attachments, tokens, logs, backups, evidence, and machine-specific tool inventory are intentionally ignored.

## Installation

The scripts currently use `/home/zisec/ctf` as the installation path.

```bash
git clone <private-repository-url> /home/zisec/ctf
source /home/zisec/ctf/config/activate-ctf.sh
```

Use the existing Python 3.12 environment at `/home/zisec/.venvs/ctf-dev`, or install the packages from `config/requirements-ctf.txt` in a compatible virtual environment. Run `ctf-doctor` after installation.

## Quick start

```bash
source /home/zisec/ctf/config/activate-ctf.sh
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull pull --name example-ctf
ctf-pull resync --name example-ctf --dry-run
ctf-pull status --name example-ctf
```

Profiles are created under `ctfs/<profile>/`. Each profile has its own CTFd config, metadata, category folders, generated reports, notes, writeups, and evidence.

## Development checks

```bash
ctf-doctor
/home/zisec/ctf/test-corpus/smoke-test.sh
/home/zisec/ctf/test-corpus/ctfd-integration-test.py
```

## Documentation

Start at [`docs/INDEX.md`](docs/INDEX.md). It covers architecture, commands, functions, challenge workflow, AI context, tools, and security.

## Suggested repository names

- `ctf-pipeline` — clearest and recommended
- `ctf-workspace` — broader workspace tooling
- `ctf-ops` — operations-focused
- `ctf-lab` — compact and memorable

Keep the remote repository private. Review `git status` and run a secret scan before every push.
