# Tool Selection

The machine-readable inventory is `$CTF_HOME/config/tools.json`; it records name, category, installation method, invocation/path and version.

```bash
jq '.[] | select(.category=="pwn")' "$CTF_HOME/config/tools.json"
jq '.[] | select(.name=="pwndbg")' "$CTF_HOME/config/tools.json"
```

Run `ctf-doctor` and `command -v` before use. Prefer the exact prerequisite requested by the challenge workflow rather than silently substituting another tool.
