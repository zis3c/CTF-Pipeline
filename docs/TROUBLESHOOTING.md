# Troubleshooting

## Profile not found

```bash
ctf-pull list
ctf-pull status --name example-ctf
```

Use the exact profile name.

## Preview reports changes

This means live CTFd metadata differs from the local JSON. Review the changed fields before a real resync.

## Missing or partial attachment

```bash
ctf-pull doctor --name example-ctf
ctf-pull pull --name example-ctf
```

Missing means it was never downloaded; `.part` means a download was interrupted before it finished. Re-run `ctf-pull pull` to fetch it again.

## `ctfd` CLI not found

`ctf-pull` first looks for `ctfd` on `PATH`, then beside the Python selected by
`CTF_PYTHON`. If the CLI is installed elsewhere, set its path explicitly:

```bash
export CTFD_BIN="$(dirname "$CTF_PYTHON")/ctfd"
ctf-pull pull --name example-ctf
```

The activation script supports both Bash and zsh. After sourcing it, verify
that `ctf-pull` points into the active pipeline checkout with `which ctf-pull`.

## Interrupted download

Downloads are written to a `.part` file and renamed on completion, so an interrupted pull never leaves a half-written attachment in place. Re-run `ctf-pull pull`; the file is fetched again and verified through its SHA-256 manifest.

## Pipeline lock

The lock prevents concurrent profile operations. Confirm no pull is running before removing a stale `.pipeline.lock` manually.

## `ctf-update` fails at a step

Each section reports `[OK]` or `[FAIL]` and the run continues. Read the full
log at `logs/update/<timestamp>.log` to see the failing command.

Common causes:

- `apt` fails on a held package or a full disk: run `sudo apt --fix-broken install` and check `df -h`.
- Ruby gems fail to build: install the native headers, then rerun the gem step.
  ```bash
  sudo apt install -y libyaml-dev
  ctf-update --skip-apt --skip-python --skip-pipx --skip-git
  ```
- A Git tool is skipped as `dirty`: commit or stash local changes in that repo.
- `pip check` reports a conflict: the update still completes, but review the
  pinned versions in `config/requirements-ctf.in`.
