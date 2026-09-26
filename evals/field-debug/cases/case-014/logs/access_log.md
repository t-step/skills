# checkout-drops access log (excerpt)

Full access log for the SNK-4471 drop window (09:00:00-09:00:47 UTC,
disambiguated from the Friday-morning UTC drop time above; timestamps
below use the same day's 14:03 UTC slice where the final unit sold,
which is the only part of the log included in this excerpt). The drop
ran across 8 app instances (`checkout-app-01` through `checkout-app-08`)
behind a load balancer; `X-App-Instance` is the instance that actually
handled the request, not the client's IP.

```
2026-09-20T14:03:21.184Z app=checkout-app-03 pid=18823 POST /drops/SNK-4471/reserve order_id=ORD-88841 request_id=a1e4c2f0 status=200 latency_ms=41
2026-09-20T14:03:21.199Z app=checkout-app-07 pid=19042 POST /drops/SNK-4471/reserve order_id=ORD-88842 request_id=c92f7ab1 status=200 latency_ms=38
```

Both requests returned `200 confirmed` -- no error, no retry, no
duplicate-request-id, no client-side double submit (the two `request_id`
values, `order_id` values, and source app instances are all distinct).
`docs/instance_count.md` in this same drop's ops runbook (not included
here) puts the drop's total instance count at 8; the load balancer
routes each incoming request to whichever instance has the shortest
queue at that instant, with no session affinity to a SKU or drop.
