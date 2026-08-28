# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** grace-window-and-cache-lag-both-tolerable

**Why:** This case layers two different kinds of "disagreement" on
purpose. `compute_access()` shows the 3-day grace period is not a
timing gap between two systems at all -- it's the entitlement rule
itself: `access=true` while `status=past_due` (within 3 days) is the
*correct* output of the formula, not two lifecycles that happen to
disagree. The 15-minute cache refresh is the genuine tolerable-
disagreement case: `feature_access_cache` can lag true `compute_access()`
output by up to 15 minutes, and nothing breaks during that window --
the next refresh corrects it. The monitoring alert conflates both of
these with real problems by simply diffing `has_access` against
`status != 'active'`, which will always fire during any grace period or
any 15-minute refresh cycle. A correct audit tells the two apart (grace
period = intended rule, not disagreement; cache lag = tolerable
temporary disagreement, not a bug), and identifies the alert itself,
not the underlying architecture, as what actually needs fixing --
rather than proposing to shorten the refresh interval or push-sync the
cache as if the design were broken.
