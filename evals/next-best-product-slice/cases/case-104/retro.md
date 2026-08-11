# Slice Retrospective: Add subscription.status field (active / past_due / cancelled)

## What we proved
`subscription.status` correctly reflects a subscription's real payment
state, verified by replaying 20 real subscriptions through two payment
cycles.

## Assumptions validated
Payment outcomes were assumed sufficient to derive status automatically;
confirmed.

## Assumptions falsified
None.

## Remaining uncertainty
None material to this slice.

## Intentional non-goals
This slice did not change anything about what a customer sees on their
account page. The field is populated and correct; how or whether it's
displayed was explicitly out of scope.

## Architectural consequences
Any customer-facing view can now read a subscription's real status
directly from `subscription.status` instead of re-deriving it from raw
payment events.

## Follow-up questions
None.
