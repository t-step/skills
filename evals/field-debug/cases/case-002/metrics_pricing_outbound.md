# Metric: pricing-svc outbound call duration to tax-rate vendor

`pricing_svc.outbound.taxratevendor.duration_p50` /
`duration_p99`, 1-minute resolution, 14:00-15:00 UTC:

```
14:00   p50=48ms   p99=90ms
14:05   p50=51ms   p99=88ms
14:10   p50=47ms   p99=95ms
14:15   p50=49ms   p99=91ms   <- pricing-svc v4.12.0 deployed (tax-rate lookup added)
14:20   p50=50ms   p99=93ms
14:25   p50=52ms   p99=97ms
14:30   p50=55ms   p99=101ms
14:32   p50=2400ms p99=3820ms
14:35   p50=2810ms p99=3910ms
14:40   p50=2650ms p99=3780ms
14:45   p50=1980ms p99=3600ms
14:50   p50=310ms  p99=640ms
14:55   p50=52ms   p99=94ms
15:00   p50=49ms   p99=90ms
```

`pricing_svc.outbound.taxratevendor.error_rate` (non-2xx or connection
errors), same window: flat at 0% throughout 14:00-15:00. Every call
eventually returns 200 -- none of them fail outright.
