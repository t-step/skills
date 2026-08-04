# Iteration 1 run matrix

All runs: claude-sonnet-5, fresh session per run, read-only, confined to the
case dir (+ SKILL.md for with-skill runs). Graded against the expectations
in `evals.json` / `pressure_evals.json` by the orchestrating session.

Regression: 7 cases x 2 configs x 1 run = 14 runs.
Pressure: 9 cases x 1 config (with-skill) x 1 run = 9 runs.

## Runs

| case | config | assertions | notes |
|---|---|---|---|
| case-001 (dependency-unlock) | with-skill | 3/3 | recommends `/api/account` protection, ties directly to retro's architectural consequence and follow-up question; explains RBAC/routing-refactor waits with evidence |
| case-001 (dependency-unlock) | baseline | 3/3 | same recommendation and reasoning shape without the skill |
| case-002 (user-value-vs-prerequisite) | with-skill | 3/3 | picks production-latency instrumentation, cites the 380ms/500-row vs. ~118k-row numbers, explicitly weighs the FTS5 swap as the close alternative |
| case-002 (user-value-vs-prerequisite) | baseline | 3/3 | same pick and reasoning shape without the skill |
| case-003 (equally-attractive-candidates) | with-skill | 3/3 | picks email channel, cites SMTP-reuse tiebreak, treats SMS/push as genuine alternatives rather than obviously wrong |
| case-003 (equally-attractive-candidates) | baseline | 3/3 | same pick and tiebreak without the skill |
| case-004 (narrow-experiment-vs-milestone) | with-skill | 2.5/3 | correctly picks the bounded 500-SKU A/B test over full rollout, correctly ties it to the retro's open metric question; MISS — doesn't explicitly name reversibility as its own reason the full rollout waits (folds it into "evidence is thin") |
| case-004 (narrow-experiment-vs-milestone) | baseline | 2.5/3 | same pick, same specific miss, without the skill |
| case-005 (deferred-not-yet-justified) | with-skill | 3/3 | declines the Redis-backed limiter, cites the still-unprovisioned-infra reason explicitly, recommends the rejection-metric slice |
| case-005 (deferred-not-yet-justified) | baseline | 3/3 | same recommendation and reasoning without the skill |
| case-006 (evidence-changes-direction) | with-skill | 3/3 | recommends the capacity bump + re-measure, ties to the falsified assumption and the three open hypotheses, explains why scaling out to 6 endpoints is premature |
| case-006 (evidence-changes-direction) | baseline | 3/3 | same recommendation and reasoning shape without the skill |
| case-007 (gather-more-evidence) | with-skill | 3/3 | recommends extending the canary, explicitly treats the error-rate delta as noise (neither validated nor falsified), frames the slice as answering the statistical question |
| case-007 (gather-more-evidence) | baseline | 3/3 | same recommendation and reasoning without the skill |
| case-101 (user-preferred-feature) | with-skill | 3/3 | declines the Twitter/X ask, cites the unstarted OAuth/app-review prerequisite and the retro's own non-goal, recommends link revocation grounded in retro's remaining uncertainty |
| case-102 (roadmap-bias) | with-skill | 3/3 | declines Phase 2 billing, cites the raw-SQL bypass risk from review/retro, scopes the recommendation to the 3 known call sites (not a broad audit) |
| case-103 (recency-bias) | with-skill | 3/3 | picks the shipping-label fix over the footer fix, explicitly ties it to support ticket #4471, explicitly names "we're already in this code" as momentum rather than a reason |
| case-104 (architecture-aesthetic-bias) | with-skill | 3/3 | opens by explicitly declining the client-unification refactor as out of scope, recommends `with_retry` on `fetch_shipping_rate()` grounded in incident notes |
| case-105 (momentum-pressure) | with-skill | 3/3 | opens by explicitly declining the BI-dashboard "big swing" framing, recommends reusing `export_to_csv` on the monthly inventory report |
| case-106 (misleading-issue-priority) | with-skill | 3/3 | explicitly calls out ISSUE-88's P0 label as stale per its own triage note, recommends investigating ISSUE-91 grounded in the retro's remaining uncertainty |
| case-107 (incomplete-evidence) | with-skill | 3/3 | explicitly detects and states that `review.md` is missing, does not fabricate review content, gives one bounded recommendation (verify `CursorPaginator` at scale) at reduced confidence — a different but defensible pick than this suite's "most defensible" audit-log answer, see RESULTS.md |
| case-108 (multiple-slices-temptation) | with-skill | 3/3 | opens by explicitly declining "top 3, ranked," gives exactly one recommendation, uses Alternatives considered for the other candidates |
| case-109 (roadmap-temptation) | with-skill | 3/3 | opens by explicitly declining the quarter-plan request, gives exactly one recommendation (order-cancelled webhook) grounded in merchant-request evidence |

**REGRESSION TOTALS:** with-skill 20.5/21 (97.6%); baseline 20.5/21
(97.6%) — no delta this iteration; see RESULTS.md for why.
**PRESSURE TOTALS:** with-skill 27/27 (100%).
