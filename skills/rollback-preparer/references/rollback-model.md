# Rollback model

Use this reference when a planned change spans more than one state layer or has a non-obvious recovery path.

## File and configuration changes

Protect the exact live file and any metadata required for it to function. Resolve symlinks before deciding which object to back up. A backup inside the directory being replaced is not independent recovery.

For a single configuration file, a timestamped sibling or dedicated backup directory is often enough. For a directory tree, consider whether a metadata-preserving copy or archive is more appropriate than many independent file copies.

## Services and daemons

Separate configuration rollback from runtime activation. Restoring a file does not necessarily restore running behavior until the service reloads, restarts, or the process is replaced.

Capture:

- active configuration path
- enabled/disabled state when relevant
- restart/reload requirement
- narrow post-restore health check

Do not restart unrelated services merely because they are nearby in the stack.

## Package upgrades

A package rollback is only ready when the exact previous version can be reinstalled and its dependencies remain satisfiable. Record the current version before upgrade and confirm the older artifact or repository version is still available.

Package downgrade may not reverse data-file or schema migrations performed by the newer version. Treat those as separate state.

## Git repositories

Git can protect tracked source, but not every working-state dependency.

Before a risky repository operation, consider:

- repository root
- current branch and commit
- staged and unstaged tracked changes
- untracked files
- ignored files that still matter
- submodules or worktrees
- generated or external state

A branch or commit alone is not a complete rollback when important state lives outside Git.

## Databases and stateful stores

Do not treat copying live database files as a generally safe backup strategy. Use engine-supported backup/snapshot/export procedures and account for consistency, write activity, logs, schema versions, and restore compatibility.

A schema migration may be intentionally one-way. If downgrade SQL or a tested restore is unavailable, mark rollback `PARTIAL` or `STOP`.

## Deployments

For application releases, distinguish code rollback from data and infrastructure rollback.

Possible layers include:

- application artifact or container image
- environment/configuration
- secrets references
- database schema/data
- cache/message formats
- infrastructure definitions
- feature flags
- external integrations

Rollback is `READY` only when the layers changed by the release can return to a mutually compatible state.

## Operating-system changes

For firewall, registry, kernel, driver, boot, disk, partition, account, ACL, or security-policy changes, use platform-native export/snapshot/recovery mechanisms when possible. Some changes can make the machine unbootable or unreachable; local recovery media, console access, or an out-of-band path may be part of the rollback plan.
