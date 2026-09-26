# payments-svc application log -- ORD-71042 (full, this order only)

```
2026-09-23T14:22:07.001Z INFO capture_payment(ORD-71042, 8450) started (attempt 1)
2026-09-23T14:22:12.014Z WARNING capture_payment(ORD-71042) request timed out after 5.0s -- retrying
2026-09-23T14:22:12.031Z INFO capture_payment(ORD-71042, 8450) started (attempt 2)
2026-09-23T14:22:13.402Z INFO capture_payment(ORD-71042) succeeded, gateway_txn_id=gw_88213
2026-09-23T14:22:13.410Z INFO order ORD-71042 marked status=paid
```

This is the complete log for `ORD-71042` -- no other `capture_payment`
or order-status lines exist for this order anywhere in `payments-svc`'s
logs. Nothing here is marked `ERROR`; the only anomaly is the one
`WARNING` line. `order.status` shows exactly one transition, to `paid`,
recorded once.
