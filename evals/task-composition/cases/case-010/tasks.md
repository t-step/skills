# Tasks: Order/Invoice Total Cross-Check

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add an `Order.total` property in `orders.py`. Its value is
  computed by calling `Invoice.compute_total(order)` from `invoicing.py`
  (added in T2) and returning that result.
- T2: Add `Invoice.compute_total(invoice)` in `invoicing.py`. Its
  computation reads `invoice.order.total` (the `Order.total` property
  added in T1) as its starting point, then adds tax and fees on top of
  it.
- T3: Add test `tests/test_order_invoice_totals.py` covering both T1 and
  T2 together.

Neither T1 nor T2 can be completed without the other already existing:
T1's implementation calls into T2, and T2's implementation reads T1's
result. No priority is stated between them.
