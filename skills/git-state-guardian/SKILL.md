---
name: git-state-guardian
description: Review Git repository state before staging, committing, rebasing, resetting, cleaning, switching branches, merging, or pushing. Use when a user asks whether a repo is clean or aligned, wants safe commit/push commands, may be in the wrong repository, has staged and unstaged work mixed together, is about to use destructive Git commands, or needs secret, backup, generated-file, large-file, upstream, detached-HEAD, submodule, or worktree risks checked first. Prove repository identity and state, keep staging explicit, and never print suspected secret values.
---

# Git State Guardian

## Purpose

Make Git operations boring and deliberate. Prove the repository, branch, worktree, and staging state before recommending a write operation, then verify the resulting state afterward.

## Workflow

1. Identify the repository and Git operation the user intends.
2. Prove the repository root with `git rev-parse --show-toplevel` before any write operation.
3. Prove branch or detached-HEAD state, current commit, remotes, and configured upstream.
4. Inventory staged, unstaged, untracked, ignored, submodule, and worktree state separately.
5. Check path names, sizes, and metadata for likely secrets, backups, generated artifacts, archives, databases, and oversized files without printing file contents.
6. Decide whether the requested operation is safe, needs narrower staging, needs a branch, needs a backup/stash, or must stop for missing proof.
7. Give the smallest safe Git sequence.
8. After the operation, verify branch, commit, upstream relation, and intentionally remaining local changes.

When code execution is available, run `scripts/git_state_report.py` for a local read-only snapshot. Treat its output as evidence, not as a substitute for repository-specific policy.

Read `references/git-evidence-guide.md` for alignment language, destructive operations, and secret-safe review rules.

## Repository identity

Do not infer repository identity from the current shell prompt, folder name, or user description alone.

Before staging, committing, resetting, cleaning, rebasing, merging, or pushing, prove:

- top-level repository path
- current branch or detached HEAD
- current commit
- remotes with credentials sanitized
- upstream branch when configured

If the user intended a different repository than the proven root, stop.

## Alignment rules

Use these terms precisely:

- `ALIGNED`: upstream is proven and local ahead = 0 and behind = 0 based on sufficiently current remote-tracking evidence
- `AHEAD`: ahead > 0 and behind = 0
- `BEHIND`: ahead = 0 and behind > 0
- `DIVERGED`: ahead > 0 and behind > 0
- `NO UPSTREAM`: no upstream is configured
- `DETACHED`: HEAD is detached
- `UNPROVEN`: upstream or remote-tracking freshness is insufficient for the claim being made

Do not claim remote alignment merely because `git status` says "up to date" if freshness matters and no recent fetch is known. A local remote-tracking ref can be stale.

Do not automatically run network-changing Git commands just to refresh evidence unless the user asked for that or the environment allows it. State when a fetch is needed.

## Worktree inventory

Keep these categories separate:

- staged tracked changes
- unstaged tracked changes
- untracked files
- ignored files relevant to the current work
- submodule changes
- additional worktrees when relevant
- merge/rebase/cherry-pick/revert state

A clean staged set does not mean the whole worktree is clean.

A clean worktree does not prove alignment with a remote.

## Secret-safe review

Inspect file names, paths, sizes, diff metadata, and Git attributes before file content.

Treat names such as these as risk indicators, not proof of a secret:

- `.env` and environment variants
- private keys, certificates, keystores, credential files
- files containing `token`, `secret`, `credential`, `cookie`, `session`, `auth`, or `service-account`
- local databases, wallet files, browser profiles, cloud credentials, or private configuration

Never print suspected secret values during the initial review.

If content inspection is required, inspect only the minimum necessary and redact values in the response.

## Large, generated, and backup files

Flag likely accidental additions such as:

- archives and installer bundles
- model weights and checkpoints
- local databases
- logs, traces, coverage output, caches, and build directories
- media or binary artifacts that are unexpectedly large
- editor swap/recovery files
- timestamped or `.bak` backups

Do not assume a large file is wrong. Explain why it deserves review before staging.

## Staging rules

Prefer explicit named paths.

Do not recommend `git add .`, `git add -A`, or broad directory staging until the full affected set has been reviewed and the user explicitly intends it.

Before commit:

1. list exact staged paths
2. review `git diff --cached --stat` and relevant staged diff metadata/content
3. verify unrelated unstaged and untracked work will remain untouched
4. run the relevant tests or syntax checks for the staged change
5. ensure the commit message matches the actual staged scope

## Destructive and history-rewriting operations

Treat these as high-risk until scope and recovery are proven:

- `git reset --hard`
- `git clean -f`, especially with `-d` or `-x`
- force push
- destructive branch deletion
- rebases of shared/published history
- checkout/restore commands that discard changes

Before recommending them:

- inventory the state that could be lost
- distinguish tracked, untracked, and ignored data
- preserve important non-Git state separately
- prefer preview options such as `git clean -n` when available
- prefer `--force-with-lease` over blind `--force` when force push is genuinely required

Do not present reflog as a universal backup. It does not protect every untracked, ignored, external, or already-garbage-collected object.

## Branch policy

Honor repository-specific contribution rules when they are known.

If no policy is known:

- documentation-only or trivial local work may be suitable for the current branch when the user explicitly intends it
- code, configuration, dependency, deployment, or mixed changes are safer on a feature branch by default
- never create or switch branches solely to appear safe if doing so would disrupt uncommitted work

State the branch recommendation and the reason rather than inventing project policy.

## Push verification

Before push, prove:

- intended remote
- intended branch/refspec
- upstream relation
- commits being sent
- whether force is involved

After push, verify:

- current branch and commit
- upstream relation using current enough evidence for the claim
- intended remaining dirty state
- that no unrelated files were accidentally staged or committed

## Output format

Use this structure:

### Git safety verdict
`SAFE`, `SAFE WITH FIXES`, or `STOP`, followed by one short reason.

### Repository identity
State proven root, branch/detached state, commit, remote names, and upstream.

### Alignment
State `ALIGNED`, `AHEAD`, `BEHIND`, `DIVERGED`, `NO UPSTREAM`, `DETACHED`, or `UNPROVEN`.

### Change inventory
Separate staged, unstaged, untracked, ignored, submodule/worktree, and in-progress-operation state. Omit empty categories when brevity helps.

### Risk findings
List only concrete risks such as wrong repo, broad staging, possible secret path, large/generated artifact, destructive command, detached HEAD, stale remote evidence, or mixed work.

### Approved next action
Give one exact Git command or a short safe sequence. If staging is approved, name the exact paths.

### Verification
Give the minimum commands or checks proving the result.

## Style

Be precise and conservative without being theatrical. Keep the difference between repository identity, worktree cleanliness, staged scope, and remote alignment explicit. Never claim a state that the evidence has not proven.
