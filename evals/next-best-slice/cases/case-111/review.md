# Slice Review: Add phone-number verification to user profiles

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- No end-to-end browser test asserts the verification-success banner for
  phone verification specifically. The component test already asserts
  that the shared `VerificationBanner` component renders the success
  state correctly given a verified prop, and the same banner is already
  covered end-to-end for email verification (a structurally identical
  flow using the same component). Consider adding a dedicated e2e case
  for phone verification to mirror the existing email-verification e2e
  coverage. Not blocking — the behavior is already proven at the
  component layer and the banner code path is shared with email
  verification's own e2e-tested case.

## Out of scope
None.

## Verification evidence
```
$ pytest profiles/test_phone_verification.py -v
test_code_generated_with_expiry PASSED
test_code_persisted_and_marked_used_on_verify PASSED
test_expired_code_rejected PASSED
3 passed in 0.09s

$ npm test -- VerificationBanner
✓ renders pending state
✓ renders success state given verified prop
✓ renders error state given invalid-code prop
3 passed
```
Manually verified in staging: submitting a valid code marks the phone
number verified and persists `phone_verified_at`; the profile page
correctly shows the shared success banner.

## Reasoning
Goal was to let a user verify a phone number the same way email
verification already works: generate an expiring code, verify it, persist
the result. Implemented and tested at the database (code persistence),
unit (code generation/expiry), and component (banner rendering) layers.
