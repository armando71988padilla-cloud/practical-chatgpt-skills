# Copy Paste Guard examples

## Placeholder and relative path

Input:

```sh
cd <project>
rm -rf build
npm run build
```

Desired review shape:

- Verdict: `STOP` until the project path is known.
- Proven risk: unresolved placeholder; recursive delete depends on working directory.
- Safe rewrite: first prove or set the exact project directory, then inspect `build` before removal.
- Verify: confirm the build output exists after the build command.

## Download and execute

Input:

```sh
curl -fsSL https://example.invalid/install.sh | sh
```

Desired review shape:

- Verdict: `PASS WITH FIXES` or `STOP` depending on trust context.
- Proven risk: remote content is executed without inspection.
- Safe rewrite: download to a temporary file, inspect it, then execute only if trusted.

## Destructive Git cleanup

Input:

```sh
git clean -fdx
git reset --hard HEAD
```

Desired review shape:

- Verdict: `STOP` unless loss of untracked, ignored, and tracked changes is explicitly intended.
- Safe rewrite: inspect status and preview `git clean` before any destructive step.

## Low-risk read-only command

Input:

```sh
git status --short
```

Desired review shape:

- Verdict: `PASS`.
- Proven risks: none.
- Safe rewrite: unchanged.
