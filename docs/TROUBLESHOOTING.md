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

## Interrupted download

Downloads are written to a `.part` file and renamed on completion, so an interrupted pull never leaves a half-written attachment in place. Re-run `ctf-pull pull`; the file is fetched again and verified through its SHA-256 manifest.

## Pipeline lock

The lock prevents concurrent profile operations. Confirm no pull is running before removing a stale `.pipeline.lock` manually.
