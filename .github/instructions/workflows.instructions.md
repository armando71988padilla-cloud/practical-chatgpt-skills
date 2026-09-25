---
applyTo: ".github/workflows/**,tools/**"
---

# Automation and validation instructions

- Default GitHub Actions permissions to read-only.
- Use write permissions only for a narrowly documented task that a human explicitly approved.
- Do not add automatic release publication, tag creation, branch deletion, force pushes, or repository-setting changes.
- Avoid `pull_request_target` unless its security implications are explicitly reviewed.
- Do not pass untrusted pull-request text directly into a shell.
- Prefer GitHub-maintained actions and a small dependency surface.
- Validation must be deterministic and should not require network access beyond obtaining the runner and declared actions.
- Do not print secrets, tokens, authenticated URLs, or private environment values.
- Keep release-building workflows separate from release-publishing workflows.
- A failing validation check should explain exactly which file or invariant failed.
