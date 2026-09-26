# PaymentGate API reference (excerpt) -- POST /v1/captures

```
POST /v1/captures

Body:
  order_id       string, required
  amount_cents   integer, required

Headers:
  Idempotency-Key   string, optional. If provided, PaymentGate returns
                    the original transaction's result for any repeated
                    request carrying the same key within 24 hours,
                    instead of creating a new capture. If omitted, every
                    request is treated as an independent capture attempt
                    with no deduplication, regardless of order_id.
```

Nothing in `payment_client.py` sets an `Idempotency-Key` header on any
request.
