# Trust boundary guide

Use only the zones relevant to the design under review.

## Operator or end user

Represents human intent and approval. Human input can still be malformed, stale, coerced, or based on incorrect information, so approval is not a substitute for validation.

## Browser, webview, or UI client

Treat presentation-layer code and all client-provided arguments as lower trust than privileged native or server logic. UI-side validation improves usability but is not authoritative enforcement.

## Local IPC or native bridge

Examples include named pipes, sockets, RPC, desktop IPC, plugin bridges, and webview-to-native commands.

Review:

- caller/origin identity
- command names
- argument validation
- path/URL/identifier scoping
- replay behavior
- privilege transition
- denial handling

## Remote API boundary

Review authentication, authorization, tenant scoping, request validation, replay/idempotency, rate limits where relevant, and error/data exposure.

Do not treat successful authentication as proof of authorization.

## Shared product core

Policy, normalized decisions, evidence rules, and platform-neutral behavior belong here. Protect this layer from platform-specific shortcuts that weaken shared invariants.

## Platform adapter

OS-specific observation and action mechanics. Treat external command output, device identifiers, filesystem state, and OS object identifiers as data that requires normalization and validation.

## Privileged helper

Strong privilege boundary. Expose only narrow named operations with strict validation and direct post-action verification.

Avoid arbitrary `run`, `exec`, `shell`, or generic filesystem/network bridges when a semantic operation can be defined instead.

## Operating system / runtime

Trusted for local security primitives being consumed, but not assumed bug-free. Distinguish ordinary user authority from administrator/root/system/service authority.

## Container or VM boundary

Host and guest/container namespaces are distinct. Mounts, published ports, credentials, host sockets, device access, and privileged container settings can collapse the boundary.

## Database, queue, cache, or state store

Treat data stores as separate trust and integrity domains when they accept structured commands or retain security-sensitive state. Review authorization, tenant isolation, query/object scoping, and migration/recovery behavior.

## Local files and evidence

Integrity-sensitive when files influence decisions, rollback, configuration, policy, or claims of success. Distinguish generated evidence from live state.

## Third-party dependencies and plugins

Trusted code introduced by package managers, build tooling, plugins, native libraries, browser extensions, SDKs, or bundled binaries.

## Update and release channel

Controls what future code can replace the current application. Signing, provenance, authorization to publish, and rollback trust matter even when transport is encrypted.

## External files, devices, or imported data

Treat content and metadata as untrusted until parsed and validated. Identity can help audit or policy but must not automatically establish trust unless the product explicitly defines that rule.

## Trust-boundary notation

Use concise arrows and annotate privilege increases where useful.

Example:

`Remote page [untrusted] -> native IPC [user] -> helper [administrator] -> filesystem`

For every privilege increase, ask:

1. Who is authorized to request it?
2. What exact operation is allowed?
3. How are arguments scoped and normalized?
4. What evidence is recorded?
5. How is the resulting state verified?
6. What happens on denial or partial failure?
