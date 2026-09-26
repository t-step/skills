# checkout-svc request log -- sample of affected requests

Debug-level logging on `checkout-svc` includes the full request context
inline, which turns out to include more than intended:

```
2026-09-26T09:12:04Z trace_id=7f3a9c1e span_id=aa11 svc=checkout-svc
  version=2.14.3 path=async_worker route
  customer_email=maria.delgado@example.com
  shipping_address="482 Larkspur Ave, Apt 3, Denver, CO 80206"
  card=4111********1142 exp=03/28
  status=payment_capture_span_missing

2026-09-26T09:14:51Z trace_id=b02e7d44 span_id=ff02 svc=checkout-svc
  version=2.14.3 path=async_worker route
  customer_email=t.oyelaran@example.com
  shipping_address="19 Birchwood Rd, Austin, TX 78701"
  card=5500********0093 exp=11/27
  status=payment_capture_span_missing

2026-09-26T09:19:33Z trace_id=c9a01f88 span_id=bb77 svc=checkout-svc
  version=2.14.3 path=sync_route
  customer_email=j.harmon@example.com
  shipping_address="7 Mill St, Providence, RI 02903"
  card=4242********0089 exp=07/29
  status=ok
```

Every request flagged `payment_capture_span_missing` this morning
(`trace_id`s `7f3a9c1e` and `b02e7d44` among them) is on `path=async_worker
route`. The one sampled `sync_route` request (`c9a01f88`) has a normal,
fully-linked trace.
