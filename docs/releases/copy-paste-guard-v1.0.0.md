# Copy Paste Guard v1.0.0

First public release candidate.

## Included

- Bash, Zsh, PowerShell, and cmd.exe command-review workflow
- explicit `PASS`, `PASS WITH FIXES`, and `STOP` verdicts
- checks for placeholders, working-directory assumptions, privilege, destructive scope, quoting, redirects, wildcards, downloader-to-shell execution, encoded execution, inline secrets, destructive Git operations, disabled TLS verification, and disabled SSH host-key checking
- read-only `command_risk_scan.py` helper that never executes reviewed commands and never echoes source lines

## Verification completed

- skill structure validation passed
- helper script compiled successfully
- risky fixture produced expected high-severity findings
- safe fixture produced zero findings
- public source tree passed declassification scan
- final packaged ZIP passed declassification scan
- final ZIP contains exactly one `SKILL.md`
- no compiled Python bytecode is included

A clean ChatGPT install test remains recommended before broad promotion.
