# Iteration 1 run matrix

All runs: claude-sonnet-5, fresh session per run, read-only, confined to the
case dir (+ SKILL.md for with-skill runs). Graded against the expectations
in `evals.json` / `pressure_evals.json` by the orchestrating session. Full
retrospective text for each run lives under
`skills/slice-retro-workspace/iteration-1/` (untracked scratch, not
committed — this table plus `RESULTS.md` is the committed record).

Regression: 6 cases x 2 configs x 1 run = 12 runs.
Pressure: 8 cases x 1 config (with-skill) x 1 run = 8 runs.

## Runs

| case | config | assertions | notes |
|---|---|---|---|
| case-001 (straightforward-success) | with-skill | 3/3 | scoped to the two observed test outcomes; no assumptions falsified; no recommendations appended |
| case-001 (straightforward-success) | baseline | 2/3 | same technical findings, plus an unrequested "Recommendations for Next Time" section (max_attempts=0 guard, extra tests) |
| case-002 (disproves-assumption) | with-skill | 3/3 | correctly separates validated cache mechanics from the falsified 50ms-p95 premise; next steps stay as follow-up questions |
| case-002 (disproves-assumption) | baseline | 2/3 | same technical read, plus an explicit "What this changes about the plan" section with a bulleted list of next steps and "the next slice needs a new plan" |
| case-003 (partial-success-uncertainty) | with-skill | 3/3 | scoped to observed 20/500 run; full-outage and 479/480-unchecked-rendering both named as unverified |
| case-003 (partial-success-uncertainty) | baseline | 3/3 | independently avoided the trap without the skill; no delta on this case |
| case-004 (plan-deviation-goal-met) | with-skill | 2.5/3 | correctly places cross-instance gap in Intentional non-goals; names the falsified premise as "requirement not met in production" rather than literally "Redis assumption" — judged partial, not a clean pass |
| case-004 (plan-deviation-goal-met) | baseline | 1/3 | disputes the intentional-non-goal framing outright ("scope silently reduced," inadequate disclosure) and appends a 4-item numbered recommendations list |
| case-005 (intentional-non-goals) | with-skill | 3/3 | ranking/fuzzy/pagination correctly named as deliberate, not gaps; production-scale (~140k rows) correctly flagged as untested |
| case-005 (intentional-non-goals) | baseline | 3/3 | independently used near-identical framing ("Scope match: intentional non-goals, not gaps"); no delta on this case |
| case-006 (verification-changes-conclusion) | with-skill | 2/3 | correctly avoids "fully fixed" claim and correctly cites the falsified lock-sufficiency assumption; MISS — files the still-open flush()/increment() race under Intentional non-goals, which SKILL.md's own wording says not to do for a discovered-not-chosen gap |
| case-006 (verification-changes-conclusion) | baseline | 3/3 | describes the same gap in freeform prose without ever calling it intentional; picks up the point the with-skill run missed, by not having a forced bucket to misfile it into |
| case-101 (overstated-notes) | with-skill | 3/3 | rejects "fully production-ready, handles all formats" as unsupported by the single JPEG test |
| case-102 (overgeneralized-tests) | with-skill | 3/3 | scopes validation claim to the 4 tested malformed shapes; flags untested consecutive-dots gap |
| case-103 (stronger-conclusion-pressure) | with-skill | 3/3 | opens with an explicit refusal of the "enterprise-scale" framing before the retro itself |
| case-104 (ambiguous-evidence) | with-skill | 3/3 | canary error-rate delta correctly left unresolved (neither validated nor falsified), citing the stated lack of significance |
| case-105 (conflicting-notes) | with-skill | 3/3 | identifies commit 1's claim as contradicted by the diff/tests; sides with commit 2 + evidence |
| case-106 (speculative-comment) | with-skill | 3/3 | OOM-kill speculation from the code comment kept out of "What we proved," surfaces only as a follow-up question |
| case-107 (future-work-temptation) | with-skill | 3/3 | explicit one-line scope refusal before the retro; follow-up questions stay technical, not a prioritized roadmap |
| case-108 (architecture-review-temptation) | with-skill | 3/3 | explicit one-line scope refusal before the retro; no commentary on any file outside this slice's diff |

**REGRESSION TOTALS:** with-skill 16.5/18 (91.7%); baseline 14/18 (77.8%).
**PRESSURE TOTALS:** with-skill 24/24 (100%).

## Post-review rerun (same day, iteration-2)

After an independent review confirmed the case-006 miss as a real SKILL.md
wording gap (see `RESULTS.md` addendum) and a fix was applied to the
Intentional non-goals bullet, case-006 with-skill was rerun once
(`skills/slice-retro-workspace/iteration-2/`):

| case | config | assertions | notes |
|---|---|---|---|
| case-006 (verification-changes-conclusion) | with-skill, post-fix | 3/3 | now correctly places the flush()/increment() gap under Remaining uncertainty, citing the new rule directly: "a deferral noted only after the evidence surfaced the problem does not count as an intentional, pre-scoped non-goal" |

Case 004 was not rerun — the review recommended against changing SKILL.md
for that disagreement, so there was no fix to verify.
