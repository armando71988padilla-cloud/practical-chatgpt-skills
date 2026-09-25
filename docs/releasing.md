# Releasing a Skill

Releases stay human-approved. Automation may validate and build a candidate, but it does not publish a GitHub Release or create a tag.

## 1. Prepare the source

- Keep the change public and generic.
- Update the Skill source, public tests, and release notes.
- Review helper behavior and permissions.
- Run `python tools/validate_public_skills.py`.

## 2. Build a release candidate

In GitHub:

1. Open **Actions**.
2. Select **Build Release Candidate**.
3. Choose **Run workflow**.
4. Enter the Skill directory name, such as `copy-paste-guard`.
5. Enter the semantic version, such as `v1.0.1`.
6. Download the generated artifact after the workflow succeeds.

The artifact contains:

- the versioned release ZIP
- a `.sha256` file containing the ZIP digest

The workflow has read-only repository permissions and does not publish releases or tags.

## 3. Human review

Before publishing:

- inspect the candidate ZIP
- compare it with the public source
- run any Skill-specific tests
- perform the private-identifier/declassification review outside the public repository
- perform the secret-pattern review
- verify the SHA-256

## 4. Publish manually

Create the GitHub Release only after the candidate passes review.

Use a Skill-specific tag such as:

`skill-name-v1.0.1`

Attach the versioned ZIP and include its SHA-256 in the release notes.

## 5. After publishing

- confirm GitHub shows the expected asset digest
- update `docs/checksums.md`
- update the README if the displayed version changed
- confirm Skill Validation and CodeQL remain healthy

Do not automate release publication until there is a clear reason and a separately reviewed permission model.
