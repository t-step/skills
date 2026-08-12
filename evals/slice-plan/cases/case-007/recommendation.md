# Accepted Slice: Rate-limit password-reset requests

## Goal
Add rate limiting to request_password_reset() so a single email
address can trigger at most 5 reset requests per hour. The 6th and
later request within that hour should be rejected with a 429 status
and a generic message, the same generic message a normal request
returns, so the rate-limit response itself can't be used to tell
whether an account exists.

## Why now
Security review flagged that the password-reset endpoint has no
throttling, which lets an attacker enumerate registered email
addresses by hammering the endpoint at volume and watching for
behavioral differences.

## What this slice proves
That requesting a password reset for the same email six times within
an hour returns a 429 on the sixth request, and that requests one
through five continue to succeed and trigger the reset email exactly
as before.

## Explicit non-goals
Does not add rate limiting to any other endpoint, does not add a
configurable limit setting, does not change send_reset_email() itself.

## Acceptance evidence
A test showing the sixth reset request for the same email within an
hour returns 429, and that requests one through five continue to
return 200 and call send_reset_email().
