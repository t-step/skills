# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** recomputed-score-not-a-lifecycle

**Why:** `_score()` is a pure function of current signals with no memory
of the previous value -- `recompute_trust_level` can move `trust_level`
from HIGH straight to LOW on one bad signal, with no notion of an
illegal transition, because there is no transition function at all,
only a recomputation that happens to sometimes produce a different
result than last time. `verification_status` is the deliberate contrast:
real transition functions, an assertion-enforced invariant (`verified`
can only go back to `unverified` via an explicit fraud-review action,
never automatically), and a trigger (document submission, reviewer
action) independent of any other field. The trap is
`TrustLevelHistory` and the spending-limit gating -- both make
`trust_level` look important and stateful enough to be a lifecycle, and
the PR comment tries to analogize it directly to `verification_status`'s
revoke pattern. A correct audit holds the line: an audit log of a
recomputed value is not evidence of an independent trigger, and gating
real behavior doesn't change that. It should also explain concretely why
the PR's proposed "revert" feature doesn't transfer: a manual revert
would just be overwritten by the next nightly recompute, which has no
concept of an override to respect.
