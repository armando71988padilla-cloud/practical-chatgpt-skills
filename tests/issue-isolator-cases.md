# Issue Isolator public test cases

These are manual trigger and behavior fixtures.

## Case 1: UI versus API

Prompt:

> Save fails in the web UI, the console has an error, and there is also a server warning. Help me isolate it.

Expected:

- defines Save failure as the active symptom
- parks unrelated warnings
- identifies the UI/API boundary
- gives one discriminating check rather than several fixes

## Case 2: Service active but no listener

Prompt:

> The service manager says active, but the expected port is closed. What layer is actually failing?

Expected:

- keeps service-active state and listener state separate
- identifies service/process/listener boundary
- does not restart the service before the boundary test

## Case 3: Source edit ignored

Prompt:

> I edited source code but the running app did not change at all.

Expected:

- tests source/build/runtime identity before logic debugging
- does not assume the edited source is live
- parks remediation until runtime target is proven

## Case 4: Several symptoms

Prompt:

> Login is broken, the dashboard is blank, jobs are failing, and health checks are red. Where do I start?

Expected:

- selects one active symptom or one proven shared boundary
- parks the remaining symptoms
- avoids four parallel debugging tracks
