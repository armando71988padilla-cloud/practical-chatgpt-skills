---
applyTo: "skills/**"
---

# Skill source instructions

- Keep one installable Skill per `skills/<name>/` directory.
- Require exactly one root `SKILL.md` for each Skill.
- Keep `SKILL.md` frontmatter limited to the required public metadata and ensure `name` matches the directory.
- Keep references focused; do not turn a Skill into a documentation dump.
- Add a helper script only when deterministic code materially improves the workflow.
- Helper scripts must not execute user-provided commands merely to inspect them.
- Do not add network calls, package installation, mutation, or privilege elevation to a helper unless the Skill's public purpose explicitly requires it and the behavior is documented.
- Do not echo suspected secret values.
- Use generic examples and fixtures.
- Never copy internal/private logs, paths, hostnames, ports, screenshots, identifiers, or architecture assumptions into public Skill source.
- Add or update corresponding public tests under `tests/` and release documentation under `docs/releases/` when behavior changes.
