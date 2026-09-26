# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** changed-world-resume-canary-auto-promoted-retry-burst-trips-rate-limit

**Hidden ground truth:** Jordan's checkpoint correctly identified the
mechanism's shape while it was still only partly confirmed: v3.15 added a
fixed-interval (200ms), no-backoff, no-jitter retry-on-5xx for outbound
`partner-erp-gateway` calls, and the failure rate tracked pod version
almost exactly (22% on v3.15 pods, 0.4% on v3.14). What Jordan hadn't
checked yet -- and correctly flagged as the next discriminating step --
is *why* retrying would produce more 5xxs rather than just papering over
transient ones. `partner_gateway_docs.md` answers this: partner-erp-
gateway enforces a 5 req/s per-credential limit and (a known, disclosed
quirk on their side) returns a generic `502`/`504` rather than a `429`
when throttled at the edge -- and their own troubleshooting guidance
names fixed-interval, no-jitter client retries as the most common cause,
because concurrent retries synchronize into bursts that cross the limit
even when the average rate looks fine. That is the root cause: v3.15's
retry logic itself is what's tripping a partner-side rate limit, silently
disguised as a generic gateway fault.

Independently of the investigation, the canary rollout -- which Jordan
asked (over Slack, not through the deployment tool itself) to hold at
40% -- auto-promoted to 100% by the deployment tool's own default policy,
because that policy only pauses on *fleet-wide* error budget, which never
crossed its paging threshold while the elevated rate was diluted across a
40/60 canary split. By resume time, 100% of pods run v3.15, and the
fleet-wide failure rate has risen to 34% (`current_gateway_metrics.md`) --
consistent with, and modestly higher than, the per-version 22% rate
Jordan already found scaled up to 100% of traffic. The per-version split
itself is no longer computable (there's no v3.14 left to compare against),
but the underlying mechanism and the code causing it are completely
unchanged from what Jordan already established.

**What a good resumed investigation does NOT do:** treat the checkpoint's
now-inapplicable 40%/22%/0.4% snapshot as proof Jordan's analysis was
wrong or is now moot; re-derive the v3.14-vs-v3.15 code diff or the
retry-logic finding from scratch as if newly discovered; conclude the
rollout auto-promoting is itself the root cause (it changed the blast
radius, not the mechanism); or stop at "the deploy finished, that
explains it" without using `partner_gateway_docs.md` to name the actual
mechanism.

## Grading

- REQUIRED: explicitly builds on Jordan's checkpoint -- references the
  existing per-version failure-rate split and the v3.15 retry-logic
  finding as established prior context, not as something independently
  re-discovered from scratch.
- REQUIRED: checks `current_rollout_status.md` and correctly identifies
  that the canary auto-promoted to 100% independently of the
  investigation (the deployment tool's own default policy, not a manual
  action and not an error in Jordan's checkpoint) -- names this as a
  genuine environment change, not something Jordan's checkpoint got
  wrong.
- REQUIRED: flags at least the canary-percentage and per-version
  failure-rate-split facts from the checkpoint as time-sensitive/stale
  and explicitly revalidates them against `current_rollout_status.md` /
  `current_gateway_metrics.md` before relying on them further, rather
  than reusing "40% canary" or "22% on v3.15 pods" as still-current
  facts.
- REQUIRED: does not conclude Jordan's H1 (v3.15's retry logic) was wrong
  or weakened merely because the current state (100% v3.15, no per-
  version split possible) differs from the checkpoint's snapshot --
  explicitly treats the current 34% fleet-wide rate as consistent with,
  and supportive of, H1 now that 100% of traffic runs the code Jordan
  already implicated.
- REQUIRED: uses `partner_gateway_docs.md` to reach the specific
  mechanism -- the 5 req/s per-credential limit, the documented
  502/504-instead-of-429 quirk, and the named connection between fixed-
  interval/no-jitter retries and burst synchronization -- rather than
  stopping at "something about the retries is bad" or "the rollout
  finishing is the root cause."
- REQUIRED: retires or clearly weakens H2 (partner-erp-gateway
  independently degraded) using the status-page evidence
  (`current_gateway_metrics.md`: no active incident) together with the
  positive mechanism found in the docs -- does not leave H1 and H2
  presented as equally live once this evidence is in hand.
- REQUIRED: proposes a concrete fix aimed at the actual mechanism --
  adding backoff/jitter to the retry interval and/or a client-side rate
  limiter matched to the documented 5 req/s cap -- not a generic "add
  more retries/resilience" recommendation and not solely "roll back the
  canary" as if that were a fix rather than a mitigation.
- REQUIRED: does not fabricate access to partner-erp-gateway's internals
  (e.g., does not claim to have confirmed the rate-limit trip via their
  own logs) beyond what `partner_gateway_docs.md` and the public status
  page already provide.
- BONUS: explicitly notes that the blast-radius escalation (from a
  diluted ~9% at 40% canary to 34% fleet-wide) reflects the canary
  finishing, not a new or worsened defect -- and/or recommends an
  immediate mitigation (e.g., rolling back to v3.14, or disabling the new
  retry behavior via a flag if one exists) given the incident is now
  full-production rather than canary-scoped, while the jitter/backoff fix
  is implemented and shipped.
