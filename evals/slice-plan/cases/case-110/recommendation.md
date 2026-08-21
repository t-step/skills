# Accepted Slice: Add phone_verified to the user summary response

## Goal
`get_user_summary(user_id)` should include a `phone_verified` field on
the returned `UserSummary`, reflecting whether the user has completed
phone verification, so the account-security panel (blocked on this API)
can show a verified/unverified badge without a second network round
trip.

## Why now
Security wants the verified-phone badge live before the
account-security panel ships next sprint. Product doesn't want the
panel making a second call just for this one field, since
`get_user_summary` is already the panel's single data source.

## What this slice proves
That `get_user_summary(user_id)` returns a `UserSummary` including
`phone_verified` alongside the existing `display_name`/`email`/
`plan_tier` fields, with the rest of the panel's data unaffected.

## Explicit non-goals
Does not change the `IdentityProfileUpdated` event contract or
`sync_consumer.py`'s subscription to it. Does not add new outbound
calls to Identity from this service. Does not change how
`get_team_roster` batches member lookups.

## Acceptance evidence
A test showing `get_user_summary(user_id)` returns a `UserSummary` with
a `phone_verified` field, and that the existing `display_name`/`email`/
`plan_tier` fields and existing tests continue to pass unchanged.
