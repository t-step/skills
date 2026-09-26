# homepage-svc Redis cache counters -- `homepage:featured_products` (excerpt)

Per-second miss/hit counters for the one cache key
`homepage:featured_products`, same window as the DB pool metrics.
`homepage-svc` runs 48 instances behind the load balancer; each instance
calls `get_featured_products()` on every homepage request it serves.

```
ts           | hits/sec | misses/sec
------------ | -------- | -----------
09:14:57     |    412   |     0
09:14:58     |    398   |     0
09:14:59     |    405   |     0
09:15:00     |      3   |    47
09:15:01     |      0   |     1
09:15:02     |    390   |     0
09:15:03     |    411   |     0
...
09:19:58     |    401   |     0
09:19:59     |    397   |     0
09:20:00     |      2   |    46
09:20:01     |      1   |     0
09:20:02     |    404   |     0
...
09:24:58     |    408   |     0
09:24:59     |    399   |     0
09:25:00     |      4   |    45
09:25:01     |      0   |     0
09:25:02     |    412   |     0
```

Outside these one- or two-second windows, misses against this key are
effectively zero (0-1/sec, consistent with occasional cold cache
clients). The miss count in each burst (45-48) lands within the normal
range of `homepage-svc`'s current instance count (48) -- consistent with
close to the entire fleet missing this one key within the same one- or
two-second window, then all repopulating it.
