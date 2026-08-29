# Slice Review: Fix memory leak in job-worker completed-job-ID tracking

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
$ pytest worker/test_loop.py -v
test_completed_ids_bounded PASSED
1 passed in 0.02s
```
Local repro: RSS stayed flat at ~85MB over a 2-hour run with the fix,
versus growing past 340MB before it.

## Reasoning
Goal was to fix the leak caused by an unbounded in-memory set of completed
job IDs. Met — replaced with a bounded deque, confirmed by both the test
and the repro's memory behavior.
