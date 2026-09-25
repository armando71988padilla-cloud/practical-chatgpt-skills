# Runtime Target Verifier v1.0.0

First public release candidate.

## Included

- `MATCH`, `MISMATCH`, and `UNPROVEN` runtime verdicts
- `SAFE TO PATCH`, `CONDITIONAL`, and `NOT SAFE TO PATCH` patch-safety states
- explicit separation between claimed and proven live targets
- Linux, macOS, and Windows runtime guidance
- service, process, symlink, wrapper, scheduled-task, container, development-server, and build-output chains
- one smallest read-only next check instead of broad mutation or debugging steps
- no helper scripts, network access, or binary payloads

## Verification completed

- skill structure validation passed
- public source passed declassification scan
- final packaged ZIP passed declassification scan
- secret-like pattern scan passed
- final ZIP contains exactly one `SKILL.md` and four readable files
- no compiled bytecode or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
