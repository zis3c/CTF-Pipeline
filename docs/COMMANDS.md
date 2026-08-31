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
