# Slice Review: Add rollback endpoint for a release

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
$ pytest releases/test_rollback.py -v
test_rollback_reverts_to_prior_version PASSED
test_rollback_is_logged_to_release_events PASSED
test_non_owner_cannot_rollback_403 PASSED
3 passed in 0.03s
```

## Reasoning
Adds `POST /releases/:id/rollback` to revert a release to its prior
version. Every rollback is written to the `release_events` table, the
same audit table `promote` and `deploy` already write to. Access is
restricted to release owners.
