# checkout-svc -> PaymentCo request log (excerpt + aggregate)

Raw sample, `2026-09-20T11:14:0*Z` (each line is one `charge()` call;
`pod` is the instance that actually issued the request, taken from the
pod's own hostname in its log prefix):

```
2026-09-20T11:14:01Z pod=checkout-pod-01 order_id=ORD-51200 status=200
2026-09-20T11:14:02Z pod=checkout-pod-03 order_id=ORD-51201 status=401 error="invalid_api_key"
2026-09-20T11:14:03Z pod=checkout-pod-08 order_id=ORD-51202 status=200
2026-09-20T11:14:04Z pod=checkout-pod-05 order_id=ORD-51203 status=401 error="invalid_api_key"
2026-09-20T11:14:05Z pod=checkout-pod-02 order_id=ORD-51204 status=200
2026-09-20T11:14:06Z pod=checkout-pod-06 order_id=ORD-51205 status=401 error="invalid_api_key"
2026-09-20T11:14:07Z pod=checkout-pod-04 order_id=ORD-51206 status=401 error="invalid_api_key"
2026-09-20T11:14:08Z pod=checkout-pod-07 order_id=ORD-51207 status=401 error="invalid_api_key"
2026-09-20T11:14:09Z pod=checkout-pod-01 order_id=ORD-51208 status=200
2026-09-20T11:14:10Z pod=checkout-pod-03 order_id=ORD-51209 status=401 error="invalid_api_key"
```

Every `401` in the full day's log carries the identical
`error="invalid_api_key"` reason from PaymentCo's own response body --
not a card-decline reason, not a fraud-hold reason, not a timeout.

Full-day aggregate, grouped by pod (400 charge attempts total,
2026-09-19T09:12Z through 2026-09-20T11:20Z, i.e. starting just after the
rollout paused):

```
pod              | attempts | 200 (success) | 401 (invalid_api_key)
---------------- | -------- | -------------- | ----------------------
checkout-pod-01  |    50    |      50        |     0
checkout-pod-02  |    50    |      50        |     0
checkout-pod-08  |    50    |      50        |     0
checkout-pod-03  |    50    |       0        |    50
checkout-pod-04  |    50    |       0        |    50
checkout-pod-05  |    50    |       0        |    50
checkout-pod-06  |    50    |       0        |    50
checkout-pod-07  |    50    |       0        |    50
---------------- | -------- | -------------- | ----------------------
total            |   400    |     150        |   250   (62.5%)
```

Every single attempt on `checkout-pod-01`, `-02`, and `-08` succeeded.
Every single attempt on `checkout-pod-03`, `-04`, `-05`, `-06`, and `-07`
failed with the same error. No pod has a mix of both outcomes.
