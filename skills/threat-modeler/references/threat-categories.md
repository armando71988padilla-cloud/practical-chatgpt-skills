# Threat categories

Use these categories as prompts for analysis. Do not mechanically include every category in the final answer.

## Identity and authenticity

Ask:

- Can one component impersonate another?
- Can requests be attributed to the wrong operator, process, device, origin, tenant, or account?
- Can stale or replayed identity evidence be accepted outside its intended scope?
- Are service-to-service identities distinguished from end-user identities?

## Input and integrity

Ask:

- Can untrusted input alter a path, identifier, command, query, policy, object reference, or evidence artifact?
- Can a caller choose a target outside its intended scope?
- Can path traversal, object confusion, parser ambiguity, or inconsistent normalization cross a boundary?
- Can a low-privilege caller influence a high-privilege decision?

## Confidentiality

Ask:

- Can logs, diagnostics, errors, exports, caches, plugins, or UI state expose more data than intended?
- Can one origin, tenant, user, plugin, or process read another's data?
- Can secrets leak through command lines, URLs, filenames, environment variables, or support bundles?

## Authorization and confused deputy

Ask:

- Can an authenticated caller request an action it is not authorized to perform?
- Can a low-privilege component persuade a privileged component to act outside the caller's authority?
- Are high-privilege operations narrow, named, validated, and auditable?
- Does the privileged component re-check authority, or trust the caller's claim?

## Availability and fail-safe behavior

Ask:

- What happens when a dependency, adapter, service, device, parser, sidecar, or API is missing or malformed?
- Does the system fail closed, fail open, loop, deadlock, retry forever, or silently report success?
- Can a single malformed input exhaust CPU, memory, disk, threads, handles, or queues?
- Can emergency recovery be blocked by the same failing component?

## Evidence and audit integrity

Ask:

- Can logs, status files, verification output, action ledgers, or cached state be tampered with before being trusted?
- Can stale evidence be mistaken for live state?
- Can verification accidentally check a different target than the one modified?
- Is audit data sufficiently attributable and ordered to reconstruct important actions?

## Supply chain and updates

Ask:

- Can an unexpected dependency, plugin, build hook, sidecar, installer, or update source introduce trusted code?
- Is artifact authenticity proven separately from transport encryption?
- Can a compromised build/release account replace trusted code?
- Are rollback artifacts protected from the same compromised channel?

## Recovery and rollback

Ask:

- Can backup or rollback data be poisoned, stale, incomplete, or point to the wrong target?
- Can the system get stuck halfway between old and new states?
- Can the component being recovered rewrite the recovery evidence?
- Is restoration independently verified?

## Cross-tenant or cross-boundary isolation

Ask:

- Can one user, tenant, plugin, container, workspace, or project influence another?
- Are identifiers globally unique or merely locally unique?
- Can shared caches, queues, temporary directories, or storage create cross-boundary leakage?

## Business-logic abuse

Ask:

- Can legitimate operations be sequenced, repeated, replayed, or combined to bypass an intended rule?
- Can rate, amount, state-transition, approval, or workflow invariants be violated without technically breaking authentication?
- Are idempotency and replay rules explicit where actions have side effects?
