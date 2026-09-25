# Dependency ecosystem checklist

## JavaScript / npm-compatible projects

Inspect `package.json` plus the lockfile used by the project.

Review:

- `dependencies`, `devDependencies`, `optionalDependencies`, and peer dependencies relevant to distribution
- `preinstall`, `install`, `postinstall`, and `prepare` lifecycle scripts
- `git:`, `git+`, `http:`, `https:`, `file:`, `link:`, `workspace:`, and `npm:` alias selectors
- wildcard, empty, `latest`, or unusually broad selectors where deterministic selection matters
- `overrides`, `resolutions`, and package-manager configuration that changes selected packages
- multiple lockfiles beside the same `package.json`
- native modules or packages that download binaries during install

A lifecycle script is not automatically malicious. Determine what executes, when it executes, and whether that behavior is necessary.

For lockfile review, compare package/source/integrity changes against the manifest change instead of treating line count alone as risk.

## Rust / Cargo

Inspect `Cargo.toml` and `Cargo.lock`.

Review:

- `git`, `path`, and custom `registry` dependencies
- source replacement or alternate registry configuration when present
- wildcard version selectors
- feature changes that enable native, network, filesystem, process, or crypto surfaces relevant to the application
- new crates with `build.rs`, FFI, system-library, or bundled-native implications when relevant
- Tauri plugins added to either Cargo or frontend manifests
- unexpectedly large `Cargo.lock` expansion after a small direct change

A Rust build script executes during build and is part of the trusted build-time code path.

## Python requirements files

Inspect `requirements*.txt` for:

- VCS/direct URL requirements
- local paths or editable `-e` installs
- `--index-url`, `--extra-index-url`, and `--trusted-host`
- fully unpinned application requirements when reproducibility matters
- hashes when the project intentionally uses hash-checked installs

Do not print private index URLs containing credentials.

`--extra-index-url` can create dependency-confusion risk when the same package name may exist on more than one index. Whether that risk is exploitable depends on package names and index behavior; do not overclaim from the directive alone.

## Python `pyproject.toml`

Review:

- PEP 621 `project.dependencies` and optional dependency groups
- direct URL dependencies
- `build-system.requires`, because build backends/dependencies execute in the build path
- Poetry/PDM/uv-specific dependency source configuration when present
- wildcard/unbounded selectors when deterministic application builds matter

A library can intentionally use ranges rather than exact pins. Distinguish library publishing from application deployment before calling a range a defect.

## Mixed Tauri projects

Treat frontend and Cargo dependencies as one supply chain.

For a new Tauri plugin ask:

1. What feature requires it?
2. Which frontend package is added?
3. Which Rust crate is added?
4. Which capabilities or permissions does it require?
5. Does it touch processes, filesystem, HTTP, URLs, updates, SQL, deep links, or sidecars?
6. Is the feature already available through an existing dependency or a narrow Rust command?

Use Tauri-specific boundary review for permission implications; supply-chain review should still account for the extra third-party code and build surface.

## Monorepos

Do not assume one root lockfile governs every nested project. Identify the package manager/workspace model first.

Review:

- workspace declarations
- nested manifests
- lockfile location
- package-manager version hints
- local workspace/path dependencies

A workspace dependency is not inherently unsafe; it changes provenance from a public registry to local repository content and should be treated accordingly.

## External verification

Use fresh upstream or registry evidence when the user asks about:

- vulnerabilities/advisories
- latest or supported versions
- maintainer activity
- package ownership or publication history
- licenses
- signing, attestations, or provenance metadata
- typosquatting or package-name confusion

Static files alone cannot prove those facts.
