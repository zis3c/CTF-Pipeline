# Challenge Folder Workflow

```text
ctfs/
└── <ctf-profile>/
    ├── _ctf-info.md
    ├── challenges-detailed.json
    ├── challenges.json
    ├── .ctfd/config.json
    └── category/challenge/
        ├── README.md
        ├── attachments
        ├── work/
        ├── notes/
        ├── writeup/solution.md
        └── flag_output_dir/
```

The profile root also contains `INDEX.md`, `_ctf-info.md`, `.ctf-profile.json`, `STALE-FILES.md`, and `challenges-detailed.json`. Each challenge contains `attachment-manifest.json`, `AGENT.md` and `EXECUTION-SAFETY.md` generated from the current metadata and local files.

`README.md` is generated metadata. `work/` holds scripts and experiments; `notes/` holds reasoning; `writeup/` holds the final explanation; `flag_output_dir/` holds only validated flags and evidence, mode `700`. Every profile is isolated from every other profile. Resync may update generated files and attachments but preserves local work, notes, writeups and evidence. Prefer per-challenge evidence; root `evidence/` is only for cross-CTF material.
