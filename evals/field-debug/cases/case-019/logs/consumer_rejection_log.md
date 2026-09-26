# shipping-label-consumer rejection log (excerpt, since v2.6 release)

```
2026-09-24T08:14:02Z ERROR rejected message evt-88213: 1 validation error for OrderCreatedEvent
shipping_method
  field required (type=value_error.missing)
2026-09-24T08:14:19Z ERROR rejected message evt-88214: 1 validation error for OrderCreatedEvent
shipping_method
  field required (type=value_error.missing)
2026-09-24T08:15:03Z ERROR rejected message evt-88215: 1 validation error for OrderCreatedEvent
shipping_method
  field required (type=value_error.missing)
2026-09-24T08:16:41Z ERROR rejected message evt-88216: 1 validation error for OrderCreatedEvent
shipping_method
  field required (type=value_error.missing)
```

Every `order.created` message received since `order-events-producer`
v2.6's release (`2026-09-24T08:00:00Z`) has been rejected with this
identical error -- 100% rejection rate, no successful label generated
since. No message before the release shows this error anywhere in the
retained log history. No other rejection reason appears anywhere in this
log since the release either.
