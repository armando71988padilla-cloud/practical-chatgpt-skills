# Dependency Supply-Chain Auditor v1.0.0

First public release candidate.

## Included

- read-only inventory for JavaScript/npm-compatible, Cargo/Rust, and Python dependency manifests
- mixed-project and simple monorepo discovery
- lifecycle-script, VCS/URL/path/workspace, alternate-index, custom-registry, wildcard/latest, and lockfile review signals
- secret-safe output that avoids printing credential-bearing dependency/index URLs
- separation between static repository facts and current vulnerability, maintainer, ownership, license, signature, and registry claims
- explicit dependency-necessity review before adding more third-party code
- no package-manager execution, dependency installation/update/removal, lockfile regeneration, project execution, build execution, or network access

## Verification completed

- skill structure validation passed
- risky mixed fixture detected npm lifecycle/source risks, Cargo VCS/path/wildcard risks, and Python alternate-index/direct-source/unpinned risks
- narrow fixture produced zero special-risk entries
- synthetic private-index password was not echoed by the scanner
- public source passed private-identifier and secret-pattern scans
- final packaged ZIP contains exactly one `SKILL.md` and five readable files
- no compiled bytecode or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
