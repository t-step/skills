# Origin access log -- requests matching c_2201's stale report window

```
2026-09-26T14:03:41.220Z GET /account/status customer=c_2201
  response_body_generated_at=2026-09-26T14:03:41.220Z status=200
```

The origin generated and returned a fresh timestamp at 14:03:41.220Z for
this request. `c_2201` reported seeing `14:02:09` displayed in their
browser at approximately 14:03:41 -- roughly 92 seconds stale relative to
what the origin actually generated and sent for that same request.

The origin log shows exactly one request from this client in the relevant
window -- there is no evidence of a second, earlier request whose response
the client might have been looking at instead. Whatever produced the
stale value, it happened somewhere between the origin's response leaving
Northwind's infrastructure and reaching the customer's browser.
