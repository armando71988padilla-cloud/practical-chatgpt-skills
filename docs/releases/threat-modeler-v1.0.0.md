# Threat Modeler v1.0.0

First public release candidate.

## Included

- asset and security-objective identification
- explicit trust-zone and privilege-transition modeling
- realistic attacker-position selection instead of universal worst-case assumptions
- specific abuse-story threats rather than generic category dumps
- `PROVEN`, `SUSPECTED`, and `UNPROVEN` evidence labels
- qualitative `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW` impact prioritization without false numeric precision
- mitigation-to-verification mapping
- trust-boundary guidance for UI/native IPC, APIs, privileged helpers, containers/VMs, databases, dependencies, updates, files/devices, and evidence stores
- defensive architectural analysis without unnecessary operational detail
- no helper scripts, network access, or binary payloads

## Verification completed

- skill structure validation passed
- public source passed private-identifier and secret-pattern scans
- final packaged ZIP passed the same scans
- final ZIP contains exactly one `SKILL.md` and five readable files
- no initializer placeholders, compiled bytecode, or hidden binary payloads are included

A clean ChatGPT install test remains recommended before broad promotion.
