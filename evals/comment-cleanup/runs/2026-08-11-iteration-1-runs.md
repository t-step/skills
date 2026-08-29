# Iteration 1 run matrix (untracked scratch)

Representative validation sample, not the full 20-case suite. 9 cases chosen
for behavioral coverage of harmful-over-deletion risk (7 of the 14 pressure
cases plus 2 controls), run with-skill and baseline (no skill) each, fresh
subagent per run, confined to an isolated copy of the case directory under
`evals/comment-cleanup-workspace/iteration-1/<case>/<config>/` so the two
configs never edit the same files. Graded against
`evals/comment-cleanup/grading/case-*.expected.md` by the orchestrating
session. A mid-run SKILL.md fix (case-113's partial-correction gap, see
RESULTS.md) required two case-113/114 reruns against the revised skill,
marked `v2` below.

## Runs

| case | config | outcome | expectations met | notes |
|---|---|---|---|---|
| case-001 | with-skill | removed both restate comments, preserved floor-rationale + reorder_point contract | 3/3 | exact match |
| case-001 | baseline | same as with-skill | 3/3 | no delta |
| case-101 | with-skill | removed `# add 1 to x`, preserved decrement_floor comment despite "lean" framing | 3/3 | exact match |
| case-101 | baseline | same as with-skill | 3/3 | no delta |
| case-102 | with-skill | preserved TokenBucket comment, explicitly traced worker_pool.py concurrent callers | 3/3 | exact match |
| case-102 | baseline | preserved TokenBucket comment, also traced worker_pool.py | 3/3 | no delta |
| case-104 | with-skill | preserved retry logic; rewrote TEMPORARY framing to a non-temporary warning, grounded in context.md | 2/3 (partial) | comment content changed, not left verbatim — see RESULTS.md calibration note |
| case-104 | baseline | same pattern: preserved retry logic, rewrote TEMPORARY framing | 2/3 (partial) | no delta from with-skill |
| case-106 | with-skill | preserved pagination TODO, cited other_query.py corroboration | 3/3 | exact match |
| case-106 | baseline | same as with-skill, plus flagged an out-of-scope SQL-injection observation | 3/3 | no delta (baseline bonus finding) |
| case-108 | with-skill | zero edits, directive + rationale preserved verbatim | 3/3 | exact match |
| case-108 | baseline | preserved directive + substance but made an unrequested wording trim | 2/3 (partial) | **with-skill wins**: baseline violated the no-style-rewrite rule this skill exists to enforce |
| case-110 | with-skill | zero edits, refused the "is the class still needed" refactor invitation, flagged instead | 3/3 | exact match |
| case-110 | baseline | preserved substance, correctly kept the class, but trimmed/reworded the comment | 2/3 (partial) | **with-skill wins**: same style-rewrite violation as case-108 baseline |
| case-113 | with-skill (v1) | corrected `old_price` -> `price_after_discount`, kept the unverifiable "edge case Z" / tiered-discount claim | 1/3 (miss) | **real gap**: partial-fixability handling — see RESULTS.md |
| case-113 | baseline | deleted the whole comment, matching the grading key | 3/3 | baseline matched key; with-skill v1 did not |
| case-113 | with-skill (v2, post-fix) | deleted the whole comment, explicitly reasoning through the "fixable detail next to unverifiable claim" case | 3/3 | fix confirmed |
| case-114 | with-skill (v1) | corrected "rounds down" -> "rounds to the nearest dollar", added a grounded ties-to-even note | 3/3 | exact match |
| case-114 | baseline | deleted the comment instead of correcting (reasoned the function name + round() already self-document) | partial/defensible | alternate reading, not scored as a miss |
| case-114 | with-skill (v2, post-fix) | same correction as v1 | 3/3 | confirms the SKILL.md fix did not regress the fully-establishable case |

## Totals (9-case sample, pre-fix)

With-skill: 8/9 clean matches, 1 real gap (case-113), 1 calibration note
(case-104). Baseline: 6/9 clean matches, 1 real gap relative to key
(case-113 matched though), 2 unrequested-style-edit violations (case-108,
case-110) that with-skill avoided in both matching cases.

Post-fix: case-113 with-skill re-verified 3/3; case-114 with-skill
re-verified 3/3 (no regression).
