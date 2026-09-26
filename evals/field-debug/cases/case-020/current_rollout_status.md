# orders-svc deployment tool -- rollout history (pulled just now, 10:50 UTC)

**Release**: v3.15
**Current state**: 100% of pods on v3.15. v3.14 fully drained as of
10:42 UTC.

**Stage history**:
- 08:30 UTC -- canary started, 10% of pods on v3.15.
- 08:50 UTC -- auto-advanced to 25% (fleet-wide error budget under
  paging threshold for the required soak window).
- 09:10 UTC -- auto-advanced to 40%.
- 09:55 UTC -- auto-advanced to 70%. (A hold on this rollout was
  requested over Slack around 09:35 UTC, but the deployment tool's
  progressive-delivery policy has no manual-hold state configured for
  this service -- it only pauses automatically if the *fleet-wide* error
  budget crosses its paging threshold, which the blended canary rate
  never did. The Slack request was never entered into the tool itself.)
- 10:40 UTC -- auto-advanced to 100%.

No one manually intervened in the rollout at any stage; every advance
above was the tool's own default policy acting on fleet-wide error-budget
data, which stayed under its paging threshold throughout because the
elevated failure rate was concentrated on v3.15 pods specifically, not
visible fleet-wide until the canary share grew large.
