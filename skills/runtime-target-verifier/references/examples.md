# Runtime Target Verifier examples

## Linux service points elsewhere

Request:

> I edited `/opt/example/app.py`, but the service did not change. Am I editing the live file?

Good behavior:

- inspect the loaded service command first
- if `ExecStart` points to `/srv/example/app.py`, report `MISMATCH`
- do not recommend another edit to `/opt/example/app.py`
- give one read-only command that proves the next runtime link

## Windows service executable

Request:

> I have two copies of `worker.exe`. Which one is the Windows service actually running?

Good behavior:

- identify the service configuration and running process
- compare the configured executable path with the process executable/command line
- resolve quoted paths and arguments
- mark patch safety only after the exact executable is proven

## Symlinked launcher

Request:

> `/usr/local/bin/tool` is the command I run, but I want to patch it.

Good behavior:

- treat `/usr/local/bin/tool` as the claimed target
- resolve whether it is a symlink or wrapper
- follow only the hop that selects the real executable/script
- do not patch the launcher when the user intends to patch the resolved target

## Containerized app

Request:

> I changed `src/server.js` on the host but my running container still has the old behavior.

Good behavior:

- do not assume the host file is mounted into the container
- inspect the container command and mounts/image
- distinguish a bind-mounted development container from an image-built production container
- use `CONDITIONAL` if a rebuild/recreate is required

## Compiled application

Request:

> I changed the source file but the desktop application still behaves the same.

Good behavior:

- distinguish source from compiled/bundled artifact
- identify the executable or bundle actually running
- prove which build output corresponds to it
- state that the source is not directly patch-safe until rebuild/activation is established
