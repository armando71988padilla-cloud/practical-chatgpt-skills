---
name: rollback-preparer
description: Prepare a concrete rollback plan before a risky system, application, configuration, deployment, service, package, or repository change. Use when a user asks how to undo a planned edit, wants backup and restore commands before making a change, needs a checkpoint before restarting or upgrading something, or wants to prove that rollback is actually possible. Require target proof, pair every backup with a restore path, distinguish reversible from non-reversible changes, and do not pretend a rollback exists when recovery depends on missing facts or unavailable backups.
---

# Rollback Preparer

## Purpose

Prepare the smallest practical rollback before a risky change. Make the recovery path explicit, testable, and boring before the user changes live state.

## Workflow

1. Identify the exact change and the state it could modify.
2. Prove the live target before creating backup or restore commands.
3. Classify rollback readiness as `READY`, `PARTIAL`, or `STOP`.
4. Choose the smallest backup or checkpoint that protects the proven target.
5. Pair every backup artifact with an exact restore action.
6. Record any service reload, restart, reboot, package, schema, or dependency consequence that rollback also requires.
7. Add one pre-change verification proving the checkpoint exists and is readable.
8. Add one post-restore verification proving the old state is actually active again.

Do not execute the planned change or rollback unless the user explicitly asks for execution and the available tools permit it.

Read `references/rollback-model.md` for multi-layer, package, database, service, or deployment changes. Read `references/examples.md` when a concrete example is useful.

## Readiness rules

### READY

Use when the live target is proven, the backup/checkpoint is practical, the restore command is known, and the restored state can be verified.

### PARTIAL

Use when meaningful recovery is possible but some state cannot be captured exactly, requires a reboot/redeploy, depends on an external artifact, or has a known non-reversible side effect.

### STOP

Use when the target is unproven, the proposed backup does not actually protect the changed state, the restore artifact is unavailable or untested, or the change may destroy state that cannot be reconstructed.

Never turn uncertainty into a fake rollback plan.

## Target proof

Prove the thing that will actually change, not a similarly named file or guessed path.

Useful proof may include:

- absolute file or directory path
- resolved symlink target
- running executable or process path
- active service/unit configuration path
- current package name and version
- repository root, branch, commit, and working-tree state
- deployment identifier or currently active release
- database engine, database name, backup method, and consistency requirements

If proof is missing, make target verification the first step and stop before destructive or mutating commands.

## Backup rules

- Back up only the state needed to reverse the planned change unless broader state is truly coupled.
- Prefer timestamped or uniquely named artifacts.
- Preserve permissions, ownership, ACLs, metadata, and symlink behavior when those affect restoration.
- Keep backups outside a directory that the planned change may delete or replace.
- For Git-tracked source, do not assume Git protects untracked files, ignored files, generated state, credentials, databases, or external configuration.
- For package upgrades, record the exact current version and prove the old package/artifact remains obtainable before calling rollback ready.
- For databases or transactional stores, require a backup method appropriate to the engine; a raw file copy is not automatically consistent.
- For remote or distributed deployments, identify every stateful layer that must agree after rollback.

## Restore rules

- Pair each backup with the exact restore destination.
- Restore metadata when it matters, not only file contents.
- Include reload/restart/reboot steps only when required to make restored state active.
- Prefer atomic replacement or a maintenance window when partial restoration could leave mixed state.
- Do not delete the backup as part of the restore procedure.
- Keep cleanup separate and optional until restoration is verified.

## Verification rules

Verification must prove behavior or active state, not merely that a copy command returned success.

Examples:

- compare a cryptographic hash when exact file identity matters
- inspect the active configuration path after restoration
- confirm the service is running with the restored configuration
- confirm the package version actually downgraded
- confirm the repository and working tree match the intended checkpoint
- run a narrow health/readiness check after a deployment rollback

## Cross-platform guidance

Support Linux, macOS, and Windows. Use the user's actual shell and platform when known.

- On Unix-like systems, prefer metadata-preserving tools such as `cp -a`, `rsync -a`, or an archive when appropriate.
- On Windows, prefer explicit PowerShell paths and tools such as `Copy-Item`, `robocopy`, registry export/import, or platform-native backup mechanisms as appropriate.
- Do not invent platform-specific commands when the operating system or target type is unknown.

## Output format

Use this structure:

### Rollback readiness
`READY`, `PARTIAL`, or `STOP`, followed by one short reason.

### Change at risk
One short description of the state that could be modified.

### Proven target
State the exact proven target, or say what remains unproven.

### Pre-change proof
One exact read-only command or check.

### Backup / checkpoint
One exact command or a short numbered sequence. If required facts are missing, provide only the read-only discovery step instead of guessing.

### Restore
One exact command or a short numbered sequence that uses the backup/checkpoint above.

### Restore verification
One exact command or check proving the previous state is active again.

### Caveats
Include only meaningful limitations such as irreversible data migration, unavailable prior package versions, external state, required downtime, or incomplete target proof.

## Style

Be concise and operational. Favor exact targets and commands over generic advice. Keep one rollback plan per risk surface unless the states are genuinely coupled. The recovery procedure should be understandable under stress.
