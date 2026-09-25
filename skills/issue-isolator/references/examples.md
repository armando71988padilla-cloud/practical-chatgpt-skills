# Issue Isolator examples

## UI error versus API error

Request:

> The page says Save failed, the console has an error, and I also saw a warning in the server logs. Where do I start?

Good behavior:

- define the active symptom as the failed Save operation
- park unrelated warnings unless correlated
- test the same API operation directly or inspect its response
- use the result to decide whether the failing side is UI/client or API/backend

## Service active but no port

Request:

> systemctl says the service is active but nothing is listening on its port.

Good behavior:

- record service-active state as proven
- do not equate active with healthy/listening
- choose the service/process/listener boundary
- inspect the service's actual process/command or listener state before restarting it

## Source edit has no effect

Request:

> I edited the code but the app still behaves exactly the same.

Good behavior:

- avoid assuming the source is live
- test the source/build-artifact/runtime-target chain
- use runtime path or build/deployment identity evidence
- park logic debugging until the live target is proven

## Multiple symptoms after one outage

Request:

> Login fails, the dashboard is blank, background jobs are failing, and the health page is red.

Good behavior:

- choose one active symptom or the highest shared boundary if evidence supports it
- test a shared dependency only if the symptoms genuinely converge there
- park the remaining symptoms instead of debugging four paths at once
