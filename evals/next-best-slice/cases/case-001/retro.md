# Slice Retrospective: Add JWT authentication middleware

## What we proved
The `require_auth` decorator in `middleware/auth.py` correctly accepts a
valid JWT and rejects a missing, expired, or malformed token with 401,
backed by the four passing unit tests and a manual staging check against
`GET /api/whoami`.

## Assumptions validated
The assumption that JWT verification could be added as a decorator without
touching existing route registration was validated — no existing route had
to change to add the capability.

## Assumptions falsified
None.

## Remaining uncertainty
No endpoint currently uses `require_auth` in production, so real-traffic
behavior (token refresh flows, clock-skew edge cases at scale) is untested.

## Intentional non-goals
Token refresh/rotation, and applying the decorator to any existing
endpoint, were explicitly out of scope per goal.md — this slice only adds
the capability.

## Architectural consequences
Any route can now require authentication by adding one decorator.
Previously no such mechanism existed anywhere in the codebase.

## Follow-up questions
Which existing endpoints, if any, should require auth first?
