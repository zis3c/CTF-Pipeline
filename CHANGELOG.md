# Changelog

## Unreleased

- Rewrite `ctf-update-all` as a resilient ten-step updater: apt, Python, Ruby
  gems, pipx, every Git-based tool from the inventory, source builds, inventory
  refresh, doctor and backups.
- Add `--dry-run`, per-section `--skip-*` flags and opt-in
  `--with-foundry`, `--with-web3` and `--with-pwndbg-setup` steps.
- A failing section no longer aborts the run; failures are summarised and the
  script exits non-zero.
- Pin `angr`/`claripy`/`z3-solver` and `requests` so the Python environment
  passes `pip check` (previously `ctf-doctor` reported one error).
- Add `libyaml-dev` to the installer so Ruby native gems build.

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
