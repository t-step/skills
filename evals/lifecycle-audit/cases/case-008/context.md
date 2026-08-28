# Context

Excerpts from Risk (`user_trust.py`) and Trust & Identity
(`verification.py`), both operating on fields of the same `User` row.
`checkout/limits.py` (which reads `trust_level`), `nightly_batch.py`,
and the fraud-review case-management tool are not included; treat
anything not shown here as not available for this review.

An excerpt from a design-review comment thread, forwarded for context:

> **On a PR proposing a `/admin/users/:id/trust-history` endpoint:**
>
> "Since we already log every `trust_level` change to
> `TrustLevelHistory` with old/new/timestamp, could this endpoint also
> support 'revert to previous trust level' the same way
> `revoke_verification_for_fraud` works for verification? Trying to give
> support agents a consistent mental model across the two fields --
> both are 'levels a user can be at,' both changed at some point, both
> have a history table."
