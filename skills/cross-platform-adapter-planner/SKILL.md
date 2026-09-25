---
name: cross-platform-adapter-planner
description: Plan how one product feature should be split between shared core logic and platform-specific adapters across desktop, mobile, server, container, or embedded targets. Use when a user asks what belongs in the common core versus Windows/Linux/macOS/Android/iOS code, wants an adapter interface, capability matrix, privileged-helper boundary, implementation order, unsupported-case behavior, or cross-platform test plan. Keep product policy platform-neutral, make capability gaps explicit, and do not invent parity where an operating system or application sandbox has not been proven to support it.
---

# Cross-Platform Adapter Planner

## Purpose

Design one stable product behavior while isolating unavoidable platform mechanics behind small semantic adapters. Keep policy, data contracts, evidence, and decisions shared; keep operating-system APIs, entitlements, service managers, device APIs, shell commands, and privileged mechanics out of the shared core.

## Workflow

1. Restate the requested feature in platform-neutral terms.
2. Define the product invariants that must mean the same thing on every supported platform.
3. Separate shared policy/data/decision logic from platform mechanics.
4. Define the smallest semantic adapter contract the shared core needs.
5. Build a capability matrix for the requested target platforms.
6. Mark each capability as `FULL`, `PARTIAL`, `COMPANION`, `UNSUPPORTED`, or `UNPROVEN`.
7. Place privileged operations behind a narrow helper only when ordinary application privileges cannot perform the required action safely.
8. Define fail-closed behavior for denied permissions, missing capabilities, stale targets, unsupported platforms, and unimplemented adapters.
9. Choose an implementation order that preserves one working reference path instead of creating several incomplete ports at once.
10. Define shared contract tests plus the minimum platform-specific integration tests required before enabling the feature.

Read `references/platform-boundary-guide.md` when the feature touches privilege, filesystems, services, networking, device control, OS policy, mobile sandboxes, app entitlements, or managed-device APIs. Read `references/examples.md` when a concrete architecture pattern is useful.

## Platform-neutral first rule

Describe the capability by outcome rather than by API.

Good shared-core concepts:

- enumerate removable storage devices
- report local firewall posture
- request a bounded quarantine action
- verify whether a service-like component is healthy
- normalize device identity evidence
- request one named persistence operation
- report whether a capability is available and why

Poor shared-core concepts:

- run `udevadm`
- call `launchctl`
- query one Windows registry key directly
- execute PowerShell
- invoke one Android intent
- call one iOS framework method

Those are adapter or helper implementation details unless the user is intentionally designing a platform-specific product.

## Responsibility model

Use these ownership buckets.

### Shared core

Put cross-platform meaning here:

- product policy and invariants
- risk/trust classification
- normalized data models and schemas
- evidence/audit records
- operator approval rules
- request validation that is not OS-specific
- capability-state interpretation
- rollback requirements
- action previews
- post-action verification expectations
- deterministic unsupported/denied behavior

The shared core should not import or depend directly on platform APIs.

### Adapter interface

Expose the smallest semantic contract needed by the core.

Prefer:

- `list_removable_devices()`
- `get_firewall_posture()`
- `quarantine_device(device_id)`
- `service_health(service_id)`
- `capability_status(capability)`

Avoid:

- `run_command(command, args)`
- `exec_shell(text)`
- `read_registry(path)` as a generic product contract
- `call_platform_api(name, payload)`

An adapter contract should describe intent, not transport.

### Platform adapter

Put OS-specific discovery, normalization, permissions, entitlements, API calls, command invocation, service-manager logic, path rules, and error translation here.

Adapters translate platform reality into the shared contract. They should not redefine product policy independently.

### Privileged helper

Create one only when the operating system requires elevated authority.

A helper should:

- expose a small allowlisted set of named operations
- validate all identifiers and arguments
- reject unknown operations
- use the narrowest required privilege
- return structured results
- support direct post-action verification
- expose enough evidence for rollback or review

Do not expose arbitrary shell/process execution to the UI or shared core.

### UI / client

Put presentation, operator intent, user confirmation, explanation, and platform capability display here.

Do not make the UI the only enforcement point for authoritative policy.

## Capability status vocabulary

Use exactly one status for each requested platform capability.

### FULL

The intended product capability is practical and proven for the target environment with the required privileges/entitlements.

### PARTIAL

Meaningful behavior exists, but one or more parts of the shared desktop/server contract cannot be provided.

### COMPANION

The platform can review, report, approve, coordinate, or interact with a remote/managed endpoint, but it cannot provide equivalent local endpoint control.

### UNSUPPORTED

The capability is not available for the intended product boundary and should not be simulated.

### UNPROVEN

The capability might be possible, but the required API, entitlement, deployment mode, privilege, or product boundary has not been verified.

Never promote `UNPROVEN` to `FULL` from memory or assumptions. When current platform restrictions matter, require current authoritative platform documentation or direct runtime proof.

## Capability matrix rules

For each platform ask:

1. Can the app observe the required state?
2. Can it observe it without elevation or special entitlements?
3. Can it perform the requested action?
4. What privilege, entitlement, service, device-owner/management mode, or administrator boundary is required?
5. Is the capability available to ordinary third-party apps, only managed/enterprise apps, or neither?
6. Can the action be rolled back?
7. Can the resulting state be verified independently?
8. What happens when permission is denied or revoked?
9. What product behavior should the shared core see when the platform cannot comply?

Do not force desktop semantics onto sandboxed/mobile environments merely to make the matrix look symmetrical.

## Contract design rules

- Keep adapter methods semantic and narrowly scoped.
- Normalize platform-specific errors into a stable shared error/status model.
- Represent unsupported and denied states explicitly.
- Prefer typed records over free-form dictionaries when the data model is stable.
- Avoid leaking platform-specific path syntax, service names, registry concepts, or command strings into shared policy.
- Keep platform-specific identifiers opaque to the shared core unless the core genuinely needs to compare them.
- Do not require every platform to implement an operation that the product can honestly mark unsupported.
- Version the adapter contract when changing semantics, not simply because one implementation changes internally.

## Fail-closed behavior

Define behavior for at least:

- capability unsupported
- capability not implemented
- permission denied
- entitlement missing
- target no longer exists
- platform API returns stale or ambiguous state
- privileged helper unavailable
- partial observation only
- action performed but post-action verification fails

The shared core should receive a structured failure or degraded-capability state, not a fake success.

## Implementation order

Prefer this sequence unless project constraints prove a better one:

1. Freeze the platform-neutral feature objective and invariants.
2. Define normalized records/statuses and the adapter interface.
3. Preserve or implement one working reference adapter.
4. Add shared contract tests using a fake/test adapter.
5. Implement the next platform adapter with platform-specific integration tests.
6. Enable only capabilities that have passed both contract and platform tests.
7. Add remaining adapters one at a time.
8. Revisit the shared contract only when repeated platform evidence proves the abstraction is wrong.

Do not design five full implementations before the shared contract has survived one or two real adapters.

## Verification layers

### Shared contract tests

Run the same tests against every adapter implementation for:

- required fields and normalized data shapes
- deterministic capability states
- unsupported behavior
- permission-denied behavior
- no accidental action during review-only calls
- evidence/audit shape
- stable error translation
- rollback metadata when action is supported

### Platform integration tests

For each implemented adapter test:

- normal observation
- permission denied
- capability absent
- stale or removed target
- expected successful action when action is supported
- rollback when supported
- post-action verification
- helper unavailable when a privileged helper exists

### UI/client tests

Verify the UI distinguishes `FULL`, `PARTIAL`, `COMPANION`, `UNSUPPORTED`, and `UNPROVEN` accurately and does not imply capabilities the adapter does not provide.

## Current-platform claims

Operating-system APIs, app-store rules, mobile entitlements, management APIs, sandbox restrictions, and enterprise capabilities change over time.

When a recommendation depends on current platform policy or API availability:

- use current authoritative vendor documentation when tools are available
- identify the OS/application deployment context precisely
- distinguish ordinary consumer apps from managed/enterprise/device-owner modes
- date the conclusion when freshness matters

Do not present historical capability assumptions as current facts.

## Output format

Use this structure:

### Feature objective
One concise platform-neutral description.

### Shared core contract
List product invariants, normalized data, decisions, evidence, and safety rules that belong above platform code.

### Adapter interface
List the smallest semantic methods and records the core needs.

### Platform capability matrix
Use columns: platform, status, adapter responsibility, privilege/entitlement boundary, important limitation, evidence state.

### Ownership map
Assign responsibilities to shared core, adapter interface, each platform adapter, privileged helper, and UI/client.

### Denied / unsupported behavior
State exactly what fails closed, degrades, becomes companion-only, or remains disabled.

### Implementation order
Give the smallest sequence that preserves a working reference path and avoids parallel rewrites.

### Verification matrix
List shared contract tests plus the minimum platform-specific proof for each adapter.

### Release boundary
State which capabilities must remain disabled, review-only, or `UNPROVEN` until direct evidence exists.

## Style

Be concrete and architecture-focused. Prefer one small stable contract plus honest capability differences over fake cross-platform symmetry. Do not redesign unrelated subsystems.
