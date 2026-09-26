# billing-api application error log (excerpt, 09:00-11:45 UTC)

Before 09:03 UTC: no errors on the `ledger-svc` call path in the prior 24
hours.

Starting 09:03:41 UTC, recurring:

```
09:03:41 UTC ERROR billing_api.clients.ledger: httpx.PoolTimeout:
  Pool timeout: All connections in the connection pool are in use.
  (max_connections=10)
  request_id=req-a3f91 order_id=... target=ledger-svc:8443

09:03:44 UTC ERROR billing_api.clients.ledger: httpx.PoolTimeout:
  Pool timeout: All connections in the connection pool are in use.
  (max_connections=10)
  request_id=req-a3f92 target=ledger-svc:8443

... (pattern repeats, roughly 4 out of every 10 outbound calls to
    ledger-svc, continuously from 09:03:41 UTC through the present,
    11:45 UTC)
```

Every one of these errors is an `httpx.PoolTimeout` raised client-side,
before a TCP connection to `ledger-svc` is even attempted for that
request -- the pool is exhausted and the request never leaves the
process. No `ConnectionRefusedError`, no `ConnectTimeout`, and no TLS or
DNS-related exception appears anywhere in this log.
