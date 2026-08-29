# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** incremental-and-periodic-writers-same-authority

**Why:** The naive read is "two writers to `ledger.balance_cents` = bug."
The correct read requires re-anchoring the unit of analysis: the actual
fact is "this account's balance," and its true authoritative source is
the append-only `transactions` table (balance is definitionally the sum
of transactions). `ledger.balance_cents` is a materialized cache of that
sum, kept current two ways -- incrementally in the same DB transaction as
each new append, and periodically recomputed-and-corrected by
`reconcile_balances.py`. Both paths derive their value from the same
single source; neither introduces information the transactions log
doesn't already contain. This is the "two apparent writers where one is
actually reconciliation" trap: a correct audit names the real authority
(transactions), reclassifies both ledger writers as synchronization paths
into the same materialized total, and explicitly rejects the "isn't this
a bug" framing.
