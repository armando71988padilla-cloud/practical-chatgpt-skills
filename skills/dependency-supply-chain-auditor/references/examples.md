# Dependency Supply-Chain Auditor examples

## npm lifecycle script

Request:

> A dependency change added a root `postinstall` script. Is that a problem?

Good behavior:

- prove the lifecycle script exists and what project owns it
- treat automatic install-time code execution as a high-impact review point
- inspect what the script invokes before judging it
- do not label it malicious without evidence

## Python extra index

Request:

> My requirements file uses `--extra-index-url`. Audit it.

Good behavior:

- flag the alternate-index source model
- avoid printing embedded credentials or private host details unnecessarily
- explain dependency-confusion conditions without claiming exploitation is proven
- verify package-name/source expectations if current registry access is available and approved

## Cargo Git dependency

Request:

> We replaced a crates.io dependency with a Git revision. What changed from a trust perspective?

Good behavior:

- prove the dependency source changed to VCS
- determine whether a specific revision is selected
- distinguish registry provenance from repository provenance
- review the resulting `Cargo.lock` change
- avoid calling the Git source unsafe merely because it is Git-based

## Tauri plugin

Request:

> I added a Tauri shell plugin. Is the dependency change okay?

Good behavior:

- review both frontend and Rust dependency additions
- identify build/install/native surface changes
- hand off permission/capability implications to Tauri boundary review
- ask whether shell functionality can be modeled as a narrower named operation

## Current vulnerability question

Request:

> Is package X version Y vulnerable right now?

Good behavior:

- do not answer from static manifest inspection alone
- use current advisory/registry/upstream evidence when available
- date the conclusion and distinguish known advisories from general package risk
