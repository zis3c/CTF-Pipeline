#!/usr/bin/env bash
set -euo pipefail
R="/home/zisec/ctf/test-corpus"
source /home/zisec/ctf/config/activate-ctf.sh >/dev/null
TMP_RSA="$(mktemp)"
trap 'rm -f "$TMP_RSA"' EXIT
test -x "$R/pwn/ret2win"
checksec --file="$R/pwn/ret2win" >/dev/null
python "$R/rsa/small_rsa.py" > "$TMP_RSA"
test -s "$TMP_RSA"
file "$R/apk/sample.apk" | grep -q 'Android package'
tshark -r "$R/pcap/sample.pcap" -c 2 >/dev/null
strings "$R/memory/synthetic.raw" | grep -q 'CTF-MEMORY-TEST'
printf 'corpus smoke test: OK\n'
