# Review: Add subscription.status field (active / past_due / cancelled)

**Verdict:** Ready to merge

## Blocking
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
Ran the billing test suite (31 tests, all passing) and confirmed the new
`status` field transitions correctly for 20 real subscriptions replayed
through the last two payment cycles.

## Reasoning
Status transitions correctly track real payment outcomes; no billing
behavior changed.
