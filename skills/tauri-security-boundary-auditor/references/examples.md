# Tauri Security Boundary Auditor examples

## Generic shell bridge

Request:

> My Tauri frontend calls a Rust command with an executable name and argument array. Is that okay?

Good behavior:

- treat arbitrary executable/argument forwarding as a high-impact review area
- identify whether shell/plugin permissions or direct Rust process execution are involved
- recommend a named operation with typed/validated arguments when possible
- require rejection tests for unsupported commands and extra arguments

## Scoped file export

Request:

> The app needs to save one exported report chosen by the user. Should I give it broad filesystem write permission?

Good behavior:

- question whether broad write scope is necessary
- prefer a user-selected destination or narrowly scoped write permission
- verify paths cannot escape the allowed destination through traversal or symlink tricks when relevant

## Remote dashboard

Request:

> I want a remote web dashboard loaded in the Tauri window to call native commands.

Good behavior:

- treat the remote origin as a separate trust zone
- inspect remote capability/origin settings and CSP
- require a narrow native authority model or recommend keeping remote content away from privileged IPC
- do not assume HTTPS alone makes the remote page safe to grant native authority

## Sidecar

Request:

> My Tauri app bundles a helper binary and passes frontend arguments straight through to it.

Good behavior:

- treat the sidecar as privileged trusted code
- inspect allowed subcommands/argument scopes
- reject arbitrary passthrough when the feature can be modeled as named operations
- test malformed and unsupported arguments

## Updater

Request:

> Can you review my Tauri updater config before release?

Good behavior:

- inspect endpoints, insecure transport settings, public-key/signature configuration, and granted updater permissions
- separate transport security from artifact authenticity
- define a failure test for invalid/missing signatures
