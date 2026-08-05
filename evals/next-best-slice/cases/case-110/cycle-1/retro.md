# Slice Retrospective: Verify inbound payment-provider webhook signatures

## What we proved
`POST /webhooks/payment-provider` now verifies the provider's HMAC
signature and dedups on event id before processing, backed by the four
passing unit tests and a manual staging check against the provider's
signed test events.

## Assumptions validated
The provider's documented signature scheme could be verified without
requiring any change to how events are processed once accepted.

## Assumptions falsified
None.

## Remaining uncertainty
Invalid-signature requests are indistinguishable in logs and metrics from
ordinary internal errors — the handler logs them at the same ERROR tag
used for unrelated bugs. We currently have no way to tell a burst of
invalid-signature attempts (which could mean someone is probing the
endpoint, or that the shared secret was rotated and a config wasn't
updated) from unrelated internal failures.

## Intentional non-goals
Rate limiting or blocking repeat offenders was out of scope per goal.md —
this slice only added verification and dedup.

## Architectural consequences
A signature-verification helper and an event-id dedup table now exist for
this endpoint.

## Follow-up questions
Should invalid-signature attempts be logged and counted distinctly from
other failures, so a spike is visible instead of blending into general
error noise?
