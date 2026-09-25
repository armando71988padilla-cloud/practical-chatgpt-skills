# Log Slice Analyzer public test cases

These are manual trigger and behavior fixtures.

## Case 1: Missing file then restart loop

Prompt:

> Here is a journal slice. The app says a required config file is missing, exits, then systemd keeps restarting it. What actually matters?

Expected:

- identifies the missing required path as the primary signal
- treats restart-loop messages as downstream effects
- separates proven facts from suspected configuration cause
- asks for at most 1 to 3 targeted checks

## Case 2: Connection refused storm

Prompt:

> Hundreds of requests say connection refused to the same dependency. Is that the root cause?

Expected:

- proves only that clients could not connect to the shown endpoint
- does not invent why the dependency is unavailable
- requests one dependency status/listener check or a narrow dependency log slice

## Case 3: Long traceback

Prompt:

> Analyze this long Python traceback and tell me the useful part only.

Expected:

- identifies exception type and relevant application frame
- does not paraphrase framework boilerplate
- gives a narrow next check tied to the failing input or state

## Case 4: Weak evidence

Prompt:

> This warning happened three hours before the outage. Is it what broke the service?

Expected:

- classifies the slice as `WEAK` unless other evidence connects it
- does not assign root cause
- requests a tighter failure-time slice
