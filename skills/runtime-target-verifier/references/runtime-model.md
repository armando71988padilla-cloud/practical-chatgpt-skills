# Runtime target evidence model

Use this reference when the runtime chain spans more than one hop.

## Direct processes

A process name is weak evidence because multiple binaries or scripts can share the same name. Prefer the running process ID, executable path, command line, working directory, and relevant environment or arguments.

For interpreted programs, distinguish the interpreter executable from the script/module it was told to run. For example, proving `python` is live does not prove which Python file or module is live.

## Linux services

For systemd-managed workloads, the useful chain is often:

`unit -> ExecStart -> wrapper/interpreter -> real path -> process`

Use unit content and runtime properties rather than guessing from filenames. Resolve symlinks and relative paths. User units and system units can have the same service name, so scope matters.

A unit file on disk is not automatically the loaded unit definition if daemon-reload or an override is involved. When that distinction matters, inspect the loaded service properties and drop-ins.

## Windows services and scheduled tasks

For Windows Services, distinguish the service display name from its service name and executable path. Query the configured service path and compare it with the running process command line when possible.

For scheduled tasks, inspect the task action, arguments, and working directory. A shortcut, batch file, PowerShell wrapper, or environment variable may add another hop.

## macOS launchd and applications

For launchd, trace the loaded job label to its program/program arguments and then to the running process. LaunchAgents and LaunchDaemons can live in different domains and directories.

For `.app` bundles, distinguish the bundle directory from the executable inside `Contents/MacOS` and from any helper process the app launches.

## Symlinks, wrappers, and relative paths

Resolve symlinks before editing unless changing the symlink itself is intentional. For wrapper scripts, inspect the exact child command and arguments that select the next target.

Relative paths depend on a working directory. Prove the working directory before converting a relative runtime argument into an absolute claimed target.

## Containers

The host path, image filesystem, and live container filesystem are distinct namespaces.

Useful evidence may include:

- container identity and image digest/tag
- configured entrypoint and command
- bind mounts and volumes
- working directory
- in-container real path
- whether the container was recreated after a host-side change

Do not claim that editing a Dockerfile, source directory, or image tag changes an already running container.

## Development servers and build systems

A development server may use hot reload, a transpiled output tree, a generated bundle, or a different project root than the shell currently displays.

For compiled, bundled, or transpiled applications, prove the relationship:

`source -> build artifact -> launcher/runtime`

If the build artifact is live, source edits are only `CONDITIONAL` until rebuild/reload behavior is established.

## Remote and distributed runtimes

A local repository does not prove a remote server, VM, container cluster, function, or deployment is using the same revision. Require deployment identity, artifact/version, image digest, commit reference, or another direct runtime marker.

When more than one instance is active, avoid calling the target proven until the evidence covers the instance or population the user actually intends to change.
