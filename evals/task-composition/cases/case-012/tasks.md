# Tasks: Webhook Subscriptions

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `POST /webhooks/subscriptions` endpoint in `api/webhooks.py`
  accepting `{url, event_types}`.
- T2: Add validation in `api/webhooks.py`'s handler for T1 -- reject a
  non-HTTPS `url`, reject any `event_types` value outside the known set.
- T3: Add `create_subscription(url, event_types)` in
  `storage/webhook_store.py`, writing a row to the
  `webhook_subscriptions` table and returning its generated `id`.
- T4: Wire the POST handler (T1) to call `create_subscription` (T3) once
  validation (T2) passes, returning the created subscription's `id` in
  the response body.
- T5: Add `GET /webhooks/subscriptions/{id}` in `api/webhooks.py`,
  reading the row back via `storage/webhook_store.py` and returning 404
  if no subscription with that `id` exists.
- T6: Add test `tests/test_webhook_subscriptions.py` covering POST (a
  valid payload creates a subscription and returns its id; an invalid
  `url` or `event_types` value returns 400 with no row written) and GET
  (returns the subscription that was created; an unknown id returns
  404).

Before T4, calling `POST /webhooks/subscriptions` with a valid payload
returns success without writing anything to `webhook_subscriptions`.
Before T3 exists, there is nothing for the endpoint to call to persist a
subscription. No priority is stated between these tasks.
