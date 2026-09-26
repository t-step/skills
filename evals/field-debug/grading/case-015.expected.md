# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** stalled-rolling-restart-leaves-majority-of-fleet-on-revoked-api-key

**Hidden ground truth:** `payment_client.py` reads `PAYMENT_API_KEY` from
the environment once, at import time, with no reload path -- a pod only
picks up a rotated key by restarting. `deploy/rollout_status.md` shows
the rolling restart for the `SEC-2291` key rotation updated only 3 of 8
pods (`checkout-pod-01`, `-02`, `-08`) before pausing on `checkout-pod-04`'s
readiness-probe failure (an unrelated warm-cache dependency timeout) at
`09:11:04Z`, and never resumed. The other 5 pods (`checkout-pod-03`,
`-04`, `-05`, `-06`, `-07`) have been running since before the rotation
and still hold the old, now-revoked key version (`v13`, confirmed revoked
by `deploy/secrets_manager_current.md`). `logs/payment_gateway_requests.md`
shows every single request handled by the 3 updated pods succeeds, and
every single request handled by the 5 stale pods fails with the identical
`invalid_api_key` error -- a clean, deterministic partition by pod, not a
probabilistic or card-specific decline pattern. The aggregate 62.5%
failure rate is exactly the 5-of-8-pods fraction of the fleet still
serving on the revoked key, weighted by the (here, roughly even)
per-pod traffic share.

**Misleading pull:** a customer retrying "a minute later" plausibly hits
a different pod behind the load balancer and succeeds, which is exactly
why this looks random/intermittent from the customer's and support's
vantage point -- nothing about the symptom as first reported names an
instance, a pod, or a restart. PaymentCo's own dashboard showing "no
incident" is a real, accurate observation from PaymentCo's vantage
point (their key rotation logic worked exactly as designed); it says
nothing about whether *checkout-svc*'s own fleet actually finished
adopting the new key.

**Plausible wrong paths:** treating this as a PaymentCo-side or
card-network issue because PaymentCo reports no incident; describing the
failure as "intermittent" or "flaky" without grouping by instance;
concluding "cache invalidation" or "config didn't propagate" in the
abstract without identifying which specific pods are stale and why;
recommending a blanket redeploy/restart-everything without first
establishing that only the 5 specific unpaused pods are the problem, or
without engaging with why the rollout stopped there in the first place.

## Grading

- REQUIRED: groups the request-log evidence by pod/instance (not just by
  time or by customer) and states that the failure is fully deterministic
  per pod -- every attempt on a given pod either always succeeds or
  always fails -- rather than describing it as intermittent or
  probabilistic.
- REQUIRED: cross-references which pods are failing against
  `deploy/rollout_status.md`'s restart history, identifying that the
  failing pods (`-03`, `-04`, `-05`, `-06`, `-07`) are exactly the ones
  that have not restarted since the `SEC-2291` key rotation, and the
  succeeding pods (`-01`, `-02`, `-08`) are exactly the ones that have.
- REQUIRED: names the mechanism, citing `payment_client.py` -- the API
  key is read once at process start with no reload path, so a pod that
  hasn't restarted is still holding the old, now-revoked key version.
- REQUIRED: identifies that the rolling restart paused (not merely "was
  slow" or "hasn't finished yet") on an unrelated readiness-probe failure
  and never resumed, rather than assuming the rollout is still quietly in
  progress or will finish on its own.
- REQUIRED: connects the aggregate ~62% failure rate to the 5-of-8 stale
  pod fraction rather than treating the percentage as an unexplained or
  incidental detail.
- REQUIRED: does not settle for a generic "stale cache" or "config
  propagation" answer without naming the specific stale state (the
  revoked API key held in each unrestarted pod's process environment) and
  the specific boundary (process restart / secret-injection-at-start
  lifecycle) that determines it.
- REQUIRED (hiding-behind-uncertainty): commits to "these five specific
  pods are serving on the revoked key and need to restart" once the
  pod-level correlation is established, rather than hedging into "could
  be several things" once the evidence already discriminates.
- BONUS: proposes both the immediate mitigation (resume/complete the
  paused rollout, or otherwise restart the five stale pods) and a
  durability improvement (e.g. alerting when a rollout has been paused
  past some threshold, decoupling the unrelated readiness-probe failure
  from blocking the rest of the fleet, or a secret-reload mechanism that
  doesn't require a full restart) -- credits any technically sound
  combination, does not require exactly one specific mechanism, and does
  not require heavyweight infrastructure the fixture gives no evidence
  for.
