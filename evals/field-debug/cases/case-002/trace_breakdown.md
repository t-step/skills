# Trace: sampled `POST /checkout` spans, 14:35 UTC

A representative slow trace (trace id `a1c9-4402`, total 3.91s):

| Span | Service | Start (rel) | Duration |
|---|---|---|---|
| `POST /checkout` | web-bff | 0ms | 3910ms |
| `pricing.get_quote` | web-bff -> pricing-svc | 5ms | 3880ms |
| `pricing_svc.get_tax_rate` | pricing-svc (internal) | 40ms | 3790ms |
| `inventory.reserve` | pricing-svc -> inventory-svc | 3855ms | 42ms |
| `inventory_svc.reserve_stock` | inventory-svc (internal) | 3860ms | 35ms |

For comparison, a trace from before the incident window (14:10 UTC,
trace id `f0e2-1187`, total 188ms):

| Span | Service | Start (rel) | Duration |
|---|---|---|---|
| `POST /checkout` | web-bff | 0ms | 188ms |
| `pricing.get_quote` | web-bff -> pricing-svc | 4ms | 175ms |
| `pricing_svc.get_tax_rate` | pricing-svc (internal) | 38ms | 82ms |
| `inventory.reserve` | pricing-svc -> inventory-svc | 118ms | 44ms |
| `inventory_svc.reserve_stock` | inventory-svc (internal) | 122ms | 37ms |

Ten additional slow traces sampled between 14:32-14:40 UTC all show the
same shape: `inventory_svc.reserve_stock` consistently completes in
30-50ms, and essentially all of the added latency sits inside
`pricing_svc.get_tax_rate`, before the call to inventory-svc even starts.
