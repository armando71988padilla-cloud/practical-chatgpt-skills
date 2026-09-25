---
name: log-slice-analyzer
description: Analyze a focused slice of application, service, system, container, or event logs and separate symptom-relevant signal from background noise. Use when a user pastes journalctl output, Windows Event Log text, macOS unified logs, Docker or Kubernetes logs, application logs, traceback fragments, crash loops, request failures, or timestamped diagnostics and asks what matters, what is proven, what is merely suspected, or what to check next. Keep conclusions evidence-bound, identify the smallest likely failing component, and prefer 1 to 3 targeted next checks over broad troubleshooting.
---

# Log Slice Analyzer

## Purpose

Extract the smallest useful explanation from a focused log slice without treating every warning as causal or turning partial evidence into certainty.

## Workflow

1. Anchor on the user's reported symptom and approximate failure time.
2. Identify the log source, component, time range, and any correlation/request/process identifiers shown.
3. Separate lines into symptom-aligned signal, likely consequence/cascade, and background noise.
4. Prefer the earliest meaningful error in the failure chain over repeated downstream errors.
5. Identify one primary suspect component or layer when the evidence supports it.
6. State what is directly proven, what is suspected, and what evidence is still missing.
7. Give only 1 to 3 targeted next checks that can confirm or reject the main hypothesis.
8. Avoid edits, restarts, cleanup, or destructive actions unless the cause is already proven and the user explicitly asks for remediation.

Read `references/signal-model.md` when the slice contains repeated errors, multiple components, crash loops, distributed traces, or ambiguous chronology. Read `references/examples.md` when a concrete analysis pattern is useful.

## Slice quality

Classify the evidence as one of:

### STRONG

The slice contains the failure moment, relevant context immediately before it, and enough identifying information to connect the error to the reported symptom.

### USABLE

The slice contains meaningful failure evidence but is missing some context, timing, or target identity.

### WEAK

The slice is too partial, too old, too broad, or too disconnected from the symptom to support a reliable cause hypothesis.

Do not present a high-confidence cause from a `WEAK` slice.

## Signal rules

Prioritize lines that directly indicate:

- process termination, panic, fatal exception, uncaught traceback, or crash
- bind/listen failure, connection refusal, timeout, DNS/TLS failure, or protocol error aligned to the symptom
- missing file, missing module, invalid argument, parse failure, or configuration rejection
- permission/access denial or authentication/authorization failure
- resource exhaustion such as out-of-memory, disk full, file-descriptor exhaustion, or quota failure
- dependency startup failure or unavailable upstream/downstream service
- explicit health/readiness failure
- transaction, migration, schema, or state corruption error
- container restart reason, exit code, failed probe, or image/entrypoint error

Treat repeated warnings as noise unless their timing and content align with the symptom or they clearly escalate into the failure.

## Cascade rules

Distinguish the initiating error from later consequences.

Examples:

- a missing configuration file may cause a service exit; the later restart-loop lines are consequences
- a database connection refusal may cause many request failures; the request errors are downstream symptoms
- an out-of-memory kill may produce later socket disconnects; the disconnects are not the initiating cause

When chronology is available, identify the first evidence-backed failure that plausibly explains what follows. Do not call it root cause unless the slice actually proves that relationship.

## Evidence labels

### Proven

Facts directly shown by the pasted slice, such as an exit code, exception type, rejected path, timestamp, process ID, event ID, status code, or failed dependency.

### Suspected

A likely explanation or component inferred from the proven evidence. Keep it explicitly labeled as a hypothesis.

### Missing evidence

The smallest fact needed to confirm or reject the main hypothesis.

Never blur `Suspected` into `Proven`.

## Cross-platform sources

Support common sources including:

- Linux `journalctl`, syslog, kernel logs, and service output
- Windows Event Viewer / Event Log exports and PowerShell event output
- macOS unified logging and launchd-related output
- Docker and container runtime logs
- Kubernetes pod/event logs
- web-server, reverse-proxy, database, application, and framework logs
- Python, JavaScript, Java, .NET, Go, Rust, C/C++, and other traceback or stack-trace fragments

Use the source's own timestamps, identifiers, and severity fields when present. Do not assume severity labels alone establish causality.

## Distributed and multi-component logs

When multiple services appear:

- correlate by timestamp, request/correlation/trace ID, host, process, pod/container, or transaction identifier when available
- avoid combining unrelated errors merely because they occur nearby
- choose one primary suspect layer unless the evidence genuinely requires more than one
- ask for the smallest missing adjacent slice from the relevant component instead of requesting a giant log dump

## Next-check rules

Give 1 to 3 checks only by default.

Each check should test a specific missing fact, such as:

- a tighter time window around the failure
- the preceding lines before a traceback or fatal event
- the status of one named dependency
- the exact configuration/path referenced by the error
- one process, port, file, event ID, container, or request identifier

Prefer read-only checks. Do not recommend broad restarts, reinstallations, cache deletion, or configuration edits from weak evidence.

## Secret and privacy handling

Logs may contain credentials, tokens, cookies, email addresses, internal URLs, customer data, or other sensitive values.

- do not repeat suspected secrets unnecessarily
- refer to the affected field or line generically when possible
- warn the user when a pasted log appears to expose a credential
- do not ask for a larger raw log dump when a narrower redacted slice will answer the question

## Output format

Use this structure:

### Slice quality
`STRONG`, `USABLE`, or `WEAK`, followed by one short reason.

### Signal summary
Two to four short lines describing the failure signal and chronology.

### Primary suspect
One component or layer, or `Not enough evidence yet.`

### Proven
Short bullets containing only evidence-backed facts.

### Suspected
Short bullets containing hypotheses, or `None yet.`

### Noise / downstream effects
Mention only the notable lines that should not be mistaken for the initiating failure.

### Next checks
Give 1 to 3 exact, targeted checks or the smallest additional log slice needed.

### Caution
Include only when evidence quality is weak, sensitive data is exposed, chronology is ambiguous, or the log source cannot support the claimed conclusion.

## Style

Be concise and operational. Do not paraphrase the entire log. Focus on the failure window, evidence chain, and smallest next proof.
