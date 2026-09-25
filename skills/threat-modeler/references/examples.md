# Threat Modeler examples

## Desktop webview to privileged helper

Request:

> Threat-model a desktop app where a webview can ask a native helper to write configuration files with administrator privileges.

Good behavior:

- identify configuration integrity and privilege boundary as primary assets/concerns
- model the webview as lower trust than the helper
- identify arbitrary path selection, confused-deputy, origin/caller identity, and stale verification threats
- recommend narrow named operations and scoped paths instead of generic file writes
- include denied out-of-scope path tests and unauthorized-caller tests

## File import parser

Request:

> We import user-supplied archive files and create records from them. What should we threat-model?

Good behavior:

- model archive content and metadata as untrusted
- include path traversal, parser ambiguity, resource exhaustion, duplicate/replay, and record-ownership integrity where relevant
- stay at defensive design and test level
- define tests with malformed archives, oversized inputs, duplicate identifiers, and out-of-scope paths

## Update mechanism

Request:

> Threat-model our auto-updater.

Good behavior:

- separate transport security from artifact authenticity
- identify update signing keys, publish authorization, update metadata, rollback artifacts, and installed binaries as assets
- include compromised release account/channel and stale/downgrade cases
- require invalid-signature and unauthorized-publisher failure tests

## Local API with privileged actions

Request:

> A local HTTP API can restart services and edit firewall rules. Model the risks.

Good behavior:

- identify who can reach the local API and what identity/authentication exists
- model localhost/loopback as network reachability, not automatic authorization
- focus on confused-deputy, browser-to-localhost reachability where relevant, command scope, and privilege transition
- recommend named operations, caller checks, strict input validation, and direct post-action verification

## Evidence-driven security decision

Request:

> The app decides whether a device is trusted based on cached JSON from the last scan.

Good behavior:

- treat cached evidence integrity and freshness as assets
- include stale/tampered evidence and target-identity mismatch threats
- recommend freshness/identity binding and live revalidation for high-impact decisions
- include stale-evidence and wrong-target verification tests
