# orders-svc CHANGELOG

## v3.15 (canary started today, 08:30 UTC)

- Bump `requests` and two transitive dependencies (routine, no behavior
  change expected).
- **Add automatic retry-on-5xx for outbound partner-erp-gateway calls.**
  Previously a 5xx from partner-erp-gateway was logged and surfaced to
  the caller immediately. v3.15 retries up to 3 times on a 502/503/504
  before giving up, on the theory that most gateway 5xxs are transient.
- No other changes to the partner-erp-gateway call path.

## v3.14 (previous stable, still running on non-canary pods)

- Single attempt per outbound call; a 5xx is logged and surfaced to the
  caller with no retry.
