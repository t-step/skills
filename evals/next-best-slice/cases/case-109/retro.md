# Slice Retrospective: Add webhook delivery for order-status-change events

## What we proved
A webhook fires correctly when an order's status changes, and retries with
backoff on 4xx/5xx responses up to a configured max attempts — backed by
the four passing tests and a manual staging check against both a working
and a deliberately broken endpoint.

## Assumptions validated
The event-driven dispatch approach (fire a webhook from the status-change
code path) works without needing a separate polling or queue mechanism.

## Assumptions falsified
None.

## Remaining uncertainty
None significant for order-status-change delivery itself; delivery
ordering under rapid, repeated status changes on the same order in a short
window is untested.

## Intentional non-goals
Any webhook management UI (configuring endpoints, viewing delivery logs)
and signature verification for outgoing payloads were both explicitly out
of scope per goal.md — this slice only built the dispatch mechanism and
one event type.

## Architectural consequences
A generic `WebhookDispatcher`, keyed by event type, now exists. Any other
event type can register a webhook handler without new dispatch code.

## Follow-up questions
Which other event types should get webhook support?
