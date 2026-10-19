# Command Reference

```bash
source "$CTF_HOME/config/activate-ctf.sh"

# Optional: place profiles outside the pipeline checkout.
# export CTF_PROFILES_ROOT="$HOME"

ctf-install-tools --dry-run
ctf-install-tools
ctf-pull init --name example-ctf --url https://ctf.example.com
ctf-pull sync --name example-ctf
ctf-pull pull --name example-ctf
ctf-pull resync --name example-ctf
ctf-pull resync --name example-ctf --dry-run
ctf-pull status --name example-ctf
ctf-pull list
ctf-pull doctor --name example-ctf
ctf-pull set-status --name example-ctf --challenge sample-challenge --status in_progress
ctf-pull open --name example-ctf --challenge sample-challenge
ctf-pull git-init --name example-ctf
ctf-doctor
ctf-new "Manual Challenge"
ctf-update
"$CTF_HOME/bin/run-isolated" /path/to/challenge -- /bin/bash
```

## Update everything

`ctf-update` runs `bin/ctf-update-all`. It backs up the configuration, updates
apt packages, the Python environment, Ruby gems, pipx tools, Git-based tools
and source builds, then refreshes the inventory and runs `ctf-doctor`. Every
run is logged to `logs/update/<timestamp>.log`; a failing section is reported
but does not abort the remaining sections.

```bash
ctf-update --dry-run            # preview every action
ctf-update                      # full update (asks for sudo)
ctf-update --skip-apt           # leave system packages alone
ctf-update --skip-python --skip-gem --skip-pipx
ctf-update --with-foundry --with-web3 --with-pwndbg-setup
```

Git repositories with local modifications are skipped so solver work is never
discarded. Use `git -C <repo> status` and commit or stash before updating.

Use `ctf-pull pull` or `ctf-pull resync` for profile downloads. These commands
normalize upstream category names into the pipeline's lowercase layout and
regenerate the profile reports. Calling the upstream `ctfd challenges`
command directly can recreate parallel `Forensics/`/`forensics/`-style
folders and bypass that normalization.

## Submit a flag

Submit through the CTFd player CLI using the profile's private configuration.
After activating the pipeline environment, prefer the challenge name so the
command does not depend on a numeric CTFd ID:

```bash
source "$CTF_HOME/config/activate-ctf.sh"
ctfd --config-dir "${CTF_PROFILES_ROOT:-$CTF_HOME/ctfs}/<profile>/.ctfd" \
  submit --challenge-name '<challenge name>' --flag '<flag>'
```

For scripts that need a stable numeric target, use the challenge ID instead:

```bash
ctfd --config-dir "${CTF_PROFILES_ROOT:-$CTF_HOME/ctfs}/<profile>/.ctfd" \
  submit --challenge-id <id> --flag '<flag>'
```

If a challenge folder contains a generated `submit.sh`, it is a convenience
wrapper for the same operation:

```bash
./submit.sh '<flag>'
```

The profile config supplies the CTFd URL and token; do not put credentials in
the command, documentation, shell scripts or logs. If `ctfd` is not on
`PATH`, set its path and invoke it explicitly:

```bash
export CTFD_BIN="/path/to/python-environment/bin/ctfd"
"$CTFD_BIN" --config-dir "$CTF_PROFILES_ROOT/<profile>/.ctfd" \
  submit --challenge-name '<challenge name>' --flag '<flag>'
```

The generated wrapper resolves the profile relative to its challenge folder,
so it remains usable when the pipeline is moved. It can also use `CTFD_BIN`
or `CTF_PYTHON` when `ctfd` is not on `PATH`. The activation plus
`ctfd --challenge-name` form remains useful for submitting by name. See
[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) for the environment-specific
`CTFD_BIN` lookup.

Each CTF has its own token, JSON and challenge tree under `ctfs/<profile>/`. Manual challenges go under `ctfs/manual/`. `status` never prints a token.

Set solver progress by writing one of `not_started`, `in_progress` or `solved` to a challenge's `.solver-status` file. The profile `INDEX.md` displays this as `[ ]`, `[~]` or `[x]`.

## Generated profile files

- `INDEX.md`: challenge list, category, points, ID and solver status.
- `_ctf-info.md`: profile summary and category counts.
- `.ctf-profile.json`: non-secret profile name, URL, sync time, count and token status.
- `attachment-manifest.json`: attachment size and SHA-256 per challenge.
- `AGENT.md`: machine-readable context for an AI agent.
- `EXECUTION-SAFETY.md`: possible executable/script attachments and isolation advice.
- `STALE-FILES.md`: files no longer listed by CTFd; report only, never auto-deleted.
- `.history/<timestamp>/`: archived generated metadata and attachments before a real pull/resync.

`--dry-run` contacts CTFd, shows `+`, `~` and `-` metadata changes, and performs no archive or overwrite.

Downloads retry failed CLI runs up to three times, and the local downloader resumes `.part` files with HTTP Range when the server supports it. `ctf-pull doctor` checks generated profile files and attachment state; `set-status` updates the dashboard; `open` prints the challenge path; `git-init` enables local tracking without committing.

`CTF_PROFILES_ROOT` overrides the default `$CTF_HOME/ctfs` profile directory. For example, setting it to `$HOME` and using the profile name `3108-ctf-warisan-takhta` produces `$HOME/3108-ctf-warisan-takhta/`. The wrapper exports the upstream CTFd challenge cache to `challenges.json` and `challenges-detailed.json` before generating the local workspace.
