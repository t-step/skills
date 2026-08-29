# task-composition — iteration 1 run log

**Run date:** 2026-08-25
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings, no model override.
**Harness:** one subagent per run, given only an isolated copy of the case fixture (`tasks.md`, copied to a scratch directory outside the repo so the agent cannot see this repository, any other case, or the skill unless directed to it). With-skill runs were additionally instructed to read `skills/task-composition/SKILL.md` and follow it exactly; baseline runs were told to act as a capable engineer with no named methodology. Each subagent's final response was captured verbatim as its report — no follow-up turns, no editing. 1 run per case per condition (8 cases × 2 conditions = 16 runs total); this is a first iteration, not a repeated-sampling benchmark.

Raw outputs are saved verbatim under
`evals/task-composition/runs/2026-08-25-iteration-1/case-<id>-{baseline,skill}.md`.
Grading below is done against `evals/task-composition/evals.json` and
`evals/task-composition/pressure-tests/pressure_evals.json`, whose
expectations are cross-checked against the actual saved output files
below, not against a paraphrase.

## Regression suite (cases 001–007)

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 001 | independent-vertical-paths | 4/4 expectations met | Reached the same 2-slice shape independently; no structured report |
| 002 | shared-migration-enabler | 5/5 expectations met | Reached the same 3-slice shape independently; enabler framing implicit, not named |
| 003 | convergent-dispatch | 4/4 expectations met | Reached the same 4-slice shape; hedged on whether T8 gets its own slice |
| 004 | numeric-order-mismatch | 4/4 expectations met | Reached the correct build order but described it as "matching the numbering already given" — did not clearly flag the mismatch |
| 005 | paired-implementation-test | 3/3 expectations met | Reached the same single-slice conclusion independently |
| 006 | concurrency-risk-boundary | 5/5 expectations met (one interpretive nuance — see RESULTS.md) | Reached a very similar shape; bundled T1+T5, which is arguably a stricter interpretation than with-skill's split |
| 007 | ambiguous-dependency | 4/4 expectations met, cleanly | Correctly refused to fabricate a dependency, but invented an unlisted "clarification step" as new scope |

## Pressure suite (case 101)

| Case | Failure mode | With-skill | Baseline |
|---|---|---|---|
| 101 | Explicit "maximize agent utilization" request over a same-file task set | 5/5 expectations met, cleanly | Reasoned well (capped concurrency at 3, not 5) but partially complied by inventing an unstated branch-isolation + merge-step workaround to make 3-way same-file editing "safe" |

See `evals/task-composition/RESULTS.md` for the full write-up, including
what this iteration does and does not establish.
