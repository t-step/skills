# Accepted Slice: Improve error handling in the payment retry path

## Goal
attempt_charge() should be more resilient to the payment provider's
transient errors -- right now a single transient blip fails the whole
charge attempt, which is causing avoidable declined-looking failures
for real customers.

## Why now
Support has linked several "my card was declined" tickets to
TransientProviderError entries in the provider's own status page during
brief provider outages -- these weren't actual declines.

## What this slice proves
That a charge which fails transiently and then would succeed on a
later attempt no longer surfaces as a failure to the caller.

## Explicit non-goals
Does not change how ChargeDeclinedError is handled -- non-retryable
declines should still fail immediately, as they do today.

## Acceptance evidence
A test showing a charge that fails transiently at least once and then
succeeds no longer raises, and a charge that fails with
ChargeDeclinedError still raises immediately without retrying.
