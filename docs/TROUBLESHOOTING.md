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

Missing means it was never downloaded; `.part` means a resumable download is incomplete.

## Server does not support Range

The downloader safely restarts the partial file and verifies the completed file through its SHA-256 manifest.

## Pipeline lock

The lock prevents concurrent profile operations. Confirm no pull is running before removing a stale `.pipeline.lock` manually.
