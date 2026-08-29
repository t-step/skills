# Slice Review: Verify inbound payment-provider webhook signatures

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- When HMAC signature verification fails, the handler returns a generic
  500 and logs at ERROR with the same tag used for unrelated internal
  failures. Not blocking for this slice — verification itself is correct
  and tested — but nothing distinguishes a rejected-signature request from
  an ordinary bug in the logs or metrics.

## Out of scope
None.

## Verification evidence
```
$ pytest webhooks/test_signature.py -v
test_valid_signature_accepted PASSED
test_missing_signature_rejected PASSED
test_invalid_signature_rejected PASSED
test_replayed_event_id_deduped PASSED
4 passed in 0.11s
```
Manually verified in staging against the provider's signed test events:
a valid signature is accepted and processed exactly once per event id; an
invalid signature is rejected.

## Reasoning
Goal was to add HMAC signature verification and event-id dedup to
`POST /webhooks/payment-provider` before this endpoint processes anything
from the provider. Both are implemented and tested. No prior version of
this endpoint verified anything at all.
