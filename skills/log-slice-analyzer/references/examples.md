# Log Slice Analyzer examples

## Missing configuration followed by restart loop

Input pattern:

- application reports `No such file or directory` for a required configuration path
- process exits
- supervisor repeatedly logs restart attempts

Good analysis:

- classify the missing required path as signal
- treat restart messages as downstream noise/consequence
- mark the exact missing path and exit as proven
- suspect incorrect deployment/configuration path
- next check should verify the referenced path or active configuration source

## Connection refused storm

Input pattern:

- many requests fail with `connection refused` to one local dependency
- the dependency's own log is not included

Good analysis:

- prove only that clients could not connect to the shown endpoint
- suspect the dependency is down, not listening there, or isolated by namespace/networking
- do not claim why the dependency is unavailable
- ask for one status/listener check or the dependency's failure-time slice

## Traceback with repeated framework frames

Input pattern:

- long framework traceback
- one application frame shows invalid input conversion
- final exception is a value/format error

Good analysis:

- summarize the exception type and relevant application frame
- avoid retelling framework frames
- identify the input/parse layer as the primary suspect
- next check should inspect the exact input/value path, not restart the service

## Weak slice

Input pattern:

- one warning from hours before the reported outage
- no timestamp around the failure and no terminal error

Good analysis:

- classify slice quality as `WEAK`
- do not assign root cause
- request a narrow slice around the actual failure time
