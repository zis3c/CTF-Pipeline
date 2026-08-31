# CTF Pipeline

[![CI](https://github.com/OWNER/ctf-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/ctf-pipeline/actions/workflows/ci.yml)
[![Platform](https://img.shields.io/badge/platform-Linux-blue)](docs/OS-COMPATIBILITY.md)
[![Python](https://img.shields.io/badge/python-3.12-blue)](config/requirements-ctf.txt)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Repository](https://img.shields.io/badge/repository-private-lightgrey)](#repository-scope)

CTF Pipeline is a local, multi-CTF operations toolkit. It retrieves challenges from CTFd, keeps events isolated, preserves solver work during resync, generates AI-readable context, and verifies the local toolchain.

It is intended for authorized CTF participation and lab environments. It does not solve challenges automatically or bypass access controls.

## What problem does it solve?

It replaces ad-hoc copying of challenge descriptions, attachments, notes, scripts and evidence with a predictable, repeatable workspace.

```text
CTFd -> ctfd-player-cli -> ctf-pull -> ctfs/<profile>/<category>/<challenge>/
                                      ├── README.md
                                      ├── work/notes/writeup
                                      └── flag_output_dir
```

## Features

- Multiple isolated CTFd profiles with separate tokens and metadata.
- Metadata sync, attachment download, retry and `.part` HTTP Range resume.
- Dry-run preview with `+ new`, `~ modified` and `- removed` changes.
- Timestamped archives before real pull/resync operations.
- SHA-256 attachment manifests and profile health checks.
- Generated `INDEX.md`, `STATUS.md`, `_ctf-info.md` and AI `AGENT.md` files.
- Stale-file and renamed-folder reports; no automatic deletion.
- Safety hints for executable attachments and a Podman isolation helper.
- Smoke tests for pwn, crypto, APK, PCAP and memory workflows.

## Supported platforms

Kali Linux amd64 is the primary tested platform. Debian/Ubuntu amd64 is supported with manual package setup. ARM64 and WSL2 are best effort; macOS is not turnkey; native Windows is unsupported. See [`docs/OS-COMPATIBILITY.md`](docs/OS-COMPATIBILITY.md).

## Installation

```bash
export CTF_HOME="$HOME/ctf-pipeline"
git clone <private-repository-url> "$CTF_HOME"
source "$CTF_HOME/config/activate-ctf.sh"
ctf-doctor
```

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for prerequisites and setup details.

## Quick start

```bash
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull pull --name example-ctf
ctf-pull resync --name example-ctf --dry-run
ctf-pull resync --name example-ctf
```

## Repository scope

This repository contains reusable pipeline code, documentation and safe test fixtures. Real profiles, challenge attachments, tokens, logs, backups, evidence, third-party source and machine-specific inventory are ignored by Git.

## Documentation

Start at [`docs/INDEX.md`](docs/INDEX.md). See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development checks and [`LICENSE`](LICENSE) for licensing.
