---
name: dependency-supply-chain-auditor
description: Audit what third-party code a project is choosing to trust and how reproducibly those dependencies are selected. Use when a user asks to review package.json, package-lock.json, Cargo.toml, Cargo.lock, pyproject.toml, requirements files, Poetry/uv/Pipenv locks, a dependency upgrade, a new Tauri plugin, install/build lifecycle scripts, VCS/path/URL dependencies, alternate registries, missing locks, unpinned versions, or unexpected dependency-tree expansion. Keep static findings separate from current vulnerability, maintainer, license, or registry claims that require fresh external evidence.
---

# Dependency Supply-Chain Auditor

## Purpose

Determine what third-party code a project trusts, where it comes from, whether selection is reproducible, and whether a dependency change expands execution or provenance risk. Favor fewer dependencies when existing code or the standard library already satisfies the need.

## Workflow

1. Prove the project or repository root in scope.
2. Identify dependency ecosystems and manifest/lock pairs.
3. When local files are available, run `scripts/dependency_inventory.py <project-root>` for a read-only static inventory.
4. Review direct dependencies, version selectors, source types, lifecycle/build hooks, alternate registries/indexes, native-code surfaces, and lockfile coverage.
5. When a dependency change is under review, compare both manifest and lockfile changes; do not judge only the one edited line.
6. Separate static repository facts from claims requiring current registry, advisory, license, signature, or maintainer evidence.
7. Ask whether each newly added dependency is actually necessary.
8. Recommend the smallest safe action: keep, pin, narrow, remove, replace, split, or gather one missing proof.
9. Define verification without mutating dependencies by default.

Read `references/ecosystem-checklist.md` for ecosystem-specific review details. Read `references/examples.md` when a concrete analysis pattern is useful.

## Scanner use

Use `scripts/dependency_inventory.py` only as a read-only static inventory aid.

The scanner:

- never installs, updates, removes, or resolves dependencies
- never runs package-manager scripts or builds
- never regenerates lockfiles
- never performs network requests
- avoids printing credential-bearing registry/index URLs or dependency URL values
- reports source types, names, line numbers, counts, and lock presence instead

Treat scanner output as evidence about repository files, not as proof that a package is safe, malicious, maintained, abandoned, vulnerable, or license-compatible.

## Evidence labels

### PROVEN

Visible directly in manifests, lockfiles, repository files, or verified local command output.

Examples:

- `postinstall` exists in the root `package.json`
- a Cargo dependency uses `git = ...`
- a requirements file uses `--extra-index-url`
- an application manifest has no recognized lockfile beside it
- a package selector is `*`, `latest`, a VCS source, or a local path

### NEEDS EXTERNAL VERIFICATION

Requires current information outside the repository.

Examples:

- known vulnerabilities or advisories
- package ownership and publication history
- maintainer activity or abandonment
- current latest/supported version
- license text or compatibility
- signatures, attestations, provenance services, or registry metadata

### UNPROVEN

Cannot be determined from available evidence.

Never call a package malicious, compromised, abandoned, vulnerable, or license-incompatible without current evidence supporting that claim.

## High-impact review areas

Prioritize:

- dependency install/build hooks that execute code automatically
- VCS, URL, local path, editable, or custom-registry dependencies
- alternate Python indexes or trusted-host bypasses
- missing lockfiles where reproducible application builds are expected
- multiple competing lockfiles for one JavaScript package root
- lockfile changes unexpectedly large relative to the direct manifest change
- packages that download or execute native binaries during install/build
- FFI/native extensions or Rust `build.rs` implications when relevant
- new Tauri plugins that add native permissions or privileged behavior
- package source changes that bypass the project's normal registry
- wildcard, `latest`, or otherwise non-deterministic selectors where reproducibility matters
- vendored/bundled binaries with unclear provenance
- suspicious package-name substitutions or near-name typos when there is concrete reason to review them

Do not equate a large dependency tree with insecurity by itself.

## Lockfile rules

A lockfile is evidence of selected versions, not a guarantee of safety.

Check:

- whether the application's active package manager has the expected lockfile
- whether more than one JavaScript lockfile is present unexpectedly
- whether lockfile source/provenance changed
- whether direct manifest changes caused a much larger transitive change than expected
- whether lockfiles are intentionally omitted for a library rather than an application

Do not regenerate a lockfile just to inspect it.

## Necessity check

For each newly added direct dependency, ask:

1. What user-visible or engineering requirement needs it?
2. Is equivalent functionality already available in the standard library/platform?
3. Is an existing direct dependency already capable of the job?
4. Does the dependency introduce install scripts, native code, privileged plugins, extra registries, or a materially larger transitive tree?
5. Is a small purpose-built implementation lower risk and maintainable, or would reinventing it create more risk?

Do not recommend removing a dependency merely because it has transitive dependencies.

## Ecosystem support

Support at least:

- npm-compatible projects: `package.json`, `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock`
- Rust/Cargo: `Cargo.toml`, `Cargo.lock`
- Python: `requirements*.txt`, `pyproject.toml`, `uv.lock`, `poetry.lock`, `Pipfile`, `Pipfile.lock`
- mixed Tauri projects using JavaScript/TypeScript plus Cargo
- simple monorepos containing multiple supported manifests

## Current vulnerability and license checks

When the user asks whether a dependency is currently vulnerable, maintained, latest, compromised, or license-compatible, use current authoritative evidence when tools are available.

Prefer sources such as:

- the package's official registry entry
- upstream project/repository/security advisories
- GitHub Security Advisories or OSV where appropriate
- official license files or SPDX metadata

Date the conclusion when freshness matters. Keep static repository findings separate from external facts.

Do not run `npm audit fix`, package upgrades, lock regeneration, or equivalent mutation as an inspection step.

## Secret handling

Dependency configuration can contain private registry credentials, tokens, usernames, signed URLs, or internal hosts.

- do not repeat suspected credentials
- sanitize authenticated URLs before displaying them
- report the file, line, directive/source type, and risk category instead of the value when possible
- do not upload private manifests or lockfiles to public services without explicit user approval

## Output format

Use this structure:

### Supply-chain verdict
`LOW CONCERN`, `REVIEW NEEDED`, or `UNPROVEN`, followed by one short reason.

### Project and ecosystems
State the proven root and detected ecosystems.

### Deterministic inventory
List manifests, recognized lockfiles, package-manager hints, and direct dependency counts when available.

### High-impact findings
List proven executable hooks, special sources, missing/competing locks, native-code surfaces, provenance changes, or major dependency expansion.

### Medium-impact findings
List version-selector, duplication, maintainability, or reproducibility concerns that are not immediate high-impact findings.

### Necessity check
For newly added dependencies, state the proven need or what still must be justified.

### External checks still required
List vulnerability, license, ownership, maintainer, signature, provenance, or registry facts requiring current evidence.

### Smallest safe action
Recommend the minimum next decision or one missing proof.

### Verification
Give read-only checks or tests that prove dependency state and build behavior. Do not mutate lockfiles by default.

## Style

Be precise and evidence-bound. Prefer provenance, reproducibility, and executable-install risk over popularity judgments. Avoid dependency fearmongering and avoid treating every third-party package as inherently unsafe.
