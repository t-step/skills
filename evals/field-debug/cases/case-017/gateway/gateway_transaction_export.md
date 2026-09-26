# PaymentGate transaction ledger export -- order_id=ORD-71042

Pulled directly from PaymentGate's own merchant dashboard export (not
`payments-svc`'s logs) for the same time window:

```
gateway_txn_id | order_id   | amount_cents | status  | received_at              | completed_at
-------------- | ---------- | ------------ | ------- | ------------------------ | ------------------------
gw_88201       | ORD-71042  |    8450      | SUCCESS | 2026-09-23T14:22:07.048Z | 2026-09-23T14:22:11.981Z
gw_88213       | ORD-71042  |    8450      | SUCCESS | 2026-09-23T14:22:12.058Z | 2026-09-23T14:22:13.317Z
```

Both transactions show `status = SUCCESS` and both actually moved funds
-- PaymentGate's own settlement batch for 2026-09-23 includes both
`gw_88201` and `gw_88213` as two separate captures against the same
card, same amount, same `order_id`. `payments-svc` never received
PaymentGate's response for `gw_88201`: its `completed_at`
(`14:22:11.981Z`) is before `payments-svc`'s client-side timeout fired
(`14:22:12.014Z` per `logs/payments_svc_logs.md`), meaning PaymentGate
had already finished and marked the capture successful before
`payments-svc` gave up waiting -- the response for `gw_88201` was
in flight (or never sent/acknowledged) when the client's 5-second
timeout elapsed. Nothing in this export shows `gw_88201` and `gw_88213`
linked, deduplicated, or flagged as related in any way -- PaymentGate
processed them as two independent, unrelated capture requests.
