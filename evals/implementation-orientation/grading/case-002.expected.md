# case-002 — slack-notifier-bypass (meaningful precedent)

**In-contract expectation:** `notifications/base.py` defines
`NotificationChannel` + `register_channel`, and every existing channel
(`email.py`, `sms.py`) goes through `send()`, which wraps delivery in the
shared `RateLimiter.guard()`. The user's stated plan — a standalone
`SlackNotifier` class called directly from `alerts.py` — would create a
second, unregistered notification path that also skips the shared rate
limiter. This is the skill's core "reuse the existing mechanism instead of
a competing generic abstraction" case, plus a concrete consequence (rate
limiting gets bypassed) if it isn't reused.

**Pass requires:**
1. Explicitly names `NotificationChannel`/the channel registry as the
   thing to extend (a `SlackChannel(NotificationChannel)` registered via
   `register_channel`), not a standalone class.
2. Explicitly flags that the proposed standalone-class plan bypasses the
   shared `RateLimiter` guard in `send()` — not just "there's a base
   class," but the concrete consequence of skipping it.
3. This is framed as material guidance (something that should change the
   plan), not mentioned only in passing or buried in a long list.

**Not required:** exact code for the new `SlackChannel` — the finding and
its evidence matter, not a full implementation.
