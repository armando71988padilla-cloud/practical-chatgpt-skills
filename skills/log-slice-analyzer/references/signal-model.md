# Log signal model

Use this reference when the slice has multiple errors, repeated lines, restarts, or more than one component.

## Chronology before severity

The highest-severity line is not always the initiating failure. Prefer the earliest error that is both temporally aligned with the symptom and capable of explaining the later cascade.

Useful sequence:

`normal state -> first anomaly -> initiating failure candidate -> downstream failures -> restart/retry noise`

If timestamps are missing or reordered, say chronology is unproven.

## Repetition and deduplication

Repeated identical messages often add frequency information rather than new causes. Collapse them conceptually and note the count or pattern when it matters.

A warning repeated thousands of times may still be noise. A single fatal line may be more informative.

## Crash loops

For restart loops, separate:

- the original process failure
- supervisor/container restart messages
- readiness/health failures after restart
- repeated downstream connection errors caused by the unavailable process

Ask for the final lines from one failed process instance, not an enormous aggregate dump, when the initiating error is missing.

## Stack traces

For stack traces:

- identify the exception/error type first
- prefer the first application-relevant frame near the failure over framework boilerplate
- distinguish the exception cause from later wrappers such as `caused by`, nested exceptions, or promise/task propagation
- do not infer a bad source line merely because it is the last visible application frame

## Network failures

Differentiate:

- name resolution failure
- connection refused
- connection reset
- timeout
- TLS/certificate failure
- HTTP/application status errors

These represent different layers. Do not call a timeout a DNS problem without evidence, or a 500 response a connectivity failure when the server clearly answered.

## Resource failures

Evidence such as OOM kill, disk full, inode exhaustion, quota failure, or too many open files can generate many secondary application errors. Treat the resource event as the initiating failure candidate when chronology supports it.

## Distributed systems

Correlate with stable identifiers whenever possible:

- trace ID
- request ID
- transaction ID
- pod/container ID
- host/node
- process ID
- user/session ID when appropriate and non-sensitive

Timestamp proximity alone is weak correlation across busy systems.

## Confidence discipline

Use high confidence only when the slice directly links the observed failure to the reported symptom. Otherwise use language such as `likely`, `consistent with`, or `needs confirmation`.

Do not use `root cause` when the evidence only shows a failure location or proximate cause.
