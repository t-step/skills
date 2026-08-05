# Slice Review: Add retry backoff to webhook event forwarding

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Retry backoff caps at 5 attempts over roughly 2 minutes; there is no
  dead-letter queue yet for events that exhaust all 5 attempts, so they
  are currently just dropped after logging. Not blocking — this matches
  goal.md's scope, which was to add backoff, not a full DLQ.

## Out of scope
None.

## Verification evidence
```
$ pytest webhooks/test_forwarding.py -v
test_first_attempt_success_no_retry PASSED
test_transient_failure_retries_with_backoff PASSED
test_exhausts_after_five_attempts PASSED
test_exhausted_event_is_logged PASSED
4 passed in 0.4s
```
Staging check: killed the downstream consumer mid-test, confirmed 5
retries with increasing backoff, then confirmed the event was logged as
exhausted once retries ran out.

## Reasoning
Goal was to stop losing forwarded events on the first downstream hiccup by
adding exponential backoff. Implemented and tested exactly as scoped; a
durable dead-letter queue was explicitly deferred.
