# CTF Pipeline

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

| Platform | Support | Notes |
|---|---|---|
| Kali Linux amd64 | Full | Primary tested platform. |
| Debian/Ubuntu amd64 | Supported | Install the documented packages manually. |
| Debian-based ARM64 | Best effort | Native and reverse tools vary by architecture. |
| WSL2 Debian/Ubuntu | Best effort | Podman, GUI tools and browser integration need setup. |
| macOS | Not turnkey | Linux paths and package assumptions need adaptation. |
| Native Windows | Not supported | Use WSL2 or a Linux VM. |

The current scripts use `/home/zisec/ctf` as their installation root and are Linux-first.

## Installation

```bash
git clone <private-repository-url> /home/zisec/ctf
source /home/zisec/ctf/config/activate-ctf.sh
/home/zisec/ctf/bin/ctf-doctor
```

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for prerequisites and setup details.

## Quick start

```bash
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull pull --name example-ctf
ctf-pull resync --name example-ctf --dry-run
ctf-pull resync --name example-ctf
```

Profiles live under `ctfs/<profile>/`. Runtime profiles, challenge files, tokens, logs, backups, evidence and machine-specific inventory are ignored by Git.

## Documentation

Start at [`docs/INDEX.md`](docs/INDEX.md). It links installation, architecture, commands, data layout, troubleshooting, security, AI context and contribution guidance.
