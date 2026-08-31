#!/usr/bin/env bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export CTF_HOME="${CTF_HOME:-$(cd "$SCRIPT_DIR/.." && pwd)}"
if [ -z "${CTF_PYTHON:-}" ]; then
  if [ -f "${HOME:-}/.venvs/ctf-dev/bin/activate" ]; then CTF_PYTHON="$HOME/.venvs/ctf-dev/bin/python"; else CTF_PYTHON=python3; fi
fi
export CTF_PYTHON
if [ -f "$(dirname "$CTF_PYTHON")/activate" ]; then source "$(dirname "$CTF_PYTHON")/activate"; fi
export PATH="$CTF_HOME/bin:${HOME:-}/.local/share/gem/ruby/3.3.0/bin:$PATH"
export CTF_GLOBAL_EVIDENCE_DIR="$CTF_HOME/evidence"
alias ctf-update="$CTF_HOME/bin/ctf-update-all"
alias ctf-pull="$CTF_HOME/bin/ctf-pull"
echo "CTF environment: ${VIRTUAL_ENV:-system Python ($CTF_PYTHON)}"
echo "Global evidence directory: $CTF_GLOBAL_EVIDENCE_DIR"
