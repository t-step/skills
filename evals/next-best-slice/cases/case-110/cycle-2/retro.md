# Slice Retrospective: Add retry backoff to webhook event forwarding

## What we proved
Forwarding a verified webhook event to internal consumers now retries up
to 5 times with exponential backoff on transient failure, backed by the
four passing tests and a staging kill-the-consumer check.

## Assumptions validated
Most downstream forwarding failures in this system are transient (the
consumer briefly unavailable) rather than permanent — backoff alone
resolved every failure injected during staging testing within the 5
attempts.

## Assumptions falsified
None.

## Remaining uncertainty
There's no data yet on how often real production events exhaust all 5
attempts, so the dead-letter-queue retry threshold (how long to keep
retrying before giving up permanently) is still just the retry library's
default value, not something tuned to this service's actual traffic.

## Intentional non-goals
A durable dead-letter queue for exhausted events was out of scope per
goal.md — this slice only added the backoff/retry mechanism itself.

## Architectural consequences
Webhook forwarding now goes through a shared `with_backoff` wrapper that
any other at-least-once delivery path in this service could reuse.

## Follow-up questions
Once we have production data, is 5 attempts / ~2 minutes the right
exhaustion threshold, or does it need tuning?
