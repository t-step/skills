# Accepted Slice: Reject overly long usernames at signup

## Goal
Add a maximum-length check to validate_username() -- usernames longer
than 24 characters should be rejected with a clear error message, the
same way validate_username() already rejects too-short, badly-started,
or invalid-character usernames.

## Why now
Support flagged that a handful of signups used 200+ character
usernames (copy-pasted from elsewhere), which break the profile page
layout. No existing check catches this.

## What this slice proves
That validate_username() correctly rejects a username of 25+
characters with a clear error message, and that existing valid/invalid
cases are unaffected.

## Explicit non-goals
Does not change MIN_LENGTH, does not add a max-length setting anywhere
else in the app, does not touch the signup HTTP handler beyond calling
the existing validator.

## Acceptance evidence
A new unit test showing a 25-character username produces a "username
must be at most 24 characters" error, and the existing test suite in
tests/test_validators.py still passes unchanged.
