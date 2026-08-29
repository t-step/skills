# Tasks: Webhook Delivery System

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `SlackWebhookHandler.send(event)` in `webhooks/slack.py`. It
  calls `webhook_signing.sign_payload(payload, secret)` (added in T4) to
  sign the outgoing payload before POSTing it to Slack.
- T2: Add `EmailWebhookHandler.send(event)` in `webhooks/email.py`. It
  calls `webhook_signing.sign_payload(payload, secret)` (added in T4) to
  sign the payload before including it in the email body.
- T3: Add `DeliveryQueue` in `webhooks/queue.py`, replacing synchronous
  delivery with a background worker pool that retries failed deliveries
  with exponential backoff. This introduces concurrency that didn't
  exist before: multiple worker threads may pull from the queue at the
  same time, and whether `DeliveryQueue`'s dequeue operation is actually
  safe under concurrent access has not been verified.
- T4: Add `webhook_signing.sign_payload(payload, secret) -> str` in
  `webhooks/signing.py` (HMAC-SHA256), used by T1 and T2.
- T5: Add `dispatch_event(event, handlers)` in `webhooks/dispatch.py`.
  It routes an event to whichever of `SlackWebhookHandler` (T1) and
  `EmailWebhookHandler` (T2) are configured, enqueuing each delivery via
  T3's `DeliveryQueue` instead of calling `send()` directly.
- T6: Add test `tests/test_signing.py` covering T4.
- T7: Add test `tests/test_slack_handler.py` covering T1.
- T8: Add test `tests/test_email_handler.py` covering T2.
- T9: Add a concurrency test, `tests/test_queue_concurrency.py`, that
  drives T3's `DeliveryQueue` from multiple concurrent worker threads
  and checks for lost or duplicated deliveries.
- T10: Add end-to-end test `tests/test_dispatch_e2e.py` covering T5:
  dispatches an event to both handlers via the queue and confirms both
  are eventually delivered.

`webhooks/slack.py`, `webhooks/email.py`, `webhooks/queue.py`,
`webhooks/signing.py`, and `webhooks/dispatch.py` are five separate
files; nothing in this plan states that any two of them share a file.
No priority is stated across the whole list.
