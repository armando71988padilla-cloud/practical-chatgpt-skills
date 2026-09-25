# Cross-Platform Adapter Planner examples

## Removable storage control

Request:

> I want one feature that detects removable drives and blocks unsafe ones on Windows, Linux, macOS, Android, and iOS.

Good behavior:

- define the core feature as observe removable-storage identity, evaluate policy, request a bounded containment action, and verify outcome
- separate enumeration from block/eject/quarantine mechanics
- mark mobile capabilities `UNPROVEN`, `PARTIAL`, `COMPANION`, or `UNSUPPORTED` unless current platform evidence proves ordinary-app control
- keep OS APIs and shell commands inside adapters/helpers
- preserve a shared evidence and policy model even when action capability differs

## Firewall posture

Request:

> How should I support firewall status and rule changes cross-platform?

Good behavior:

- put normalized posture/rule intent in the shared core
- keep Windows/Linux/macOS firewall APIs in platform adapters or privileged helpers
- expose named rule operations rather than arbitrary command execution
- separate observe-only capability from mutate capability in the matrix
- test permission denied and post-change verification separately

## Background service health

Request:

> I want a shared service health feature for desktop and mobile.

Good behavior:

- avoid making `systemd`, Windows Services, or `launchd` part of the shared contract
- define `component_health()` semantics instead
- model mobile background execution separately if the concept does not map cleanly
- do not pretend a mobile app has a desktop daemon when it does not

## Cross-platform file export

Request:

> I need one save/export workflow on Windows, macOS, Linux, Android, and iOS.

Good behavior:

- keep the shared operation as "request user-approved destination and write export artifact"
- keep picker/storage-provider/sandbox mechanics in each adapter/UI boundary
- represent denied or unavailable destination access explicitly
- avoid hard-coded paths in the shared core

## Managed mobile device feature

Request:

> This capability works on enterprise-managed Android but not ordinary Android apps. How should I model it?

Good behavior:

- distinguish deployment modes in the capability matrix
- avoid marking all Android support `FULL`
- keep the ordinary-app path `PARTIAL`, `COMPANION`, `UNSUPPORTED`, or `UNPROVEN` as appropriate
- allow a managed-device adapter variant if the product genuinely supports that deployment mode
