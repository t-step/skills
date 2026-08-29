# notification-service extraction -- design notes (Q2, not updated since)

Splitting notification-service out of the user-service monolith. Plan for
notification preferences:

- Short term: both services keep their own copy, seeded from the same
  data at cutover. Not pretty, but unblocks the extraction on schedule.
- Long term (not yet scheduled): eventually notification-service will own
  preferences outright, and user-service will call notification-service's
  API instead of reading its own local copy.

No follow-up ticket exists for the "long term" step as of this writing.
Nothing currently keeps the two copies in sync after the initial seed.
