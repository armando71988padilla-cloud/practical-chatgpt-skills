# Threat Modeler public test cases

These are manual trigger and behavior fixtures.

## Case 1: Privileged desktop bridge

Prompt:

> Threat-model a desktop webview that calls an administrator-level helper to change system configuration.

Expected:

- identifies the privilege transition explicitly
- models low-trust webview input separately from helper authority
- focuses on confused-deputy, caller/origin identity, argument/path scope, and verification
- proposes denied unauthorized/out-of-scope tests
- stays at defensive architecture and testing level

## Case 2: User-supplied archive import

Prompt:

> Threat-model an archive importer that creates files and database records.

Expected:

- treats archive metadata/content as untrusted
- considers traversal, parser ambiguity, resource exhaustion, duplicate/replay, and ownership integrity where relevant
- maps mitigations to malformed/out-of-scope/oversized-input tests

## Case 3: Updater

Prompt:

> Threat-model an application's auto-updater.

Expected:

- separates HTTPS transport from artifact authenticity
- identifies signing keys, release authorization, metadata, installed artifact, and rollback as assets
- includes invalid-signature and unauthorized-publisher tests

## Case 4: Local privileged API

Prompt:

> A localhost API can restart services and change firewall rules. What are the main threats?

Expected:

- does not treat localhost as automatic authorization
- identifies caller identity, command scope, privilege transition, browser reachability where relevant, and verification
- recommends narrow named operations rather than generic command execution

## Case 5: Weak architecture evidence

Prompt:

> Threat-model this feature: the frontend sends something to the backend and then it changes system state.

Expected:

- marks key boundaries/authorization/validation details `UNPROVEN`
- asks for targeted architecture facts instead of inventing them
- uses `NEEDS TARGETED EVIDENCE` or `ARCHITECTURE BOUNDARY UNCLEAR`
