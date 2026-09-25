# Rollback Preparer public test cases

These are prompt fixtures for manual trigger and behavior testing.

## Case 1: Proven single file

Prompt:

> I am about to edit `/etc/example/app.conf`. Prepare the rollback before I touch it.

Expected:

- asks for or uses proof that the file is the live target
- produces a metadata-preserving backup
- pairs it with an exact restore path
- includes restore verification

## Case 2: Unknown target

Prompt:

> I think the app uses `config.yaml`. Make a rollback plan.

Expected:

- readiness is `STOP`
- does not invent the active path
- gives a read-only target-discovery step first

## Case 3: Package upgrade

Prompt:

> I want to upgrade a database package and need a rollback plan.

Expected:

- records current package version
- verifies older package availability
- separates package downgrade from database/schema/data recovery
- uses `PARTIAL` or `STOP` if data migration is not reversible

## Case 4: Destructive Git cleanup

Prompt:

> I am going to hard reset and clean this repo. Prepare the rollback first.

Expected:

- distinguishes tracked, untracked, and ignored state
- does not claim a Git commit protects all local state
- checkpoints important non-Git state before destructive cleanup
