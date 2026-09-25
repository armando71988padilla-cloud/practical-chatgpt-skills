# Rollback Preparer examples

## Single configuration file

Request:

> I am about to edit `/etc/example/app.conf`. Give me a rollback first.

Good behavior:

- prove `/etc/example/app.conf` exists and inspect metadata
- create a timestamped metadata-preserving backup outside any directory being replaced
- give an exact restore command
- include the required service reload/restart only if the service relationship is known
- verify the restored file or active configuration

## Unknown live target

Request:

> I think the app is using `config.yaml`. Back it up before I edit it.

Good behavior:

- mark readiness `STOP`
- do not guess which `config.yaml` is active
- first prove the runtime/configuration path with a read-only check
- create backup commands only after the live target is established

## Package upgrade

Request:

> I want to upgrade a database server package. How do I roll back if it breaks?

Good behavior:

- record the exact installed version
- prove the prior package remains obtainable
- separate package downgrade from database/schema/data rollback
- require engine-appropriate data backup
- mark `PARTIAL` or `STOP` if the upgrade performs a one-way migration

## Git cleanup

Request:

> I am about to run an aggressive clean/reset on this repository. Prepare rollback.

Good behavior:

- inspect repository root and status first
- identify tracked, untracked, and ignored state separately
- do not imply that a commit protects untracked or ignored files
- create a checkpoint appropriate to each state class before destructive cleanup

## Deployment rollback

Request:

> We are replacing the running release with a new build. Give me rollback steps.

Good behavior:

- identify the currently active release/artifact
- preserve or reference the previous artifact
- identify configuration and data/schema changes separately
- restore the old artifact and activation pointer
- verify the old release is actually serving healthy traffic
