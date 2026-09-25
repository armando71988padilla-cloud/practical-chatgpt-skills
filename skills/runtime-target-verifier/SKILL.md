---
name: runtime-target-verifier
description: Verify that the file, service, script, binary, container, configuration, wrapper, symlink, or application entrypoint a user plans to edit is the same target the live runtime is actually using. Use when a user asks whether they are editing the right file, wants to trace what a service or process is running, sees changes not taking effect, has duplicate or similarly named copies, or needs the first unproven link between a launcher and live code. Distinguish proven, suspected, mismatched, and unproven links, and do not recommend patching until the live target is sufficiently proven.
---

# Runtime Target Verifier

## Purpose

Prove what the live runtime is actually using before the user edits, replaces, restarts, or debugs the wrong target. Trace the smallest evidence chain from launcher to process to real path and configuration.

## Workflow

1. Identify the claimed target the user believes is live.
2. Identify the runtime type: direct process, service, scheduled task, launcher, container, development server, or other supervisor.
3. Gather direct runtime evidence before relying on names or repository layout.
4. Resolve wrappers, arguments, working directories, symlinks, environment files, mounts, and interpreters only as far as needed.
5. Label each link in the chain as `PROVEN`, `SUSPECTED`, `MISMATCH`, or `UNPROVEN`.
6. Stop at the first unproven link that could change which file or binary is actually used.
7. Give the smallest read-only command or check that can prove that link.
8. State patch safety as `SAFE TO PATCH`, `NOT SAFE TO PATCH`, or `CONDITIONAL`.

Do not modify files, services, processes, containers, or configuration while establishing the runtime target.

Read `references/runtime-model.md` for platform-specific evidence and multi-hop chains. Read `references/examples.md` when a concrete example is useful.

## Evidence rules

### PROVEN

Use only for a link established by direct runtime or filesystem evidence, such as a process executable path, service command line, resolved symlink, container mount, active working directory, loaded configuration path, or exact runtime argument.

### SUSPECTED

Use when names, conventions, repository layout, documentation, or timestamps make a connection likely but do not prove the live runtime uses it.

### MISMATCH

Use when evidence points to a different target than the file, binary, service, container, branch, or configuration the user expected.

### UNPROVEN

Use when a meaningful hop still needs evidence.

Never promote `SUSPECTED` to `PROVEN` merely because the path looks right.

## Patch safety rules

### SAFE TO PATCH

Use when the claimed target matches the proven live target closely enough that editing it would affect the intended runtime after any known reload/restart/rebuild step.

### CONDITIONAL

Use when the target is proven but another required activation step remains, such as a rebuild, service restart, container recreation, cache invalidation, or deployment switch.

### NOT SAFE TO PATCH

Use when the live target is unproven, evidence points somewhere else, or multiple plausible targets remain.

Do not recommend a patch while status is `NOT SAFE TO PATCH`.

## What to prove

Trace only the links that can alter runtime identity. Common links include:

- service or supervisor -> command line
- command line -> interpreter or executable
- wrapper -> child script or binary
- relative path -> working directory -> absolute path
- symlink -> real target
- environment variable -> selected config or executable
- process -> executable path and command arguments
- container -> image, command, bind mount, volume, and in-container path
- development server -> project root and entry module
- scheduled task -> executable, arguments, and working directory
- launcher shortcut -> target and arguments

A repository filename by itself is not runtime proof.

## Cross-platform guidance

Support Linux, macOS, and Windows using the user's actual shell when known.

On Linux, useful evidence may include `systemctl cat`, `systemctl show`, `/proc/<pid>/exe`, `/proc/<pid>/cwd`, `ps`, `pgrep`, `readlink -f`, `realpath`, and container inspection tools.

On macOS, useful evidence may include `launchctl print`, `ps`, `lsof`, resolved paths, application bundle executables, and launch-agent or launch-daemon property lists.

On Windows, useful evidence may include PowerShell `Get-CimInstance Win32_Process`, `Get-Process`, `Get-CimInstance Win32_Service`, `Get-Service`, Task Scheduler inspection, `Get-Item`, and resolved shortcut or executable paths.

Do not invent commands for a platform or supervisor that has not been established.

## Containers and build outputs

Treat source code, build output, and running container paths as separate targets until proven connected.

For containers, prove at least the relevant container identity plus the command and mount/image relationship that determines the live file. Editing a host source file does not prove the container consumes it.

For compiled or bundled applications, editing source is not the same as changing the running artifact. Identify the build output and activation step before calling the source path patch-safe.

## Output format

Use this structure:

### Runtime verdict
`MATCH`, `MISMATCH`, or `UNPROVEN`, followed by one short reason.

### Claimed target
State what the user believes is live.

### Proven live target
State the exact proven target, or `Not yet proven.`

### Proven chain
List only links supported by direct evidence.

### First unproven or mismatched link
State one link only.

### Smallest safe next check
Give one exact read-only command or inspection step.

### Patch safety
`SAFE TO PATCH`, `CONDITIONAL`, or `NOT SAFE TO PATCH`, with one short reason.

### Activation note
Include only when a proven edit still requires rebuild, reload, restart, recreation, redeploy, or another activation step.

## Style

Be direct and operational. Prefer exact paths, process IDs, service names, command lines, and one next check over a broad debugging checklist. Keep proven evidence separate from inference.
