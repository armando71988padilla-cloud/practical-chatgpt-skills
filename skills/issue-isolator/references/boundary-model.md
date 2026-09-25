# Issue isolation boundary model

Use this reference when the problem spans several layers or the evidence appears contradictory.

## Boundary-first debugging

A boundary test asks whether the failure exists before or after a specific interface. Good boundaries often exist between components that can be checked independently.

Examples:

- client -> API
- reverse proxy -> application server
- service manager -> process
- process -> listener
- application -> database
- host -> container
- source tree -> build artifact
- build artifact -> deployed release
- authentication -> authorization

The goal is not to identify the whole root cause in one move. The goal is to cut the search space substantially.

## Working side versus failing side

A useful isolation statement looks like:

`A is proven working; B is failing or unproven; test the A -> B boundary.`

If neither side is proven, choose the cheapest reliable observation first rather than declaring a boundary prematurely.

## Competing hypotheses

When two hypotheses fit the same symptom, choose a test whose possible outcomes separate them.

Weak test:

`restart the application and see if it helps`

Strong test:

`call the backend endpoint directly; if it succeeds, the UI/client path remains suspect; if it fails identically, move below the UI boundary`

## Conflicting evidence

Do not average conflicting facts into a vague conclusion. Name the contradiction.

Examples:

- service manager says active, but no expected process exists
- process is listening locally, but proxy says connection refused
- edited file hash changed, but runtime executable path points to another tree
- deployment reports version B, but application status endpoint reports version A

The next test should reconcile the contradiction before remediation.

## Cascading failures

One upstream failure can produce many downstream symptoms. Park symptoms that are explainable as consequences until the upstream boundary is tested.

Examples:

- database unavailable -> API errors -> UI failures
- process crash -> port closed -> proxy 502 -> browser error
- invalid config -> service exit -> restart loop -> dependent health failures

Do not debug each downstream symptom independently unless evidence shows they have separate causes.

## Layer changes are experiments

A patch, restart, reinstall, or configuration change alters evidence. Prefer observation before mutation. When a change is necessary as a diagnostic experiment, change one variable, define the expected result first, and preserve rollback when practical.
