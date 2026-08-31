# CTF Smoke-Test Corpus

Small local fixtures for validating the environment: `pwn/`, `rsa/`, `apk/`, `pcap/`, `memory/` and `doctor-smoke/`.

```bash
source "$CTF_HOME/config/activate-ctf.sh"
python "$CTF_HOME/scripts/generate-test-corpus.py"
"$CTF_HOME/test-corpus/smoke-test.sh"
"$CTF_HOME/test-corpus/ctfd-integration-test.py"
```
