# Tauri Security Boundary Auditor public test cases

These are manual trigger and behavior fixtures.

## Case 1: Generic shell bridge

Prompt:

> My Tauri frontend can pass an executable name and argument array to Rust. Audit that boundary.

Expected:

- treats arbitrary command/argument forwarding as a high-impact review area
- distinguishes proven code behavior from scanner warnings
- recommends a narrower named command contract when practical
- requires denial tests for unsupported commands and extra arguments

## Case 2: Broad filesystem write

Prompt:

> My Tauri app only exports one report, but the main window has broad filesystem write access. Is that okay?

Expected:

- reviews the actual capability and path scope
- recommends least privilege rather than assuming broad write is required
- tests traversal/out-of-scope paths where relevant

## Case 3: Remote content

Prompt:

> I load a remote dashboard in a Tauri webview and want it to call native commands.

Expected:

- treats remote content as a separate trust zone
- inspects remote capability/origin configuration and CSP
- does not equate HTTPS with safe native authority

## Case 4: Sidecar

Prompt:

> The app bundles a sidecar and forwards whatever arguments the frontend gives it.

Expected:

- treats the sidecar as part of the trusted computing base
- reviews executable identity and argument constraints
- recommends rejecting unsupported subcommands/arguments

## Case 5: Updater

Prompt:

> Review my Tauri updater config before I ship.

Expected:

- checks endpoints, insecure transport, signing/public-key configuration, and updater permissions
- separates transport security from update artifact authenticity
- defines an invalid/missing-signature failure test
