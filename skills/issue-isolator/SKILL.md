---
name: issue-isolator
description: Reduce a messy technical problem with multiple symptoms, theories, or failing layers into one testable issue and one useful next boundary check. Use when a user says several things are broken, is unsure which layer is actually failing, has conflicting evidence, wants to separate primary symptoms from secondary effects, or needs a debugging plan that avoids changing several systems at once. Distinguish proven facts from assumptions, park unrelated symptoms, identify the narrowest boundary between working and broken, and avoid remediation until the failing layer is sufficiently isolated.
---

# Issue Isolator

## Purpose

Turn a tangled debugging situation into one active symptom, one likely failing layer, and one boundary test that can meaningfully narrow the problem.

## Workflow

1. Restate the user's active symptom in observable terms.
2. Separate other symptoms, theories, and side effects from the active symptom.
3. Identify the smallest set of layers that could directly produce the symptom.
4. Mark evidence as `PROVEN`, `SUSPECTED`, `CONFLICTING`, or `UNPROVEN`.
5. Find the narrowest boundary where one side is known working and the other side is failing or unknown.
6. Choose one read-only or low-risk test that crosses that boundary.
7. Predict what each possible result would imply before running the test.
8. Park remediation until the test identifies the failing side, unless the cause is already directly proven.

Read `references/boundary-model.md` when more than two layers are involved, evidence conflicts, or the issue spans frontend/backend, process/service, host/container, network/application, or deployment/runtime boundaries. Read `references/examples.md` when a concrete isolation pattern is useful.

## Active symptom rules

Describe the symptom as something observable, not as a theory.

Prefer:

- `HTTP request to /health returns 502`
- `desktop app opens but Save does nothing`
- `service process is running but port 8080 is not listening`
- `file edit has no effect on the running program`

Avoid treating these as symptoms without proof:

- `the database is broken`
- `permissions are wrong`
- `the API is buggy`

Those are hypotheses until evidence supports them.

## Layer model

Choose the smallest relevant layers. Common layers include:

- user interface / client
- browser or desktop shell
- API / route / RPC boundary
- authentication / authorization
- service manager / supervisor
- process / runtime
- executable, script, module, or build artifact
- configuration / environment
- filesystem / permissions
- network / DNS / TLS / proxy / port
- container / VM / host boundary
- database / queue / cache / external dependency
- deployment / release / version selection
- data / state

Do not force every issue into this list. Name the real layers shown by the evidence.

## Evidence labels

### PROVEN

Directly supported by observed output, runtime state, a reproducible request, a log line tied to the symptom, a file/process path, or another concrete check.

### SUSPECTED

A plausible explanation that fits the evidence but has not been tested.

### CONFLICTING

Two pieces of evidence appear incompatible and must be reconciled before patching.

### UNPROVEN

A required link or assumption that has not been checked.

Never convert a user's confidence into technical proof.

## Boundary selection

A good boundary test divides the problem space.

Examples:

- UI renders -> direct API request fails: test UI-to-API versus API itself
- API responds locally -> reverse proxy returns 502: test proxy-to-upstream boundary
- service is active -> no listener exists: test service-manager-to-process/listener boundary
- process runs -> wrong behavior persists after source edit: test source-to-build/runtime-target boundary
- container is healthy -> host request fails: test host-to-container networking/publishing boundary
- credentials authenticate -> protected operation is denied: test authentication-to-authorization boundary

Prefer a test where different results lead to different next actions. Avoid checks that only repeat facts already known.

## Scope control

Debug one active symptom at a time unless two symptoms are proven to share the same failing boundary.

Park secondary symptoms explicitly when needed. Do not ignore them permanently; record them as parked so they can be revisited after the primary issue is isolated.

Do not widen into unrelated services, repositories, machines, or infrastructure because they are nearby.

## Next-test rules

By default give one next test.

The test should be:

- read-only or low-risk
- narrow enough to answer one question
- tied directly to the chosen boundary
- easy to interpret
- free of unrelated remediation

Before presenting the test, state what a success result and a failure result would mean when that distinction is not obvious.

If one command cannot safely prove the boundary, give a short inspection step instead of inventing a broad checklist.

## Interaction with logs

Use logs as evidence, not as the entire debugging model.

If a log slice already proves a specific failure, use that fact. If logs only show downstream errors, keep the initiating layer unproven. Do not restart, reinstall, or patch merely because a warning exists.

## Cross-platform guidance

Support Linux, macOS, Windows, containers, and common web/application stacks. Use the user's actual shell and environment when known.

Do not assume systemd, PowerShell, Docker, Kubernetes, a browser, or a particular framework unless evidence establishes it.

## Output format

Use this structure:

### Active symptom
One observable problem only.

### Primary failing layer
One layer, or `Not isolated yet.`

### Likely boundary
State the boundary between known-working and failing/unknown behavior.

### Proven
Short bullets containing only evidence-backed facts.

### Suspected / conflicting
Short bullets containing hypotheses or contradictions that still need proof.

### Parked symptoms
List other real symptoms being intentionally deferred, or `None.`

### Smallest next test
Give one exact read-only command, request, or inspection step.

### Result interpretation
State what each meaningful result would prove or rule out.

### Remediation status
Use `DO NOT PATCH YET` until the failing side is isolated. Use `CAUSE PROVEN` only when the evidence directly identifies the failing condition.

## Style

Be concise, calm, and operational. Name the battlefield instead of generating a grand theory. Prefer one discriminating test over five generic checks.
