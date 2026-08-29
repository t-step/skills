# Slice Review: Add webhook delivery for order-status-change events

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
```
$ pytest webhooks/test_dispatch.py -v
test_fires_on_status_change PASSED
test_retries_on_4xx PASSED
test_retries_on_5xx PASSED
test_gives_up_after_max_attempts PASSED
4 passed in 0.15s
```
Manually verified in staging: changing an order's status triggers a
delivery to a test endpoint within a few seconds, and a deliberately
broken endpoint gets retried per the backoff schedule.

## Reasoning
Goal was webhook delivery for order-status-change events specifically,
with retry on failure. Met and verified end to end in staging.
