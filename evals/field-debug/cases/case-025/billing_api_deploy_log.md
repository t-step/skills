# billing-api deploy log (excerpt)

```
09:02:14 UTC  deploy billing-api v2.41.0 started (rolling, 12 pods)
09:04:58 UTC  deploy billing-api v2.41.0 complete -- 12/12 pods healthy
```

## v2.41.0 changelog (excerpt)

- Bump `platform-http` 3.2.0 -> 3.4.0 (internal HTTP client wrapper,
  maintained by the Platform team, built on top of `httpx`; picked up in
  the course of an unrelated security-patch sweep).
- No application code in the `ledger-svc` client path was touched.

## Notes carried over from the dependency bump (from `platform-http`'s
## own internal CHANGELOG, linked in the PR that did the bump)

`platform-http` 3.4.0 changed the wrapper's own default connection-pool
limits -- the `Limits` object it hands to the underlying `httpx.Client`
when a caller doesn't supply its own: `max_connections=100` in 3.2.0 ->
`max_connections=10` in 3.4.0, "to cut idle-connection overhead for the
wrapper's typical caller (low-QPS internal batch/cron jobs)." `billing-api`'s
`ledger-svc` client uses `platform-http` and does not pass an explicit
`Limits` override anywhere in its construction -- it uses whatever
`platform-http`'s current default is.
