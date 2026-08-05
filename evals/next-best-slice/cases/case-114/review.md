# Slice Review: On-call history log

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
$ pytest oncall/test_log.py -v
test_contact_change_appends_log_row PASSED
test_log_row_captures_old_and_new_contact PASSED
test_log_is_append_only PASSED
3 passed in 0.04s
```

## Reasoning
Adds an `on_call_log` table and appends a row (service id, old contact,
new contact, timestamp) whenever a service's on-call contact changes via
`PATCH /services/:id`. No UI reads from it yet — this slice only adds
the persistence and the write path.
