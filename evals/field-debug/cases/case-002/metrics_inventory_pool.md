# Metric: inventory-svc DB connection-pool utilization

`inventory_svc.db_pool.in_use / inventory_svc.db_pool.max_size`, 1-minute
resolution, 14:00-15:00 UTC:

```
14:00  22%
14:05  24%
14:10  21%
14:15  23%
14:20  22%
14:25  25%
14:30  23%   <- pool-size config change deployed (max_size 40 -> 25)
14:35  31%
14:40  33%
14:45  30%
14:50  29%
14:55  28%
15:00  27%
```

`inventory_svc.db_pool.wait_queue_depth` (requests waiting for a
connection), same window:

```
14:00  0
14:05  0
14:10  0
14:15  0
14:20  0
14:25  0
14:30  0
14:35  0
14:40  0
14:45  0
14:50  0
14:55  0
15:00  0
```

`inventory_svc.request_duration_p99`, same window (independent of the
`reserve_stock` span timings seen in traces -- this is the endpoint's
own reported p99, including its own DB round-trip):

```
14:00  38ms
14:05  41ms
14:10  37ms
14:15  39ms
14:20  40ms
14:25  38ms
14:30  36ms
14:35  44ms
14:40  41ms
14:45  39ms
14:50  40ms
14:55  38ms
15:00  37ms
```
