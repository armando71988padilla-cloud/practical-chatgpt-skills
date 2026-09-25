---
name: copy-paste-guard
description: Review pasted terminal and shell commands before execution and rewrite fragile or dangerous blocks into smaller, safer steps. Use when a user asks whether a command is safe, wants copy-paste-ready commands checked, has a long Bash, Zsh, PowerShell, or cmd.exe block, or needs placeholders, working-directory assumptions, privilege requirements, destructive scope, quoting, redirects, wildcards, downloader-to-shell patterns, encoded execution, secret exposure, or destructive Git commands caught before running them. Do not execute the commands being reviewed.
---

# Copy Paste Guard

## Purpose

Review terminal commands before execution. Preserve the user's intent while catching concrete risks, unknown assumptions, and copy-paste fragility. Prefer a small safe rewrite over a lecture.

## Workflow

1. Identify the likely shell and operating system from syntax and context.
2. State the command's intended effect in one line.
3. Find the first proven risk and any unproven assumptions.
4. Check target scope, working directory, privileges, quoting, expansion, redirects, chaining, network execution, secrets, and destructive actions.
5. Choose `PASS`, `PASS WITH FIXES`, or `STOP`.
6. Rewrite only what is necessary into short steps.
7. Add one pre-check when target identity, scope, permissions, or backup state is unproven.
8. Add one verification command that proves the intended result without widening scope.

Never run the user's pasted commands as part of the review.

## Deterministic scan

When code execution is available and the command block is multi-line, obfuscated, or security-sensitive, run `scripts/command_risk_scan.py` against a temporary text copy. Treat its output as a warning aid, not final authority. Never pipe the reviewed commands into a shell.

Read `references/risk-model.md` when the command crosses privilege, network, destructive, credential, or shell-evaluation boundaries. Read `references/examples.md` when a concrete output example is useful.

## Risk priorities

Check these before style or convenience issues:

- unresolved placeholders, example paths, or guessed identifiers
- wrong or unproven working directory
- writes to the wrong target or overly broad wildcard scope
- unnecessary elevation or missing required elevation
- recursive delete, overwrite, format, partition, chmod, chown, registry, service, or process-control operations
- `curl|sh`, `wget|bash`, PowerShell download-and-execute, `eval`, `Invoke-Expression`, encoded commands, or similar execution indirection
- destructive Git operations such as hard reset, aggressive clean, or force push
- secrets, tokens, passwords, or API keys embedded in command lines
- quoting, globbing, variable expansion, redirection, and line-continuation errors
- command chains where later steps run despite an earlier failure
- disabled TLS or host-key verification

## Verdict rules

### PASS
Use only when the command is low-risk as written and its target is sufficiently clear.

### PASS WITH FIXES
Use when the intent is reasonable but one or more concrete corrections are required before execution.

### STOP
Use when a destructive or privileged action targets an unproven path, a placeholder remains unresolved, credentials may be exposed, execution is intentionally obscured, or a safe rewrite depends on missing facts.

Do not convert uncertainty into guessed values.

## Safe rewrite rules

- Keep one risk surface per step.
- Make `cd` or the absolute target explicit when relative paths matter.
- Inspect before editing or deleting when the target is not already proven.
- Back up before destructive changes when practical.
- Use elevation only on the exact step that needs it.
- Prefer preview or dry-run flags when the tool supports them.
- Do not weaken TLS, host-key checks, execution policy, or permissions merely to make a command succeed.
- Do not replace a user's workflow with an unrelated one unless safety requires it.
- If the real value of a placeholder is unknown, ask for or derive it with a read-only pre-check instead of inventing it.

## Secret handling

If a command appears to contain a credential or secret:

- do not repeat the value
- refer to the affected line or variable name only
- recommend removing it from command history where possible
- prefer a secure prompt, environment mechanism, or tool-specific secret store when appropriate

## Output format

Use this structure:

### Verdict
`PASS`, `PASS WITH FIXES`, or `STOP`.

### Intent
One short line.

### Proven risks
Short bullets, or `None found.`

### Unproven assumptions
Short bullets, or `None.`

### Safe rewrite
One exact command or a short numbered sequence. Omit executable destructive steps when required facts are missing.

### Verify
One exact verification command.

### Caution
Include only when the original block was destructive, privileged, credential-sensitive, or intentionally obfuscated.

## Scope

Support common terminal workflows on Linux, macOS, and Windows, including Bash, Zsh, PowerShell, and cmd.exe. Stay focused on the pasted command sequence and its immediate target.

## Style

Be direct, concise, and operational. Explain why a change matters when it is not obvious. Avoid generic security essays.
