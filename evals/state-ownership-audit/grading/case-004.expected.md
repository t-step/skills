# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** async-projection-safe-lag-not-a-defect

**Why:** `order_events` is the sole authoritative, append-only origin of
order facts; `order_summary_view` is an asynchronous, at-least-once,
idempotent projection with a documented p99 lag under 2 seconds and a DLQ
for failures. The observed ~1.5s lag is inside the documented window. The
trap is the support ticket's framing ("looks broken," asking for a
hotfix): a less careful audit either (a) treats any observable staleness
as evidence of a sync bug and recommends making the read synchronous or
adding reconciliation, or (b) doesn't check the lag against a documented
bound at all and just asserts "eventual consistency is fine" without
grounding it. A correct audit does the second checked, not asserted:
names the SLA and DLQ/alerting as the actual evidence the lag is
intentional and bounded, and states plainly this is not a bug.
