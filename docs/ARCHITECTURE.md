# Architecture

```text
CTFd -> ctfd-player-cli -> challenges-detailed.json -> ctf-pull -> ctfs/<profile>/
                                                                  └─ category/challenge
tools.json -> ctf-doctor       requirements -> Python environment
test-corpus -> smoke-test      run-isolated -> Podman sandbox
```

Each profile is independent: `ctfs/<profile>/challenges-detailed.json`, `ctfs/<profile>/challenges.json` and `ctfs/<profile>/.ctfd/config.json`. Global sources are `config/tools.json` and `config/requirements-ctf.*`.

`sync` fetches metadata and organizes folders. `pull` and `resync` also download attachments. The wrapper clears the upstream global `/tmp/.ctfd.cache` before every CLI call.

Before sync, the pipeline snapshots metadata; after sync it prints a diff. Before downloads it archives generated content under `.history/`. Afterward it regenerates indexes, profile metadata, AI context, SHA-256 manifests, solver status views and a non-destructive stale-file report.

An advisory cleanup report is generated for old archives, stale attachments and possible duplicates. Download failures are retried by the wrapper, while the local CLI patch resumes `.part` files using HTTP Range when supported.
