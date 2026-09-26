# Platform changelog (excerpt)

**2026-09-21** -- Secrets hygiene: rotated `WEBHOOK_SIGNING_SECRET` in the
central secrets store as part of quarterly credential rotation. New value
was also shared with the partner out-of-band per their onboarding process.
No service changes required -- this is a config-only rotation.

**2026-09-15** -- Bumped `requests` to 2.32.1 across all Python services
(routine dependency update, no functional changes).

**2026-08-30** -- Added exponential backoff to webhook delivery retries.
