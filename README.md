# Practical ChatGPT Skills

[![Skill Validation](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/actions/workflows/skill-validation.yml/badge.svg)](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/actions/workflows/skill-validation.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Public Skills](https://img.shields.io/badge/public%20skills-10-6f42c1.svg)](#skill-catalog)
[![Security](https://img.shields.io/badge/security-private%20reporting-enabled-brightgreen.svg)](SECURITY.md)

A small collection of free, open-source ChatGPT Skills for safer development, debugging, Git, architecture, and system administration.

The goal is simple: solve repeatable technical problems with clear workflows, conservative defaults, readable source, and no hidden behavior.

## Quick start

1. Pick a Skill below.
2. Open its release page or use the direct ZIP link.
3. Review the public source if you want to inspect exactly what it does.
4. Upload the ZIP in ChatGPT Skills.
5. Use the Skill normally in chat.

Each release publishes a SHA-256 so you can verify the downloaded archive.

See [Installing Skills](docs/installing-skills.md) and [Release checksums](docs/checksums.md).

## GitHub automation

This repository now includes a small, human-controlled automation layer:

- **Skill Validation** runs automatically on pushes and pull requests and checks Skill structure, Python helper syntax, release/test presence, and accidental compiled artifacts.
- **Build Release Candidate** is a manual GitHub Action that builds one versioned Skill ZIP plus its SHA-256 file. It cannot publish a release or create a tag.
- **Skill Release Steward** is a repository custom agent for preparing release-ready changes and PRs.
- **Skill Security Reviewer** is a read-only custom agent for reviewing privacy leaks, helper behavior, workflow permissions, and evidence quality.
- Structured **Bug report** and **New Skill idea** forms keep Issues useful.
- **CODEOWNERS** requests maintainer review on repository changes.
- Pull requests get a public-data, validation, and helper-behavior checklist automatically.

See [Releasing a Skill](docs/releasing.md) for the human-approved release flow.

## Skill catalog

### Safety and change control

| Skill | What it helps with | Source | Release | Download |
| --- | --- | --- | --- | --- |
| **Copy Paste Guard** | Reviews terminal commands before execution and rewrites risky command blocks into safer steps. | [Source](skills/copy-paste-guard) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/copy-paste-guard-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/copy-paste-guard-v1.0.0/copy-paste-guard-v1.0.0-release.zip) |
| **Rollback Preparer** | Builds a proven backup and restore path before risky changes. | [Source](skills/rollback-preparer) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/rollback-preparer-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/rollback-preparer-v1.0.0/rollback-preparer-v1.0.0-release.zip) |

### Debugging and troubleshooting

| Skill | What it helps with | Source | Release | Download |
| --- | --- | --- | --- | --- |
| **Runtime Target Verifier** | Proves which file, binary, service, container, or runtime target is actually live before patching. | [Source](skills/runtime-target-verifier) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/runtime-target-verifier-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/runtime-target-verifier-v1.0.0/runtime-target-verifier-v1.0.0-release.zip) |
| **Log Slice Analyzer** | Separates failure-relevant log signal from warning noise and identifies the smallest useful next checks. | [Source](skills/log-slice-analyzer) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/log-slice-analyzer-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/log-slice-analyzer-v1.0.0/log-slice-analyzer-v1.0.0-release.zip) |
| **Issue Isolator** | Reduces messy multi-symptom bugs to one testable boundary and one useful next check. | [Source](skills/issue-isolator) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/issue-isolator-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/issue-isolator-v1.0.0/issue-isolator-v1.0.0-release.zip) |

### Git and repository safety

| Skill | What it helps with | Source | Release | Download |
| --- | --- | --- | --- | --- |
| **Git State Guardian** | Checks repository identity, staging scope, worktree state, upstream alignment, and risky files before Git operations. | [Source](skills/git-state-guardian) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/git-state-guardian-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/git-state-guardian-v1.0.0/git-state-guardian-v1.0.0-release.zip) |

### Architecture and security

| Skill | What it helps with | Source | Release | Download |
| --- | --- | --- | --- | --- |
| **Tauri Security Boundary Auditor** | Audits Tauri v2 capabilities, permissions, IPC, plugins, sidecars, CSP, remote content, and updater trust. | [Source](skills/tauri-security-boundary-auditor) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/tauri-security-boundary-auditor-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/tauri-security-boundary-auditor-v1.0.0/tauri-security-boundary-auditor-v1.0.0-release.zip) |
| **Dependency Supply-Chain Auditor** | Reviews dependency provenance, lockfiles, executable install hooks, alternate indexes, VCS/path sources, and reproducibility. | [Source](skills/dependency-supply-chain-auditor) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/dependency-supply-chain-auditor-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/dependency-supply-chain-auditor-v1.0.0/dependency-supply-chain-auditor-v1.0.0-release.zip) |
| **Cross-Platform Adapter Planner** | Separates shared product behavior from platform-specific adapters, privileges, and capability limits. | [Source](skills/cross-platform-adapter-planner) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/cross-platform-adapter-planner-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/cross-platform-adapter-planner-v1.0.0/cross-platform-adapter-planner-v1.0.0-release.zip) |
| **Threat Modeler** | Maps assets, trust boundaries, realistic abuse paths, mitigations, and security verification tests. | [Source](skills/threat-modeler) | [v1.0.0](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/tag/threat-modeler-v1.0.0) | [ZIP](https://github.com/armando71988padilla-cloud/practical-chatgpt-skills/releases/download/threat-modeler-v1.0.0/threat-modeler-v1.0.0-release.zip) |

## Which one should I use?

| Situation | Start here |
| --- | --- |
| "Is this terminal command safe to paste?" | **Copy Paste Guard** |
| "How do I undo this before I change it?" | **Rollback Preparer** |
| "Am I editing the code that is actually running?" | **Runtime Target Verifier** |
| "Which lines in these logs actually matter?" | **Log Slice Analyzer** |
| "Five things look broken; where do I start?" | **Issue Isolator** |
| "Is this repo safe to commit/reset/clean/push?" | **Git State Guardian** |
| "Is my Tauri native boundary too broad?" | **Tauri Security Boundary Auditor** |
| "What third-party code am I trusting here?" | **Dependency Supply-Chain Auditor** |
| "What belongs in shared core versus OS adapters?" | **Cross-Platform Adapter Planner** |
| "How could this design be abused across trust boundaries?" | **Threat Modeler** |

## Trust at a glance

The project is intentionally source-first and boring in the good way.

| Skill | Bundled helper | Helper network access | Helper mutates project/system state |
| --- | --- | --- | --- |
| Copy Paste Guard | Read-only command-text scanner | No | No |
| Rollback Preparer | None | — | — |
| Runtime Target Verifier | None | — | — |
| Log Slice Analyzer | None | — | — |
| Issue Isolator | None | — | — |
| Git State Guardian | Read-only Git/state reporter | No | No |
| Tauri Security Boundary Auditor | Read-only static scanner | No | No |
| Dependency Supply-Chain Auditor | Read-only manifest/lock inventory | No | No |
| Cross-Platform Adapter Planner | None | — | — |
| Threat Modeler | None | — | — |

A Skill may recommend commands or actions for the user to review when that is its purpose. The table above describes only bundled helper behavior.

## Release and security model

Every public release is intended to pass this gate:

```text
public source
    ↓
skill validation
    ↓
helper tests (when a helper exists)
    ↓
private-identifier / declassification scan
    ↓
secret-pattern scan
    ↓
package inspection
    ↓
SHA-256 published with release
```

Project rules:

- Source is visible before installation.
- Helper code is readable and non-obfuscated.
- No hidden binary payloads are intentionally bundled.
- Helper scripts are read-only unless a future Skill explicitly documents otherwise.
- Network access is avoided unless a Skill genuinely requires it and documents why.
- Public examples use generic or fictional infrastructure rather than private project data.
- Security findings distinguish proven evidence from assumptions or heuristic warnings.

See [SECURITY.md](SECURITY.md) and [Security model](docs/security-model.md).

## Repository layout

```text
skills/      public Skill source
docs/        installation, security, release, and supporting documentation
tests/       public manual test fixtures
```

GitHub Releases are the preferred distribution surface for installable ZIPs.

## Contributing

Contributions are welcome when they add a distinct, reusable workflow instead of duplicating an existing Skill.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).
