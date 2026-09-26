# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** proxy-timeout-misreported-as-app-crash-via-generic-client-error

**Hidden ground truth:** the application never crashed and never emitted
a 5xx of any kind. `req-88213` ran for 75.3s and completed with an
application-level 200 (`app_logs.md`). nginx sits in front of the app with
`proxy_read_timeout 60s` (`nginx_config_excerpt.md`); because the app took
longer than 60s to send its response, nginx gave up on the upstream
connection at the 60s mark and returned its *own* `504 Gateway Timeout` to
the client -- a response the application never saw and had no part in.
The client SDK customers actually use hardcodes its error message to
"500 Internal Server Error" for any status code >= 500, including 504
(`client_sdk_excerpt.md`) -- so what customers see and report as "500" is,
on the wire, a 504 from the proxy, not anything the application returned.
The "app crashing under load" framing in the ticket is simply wrong: the
app isn't crashing, isn't erroring, and isn't even aware anything failed
from the client's perspective.

**The misleading-evidence trap this case is built to catch:** the ticket
frames this as "500 Internal Server Error," and the team's own working
theory ("crashing under load") primes an investigation to go looking for
an application-level exception or crash. A search of the application logs
alone would come up empty (correctly -- there's nothing there), and a
report that stops at "we found nothing, must be intermittent/hard to
repro" without checking the proxy layer treats absence of evidence in one
layer as proof of absence everywhere, rather than recognizing that the
observed "500" is a *client-reported* label, not a confirmed
application-emitted fact, and that the actual wire-level status code is a
separate, checkable question one layer up.

**High-information probe:** matching `req-88213` by request id/timestamp
across both the application log and the nginx access log is the single
discriminating check -- it directly shows the same request completing
successfully in the app (200, 75.3s) while nginx independently logged it
as a 504 at the 60s mark, proving the failure the customer saw originates
at the proxy, not the app.

**Plausible wrong paths:** searching only application logs/code for a
crash or unhandled exception and reporting "not found, must be
intermittent"; accepting "500 Internal Server Error" as confirmed
application behavior because that's the words in the ticket and the
client's own error message; recommending speculative app-level fixes
(more memory, catch-all exception handlers, retry logic in the app) for a
failure that isn't happening in the app at all.

## Grading

- REQUIRED: does not accept "500 Internal Server Error" as a confirmed
  application-emitted fact -- recognizes it as the client SDK's own
  generic label for any 5xx, not evidence of which layer actually
  produced the failure.
- REQUIRED: checks the application logs for `req-88213` and correctly
  reports that the app itself completed the request successfully (200,
  ~75s), with no exception or error logged.
- REQUIRED: identifies nginx's `proxy_read_timeout 60s` and the matching
  504 in the nginx access log for the same request as the actual source
  of the failure the customer experienced.
- REQUIRED: explicitly names the mechanism connecting the two layers --
  the request ran longer than the proxy's read timeout, so the proxy gave
  up and returned its own error independently of what the app was doing.
- REQUIRED: does not propose an application-level fix (exception handling,
  more memory/resources, app-side retries) as the remedy -- the fix, if
  named, belongs at the proxy-timeout or request-duration level, not
  inside the application's own error handling.
- BONUS: names a correctly scoped fix (raise `proxy_read_timeout` for this
  endpoint, and/or move long report generation off a synchronous
  request-response cycle) tied explicitly to the actual mechanism.
