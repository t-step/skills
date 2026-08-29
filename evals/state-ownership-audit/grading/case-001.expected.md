# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** clean-invalidate-on-write-cache

**Why:** `update_price()` is the only writer of `products.price_cents`,
and the Redis cache is only ever populated by `get_price()` from a value
it just read out of Postgres on a miss; `update_price()` deletes the key
rather than writing through it a new value. Structurally, this cache
cannot hold an independently-sourced value -- it is always either absent
or a copy of something just read from the authority. The trap is the
ticket's framing: a customer briefly saw a stale price, which reads like
"these can drift" and invites a reconciliation-job "fix." A correct audit
recognizes that the *ordinary* propagation delay this ticket describes is
the cache's designed, self-correcting staleness bound, not evidence of an
authority gap, and declines the reconciliation job as solving a problem
that doesn't exist for a cache that is invalidate-then-repopulate by
construction.

**Update after first with-skill run:** the graded run (see
`runs/2026-08-29-iteration-1.md`) additionally found a real, narrower
finding this key did not originally anticipate: because `update_price()`'s
`UPDATE` and `r.delete()` are two separate, non-atomic steps, a concurrent
`get_price()` cache-miss read that reads the pre-update price and then
writes it to the cache *after* the `delete()` has already run can silently
re-populate the cache with a stale value that then survives up to the full
TTL (300s), not just the ordinary sub-millisecond gap. This is a genuine,
narrow race in the fixture as written, not a defect in the skill's
reasoning -- treat a report that surfaces this race, states it plainly as
a bounded/self-correcting-by-TTL finding, and still declines to recommend
a *new* reconciliation job or coordinator as fully correct and preferable
to a report that misses it. The bar for this case is: right authority
(Postgres/`update_price()`), right characterization of the cache as
derived (never independently written), and no invented fix -- not "zero
hazards found," which this fixture does not actually guarantee.
