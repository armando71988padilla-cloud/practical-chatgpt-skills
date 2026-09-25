# Rollback Preparer v1.0.0

First public release candidate.

## Included

- rollback readiness classification: `READY`, `PARTIAL`, or `STOP`
- live-target proof before backup or restore commands
- paired backup/checkpoint and restore steps
- restore verification focused on active state, not just copy success
- Linux, macOS, and Windows guidance
- explicit handling for files, services, packages, Git repositories, databases, deployments, and operating-system changes
- no helper scripts or network access

## Verification completed

- skill structure validation passed
- public source passed declassification scan
- final packaged ZIP passed declassification scan
- final ZIP contains exactly one `SKILL.md`
- no compiled bytecode or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
