# inventory audit history -- SNK-4471 (excerpt)

`checkout-drops`'s Postgres instance has row-level audit logging on
`inventory` (a trigger writes one row per `UPDATE` to `inventory_audit`,
capturing the value before and after the statement, the transaction id,
and which app instance issued it). Full history for SNK-4471 during the
drop is ~50 rows; the first 47 are one decrement per order, strictly
serial, no two transactions overlapping (each `before_available` matches
the prior row's `after_available`). The last few rows, where the drop's
final unit sold, are reproduced in full below.

```
txn_id | ts                       | app_instance      | before_available | after_available | order_id
------ | ------------------------ | ----------------- | ---------------- | --------------- | ----------
t0512  | 2026-09-20T14:03:19.740Z | checkout-app-02   | 3                | 2               | ORD-88839
t0513  | 2026-09-20T14:03:20.101Z | checkout-app-05   | 2                | 1               | ORD-88840
t0514  | 2026-09-20T14:03:21.203Z | checkout-app-03   | 1                | 0               | ORD-88841
t0515  | 2026-09-20T14:03:21.211Z | checkout-app-07   | 1                | 0               | ORD-88842
```

`t0512` and `t0513` are ordinary serial decrements -- each transaction's
`before_available` is the previous transaction's `after_available`,
exactly as expected for one worker at a time. `t0514` and `t0515` are
the last two rows for this SKU: both show `before_available = 1`, and
both show `after_available = 0` -- the row was read at `1` twice before
either write committed, roughly 8ms apart, from two different app
instances. `orders` has both `ORD-88841` and `ORD-88842` marked
`confirmed` against `SNK-4471`.

A grep of the full audit export for any other SKU sold during Friday's
run turns up one more `before_available`-collision pair earlier in the
same drop (`ORD-71053` / `ORD-71054`, `checkout-app-01` and
`checkout-app-06`, `14:01:47.3xxZ`, same `before_available`/
`after_available` signature) -- not reproduced row-by-row here, but
consistent with the same pattern occurring twice across the full drop,
which lines up with finance's count of 2 extra confirmed orders against
a 50-unit stock.
