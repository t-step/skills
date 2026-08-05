# Slice Retrospective: Add phone-number verification to user profiles

## What we proved
A user can now verify a phone number via an expiring code, backed by
passing database-layer tests (code persistence and use-once marking),
unit tests (code generation and expiry), and a component test confirming
the shared `VerificationBanner` renders correctly for the verified state.
Manually confirmed end-to-end in staging.

## Assumptions validated
The existing `VerificationBanner` component, already exercised end-to-end
by the email-verification flow, renders identically regardless of which
channel (email or phone) triggered it — validated by the component test
asserting the same rendering path from the same `verified` prop that the
email flow already uses.

## Assumptions falsified
None.

## Remaining uncertainty
Emoji/unicode phone number labels (some international formats) weren't in
the fixture set for code generation and are untested.

## Intentional non-goals
SMS delivery cost optimization (e.g. provider fallback) was out of scope
per goal.md — this slice only added the verify-and-persist capability
using the existing SMS provider integration.

## Architectural consequences
A phone number can now be verified and is persisted as a trusted
attribute on the user profile (`profile.phone_verified_at`) — the first
channel besides email this system has ever been able to verify. Account
recovery today depends entirely on email: a user who has lost access to
their email currently has no way to recover their account at all, even
though the profile can now hold a second verified contact method.

## Follow-up questions
Now that a verified phone number is a real, persisted capability and not
just an email-only concept, should anything that currently depends solely
on verified email — account recovery, notification opt-in, 2FA — be able
to use it too?
