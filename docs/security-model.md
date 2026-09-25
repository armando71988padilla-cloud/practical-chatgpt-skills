# Security model

The project treats Skills as code-adjacent artifacts, not harmless prompt snippets.

## Defaults

- source visible before install
- no obfuscated helper code
- no hidden binary payloads intentionally bundled
- no helper network access unless the Skill explicitly requires and documents it
- no helper mutation unless the Skill explicitly requires and documents it
- least privilege when commands, connectors, native bridges, or elevated operations are involved
- generic or fictional examples instead of copied real infrastructure
- proven evidence kept separate from assumptions and heuristic warnings

## Clean-room public release boundary

Public Skills are maintained as public editions, not as direct exports of private project repositories.

Public release material must not depend on private repository history, private logs, screenshots, machine names, usernames, internal paths, internal ports, service identifiers, secrets, operational evidence, or private architecture assumptions.

Before release, source and packaged output are checked independently because packaging mistakes can differ from source-tree mistakes.

## Release gate

A normal release is expected to pass:

```text
public source
    ↓
Skill validation
    ↓
helper tests when a helper exists
    ↓
private-identifier / declassification scan
    ↓
secret-pattern scan
    ↓
final ZIP inspection
    ↓
SHA-256 publication
```

## Helper-script policy

Current bundled helper scripts are intended to be read-only and local:

- Copy Paste Guard: scans command text; does not execute it.
- Git State Guardian: reports local Git/repository state; does not fetch or mutate.
- Tauri Security Boundary Auditor: statically inventories project files; does not build or run the app.
- Dependency Supply-Chain Auditor: inventories manifests/locks; does not install, resolve, update, or contact registries.

Future helpers that need network access, mutation, or elevated privilege should document that requirement prominently in both source and release notes.

## Evidence discipline

Static inspection can prove what a repository file contains. It cannot by itself prove current external facts such as vulnerability status, package ownership, platform policy, maintainer activity, or remote service state.

When freshness matters, current authoritative evidence should be used and kept separate from local static findings.
