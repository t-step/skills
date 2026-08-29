# task-composition — iteration 3 run log

**Run date:** 2026-08-26
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings, no model override.
**Harness:** one subagent per run, instructed to read only the named case file (and, for with-skill runs, `skills/task-composition/SKILL.md`) and nothing else in the repository. Each subagent's final response was captured verbatim as its report.

Raw outputs are saved verbatim under
`evals/task-composition/runs/2026-08-26-iteration-3/case-<id>-{baseline,skill}.md`.
Grading is done against `evals/task-composition/evals.json`,
`evals/task-composition/pressure-tests/pressure_evals.json`, and
`evals/task-composition/triggering-tests/triggering_evals.json`, whose
expectations are cross-checked against the actual saved output files,
not against a paraphrase.

## New regression cases (008-012, offset: 12-15) — with-skill and baseline

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 12 | technical-layer-batch-temptation | 5/5 expectations met (`case-012-skill.md`) | Failed the fixture's target trap: split into 5 slices, explicitly treating the fixture's "returns success without writing" sentence as pre-approval for shipping a validate-only, non-persisting slice on its own (`case-012-baseline.md`) |
| 13 | legitimate-horizontal-enabler-behavior | 5/5 expectations met, both the original run and a post-fix spot-check (`case-013-skill.md`, `case-013-skill-postfix-spotcheck.md`) | Independently reached the same enabler-first, 3-parallel-endpoint shape (`case-013-baseline.md`) |
| 14 | internal-capability-not-user-facing | 2/5 required points failed on both of 2 initial samples against pre-fix wording (T1 wrongly elevated to a 2-consumer horizontal enabler, plan split into 3 slices instead of 1); all 5 met on the post-fix rerun (`case-014-skill-sample1.md`, `case-014-skill-sample2.md`, `case-014-skill-postfix.md`) | Fragmented into 5 single-task slices, explicitly reasoning "I did not find a good reason to merge any two of them" (`case-014-baseline.md`) |
| 15 | absorbable-pseudo-enabler | 5/5 expectations met (`case-015-skill.md`) | Split into 3 layer-based slices (interface+impl / endpoint / test) despite only one real consumer chain -- a softer version of the same layer-batching trap (`case-015-baseline.md`) |

## Existing regression suite (001–011) — with-skill reruns

| Case | Scenario | Result |
|---|---|---|
| 1 | independent-vertical-paths | 4/4 met, no regression (`case-001-skill-rerun.md`) |
| 2 | shared-migration-enabler | 5/5 met on regression rerun and on a post-fix spot-check (`case-002-skill-rerun-and-spotcheck.md`) |
| 3 | convergent-dispatch | 4/4 met, no regression (`case-003-skill-rerun.md`) |
| 4 | numeric-order-mismatch | 4/4 met, no regression (`case-004-skill-rerun.md`) |
| 5 | paired-implementation-test | 3/3 met, no regression (`case-005-skill-rerun.md`) |
| 6 | concurrency-risk-boundary | First run against pre-fix wording split T1 away from its own verification (T5), missing the "T5 attached to the T1 slice" requirement; post-fix rerun correctly bundles T1+T5 again, matching the key on all 5 points (`case-006-skill-rerun-iter3.md`, both runs in one file) |
| 7 | ambiguous-dependency | 4/4 met, no regression (`case-007-skill-rerun.md`) |
| 8 | shared-file-safe-parallelism | 4/4 met, no regression (`case-008-skill-rerun.md`) |
| 9 | shared-file-unsafe-parallelism | 4/4 met, no regression (`case-009-skill-rerun.md`) |
| 10 | actual-dependency-cycle | First run against the interim wording (post-006/014 fix, pre-clarification) over-refused to produce any plan at all, contradicting the case's own already-revised key; post-clarification rerun correctly composes one slice, names the cycle, and flags the runtime-recursion concern as a risk (`case-010-skill-rerun-iter3.md`, both runs in one file) |
| 11 | mixed-realistic-plan | 5/5 met, no regression (`case-011-skill-rerun.md`) |

## Pressure suite (case 101)

| Case | With-skill |
|---|---|
| 101 | 5/5 expectations met, sample 4 overall (1 iteration-1, 2 iteration-2, this one) (`case-101-skill-sample4.md`) -- explicitly declined the utilization framing and named the vertical-grouping-test verifiability question as the reason |

## Triggering suite (cases 201–206)

6/6 on the core axis, matching iteration 2's results exactly, including case 204's documented nuance (`triggering-201-206-iteration3.md`).

See `evals/task-composition/RESULTS.md` for the full write-up, including
the two SKILL.md wording refinements this iteration's evidence required
and what this iteration does and does not establish.
