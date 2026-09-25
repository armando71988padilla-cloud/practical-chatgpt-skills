---
name: tauri-security-boundary-auditor
description: Review a Tauri v2 application's native security boundary, permissions, capabilities, plugins, IPC commands, sidecars, remote-content exposure, CSP, updater configuration, shell/process access, filesystem scopes, and frontend-to-Rust trust transitions. Use when a user asks whether a Tauri app is safely scoped, wants to audit tauri.conf.json or capability files, is adding invoke commands or plugins, exposes native functionality to a webview, packages sidecars, loads remote content, or needs least-privilege checks before shipping. Treat scanner findings as review signals, not proof of a vulnerability.
---

# Tauri Security Boundary Auditor

## Purpose

Review a Tauri v2 app as a native security boundary, not merely as a frontend project. Keep webview authority narrow, make native privilege explicit, and separate proven findings from heuristic warnings.

## Workflow

1. Prove the exact project root and confirm it is a Tauri v2 project.
2. Identify the feature or boundary under review instead of auditing unrelated surfaces.
3. Inventory relevant Tauri config, capability files, plugins, Rust commands, frontend `invoke()` calls, sidecars, remote origins, CSP, updater settings, and native scopes.
4. When local files are available, run `scripts/tauri_surface_scan.py <project-root>` for a read-only static inventory.
5. Trace each relevant frontend action through capability/permission checks to the Rust command, plugin, sidecar, or native operation it reaches.
6. Check least privilege, input validation, path/URL normalization, origin restrictions, argument constraints, denial behavior, and privilege transitions.
7. Label evidence as `PROVEN`, `SUSPECTED`, or `UNPROVEN`.
8. Recommend the smallest boundary-tightening change that fixes the concrete issue.
9. Define verification tests, including at least one denied or malformed-input case for privileged operations.

Read `references/tauri-v2-review-checklist.md` when reviewing a real project or designing a native bridge. Read `references/examples.md` when a concrete review pattern is useful.

## Boundary inventory

Prioritize only the surfaces relevant to the request:

- `src-tauri/tauri.conf.json` or equivalent Tauri configuration
- `src-tauri/capabilities/` and any explicit capability declarations
- custom permission definitions when present
- Rust `#[tauri::command]` functions
- `.invoke_handler(...)` registration
- frontend `invoke()` calls
- Tauri plugins and the permissions/scopes they expose
- shell, process, filesystem, HTTP, opener, deep-link, dialog, SQL, store, and updater access when relevant
- sidecar binaries and allowed argument shapes
- CSP and production content origins
- remote URLs, remote capability declarations, or remote-domain IPC access
- localhost plugin or production localhost bridges
- updater endpoints, public key, artifact generation, and insecure-transport settings
- protocol handlers, file-open handlers, deep links, and externally supplied parameters

## Security rules

Apply these rules consistently:

- Treat frontend/webview input as untrusted input to native code.
- Prefer named, purpose-built native commands over generic execution bridges.
- Prefer typed and validated arguments over arbitrary strings, command arrays, or paths.
- Grant the minimum capability to the minimum window/webview that needs it.
- Remember that overlapping capabilities can merge effective permissions for the same window/webview.
- Avoid broad shell/process access when a narrow native command can perform the exact operation.
- Scope filesystem access to the smallest path set and operation set required.
- Scope HTTP access to intended hosts and methods when possible.
- Treat remote content as a separate trust zone. Do not let remote origins inherit local native authority accidentally.
- Prefer packaged/local production assets unless remote content is explicitly required.
- Keep CSP restrictive and intentional. Treat missing, null, or broadly weakened CSP as a review point, not an automatic vulnerability claim.
- Treat sidecars as privileged parts of the trusted computing base. Pin identity and constrain subcommands/arguments.
- Do not forward arbitrary user-supplied argument arrays to sidecars or shell commands without an allowlist/validation model.
- Treat updater authenticity separately from transport security. Review trusted endpoints, signing/public-key configuration, and insecure transport settings.
- Fail closed when a path, origin, command, executable, or privilege boundary cannot be proven.

## Scanner use

Use `scripts/tauri_surface_scan.py` only as a read-only static inventory aid.

The scanner:

- never executes project code
- never runs Cargo, npm, pnpm, yarn, bun, or build scripts
- never starts the Tauri app
- never modifies files
- never performs network requests
- reports heuristic markers that require manual review

Do not call a scanner warning a vulnerability without reading the relevant configuration or code.

## Evidence labels

### PROVEN

Use only when the project files or direct runtime/build evidence establish the claim.

Examples:

- a capability explicitly grants `shell:allow-execute`
- a window is listed in a capability containing filesystem write permissions
- a Rust command accepts a raw path and writes to it without a scope check
- updater config explicitly enables insecure transport

### SUSPECTED

Use for a risky pattern that still needs context.

Examples:

- shell plugin dependency is present but its permissions may not be granted
- broad filesystem markers exist but may be platform-limited or unused
- remote URLs exist but may not receive native capabilities

### UNPROVEN

Use when the relevant file, command registration, capability, origin, or runtime relationship is missing.

Never convert `SUSPECTED` or `UNPROVEN` into a vulnerability claim.

## High-impact review areas

Prioritize these when present:

- arbitrary shell/process execution
- unrestricted sidecar argument forwarding
- remote content with local native capability
- filesystem writes outside a tightly scoped application area
- arbitrary URL or host access from privileged plugins
- path traversal or absolute-path trust in privileged commands
- generic commands such as `run(command, args)` or `read_any_file(path)` exposed to the frontend
- disabled or intentionally broad CSP combined with native authority
- updater configuration that weakens transport or release authenticity
- capabilities that unintentionally apply to more windows/webviews than intended

## Verification tests

For each privileged command or plugin path, test the boundary rather than only the happy path.

Useful tests include:

- valid expected input
- invalid enum or operation name
- malformed argument shape
- extra unexpected arguments
- path traversal when a path is accepted
- absolute path outside the allowed scope
- URL/host outside the intended allowlist
- unsupported platform request
- invocation from a window/webview that should not possess the permission
- sidecar subcommand or argument not present in the allowlist
- update metadata with invalid or missing signature when updater behavior is under review

## Output format

Use this structure:

### Boundary verdict
`TIGHT`, `NEEDS HARDENING`, or `UNPROVEN`, followed by one short reason.

### Boundary under review
State the exact feature and native trust transition.

### Surface inventory
List only relevant configs, capabilities, commands, plugins, sidecars, origins, or updater settings.

### High-impact findings
List concrete excessive privilege, arbitrary execution, remote-origin, path/scope, validation, or updater trust issues. Write `None proven.` when appropriate.

### Medium-impact findings
List narrower hardening or future-risk concerns.

### Proven-safe properties
List controls directly supported by evidence.

### Smallest boundary change
Recommend one minimal hardening change or design decision.

### Verification tests
Give focused tests, including denial/invalid-input coverage where privilege is involved.

### Residual risk
State what remains intentionally trusted, platform-specific, or unproven.

## Scope control

Stay Tauri-specific unless the user asks for a wider threat model or dependency audit. Do not turn every review into a generic web-security lecture, a framework comparison, or a complete application redesign.

Do not assume Tauri makes privileged application code safe by itself. The application still owns its command design, permissions, scopes, validation, updater trust, sidecars, and native behavior.

## Style

Be direct, evidence-bound, and practical. Prefer one narrow boundary change over a broad rewrite.
