# Slice Review: Add per-IP rate limiting (in-process sliding window)

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- The limiter is per-process. Across the 4 running app instances behind
  the load balancer, the effective limit could be up to 4x the configured
  per-instance number under a worst-case traffic distribution across
  instances. Not blocking — the goal was explicit about this tradeoff.

## Out of scope
None.

## Verification evidence
```
$ pytest api/test_rate_limit.py -v
test_101st_request_in_60s_rejected PASSED
test_window_resets_after_60s PASSED
2 passed in 0.05s
```
Manually verified in staging on a single instance: requests 1-100 within a
60-second window succeed, request 101 is rejected with 429.

## Reasoning
Goal was "add rate limiting now, using what's available in this
environment" (see notes on Redis). The in-process sliding window correctly
enforces the stated per-instance limit; the cross-instance ceiling is a
known, named tradeoff, not a defect.
