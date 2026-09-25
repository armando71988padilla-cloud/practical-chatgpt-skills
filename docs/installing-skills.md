# Installing a Skill

Each release ZIP contains one installable ChatGPT Skill.

## Install

1. Open the repository README and choose the Skill you want.
2. Use its **Release** link to review release notes and SHA-256.
3. Download the versioned ZIP asset from that release.
4. Review the corresponding public source folder if you want to inspect the instructions or helper code.
5. In ChatGPT, open Skills and upload the ZIP.
6. Confirm the displayed Skill name and description match the source you reviewed.

Install one Skill per ZIP.

The public release asset uses a versioned filename such as `copy-paste-guard-v1.0.0-release.zip`. The underlying validated package is still a single Skill archive; renaming the ZIP does not change its contents.

## Verify the download

Compare the downloaded file against the SHA-256 published in the release notes or in [checksums.md](checksums.md).

Linux:

```sh
sha256sum <downloaded-release.zip>
```

macOS:

```sh
shasum -a 256 <downloaded-release.zip>
```

Windows PowerShell:

```powershell
Get-FileHash .\<downloaded-release.zip> -Algorithm SHA256
```

## Before trusting a Skill

- Read `SKILL.md`.
- Review anything in `scripts/`.
- Check whether the Skill documents network access or mutation.
- Prefer the GitHub Release asset linked from this repository over copies hosted elsewhere.
- Treat third-party forks as separate software unless you review their changes.
