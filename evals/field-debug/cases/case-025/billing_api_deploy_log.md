# billing-api deploy log (excerpt)

```
09:02:14 UTC  deploy billing-api v2.41.0 started (rolling, 12 pods)
09:04:58 UTC  deploy billing-api v2.41.0 complete -- 12/12 pods healthy
```

## v2.41.0 changelog (excerpt)

- Bump `httpx` 0.24.1 -> 0.27.0 (routine dependency update, picked up in
  the course of an unrelated security-patch sweep).
- No application code in the `ledger-svc` client path was touched.

## Notes carried over from the dependency bump (from `httpx`'s own
## release notes, linked in the PR that did the bump)

`httpx` 0.27 changed its `Client`/`AsyncClient` defaults:
`Limits(max_connections=100, max_keepalive_connections=20)` in 0.24 ->
`Limits(max_connections=10, max_keepalive_connections=5)` in 0.27, unless
a caller explicitly passes its own `Limits`. `billing-api`'s
`ledger-svc` client does not pass an explicit `Limits` object anywhere in
its construction -- it uses whatever `httpx.Client()`'s default is.
