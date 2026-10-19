#!/usr/bin/env python3
"""Make upstream-generated challenge helper scripts portable.

The upstream CTFd CLI embeds the absolute config directory in submit.sh and
launch.sh.  The pipeline owns the profile layout, so rewrite those generated
helpers after downloads using paths relative to their challenge directory.
"""

from __future__ import annotations

import re
import stat
import sys
from pathlib import Path


CHALLENGE_ID = re.compile(r"challenge-id\s+(\d+)")


def command_block() -> str:
    return '''SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROFILE_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
CONFIG_DIR="${CTF_CONFIG_DIR:-$PROFILE_ROOT/.ctfd}"

if [[ -n "${CTFD_BIN:-}" ]]; then
    CTFD_CMD="$CTFD_BIN"
elif command -v ctfd >/dev/null 2>&1; then
    CTFD_CMD="$(command -v ctfd)"
elif [[ -n "${CTF_PYTHON:-}" && -x "$(dirname -- "$CTF_PYTHON")/ctfd" ]]; then
    CTFD_CMD="$(dirname -- "$CTF_PYTHON")/ctfd"
else
    echo "ctfd CLI not found; source the pipeline environment or set CTFD_BIN" >&2
    exit 127
fi

[[ -x "$CTFD_CMD" ]] || { echo "CTFD_BIN is not executable: $CTFD_CMD" >&2; exit 126; }
'''


def render(kind: str, challenge_id: str) -> str:
    command = (
        f'exec "$CTFD_CMD" --skip --config-dir "$CONFIG_DIR" '
        f'instance start --challenge-id {challenge_id}'
        if kind == "launch.sh"
        else f'exec "$CTFD_CMD" --skip --config-dir "$CONFIG_DIR" '
        f'submit --challenge-id {challenge_id} --flag "$1"'
    )
    argument_check = (
        "[[ $# -eq 1 ]] || { echo \"Usage: $0 <flag>\" >&2; exit 1; }\n\n"
        if kind == "submit.sh"
        else ""
    )
    return "#!/usr/bin/env bash\nset -euo pipefail\n\n" + argument_check + command_block() + command + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} PROFILE_ROOT", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Profile root is not a directory: {root}", file=sys.stderr)
        return 2

    updated = 0
    skipped = 0
    for path in sorted(root.rglob("*.sh")):
        if path.name not in {"submit.sh", "launch.sh"}:
            continue
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if {".history", ".ctfd", ".pipeline", ".git"}.intersection(relative_parts):
            continue
        old = path.read_text()
        match = CHALLENGE_ID.search(old)
        if not match:
            skipped += 1
            continue
        mode = stat.S_IMODE(path.stat().st_mode)
        path.write_text(render(path.name, match.group(1)))
        path.chmod(mode | stat.S_IXUSR)
        updated += 1

    print(f"Normalized challenge scripts: {updated} updated, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
