# CTF Smoke-Test Corpus

Small local fixtures for validating the environment: `pwn/`, `rsa/`, `apk/`, `pcap/`, `memory/` and `doctor-smoke/`.

```bash
source /home/zisec/ctf/config/activate-ctf.sh
python /home/zisec/ctf/scripts/generate-test-corpus.py
/home/zisec/ctf/test-corpus/smoke-test.sh
/home/zisec/ctf/test-corpus/ctfd-integration-test.py
```
