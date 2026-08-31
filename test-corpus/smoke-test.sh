#!/usr/bin/env bash
set -euo pipefail
R="/home/zisec/ctf/test-corpus"
source /home/zisec/ctf/config/activate-ctf.sh >/dev/null
test -x "$R/pwn/ret2win"
checksec --file="$R/pwn/ret2win" >/dev/null
python "$R/rsa/small_rsa.py" > "$R/rsa/sample.txt"
test -s "$R/rsa/sample.txt"
file "$R/apk/sample.apk" | grep -q 'Android package'
tshark -r "$R/pcap/sample.pcap" -c 2 >/dev/null
strings "$R/memory/synthetic.raw" | grep -q 'CTF-MEMORY-TEST'
printf 'corpus smoke test: OK\n'
