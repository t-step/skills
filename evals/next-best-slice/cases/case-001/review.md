# Slice Review: Add JWT authentication middleware

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- `middleware/auth.py` logs the raw `Authorization` header at DEBUG level.
  Consider redacting before this log sink is shared more broadly. Not
  blocking for this slice.

## Out of scope
None.

## Verification evidence
```
$ pytest middleware/test_auth.py -v
test_valid_token_passes PASSED
test_missing_token_rejected_401 PASSED
test_expired_token_rejected_401 PASSED
test_malformed_token_rejected_401 PASSED
4 passed in 0.06s
```
Manually verified in staging: `GET /api/whoami` with a valid token returns
200 with the decoded user id; without a token returns 401.

## Reasoning
Goal was to add a `require_auth` decorator backed by JWT verification, with
no existing endpoint required to use it yet. All four token-shape cases are
covered by tests and staging confirms end-to-end behavior. No existing
route currently uses the decorator, so this slice is additive only and
changes no existing behavior.
