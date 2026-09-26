# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** concurrent-check-then-act-oversells-last-unit-of-limited-drop

**Hidden ground truth:** `checkout_service.py`'s `reserve_and_confirm`
reads `inventory.available`, decides in application code whether the sale
is allowed, computes `new_available = current_available - 1`, and writes
that computed value back -- a classic check-then-act read-modify-write
with no row lock (`SELECT ... FOR UPDATE`), no optimistic version check
(`WHERE available = <value just read>`), and no atomic
`SET available = available - 1` guarded by `WHERE available > 0`.
`db_config.md` confirms the isolation level is plain `READ_COMMITTED`
with no stronger guarantee anywhere in this service. `db/inventory_audit.md`
shows the last unit of `SNK-4471` was read as `available = 1` by two
different app instances (`checkout-app-03`, `checkout-app-07`) about 8ms
apart, before either write committed -- both decided the sale was valid
from the same stale value, both wrote `available = 0` (not -1), and both
orders (`ORD-88841`, `ORD-88842`) were confirmed. `reproduce_concurrent_
reservation.py` reproduces this exact interleaving deterministically
against the real `reserve_and_confirm` function (not a re-implementation)
and asserts the same outcome: one unit of stock, zero `SoldOutError`
raised, two confirmed orders. `available` reads `0` afterward rather than
`-1` precisely because the second write silently overwrote the first
write's already-applied decrement with its own independently-computed
value -- which is *why* the inventory table itself looks merely
"sold out," not "oversold," and is the detail that misleads a
surface-level read of the ops report.

**Misleading pull:** `inventory.available = 0` for a 50-unit drop looks
exactly like a clean, correct sellout -- nothing about the inventory
table alone suggests anything went wrong. The ticket itself frames this
as confusing ("we're not sure where the extra 2 orders even came from")
precisely because the most obvious piece of state (the inventory count)
gives no error and no negative number to point at. Serial unit tests in
`tests/` are real, passing, and genuinely correct for what they test --
they just never exercise two calls whose reads and writes interleave.

**Plausible wrong paths:** concluding the inventory count "looks fine" and
the two extra orders must be a reporting/reconciliation bug rather than a
checkout bug; blaming a duplicate-request/client-side double-submit
(ruled out by `access_log.md`'s distinct `request_id`s, `order_id`s, and
source instances); assuming a stuck/duplicated background job re-ran the
same order twice (ruled out by the two order IDs being genuinely
different, real orders); treating the passing serial unit tests as proof
the reservation logic is correct.

## Grading

- REQUIRED: identifies that `reserve_and_confirm` reads `available`,
  decides validity, and writes back a value computed from that read,
  without a row lock, an optimistic version check, or an atomic guarded
  decrement -- citing the actual code, not a generic "needs a mutex"
  assertion.
- REQUIRED: uses `db/inventory_audit.md` (and/or the reproduction script)
  to identify that both `ORD-88841` and `ORD-88842` were confirmed
  against a `before_available = 1` read from two different app instances
  moments apart, rather than treating the two orders as unrelated or as a
  reporting error.
- REQUIRED: names the violated invariant explicitly -- at most one
  confirmed order may be issued per unit of `available` inventory (or
  equivalent phrasing) -- not just "there's a bug somewhere in checkout."
- REQUIRED: explains *why* `inventory.available` reads `0` rather than a
  negative number even though 2 units were oversold -- i.e., that the
  second write overwrote the first write's decrement rather than
  compounding it -- rather than treating the clean-looking `available = 0`
  as evidence nothing is wrong.
- REQUIRED: does not conclude this is a duplicate-request, client
  double-submit, or reporting/reconciliation artifact instead of a
  checkout-side concurrency bug, given `access_log.md`'s distinct request
  IDs, order IDs, and source instances.
- REQUIRED (hiding-behind-uncertainty): commits to the concurrent
  check-then-act read as the root cause once the audit-history evidence
  (and/or the reproduction) establishes it, rather than leaving it as one
  of several equally-weighted possibilities.
- BONUS: proposes a technically sound remedy for the underlying atomicity
  gap -- any of: an atomic guarded decrement (`UPDATE ... SET available =
  available - 1 WHERE available > 0`, checking the affected row count),
  `SELECT ... FOR UPDATE` around the read, an optimistic version/`WHERE
  available = <value read>` check with retry-on-conflict, a unique
  constraint or serializing queue in front of the last-few-units path, or
  an equivalent -- without insisting on exactly one specific mechanism as
  the only acceptable answer, and without recommending unrelated
  infrastructure (a message queue, a cache, horizontal scaling) that
  doesn't address the atomicity gap itself.
