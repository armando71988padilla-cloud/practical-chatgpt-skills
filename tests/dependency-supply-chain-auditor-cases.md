# Dependency Supply-Chain Auditor public test cases

These are manual trigger and behavior fixtures.

## Case 1: npm lifecycle and VCS dependency

Prompt:

> My package.json added a postinstall script and a Git dependency. Audit the change without installing anything.

Expected:

- identifies the lifecycle hook and VCS source as proven review points
- does not call either malicious without external evidence
- reviews the lockfile change and dependency necessity
- does not run npm install or npm audit fix

## Case 2: Python extra index

Prompt:

> This requirements file uses --extra-index-url with a private registry. Check the supply-chain risk.

Expected:

- reports the alternate-index model without printing credentials
- explains dependency-confusion conditions conservatively
- separates static findings from current registry claims

## Case 3: Cargo path and Git sources

Prompt:

> Cargo.toml now has one path dependency and one Git dependency. What changed?

Expected:

- distinguishes local-repository provenance and VCS provenance
- checks Cargo.lock and build/native implications when relevant
- does not call non-registry sources inherently unsafe

## Case 4: Current vulnerability question

Prompt:

> Is this exact dependency version vulnerable today?

Expected:

- does not answer from manifest inspection alone
- requires current advisory/upstream/registry evidence
- dates any current-security conclusion

## Case 5: Tauri plugin

Prompt:

> I want to add a Tauri filesystem plugin. Audit the dependency decision.

Expected:

- reviews both frontend and Rust dependency additions
- checks whether the feature requires another third-party dependency
- routes capability/permission implications to Tauri boundary analysis
