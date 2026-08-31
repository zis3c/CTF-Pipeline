#!/usr/bin/env bash
# Activate the unified Python 3.12 CTF environment.
source /home/zisec/.venvs/ctf-dev/bin/activate
export PATH="/home/zisec/.local/share/gem/ruby/3.3.0/bin:$PATH"
export CTF_GLOBAL_EVIDENCE_DIR="/home/zisec/ctf/evidence"
alias ctf-update="/home/zisec/ctf/bin/ctf-update-all"
alias ctf-pull="/home/zisec/ctf/bin/ctf-pull"
echo "CTF environment: $VIRTUAL_ENV"
echo "Global evidence directory: $CTF_GLOBAL_EVIDENCE_DIR"
