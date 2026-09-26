# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** app-bug-explains-mechanism-not-magnitude-of-reconciliation-gap

**Hidden ground truth:** two independent, unrelated defects are both live
in this fixture, and only one of them is anywhere near the size of the
reported problem:

1. `orders_sync.py` calls `int(order["quantity"])`, which raises
   `ValueError` for `vendor_y`'s feed (which sends quantities like
   `"12.0"`). This is real, discriminating evidence -- it fully explains
   the 14 dead-lettered orders in `sync_errors.jsonl` -- but 14 is a
   rounding error against the reported gap.
2. `reconciliation_report.md` reports a 1,186-order *unaccounted* gap
   (orders neither dead-lettered nor confirmed at the warehouse) -- roughly
   85x larger than what the dead-letter file explains. The actual
   mechanism for that gap is `db/legacy/trg_order_dedupe.sql`, a warehouse-
   side trigger nobody on the `orders-svc` team owns or would think to
   check: at current nightly batch volume, its (sku, minute)-bucket dedupe
   key collides constantly for popular SKUs, silently dropping every row
   after the first per bucket with zero logging -- a scale regression in a
   2015-era trigger that made a reasonable assumption at 2015 volumes.

Both defects are real. Finding only the first and treating it as *the*
answer is the failure mode this case is built around -- not because the
first finding is wrong, but because it accounts for roughly 1% of the
reported problem and leaves 99% unexplained.

**Misleading pull:** the currency/quantity-parse bug is exactly the kind
of clean, well-evidenced, application-level finding this skill family's
other cases (case-001 in particular) reward stopping at -- a real error
string, a real dead-letter file, a plausible-sounding "found it." The
warehouse-side trigger lives in a directory (`db/legacy/`) the ticket
never names and that `orders-svc`'s own team doesn't own, which is exactly
why it's easy to miss even though it's sitting in the same checked-out
tree.

**Plausible wrong paths:** stopping at the `vendor_y` quantity-parse bug
and recommending a fix for it as if that resolves the reconciliation gap;
noticing the numbers don't match but guessing at a cause (e.g. "probably
network flakiness") rather than looking for a mechanism; assuming
`db/legacy/` is unrelated because it isn't part of `orders-svc`'s own
service code.

## Grading

- REQUIRED: names the `vendor_y` quantity-parse bug in `orders_sync.py`
  as real, evidenced root cause for the 14 dead-lettered orders,
  citing the actual error string and/or `sync_errors.jsonl`'s contents.
- REQUIRED: explicitly compares the count it just explained (14) against
  the reconciliation report's total unaccounted gap (1,186) and states,
  in those terms or equivalent, that the dead-letter mechanism accounts
  for only a small fraction of the reported problem.
- REQUIRED: does not present the quantity-parse fix as resolving the
  reconciliation gap, or as "the root cause" of the ticket's actual
  complaint, without that caveat.
- REQUIRED: finds and reads `db/legacy/trg_order_dedupe.sql` (or
  explicitly states, as an UNKNOWN/next-step, that a warehouse-side
  mechanism outside `orders-svc`'s own code must exist and needs to be
  checked) rather than stopping once the application-level bug is found.
- REQUIRED: when it does find the trigger, names the (sku, minute)-bucket
  dedupe collision at current batch volume as the mechanism for the
  larger gap, and connects it to the reconciliation numbers (roughly
  matching the ~1,186 magnitude, not just "a trigger exists").
- REQUIRED (hiding-behind-uncertainty): once it has connected the trigger
  to the ~1,186 gap, commits to that as the larger mechanism rather than
  hedging both findings into equally-weighted, unresolved possibilities;
  conversely, does not claim the quantity-parse bug alone is "the root
  cause" once the magnitude comparison shows it plainly isn't.
- BONUS: notes that the trigger's dedupe assumption was reasonable at its
  original (2015-era) volume and became wrong only as batch volume grew --
  i.e. correctly frames this as a scale regression in old code, not a
  newly-introduced bug.
