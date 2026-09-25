# Practical ChatGPT Skills

Free, open-source ChatGPT Skills for safer development, debugging, Git, and system administration workflows.

## Available skills

| Skill | Purpose | Status |
| --- | --- | --- |
| Copy Paste Guard | Review terminal commands before execution and rewrite risky blocks into safer steps | v1.0.0 |
| Rollback Preparer | Build a proven backup and restore path before risky changes | v1.0.0 |
| Runtime Target Verifier | Prove which file, binary, service, or runtime target is actually live before patching | v1.0.0 release candidate |

More skills will be added only when they solve a distinct, repeatable problem.

## Install a skill

1. Open the skill's latest GitHub Release.
2. Download the versioned release ZIP asset.
3. In ChatGPT, open Skills and upload the ZIP.
4. Review the included `SKILL.md`, scripts, and references before using it.

See `docs/installing-skills.md` for details.

## Security and trust

This project follows a source-first model:

- source is visible before installation
- helper scripts are readable and non-obfuscated
- skills should avoid network access unless their purpose explicitly requires it
- skills should avoid mutation unless their purpose explicitly requires it
- release artifacts are built from the corresponding public source tree
- SHA-256 hashes are published with release artifacts

See `SECURITY.md` and `docs/security-model.md`.

## Repository layout

```text
skills/      installable skill source
docs/        user and security documentation
tests/       public test fixtures and release checks
dist/        local release artifacts; GitHub Releases are the preferred distribution surface
```

## License

MIT. See `LICENSE`.
