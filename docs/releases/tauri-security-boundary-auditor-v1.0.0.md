# Tauri Security Boundary Auditor v1.0.0

First public release candidate.

## Included

- Tauri v2 capability, permission, plugin, IPC, sidecar, CSP, remote-content, localhost, and updater review
- explicit `PROVEN`, `SUSPECTED`, and `UNPROVEN` evidence labels
- `TIGHT`, `NEEDS HARDENING`, and `UNPROVEN` boundary verdicts
- read-only static scanner for common high-impact Tauri security surfaces
- shell/process, filesystem write, HTTP, updater, remote capability, CSP, direct Rust process, and frontend invoke inventory
- denial-case verification guidance for privileged commands
- no project execution, build execution, package-manager execution, network access, or file mutation by the helper

## Verification completed

- skill structure validation passed
- helper script compiled successfully
- deliberately risky fixture produced expected review findings
- narrow fixture produced zero findings
- public source passed private-identifier and secret-pattern scans
- final packaged ZIP passed validation
- final ZIP contains exactly one `SKILL.md` and five readable files
- no compiled bytecode or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
