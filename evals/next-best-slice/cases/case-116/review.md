# Slice Review: Add on-call contact to service registration

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
$ pytest services/test_registration.py -v
test_on_call_contact_required PASSED
test_on_call_contact_shown_in_catalog PASSED
2 passed in 0.03s
```

## Reasoning
Adds a required `on_call_contact` field to `POST /services` and surfaces
it on `/catalog`. No existing service rows are affected; the field is
required only for newly registered services.
