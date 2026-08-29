# Slice Review: Canary rollout of new checkout flow (5% of traffic)

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- The canary ran 4 days at 5% of traffic (~3,200 new-flow checkout
  sessions vs. ~1,600 old-flow sessions in the held-back comparison group).
  Error rate: 1.28% (old flow) vs. 1.39% (new flow). Data eng reviewed this
  delta and flagged it as within normal day-to-day noise for this sample
  size — not statistically significant at any conventional threshold.

## Out of scope
None.

## Verification evidence
```
$ pytest checkout/test_new_flow.py -v
... 12 passed
```
Canary dashboard export attached to the PR: session counts, error rate, and
completion-time comparison as above. No crash or automatic rollback
triggered during the 4-day run.

## Reasoning
The new checkout flow's code is correct per its own tests, and the canary
ran without operational incident. Whether the new flow is actually as safe
as the old one on error rate is not settled by this sample — noted as a
finding for whoever decides what happens next, not a defect in this diff.
