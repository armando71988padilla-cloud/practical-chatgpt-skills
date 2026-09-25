# Security policy

## Reporting a vulnerability

Do not publish sensitive exploit details in a public issue. Open a minimal issue asking for a private contact path, or use GitHub's private vulnerability reporting feature when it is enabled for the repository.

## Trust model

Skills may contain instructions and executable helper scripts. Review source before installation. This repository aims to keep helper code small, readable, non-obfuscated, and narrowly scoped.

A skill must document any meaningful network access, file mutation, command execution, external service dependency, or privileged operation required by its normal workflow.

## Release expectations

Before a release:

- validate the skill structure
- run its public tests
- scan source and packaged output for secrets and unexpected private data
- inspect the final ZIP contents
- compute and publish SHA-256 for the release asset
- install-test the final ZIP in a clean Skill environment when practical
