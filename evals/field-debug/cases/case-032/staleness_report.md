# Staleness reports -- account status page timestamp

Ten sampled complaints over the past 3 days, each with the request's CDN
edge PoP identified via the `X-Served-By` response header:

```
customer  reported_stale_by   pop
c_2201    ~92s                iad3
c_5510    ~88s                iad3
c_7742    ~95s                iad3
c_1180    ~85s                iad3
c_9903    ~91s                iad3
c_3345    (not stale)         sjc1
c_8820    (not stale)         fra2
c_0091    (not stale)         iad3   <- same PoP, not affected this time
c_6612    ~90s                iad3
c_4471    (not stale)         nrt1
```

Every stale report is `iad3`. Not every `iad3` request is stale
(`c_0091`), which is consistent with edge cache behavior (a cache hit vs.
miss on that specific edge node) rather than every request through that
PoP being affected uniformly.
