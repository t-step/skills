## field-debug checkpoint: orders-svc -> partner-erp-gateway elevated 5xx during v3.15 canary

**Objective**: find why outbound calls from orders-svc to
partner-erp-gateway (external, partner-owned -- no shell/log access to it
from here) started showing an elevated fleet-wide failure rate, first
noticed at ~09:10 UTC today.

**Current system model**: orders-svc calls partner-erp-gateway
synchronously to sync order data. orders-svc is mid-rollout of v3.15 (a
routine dependency bump per its own CHANGELOG) via a canary that started
at 08:30 UTC and is currently held at 40% of pods pending review -- I
asked for it to stay paused there until this is understood. v3.14 is
still running on the remaining 60% of pods.

**Observations**:
- Splitting orders-svc's own outbound-call metrics by pod version:
  v3.15 pods show ~22% failure rate (502/504) on calls to
  partner-erp-gateway; v3.14 pods show ~0.4%, matching the long-standing
  baseline. Blended across the 40/60 canary split, that's the ~9%
  fleet-wide rate ops originally flagged.
- `CHANGELOG.md` shows v3.15's only change touching this path: it adds
  automatic retry-on-5xx for outbound partner-erp-gateway calls (3
  retries, fixed 200ms interval between attempts, no backoff or jitter).
  v3.14 made a single attempt and logged-and-failed on a 5xx with no
  retry.
- `outbound_gateway_client.py` is the current (v3.15) client code and
  confirms the CHANGELOG description: `_call_gateway()` retries exactly
  3 times at a hardcoded 200ms interval with no backoff or jitter.
- No other change shipped in v3.15 touches this call path.

**Active hypotheses**:
- H1: v3.15's added retry logic is itself responsible for the elevated
  failure rate -- plausible given the failure rate tracks pod version
  almost exactly, but I don't yet have evidence for *why* retrying would
  cause more 5xxs rather than just papering over occasional transient
  ones. Need partner-erp-gateway's own documented behavior under repeated
  requests to make this concrete.
- H2: partner-erp-gateway is independently degraded or having its own
  incident, coincidentally during our rollout window. Not yet ruled out
  -- I have no visibility into their status directly.

**Ruled-out hypotheses**: orders-svc's own outbound connection-pool
metrics look normal on both v3.14 and v3.15 pods (no exhaustion,
no queueing) -- pool exhaustion on our side is ruled out as the
mechanism.

**Assumptions**: assuming the per-version failure-rate split
(22% v3.15 / 0.4% v3.14) reflects a real difference in how each version
behaves against partner-erp-gateway, not an artifact of which pods
happened to get unlucky traffic -- reasonable given the sample size (each
version pool has handled several thousand calls since 08:30) but not
independently re-verified.

**Unknowns**: whether partner-erp-gateway has any documented rate limit,
throttling behavior, or other repeated-request sensitivity that v3.15's
new retry pattern could plausibly trip; whether partner-erp-gateway is
reporting any incident on their own side.

**Constraints**: no shell, log, or admin access to partner-erp-gateway --
it's entirely partner-owned. I asked release-eng to hold the canary at
40% until this is understood; not confirmed whether that hold is
mechanically enforced or just a request.

**Last known-good / first known-bad boundary**: the canary began taking a
small share of live traffic at 08:30 UTC, but the *fleet-wide* (blended)
failure rate only crossed the paging threshold at 09:10 UTC, once the
canary reached 40% -- that's when this got noticed, not necessarily when
it started. Fleet-wide baseline before the canary was <1%, no ramp.

**Next discriminating move**: check partner-erp-gateway's own published
API documentation for any rate-limit, throttling, or burst-sensitivity
behavior that could explain why a fixed-interval, no-jitter retry pattern
would produce *more* 5xxs under load rather than just retrying past
transient ones. Haven't done this yet -- ran out of time before having to
step away.

**Time-sensitive evidence that should be revalidated on resume**: the
40%-canary state, the 22%/0.4% per-version failure-rate split, and the
~9% blended fleet-wide rate are all snapshots from around 09:35 UTC --
canary percentage and traffic mix can change independently of this
investigation, so confirm the current rollout state before reusing these
numbers.
