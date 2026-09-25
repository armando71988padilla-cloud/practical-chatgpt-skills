# Public tests

These fixtures contain inert command text only. They are inputs for the read-only command scanner and must never be executed as shell scripts.

Expected behavior:

- `copy-paste-guard-risky.txt` produces high-severity findings.
- `copy-paste-guard-safe.txt` produces no findings.
