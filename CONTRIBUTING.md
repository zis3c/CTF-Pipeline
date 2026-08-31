# Contributing

Contributions should improve reusable pipeline code, documentation, tests or safe fixtures. Never add real challenge attachments, private URLs, tokens or machine inventory.

Before submitting:

```bash
bash -n bin/* test-corpus/smoke-test.sh
python -m py_compile scripts/*.py
test-corpus/smoke-test.sh
test-corpus/ctfd-integration-test.py
git diff --check
```

Run a secret scan before pushing. Do not auto-commit, auto-push or delete user data.
