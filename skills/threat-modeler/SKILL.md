---
name: threat-modeler
description: Build a defensive threat model for an application, service, device workflow, plugin, update path, privileged helper, local IPC/API, data pipeline, or cross-platform feature. Use when a user asks what could go wrong under hostile, compromised, malformed, or stale input; wants assets, trust boundaries, attacker positions, privilege transitions, abuse paths, mitigations, or security verification tests; or needs to review a design before implementation. Keep claims evidence-bound, prioritize realistic boundary-crossing threats, and do not provide exploit payloads or harmful operational instructions.
---

# Threat Modeler

## Purpose

Evaluate how a concrete design could fail under hostile, compromised, malformed, or stale input. Focus on assets, trust boundaries, privilege transitions, realistic abuse paths, and testable mitigations rather than generic security checklists.

## Workflow

1. Define the exact system, feature, and deployment boundary in scope.
2. Identify assets and security objectives: confidentiality, integrity, availability, authenticity, authorization, auditability, and recoverability as relevant.
3. Identify trust zones and privilege boundaries.
4. Draw the important data and control flow in concise text.
5. Identify realistic attacker positions that can actually reach the design.
6. Enumerate threats using `references/threat-categories.md` as prompts, not as a checklist to dump into the answer.
7. Prioritize by practical impact, reachability, and boundary crossed.
8. Map every important threat to a concrete mitigation.
9. Map every mitigation to a direct verification test, denied-case test, or evidence requirement.
10. State residual risk, intentionally trusted components, and assumptions that remain unproven.

Read `references/trust-boundary-guide.md` when the design includes IPC, webviews, privileged helpers, plugins, sidecars, update channels, external files/devices, or local/remote service boundaries. Read `references/examples.md` when a concrete modeling pattern is useful.

## Scope discipline

Threat-model one defined boundary at a time unless multiple components must be modeled together to preserve the security story.

State what is explicitly out of scope. Do not silently assume:

- root/administrator compromise
- physical access
- supply-chain compromise
- remote code execution
- malicious insiders
- compromised cloud control plane

unless the user asks for those positions or the architecture makes them relevant.

Do not assume every theoretical attacker simultaneously. That produces noise instead of useful design decisions.

## Assets and objectives

Identify only assets relevant to the feature. Examples include:

- credentials, tokens, keys, and secrets
- user data or regulated data
- local files or databases
- device identity and authorization state
- configuration and policy
- code, plugins, sidecars, and update artifacts
- security evidence, logs, and audit trails
- rollback material and recovery metadata
- availability of a critical service or workflow
- integrity of commands sent across a privileged boundary

For each asset, state the property that matters. A log may be public enough for confidentiality but critical for integrity; a recovery artifact may be less sensitive than it is important to remain trustworthy.

## Trust boundaries

Treat any transition where authority, origin, validation rules, or trust level changes as a candidate boundary.

Common examples:

- browser/webview -> native code
- user process -> privileged helper
- client -> API/service
- application -> database or queue
- host -> container/VM
- core logic -> platform adapter
- local application -> remote service
- package manager -> third-party dependency
- application -> updater/release channel
- external file/device -> parser/core logic
- stored evidence -> later security decision

Every privilege increase deserves an explicit authorization, validation, audit, and verification story.

## Attacker positions

Choose only positions that can plausibly reach the scoped feature.

Useful positions include:

- malicious or compromised frontend content
- unprivileged local process
- compromised user account
- malicious file or removable device
- malicious network peer on an allowed path
- compromised dependency, plugin, or sidecar
- compromised update/release source
- compromised platform adapter or privileged helper
- stale or tampered local evidence
- authenticated but over-privileged user

State the attacker's starting authority before describing the abuse path.

## Threat statement format

Write threats as specific abuse stories, not category labels.

Prefer:

> A low-privilege webview can choose an arbitrary filesystem path passed to a privileged native command, allowing it to write outside the intended application directory.

Avoid:

> Tampering threat.

A useful threat identifies:

- attacker position
- entry point
- trust/privilege boundary crossed
- security objective affected
- concrete consequence

## Evidence labels

### PROVEN

Directly supported by architecture, code, configuration, runtime evidence, or user-provided facts.

### SUSPECTED

A plausible abuse path that fits the design but still needs one concrete fact.

### UNPROVEN

Cannot be evaluated because a relevant boundary, validation rule, permission, identity mechanism, or data flow is missing.

Do not present a scanner warning, framework reputation, or generic category as proof of a vulnerability.

## Prioritization

Use qualitative impact only.

### CRITICAL

A reachable path can cross a strong privilege/trust boundary and directly defeat a core security objective or take durable control of a high-value asset.

### HIGH

Meaningful compromise, privilege misuse, durable integrity loss, sensitive disclosure, or broad availability impact is realistic.

### MEDIUM

Narrower compromise, denial, abuse opportunity, or important hardening gap with limited reach.

### LOW

Limited impact, difficult reachability, or defense-in-depth concern.

Do not invent numeric scores or false precision. If reachability or impact is unproven, say so.

## Mitigation rules

Prefer mitigations that reduce whole classes of abuse rather than one symptom.

Strong patterns include:

- narrow named operations instead of generic command bridges
- typed and allowlisted arguments
- scoped paths/origins/hosts/identifiers
- least privilege and per-component capabilities
- explicit authorization at privilege transitions
- independent post-action verification
- signed/authenticated update artifacts
- separation of observation, decision, and action
- immutable or integrity-protected evidence where evidence drives decisions
- fail-closed behavior on malformed, stale, or ambiguous input
- rollback paths that cannot be rewritten by the same component being recovered

Do not call a mitigation complete unless a verification method exists.

## Verification rules

For each high-value mitigation include at least one of:

- denied-input test
- out-of-scope path/origin/identifier test
- unauthorized-caller test
- malformed-message test
- stale-evidence test
- missing-dependency/helper test
- invalid-signature/provenance test
- permission-denied test
- rollback/restore verification
- direct state/effect verification after a privileged action

Prefer tests that prove the boundary rejects what it must reject, not only that the happy path works.

## Safe analysis boundary

Keep analysis defensive and architectural.

Describe abuse paths only to the level necessary to improve design, policy, and tests. Do not provide:

- exploit payloads
- credential theft procedures
- persistence instructions
- evasion instructions
- destructive third-party targeting steps
- weaponized malware behavior

When more detail would materially increase offensive capability, stay at the boundary/mitigation/testing level.

## Current external assumptions

When the model depends on changing facts such as platform entitlements, protocol behavior, framework security controls, package ownership, advisory status, or update-signing requirements, use current authoritative evidence when tools are available.

Keep current external facts separate from architecture facts already proven in the user's design.

## Output format

Use this structure:

### Scope
State exact feature, components, deployment context, and explicit exclusions.

### Assets and security objectives
List only relevant assets and the properties that must be protected.

### Trust boundaries
List the meaningful trust or privilege transitions.

### Data and control flow
Use a concise text flow such as `UI -> IPC -> core -> privileged helper -> OS`.

### Attacker positions
List only realistic starting positions for this scope.

### Threats
Use a table with columns: threat, attacker position, boundary crossed, impact, evidence status, mitigation.

### Highest-value design changes
List only the few mitigations that reduce the most meaningful risk.

### Verification tests
Map each high-value mitigation to a direct test or evidence check.

### Residual risk
State intentionally trusted components, transferred risk, accepted limitations, and unproven assumptions.

### Threat-model status
Use one of: `SUFFICIENT FOR CURRENT DESIGN`, `NEEDS TARGETED EVIDENCE`, or `ARCHITECTURE BOUNDARY UNCLEAR`.

## Style

Be concrete, evidence-bound, and calm. Prioritize a few realistic boundary-crossing threats over a long catalog of theoretical possibilities. Do not sensationalize risk.
