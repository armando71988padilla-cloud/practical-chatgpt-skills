# Platform boundary guide

Use this reference when a feature crosses privilege, service, filesystem, networking, device, or mobile-sandbox boundaries.

## Shared core versus adapter

A responsibility belongs in the shared core when its meaning should stay the same regardless of operating system.

Examples:

- trust/risk decisions
- normalized device or service records
- audit/evidence schemas
- approval requirements
- capability-state semantics
- rollback prerequisites
- verification requirements

A responsibility belongs in an adapter when it answers "how does this platform expose or perform that capability?"

Examples:

- service manager APIs
- registry/plist/config-store access
- device enumeration APIs
- firewall APIs
- filesystem permission mechanics
- app entitlements
- mobile management/device-owner APIs
- OS-specific error mapping

## Privileged helper boundary

Use a helper only when application-level privileges cannot safely perform the operation.

Good helper API:

- `set_firewall_rule(rule_id, desired_state)`
- `quarantine_device(device_id)`
- `install_service(service_manifest_id)`

Bad helper API:

- `run(command)`
- `exec(program, args)`
- `shell(script_text)`

A helper should validate identifiers, reject unexpected input, use narrow privileges, and return structured status/evidence.

## Mobile and sandboxed platforms

Do not assume mobile operating systems expose desktop-equivalent endpoint control to ordinary third-party apps.

Distinguish:

- ordinary consumer application
- app with special entitlement
- enterprise/managed-device application
- device-owner/device-management mode
- companion application controlling another endpoint

If the required capability exists only in a managed mode, label ordinary-app capability separately instead of marking the platform globally `FULL`.

## Service-like concepts

Do not put `systemd`, Windows Service Control Manager, `launchd`, foreground services, background tasks, or mobile push/background APIs into the shared contract.

Use a semantic concept such as:

- `component_health(component_id)`
- `start_component(component_id)` when supported
- `capability_status("background_execution")`

Let each adapter map the semantic concept to platform mechanics or return `UNSUPPORTED`/`PARTIAL`.

## Filesystem concepts

Shared code should request semantic locations or data classes rather than hard-coded platform paths when possible.

Examples:

- app configuration directory
- user-selected export destination
- removable-media mount identity
- application cache/storage location

Adapters should normalize path syntax, permissions, symlink/reparse-point behavior, sandbox/container boundaries, and storage-provider behavior.

## Networking concepts

Keep desired policy/state shared; keep the implementation platform-specific.

Shared:

- desired allow/deny rule semantics
- endpoint/service identifiers
- verification expectations

Adapter/helper:

- firewall API or command
- administrator/elevation boundary
- rule naming/ID mechanics
- platform-specific rollback

## Device control

Separate observation from action.

A platform might be able to:

- enumerate devices but not block them
- observe metadata only with permission
- act only when managed by an enterprise policy framework
- expose no supported API for the requested action

Represent those differences explicitly instead of compressing them into a boolean "supported" field.

## Error normalization

Do not leak raw platform exceptions as the only product contract.

Useful shared classes may include:

- `unsupported`
- `not_implemented`
- `permission_denied`
- `entitlement_missing`
- `target_not_found`
- `conflict_or_stale_state`
- `action_failed`
- `verification_failed`

Preserve raw platform detail as evidence/debug metadata when useful, but keep product decisions based on normalized meaning.

## Contract evolution

A cross-platform abstraction is wrong when multiple real adapters need to lie, leak platform details upward, or implement meaningless methods.

Change the contract when repeated evidence shows the shared semantics are incorrect. Do not broaden it preemptively for hypothetical platforms.
