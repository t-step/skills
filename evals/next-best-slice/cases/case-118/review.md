# Slice Review: Add idempotency guard to retry_charge()

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
$ pytest billing/test_retry_charge.py -v
test_retry_does_not_double_charge_same_invoice PASSED
test_retry_allows_new_attempt_after_failure PASSED
test_concurrent_retries_serialize_on_charge_attempts PASSED
3 passed in 0.05s
```

## Reasoning
`retry_charge(invoice_id, attempt_number)` now checks the
`charge_attempts` table (keyed by invoice_id + attempt_number) before
issuing a new charge to the payment processor, and writes to it inside
the same transaction as the charge. Retrying the same attempt no longer
double-charges the customer.
