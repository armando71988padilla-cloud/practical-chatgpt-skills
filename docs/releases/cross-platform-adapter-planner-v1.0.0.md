# Cross-Platform Adapter Planner v1.0.0

First public release candidate.

## Included

- platform-neutral feature decomposition before OS-specific design
- explicit shared-core, adapter-interface, platform-adapter, privileged-helper, and UI ownership boundaries
- capability status model using `FULL`, `PARTIAL`, `COMPANION`, `UNSUPPORTED`, and `UNPROVEN`
- fail-closed handling for denied permissions, missing entitlements, unsupported capabilities, stale targets, and failed verification
- implementation sequencing that preserves one reference adapter and avoids parallel rewrites
- shared contract tests plus platform-specific integration-test guidance
- current-platform evidence rule for changing APIs, entitlements, sandbox restrictions, and managed-device capabilities
- no helper scripts, network access, or binary payloads

## Verification completed

- skill structure validation passed
- public source passed private-identifier and secret-pattern scans
- final packaged ZIP passed the same scans
- final ZIP contains exactly one `SKILL.md` and four readable files
- no initializer placeholders, compiled bytecode, or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
