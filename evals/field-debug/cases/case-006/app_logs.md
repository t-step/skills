# Application logs, `reports-svc`, request `req-88213`

```
2026-09-24 11:02:03.100 INFO  [req-88213] POST /reports/generate started, report_type=quarterly_full
2026-09-24 11:02:03.104 INFO  [req-88213] fetching source data (est. rows=812,000)
2026-09-24 11:02:41.220 INFO  [req-88213] source data fetched, rows=812,344
2026-09-24 11:03:10.900 INFO  [req-88213] rendering report, pages=214
2026-09-24 11:03:18.412 INFO  [req-88213] report generation complete, size_mb=41.2
2026-09-24 11:03:18.415 INFO  [req-88213] POST /reports/generate completed, status=200, duration_ms=75315
```

No exception, stack trace, or error of any kind is logged for
`req-88213` -- the application handled the request start to finish and
reported its own completion as a normal `200`, 75.3 seconds after it
started.

A grep across all `reports-svc` application logs for the incident window
(all requests, not just `req-88213`) finds zero unhandled exceptions,
zero stack traces, and zero application-emitted 5xx responses of any
kind. Every request the application itself completed, it completed with
a 200.
