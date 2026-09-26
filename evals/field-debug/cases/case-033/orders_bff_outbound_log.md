# orders-bff outbound call log -- Meridian fulfillment gateway (excerpt)

Overnight batch window: 02:10-02:20 UTC. `orders-bff` submitted 3,145
fulfillment requests to Meridian's gateway in this window; 3,140
completed normally (completion webhook received within SLA, verified
against `fulfillment-webhook-receiver`'s own log). The five below are the
ones still stuck.

```
02:14:03.112 UTC  POST https://gateway.meridian-fulfillment.example/v2/fulfillment/submit
  order_id=ORD-88231 customer_id=CU-40821 warehouse_id=WH-12
  sku=SKU-2291 qty=1 ship_address=<validated, matches schema v2>
  -> 202 Accepted  X-Meridian-Correlation-Id: MF-88231-CORR

02:14:05.884 UTC  POST .../v2/fulfillment/submit
  order_id=ORD-88232 customer_id=CU-40855 warehouse_id=WH-12
  sku=SKU-1187 qty=2 ship_address=<validated, matches schema v2>
  -> 202 Accepted  X-Meridian-Correlation-Id: MF-88232-CORR

02:14:07.220 UTC  POST .../v2/fulfillment/submit
  order_id=ORD-88233 customer_id=CU-40860 warehouse_id=WH-12
  sku=SKU-3350 qty=1 ship_address=<validated, matches schema v2>
  -> 202 Accepted  X-Meridian-Correlation-Id: MF-88233-CORR

02:14:09.001 UTC  POST .../v2/fulfillment/submit
  order_id=ORD-88234 customer_id=CU-40871 warehouse_id=WH-12
  sku=SKU-2291 qty=1 ship_address=<validated, matches schema v2>
  -> 202 Accepted  X-Meridian-Correlation-Id: MF-88234-CORR

02:14:11.407 UTC  POST .../v2/fulfillment/submit
  order_id=ORD-88235 customer_id=CU-40903 warehouse_id=WH-12
  sku=SKU-4410 qty=3 ship_address=<validated, matches schema v2>
  -> 202 Accepted  X-Meridian-Correlation-Id: MF-88235-CORR
```

All five payloads were validated by `orders-bff` against Meridian's
published request schema (v2) before sending -- schema validation passed
for all five, exactly as it did for the other 3,140 orders in this
window.

Cross-referencing `warehouse_id` across the full batch: these five are
the *only* orders in tonight's batch targeting `warehouse_id=WH-12`. No
other order in tonight's 3,145-order batch used WH-12. WH-12 itself is
not a new or untested route through this integration -- 41 WH-12 orders
went through Meridian and completed normally two nights ago.
