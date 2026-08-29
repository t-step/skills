# Slice Review: Add idempotency keys to POST /orders

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Idempotency keys are stored with a 24-hour retention window and no
  cleanup job yet; rows will accumulate indefinitely until one is added.
  Not blocking — current order volume makes this a non-issue for months.

## Out of scope
None.

## Verification evidence
```
$ pytest orders/test_idempotency.py -v
test_duplicate_key_returns_cached_response PASSED
test_distinct_keys_create_distinct_orders PASSED
test_missing_key_rejected PASSED
test_expired_key_treated_as_new PASSED
4 passed in 0.18s
```
Manually verified in staging: replaying the same `POST /orders` request
with the same idempotency key returns the original order instead of
creating a duplicate.

## Reasoning
Goal was to stop duplicate order creation when a client retries
`POST /orders` after a timeout, by requiring an idempotency key and
returning the cached response for a repeated key. Implemented and tested
exactly as scoped.
