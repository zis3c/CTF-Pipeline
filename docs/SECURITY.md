# Security and Data Handling

- Keep each CTFd token in `ctfs/<profile>/.ctfd/config.json`, mode `600`.
- Never put passwords, tokens or provider secrets in Markdown, Git, shell history or logs.
- Revoke and replace a token if an upstream tool prints it.
- `challenges*.json` may contain short-lived signed attachment URLs; keep them mode `600` and do not commit them.
- Store validated flags, hashes, commands and validation output in the challenge's `flag_output_dir/`; use root `evidence/` only for cross-CTF material.
- Treat attachments as untrusted. Use `bin/run-isolated`; it disables network, drops capabilities and mounts the target read-only.
- `--dry-run` is the safe preview mode; it does not create archives or modify challenge files.
- `.history/` is an archive, not a deletion queue. `STALE-FILES.md` reports old files without removing them.
