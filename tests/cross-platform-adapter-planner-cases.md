# Cross-Platform Adapter Planner public test cases

These are manual trigger and behavior fixtures.

## Case 1: Removable storage

Prompt:

> Design one removable-drive quarantine feature for Windows, Linux, macOS, Android, and iOS.

Expected:

- defines the shared feature without OS API names
- separates observation, policy, action, and verification
- does not invent mobile parity
- uses `UNPROVEN` until current platform capability is verified
- keeps privileged mechanics out of the shared core

## Case 2: Firewall control

Prompt:

> Where should firewall policy and OS-specific firewall commands live in a cross-platform app?

Expected:

- keeps desired policy/state shared
- places API/command/elevation mechanics in adapters/helpers
- prefers named helper operations over arbitrary shell execution
- includes permission-denied and post-action verification tests

## Case 3: Service health

Prompt:

> I need one service-health abstraction across Windows, Linux, macOS, Android, and iOS.

Expected:

- avoids putting systemd, launchd, or Windows service APIs in the shared contract
- defines semantic health/status records
- allows unsupported/partial mobile mappings instead of fake daemons

## Case 4: Managed mobile capability

Prompt:

> A feature works only under enterprise device management on one mobile platform. How should the adapter model it?

Expected:

- distinguishes ordinary-app and managed-device deployment modes
- does not label the whole platform `FULL`
- captures entitlement/management boundary and release restrictions explicitly

## Case 5: Adapter contract smell

Prompt:

> My shared interface has `run_command(command, args)` so every OS can implement it. Is that a good adapter?

Expected:

- rejects generic command execution as a product-level semantic contract
- proposes narrow named operations
- keeps raw command mechanics inside platform-specific code
