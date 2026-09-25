# Git State Guardian v1.0.0

First public release candidate.

## Included

- repository-root, branch, commit, remote, and upstream proof before risky Git operations
- explicit `ALIGNED`, `AHEAD`, `BEHIND`, `DIVERGED`, `NO UPSTREAM`, `DETACHED`, and `UNPROVEN` alignment states
- separate staged, unstaged, untracked, ignored, submodule, worktree, and in-progress-operation review
- secret-safe path warnings that do not print suspected secret values
- backup, generated-artifact, binary/archive, and large-file risk checks
- conservative handling of reset, clean, rebase, branch deletion, and force push
- exact-path staging guidance instead of broad staging by default
- read-only `git_state_report.py` helper with no network access or Git mutation

## Verification completed

- skill structure validation passed
- helper script compiled successfully
- synthetic Git repository test detected staged secret-risk path, backup file, and generated artifact
- synthetic secret value was not echoed by the helper
- public source passed declassification scan
- final packaged ZIP passed declassification scan
- final ZIP contains exactly one `SKILL.md` and four readable files
- no compiled bytecode or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
