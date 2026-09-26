# Dead-letter queue entry

```json
{
  "event_id": "evt_renewal_88f3_0926",
  "subscription_id": "sub_88f3",
  "customer_id": "cus_5521",
  "amount_cents": 4900,
  "attempt": 1,
  "original_timestamp": "2026-09-26T03:14:02Z",
  "dlq_reason": "unhandled_exception",
  "moved_to_dlq_at": "2026-09-26T03:14:03Z"
}
```

This is the exact message sitting in the DLQ. Replaying it re-runs
`process_renewal()` from the top -- including the call to
`ridgeline.charge()` -- exactly as it ran the first time.
