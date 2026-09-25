# Repository instructions

This is a public, source-first repository of installable ChatGPT Skills.

- Treat every file in this repository as public.
- Never introduce private or internal project names, usernames, hostnames, ports, paths, logs, screenshots, credentials, tokens, machine identifiers, or infrastructure details from outside this repository.
- Use generic or fictional examples.
- Keep each Skill in its own directory under `skills/<skill-name>/`.
- The `name` in a Skill's `SKILL.md` frontmatter must match its directory name.
- Prefer small, readable Skills that solve one distinct repeatable problem.
- Do not duplicate an existing Skill's responsibility.
- Keep helper scripts readable and non-obfuscated.
- Helper scripts should be local and read-only by default. Any network access, mutation, or elevated privilege must be essential to the Skill's documented purpose and called out prominently.
- Never embed secrets or credential-bearing URLs in source, fixtures, examples, tests, workflows, or documentation.
- Keep proven evidence separate from assumptions, heuristics, and current external facts.
- Do not fabricate release hashes, tags, test results, advisory status, package ownership, platform capabilities, or other facts that require evidence.
- Do not publish releases, create tags, change repository security settings, or weaken branch protections unless a human explicitly requests that exact action.
- Before proposing a merge, run or review `python tools/validate_public_skills.py`.
- Preserve the MIT license and public security/transparency model.
- Prefer minimal safe changes over broad rewrites.
