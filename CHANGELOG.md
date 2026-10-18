# Changelog

## Unreleased

- Native Windows support: PowerShell ports of every Bash script (`bin\*.ps1`, `config\activate-ctf.ps1`) sharing the same Python core.
- Bundled minimal `ctfd` client (`ctfd/`) used as `python -m ctfd`, with token auth and a username/password session fallback.
- Skip already-downloaded attachments and download atomically through `.part` files (no HTTP Range resume).
- `--dry-run` compares summary fields with a single API request instead of one request per challenge.
- Prune `.history/` to the 10 most recent snapshots; enforce UTF-8 for every generated profile file.
- CI runs both a Linux and a Windows job; optional solver modules no longer make `ctf-doctor.ps1` exit non-zero on Windows.
- Unit tests (`tests/`, standard-library `unittest`) cover the `ctfd` client (auth, downloads, skip-existing) and `ctf-pipeline.py` helpers; wired into CI.
- `ctf-doctor` (Linux) now requires Python >= 3.10 and only treats `requests` and the Python install as failures; optional solver imports and `pip check` are warnings.
- Removed personal/attribution strings from the client user agent, docs and examples so the repository can stand alone.

## 0.2.0 - 2026-08-31

- Professional multi-CTF pipeline documentation and OS compatibility guide.
- Resync diff, dry-run, archive, manifests, dashboard and AI context.
- Retry and HTTP Range partial-download support.
- Local CTFd API integration fixture.
- Allow profile workspaces outside the repository with `CTF_PROFILES_ROOT`.
- Export CTFd challenge metadata before generating the local workspace.
- Generate complete per-challenge work, notes, writeup, evidence and manifest layout.
- Prefer the installed `ctfd` executable when available.

## 0.1.0

- Initial private CTF pipeline repository layout.
