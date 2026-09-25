# Installing a Skill

1. Open the GitHub Release for the skill you want.
2. Download the attached `skill.zip`.
3. Review the source folder in this repository before installation.
4. In ChatGPT, open Skills and upload the ZIP.
5. Confirm the displayed skill name and description match the source you reviewed.

Install one Skill per ZIP.

## Verify a download

Each release should publish a SHA-256 hash. Compare it with the downloaded file before installation when integrity matters.

On Linux or macOS:

```sh
sha256sum skill.zip
```

On Windows PowerShell:

```powershell
Get-FileHash .\skill.zip -Algorithm SHA256
```
