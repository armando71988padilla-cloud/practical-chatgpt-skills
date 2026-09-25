# Security model

The project treats Skills as code-adjacent artifacts, not harmless prompt snippets.

## Defaults

- source visible before install
- no obfuscated helper code
- no hidden binary payloads
- no network access unless the skill's purpose requires it
- no mutation unless the skill's purpose requires it
- least privilege when commands or connectors are involved
- fictional examples rather than copied real infrastructure

## Release boundary

Public release material must originate from the public workspace. Private project repositories, histories, logs, screenshots, hostnames, paths, service names, identifiers, and operational evidence are not release inputs.

The final packaged ZIP is scanned again after packaging because packaging mistakes can differ from source-tree mistakes.
