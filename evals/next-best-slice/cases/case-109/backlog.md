# Backlog / candidate next work

- **Add webhook support for "order-cancelled" events**, reusing
  `WebhookDispatcher` directly. A merchant partner explicitly asked for
  this in a support thread last week — the most-requested next event type
  by a wide margin in that thread.
- **Add webhook support for "inventory-low" events.**
- **Build a webhook management UI** (configure endpoints, view delivery
  logs, retry failed deliveries) — a larger, multi-week effort.
- **Add HMAC signature verification** for outgoing webhooks — a security
  hardening item, not blocking today since only trusted early-access
  partners currently have webhook URLs configured.
