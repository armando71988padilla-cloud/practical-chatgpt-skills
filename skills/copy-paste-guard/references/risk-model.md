# Command review risk model

Use this reference for security-sensitive or destructive command blocks.

## Target certainty

Before a write, delete, permission change, service change, registry edit, disk operation, or forceful Git operation, determine whether the target is explicit and believable. Relative paths, variables, wildcards, mount points, drive letters, service names, branches, and remote names can widen impact.

If target identity is not proven, prefer a read-only pre-check and stop before the mutating step.

## Destructive operations

Treat these as high-risk until scope is proven:

- recursive delete or forced removal
- disk formatting, partitioning, raw writes, or filesystem creation
- recursive ownership or permission changes
- registry deletion or broad configuration replacement
- service disable/remove operations
- destructive Git reset, clean, or forced push
- overwrite redirects or forceful file replacement where no backup exists

A safer sequence is normally: inspect -> preview -> backup if practical -> mutate -> verify.

## Execution indirection

Treat downloaded or transformed code executed immediately as higher risk because review is bypassed. Examples include downloader-to-shell pipelines, `eval`, `Invoke-Expression`, encoded PowerShell, shell `-c` wrappers, and dynamically constructed commands.

Prefer downloading to a file, inspecting provenance and content, then executing only after review when execution is actually required.

## Privilege boundary

Elevation magnifies mistakes. Keep `sudo`, Administrator privileges, or root context limited to the exact command that needs it. Do not solve a permission error with recursive `chmod 777`, broad `chown`, or disabling platform protections.

## Credentials

Command-line secrets can leak into shell history, process listings, logs, screenshots, and support transcripts. Do not echo suspected secret values in the review.

## Network trust

Flag disabled TLS validation, disabled SSH host-key checking, unsigned or unknown downloads, and remote scripts executed without inspection. Do not recommend bypassing verification just to make the command work.

## Shell semantics

Pay attention to differences between Bash/Zsh, PowerShell, and cmd.exe. Quoting, variable expansion, wildcard behavior, command separators, redirection, and error propagation differ. When shell identity materially changes safety, say so instead of guessing.
