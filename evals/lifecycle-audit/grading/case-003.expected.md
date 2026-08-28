# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** transfer-conservation-genuine-reconciliation

**Why:** Each FC's ledger is independently authoritative by deliberate
design (must keep selling through a network partition), so neither is a
projection of the other -- this rules out the "just a cache" answer.
But a transfer is not merely "sequencing" or "one-way observation"
either: `dispatch()` removes units from the source's authoritative count
before `receive()` adds them to the destination's, and if `receive()`
never runs (the dead-scanner-battery incident), the units are gone from
both ledgers' perspective simultaneously -- a real violation of unit
conservation, which is the actual business invariant at stake, not a
vague "things should match." `reconcile_job.py` shows an active
mechanism exists (the 48h staleness check) but stops at opening a
ticket -- it does not itself decide how to resolve a confirmed mismatch.
The incident retro explicitly leaves that resolution policy an open
question. A correct audit says: yes, this needs reconciliation (unlike
cases 1/2/4/5 in this suite), names the conservation invariant
specifically, explains why neither side is a projection, and separates
"a reconciliation job exists and does X" (mechanical) from "how
mismatches should ultimately be resolved" (unresolved judgment call) --
without inventing a full resolution policy itself.
