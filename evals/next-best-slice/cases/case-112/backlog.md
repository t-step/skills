# Backlog / candidate next work

- **Add a cleanup job for expired idempotency-key rows** — small scheduled
  job, deletes rows past their 24-hour window. Nothing depends on this yet
  at current order volume.
- **Add order search by customer email** — support has asked for this a
  few times; would let support find a customer's orders without a
  database query.
- **Add CSV export of orders for finance's month-end close** — finance
  currently asks engineering to run a one-off query every month.
- **Increase the idempotency key retention window from 24 hours to 7
  days** — would cover longer client retry windows, but no client has
  reported a retry beyond 24 hours.
