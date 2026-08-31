# Data Layout Contract

```text
ctfs/<profile>/
├── .ctfd/                         # private CTFd config
├── challenges-detailed.json       # runtime metadata, ignored by Git
├── challenges.json                # runtime index, ignored by Git
├── _ctf-info.md / INDEX.md / STATUS.md
├── .history/                      # pre-resync generated snapshots
└── <category>/<challenge>/
    ├── README.md
    ├── AGENT.md
    ├── attachment-manifest.json
    ├── EXECUTION-SAFETY.md
    ├── work/
    ├── notes/
    ├── writeup/solution.md
    └── flag_output_dir/
```

Generated metadata may change during resync. `work/`, `notes/`, `writeup/` and `flag_output_dir/` are user-owned and preserved. Stale and renamed files are reported, never deleted automatically.
