# Installing a Skill

1. Open the GitHub Release for the skill you want.
2. Download the attached versioned release ZIP, such as `copy-paste-guard-v1.0.0-release.zip`.
3. Review the corresponding source folder in this repository before installation.
4. In ChatGPT, open Skills and upload the ZIP.
5. Confirm the displayed skill name and description match the source you reviewed.

Install one Skill per ZIP. The release ZIP may have a versioned filename even though the validated package was produced as `skill.zip`; renaming the archive does not change its contents.

## Verify a download

Each release should publish a SHA-256 hash. Compare it with the downloaded file before installation when integrity matters.

On Linux or macOS:

```sh
sha256sum <downloaded-release.zip>
```

On Windows PowerShell:

```powershell
Get-FileHash .\<downloaded-release.zip> -Algorithm SHA256
```
