# Tauri v2 security review checklist

Use this reference after the exact project root and feature boundary are known.

## Project identity

- Confirm the real `src-tauri` directory.
- Confirm Tauri v2 from Cargo/package metadata rather than assuming from folder layout.
- Distinguish development `devUrl` from the production asset/origin model.
- Identify whether production content is packaged locally or loaded from remote origins.

## Capabilities and permissions

For every relevant window/webview:

- identify every capability that applies
- remember that multiple applicable capabilities can combine their effective permissions
- identify plugin/core permissions granted by each capability
- identify explicit allow/deny scopes
- identify platform restrictions
- identify remote capability declarations

Review high-impact permission families especially carefully:

- shell/process execution
- filesystem writes or broad recursive reads
- HTTP access
- opener/external URL handling
- updater install/download authority
- SQL or persistent stores that expose sensitive state
- deep links or protocol handlers that feed untrusted parameters into privileged commands

Prefer narrowly scoped permissions over broad defaults when the feature only needs one operation.

## Commands and IPC

For each frontend `invoke()` or native command path:

- identify the matching Rust command
- identify how the command is registered
- identify all arguments and their types
- identify normalization and validation
- identify any path, URL, command, service, device, or process privilege transition
- identify denial behavior

High-risk patterns include:

- arbitrary executable names
- arbitrary shell text
- user-supplied argument arrays forwarded directly to a process
- arbitrary absolute paths
- user-supplied URLs passed directly to privileged HTTP/opener functionality
- generic filesystem bridges such as `read_file(path)` or `write_file(path, data)` without path scoping

## Remote content and origins

Treat remote pages as a separate trust zone.

Review:

- remote URLs in configuration
- remote capability declarations
- remote-domain IPC access settings
- navigation to external origins
- CSP
- localhost production bridges
- external URL opening

Do not assume a trusted organization domain is equivalent to trusted native code. Remote content can change independently of the packaged binary.

## CSP

Review the production CSP and the reason for every widened source.

Flag for review:

- `csp: null`
- missing CSP when the application has meaningful native authority
- broad `*` sources
- unnecessary `unsafe-eval`
- remote scripts or CDNs that are not required

Do not automatically call `unsafe-inline` a vulnerability; determine whether Tauri's nonce/hash handling and application requirements justify it.

## Shell and sidecars

For shell/process plugins or sidecars, confirm:

- exact executable identity
- sidecar vs system binary distinction
- exact allowed subcommands
- argument constraints
- no arbitrary pass-through arrays unless explicitly justified and validated
- no user-controlled executable path replacement
- output is treated as untrusted data
- failures do not silently broaden scope

Prefer a narrow contract such as `status --json` over a generic `exec <args...>` bridge.

## Filesystem access

Confirm:

- read versus write need
- exact path scopes
- recursive behavior
- symlink behavior when relevant
- whether user-controlled paths are normalized and checked after resolution
- whether temporary/export directories can be used instead of broad home-directory access

## HTTP and opener access

Confirm:

- intended hosts/origins
- whether redirects can escape the intended trust zone
- whether arbitrary schemes are accepted
- whether URLs are validated before opening or fetching
- whether credentials/cookies/tokens can be exposed to unintended origins

## Localhost plugin

A production localhost server changes the local attack surface.

When present, review:

- why the default packaged/custom-protocol model is insufficient
- bind address
- authentication/authorization assumptions
- origin behavior
- CSRF-style local browser interactions when state-changing routes exist
- whether native IPC authority is exposed through the localhost surface

Do not call localhost inherently unsafe; require a concrete reason for the added surface.

## Updater and release trust

When updater functionality is enabled, confirm:

- intended endpoints
- HTTPS in production
- insecure transport is not enabled without an explicit reason
- expected signing/public-key configuration
- update artifact provenance
- behavior when signature verification fails
- update install permissions are granted only where needed

Transport security and artifact authenticity are separate controls.

## Verification pattern

For privileged behavior, test at least:

- valid expected input
- malformed input
- unsupported operation name
- out-of-scope path or URL
- traversal/normalization edge case when paths are accepted
- unexpected sidecar argument
- invocation from a window/webview that should not have access
- failure behavior when a required trusted artifact is missing or invalid

The review is incomplete if only the happy path was tested.
