# Function Reference

## `bin/ctf-pull`

| Function | Purpose |
|---|---|
| `usage` | Prints supported modes. |
| `resolve_root` | Reads the event-root marker and sets paths. |
| `event_slug` | Converts an event title into a stable folder slug. |
| `migrate_to_event_root` | Migrates legacy metadata and categories. |
| `write_event_info` | Generates `_ctf-info.md`. |
| `normalize_categories` | Converts emoji/long categories to stable slugs. |
| `organize_from_json` | Creates category/challenge folders and README metadata from detailed JSON. |
| `run_ctfd` | Runs the upstream CLI, logs output and clears its cache. |
| `ensure_layout` | Creates work, notes, writeup, evidence and writeup template folders without overwriting a writeup. |

Other scripts: `ctf-doctor` uses `pass`, `warn` and `fail` for checks; `ctf-update-all` uses `update_repo` and skips dirty Git repositories; `backup-ctf-config`, `ctf-new`, `run-isolated` and the smoke test are single-flow scripts without named functions.

The pipeline helper also provides `snapshot`, `diff`, `dry-run`, `archive`, `generate`, `set-status`, `doctor`, `git-init` and `open` operations. These create reports and metadata without deleting user work.
