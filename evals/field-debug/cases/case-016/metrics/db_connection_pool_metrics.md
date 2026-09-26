# homepage-svc DB connection pool metrics (excerpt, 2026-09-22 09:14-09:26 UTC, ~4.5 hours after the TICKET-5521 deploy)

Pool size is fixed at 80 connections, shared across all 48 `homepage-svc`
instances (round-robin, no per-instance reservation). Sampled every 5s.

```
ts       | active_connections | pool_utilization_pct | p99_latency_ms
-------- | ------------------ | --------------------- | ---------------
09:14:40 |         14         |          18%          |       32
09:14:45 |         15         |          19%          |       31
09:14:50 |         16         |          20%          |       30
09:14:55 |         17         |          21%          |       33
09:15:00 |         79         |          99%          |      4102
09:15:05 |         80         |         100%          |      6844
09:15:10 |         80         |         100%          |      7011
09:15:15 |         41         |          51%          |      2203
09:15:20 |         16         |          20%          |       34
09:15:25 |         15         |          19%          |       32
...
09:19:55 |         16         |          20%          |       33
09:20:00 |         80         |         100%          |      6512
09:20:05 |         80         |         100%          |      6977
09:20:10 |         38         |          48%          |      1988
09:20:15 |         15         |          19%          |       31
...
09:24:55 |         17         |          21%          |       35
09:25:00 |         80         |         100%          |      6633
09:25:05 |         79         |          99%          |      6390
09:25:10 |         35         |          44%          |      1704
09:25:15 |         16         |          20%          |       32
```

Every spike in this window lands on an exact 300-second boundary
(09:15:00, 09:20:00, 09:25:00, ...) and lasts 10-15 seconds before the
pool drains back to baseline. This pattern has been continuous since
shortly after this morning's `TICKET-5521` deploy and has not varied in
period the whole time it's been observed.
