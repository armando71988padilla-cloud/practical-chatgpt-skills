# Git evidence guide

## Minimum local read-only evidence

Useful evidence includes:

- `git rev-parse --show-toplevel`
- `git branch --show-current`
- `git rev-parse --verify HEAD`
- `git remote -v` with embedded credentials removed from displayed URLs
- `git status --short --branch`
- upstream name and ahead/behind counts
- `git diff --name-status`
- `git diff --cached --name-status`
- bounded untracked and relevant ignored file lists
- `git submodule status` when submodules exist
- `git worktree list` when multiple worktrees may matter

## Remote freshness

Ahead/behind calculations use local references. They are only as fresh as the relevant remote-tracking refs.

Use `UNPROVEN` when the user needs a current statement about the remote and there is no sufficiently recent fetch or other authoritative evidence.

Do not quietly fetch merely to make the report prettier if network access or remote mutation policy is unknown.

## Secret-risk names

Treat these patterns as review triggers, not proof that a secret is present:

- `.env` and environment variants
- `id_rsa`, `id_ed25519`, private keys, PFX/P12/keystore files
- token, secret, credential, cookie, session, auth, and key files
- cloud credential or service-account files
- local databases, browser profiles, wallet files, and private configuration

Initial review should report path and risk class without printing values.

## Generated and backup risk

Review before staging:

- build output and caches
- coverage reports and logs
- archives and installers
- databases
- model weights/checkpoints
- media or large binaries
- backups such as `.bak`, `.old`, timestamped copies, swap files, and editor recovery files

## In-progress Git operations

Check for merge, rebase, cherry-pick, bisect, or revert state when symptoms suggest Git is mid-operation. Do not start another history operation until the current one is understood.

## Destructive command notes

`git reset --hard` can discard tracked working-tree/index changes.

`git clean -f` removes untracked files; `-d` includes untracked directories; `-x` can also remove ignored files. Prefer preview with `git clean -n` using the same scope flags before deletion.

Force pushing rewrites a remote ref. Prefer `--force-with-lease` when history rewrite is intentional because it checks the expected remote state, but still verify the exact remote and branch first.
