# Runtime Target Verifier public test cases

These are manual trigger and behavior fixtures.

## Case 1: Duplicate file paths

Prompt:

> I edited `/opt/example/app.py`, but the service did not change. How do I prove which copy is live?

Expected:

- does not assume the edited path is live
- starts from service or process runtime evidence
- labels unproven links explicitly
- gives one read-only next check

## Case 2: Windows service

Prompt:

> There are two `worker.exe` files on this Windows machine. Which one is my service running?

Expected:

- inspects service configuration and process evidence
- distinguishes service display name from executable path
- does not recommend patching until exact runtime path is proven

## Case 3: Container source mismatch

Prompt:

> I changed a host source file but the Docker container did not change behavior.

Expected:

- distinguishes host source, image contents, and live container filesystem
- inspects command/mount/image relationship
- marks source editing as conditional when rebuild/recreate is needed

## Case 4: Symlink wrapper

Prompt:

> I am about to edit `/usr/local/bin/tool`. Make sure that is the real file being used.

Expected:

- resolves symlink or wrapper first
- reports mismatch if the launcher points elsewhere
- gives one exact read-only check rather than a long checklist
