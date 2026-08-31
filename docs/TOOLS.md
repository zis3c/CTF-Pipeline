# Tool Selection

The machine-readable inventory is `/home/zisec/ctf/config/tools.json`; it records name, category, installation method, invocation/path and version.

```bash
jq '.[] | select(.category=="pwn")' /home/zisec/ctf/config/tools.json
jq '.[] | select(.name=="pwndbg")' /home/zisec/ctf/config/tools.json
```

Run `ctf-doctor` and `command -v` before use. Prefer the exact prerequisite requested by the challenge workflow rather than silently substituting another tool.
