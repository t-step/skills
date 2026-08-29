# Slice Retrospective: Add idempotency keys to POST /orders

## What we proved
`POST /orders` now accepts a client-supplied idempotency key, persists it
against the resulting order, and returns the original order (not a
duplicate) when the same key is replayed within 24 hours — backed by four
passing tests and a staging replay check.

## Assumptions validated
A simple key-to-order lookup table, checked before order creation runs,
is enough to make retries safe without any change to the order-creation
logic itself.

## Assumptions falsified
None.

## Remaining uncertainty
No cleanup job exists for expired idempotency-key rows yet; at current
volume this won't matter for months, but there's no data on how it
behaves once volume grows.

## Intentional non-goals
Applying the same mechanism to other write endpoints was out of scope
per goal.md — this slice only covers order creation.

## Architectural consequences
There is now a generic `idempotency_keys` table and a
`require_idempotency_key(handler)` wrapper that any other write endpoint
in this service could adopt to get the same duplicate-request protection.
`POST /payments/:id/capture` is the only other write endpoint in this
service that mutates money and has no such protection today — it has been
the subject of two known duplicate-charge incidents (INC-4432, INC-4501),
both traced to a client retrying after a timeout with no idempotency
guard in place.

## Follow-up questions
Now that a reusable idempotency mechanism exists, should payment
capture — the endpoint with actual documented duplicate-charge
incidents — adopt it next, instead of building a bespoke guard for it
later?
