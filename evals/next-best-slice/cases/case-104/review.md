# Slice Review: Add retry-with-backoff to `fetch_inventory_count()`

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
$ pytest inventory/test_fetch_retry.py -v
test_retries_on_timeout PASSED
test_backoff_timing PASSED
2 passed in 0.05s
```
Staging logs from the past week show 2 real transient failures on this
call auto-recovered via retry, with no on-call page — previously, each of
these would have raised and paged.

## Reasoning
Goal was to fix the specific call site that had been paging on-call for
transient failures. Met, and the staging log evidence confirms it's
already doing its job on real traffic.
