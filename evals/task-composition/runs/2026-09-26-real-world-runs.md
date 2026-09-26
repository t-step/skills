# task-composition — real-world fixture run log (iteration 1)

**Run date:** 2026-09-26
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings, no model override.
**Harness:** one subagent per run, instructed to read only the named case's agent-visible files (never `provenance/`, `grading/`, `RESULTS.md`, `evals.json`, or any suite README) and told explicitly not to use WebSearch/WebFetch/`gh`/`git log` and not to rely on any memorized/trained knowledge of the real project's actual history. With-skill runs additionally read and followed `skills/task-composition/SKILL.md` and its exact report format. Baseline runs used a free-form structure of their own choosing. Raw outputs are saved verbatim under `evals/task-composition/runs/2026-09-26-real-world-iteration-1/` (gitignored per this repo's existing convention for raw per-run transcripts — see `.gitignore`). Grading is done against `evals/task-composition/grading/case-30{1,2,3}.expected.md`'s REQUIRED items, cross-checked against the actual saved output files.

## Fixture-defect found and fixed mid-run (case-303)

The first case-303 baseline run (against the pre-review-fix fixture) surfaced a real fixture defect: `cases/case-303/source-notes.md` contained a sentence referencing the fixture's own construction process ("a later changelog-verification pass... trimmed both back... see provenance/case-303/cutoff-rationale.md... if you need it"), and the baseline agent's report explicitly cited this as a "provenance caveat... relevant to trusting this plan." This is a fourth-wall break: it told the tested agent it was in a constructed exercise rather than a plausible point-in-time snapshot. A broader grep then found two more instances of the same class of leak: an entire "methodological note, for whoever maintains this fixture next" section in `cases/case-301/source-notes.md`, and the phrase "provenance PR search" in `cases/case-303/dependencies.md`. Also found: the phrase "than a typical synthetic fixture" in `cases/case-303/dependencies.md`. All four were removed (see the diff on this branch). Per the stated protocol, the case-303 baseline run was discarded (not graded) and both conditions were rerun fresh against the corrected fixture; case-301 and case-302 had not yet been run at the time this was found, so their first runs are against the corrected fixture directly.

## Results

| Case | Condition | REQUIRED items met | File |
|---|---|---|---|
| 301 (Ignite IEP-119 Phase 1) | Baseline | 6/7, plus one notable extra-scope issue (invented a 3-part F1/F2/F3 sub-decomposition of the tangled pair) | `case-301-baseline.md` |
| 301 (Ignite IEP-119 Phase 1) | With-skill | 6/7 (missed the IGNITE-24782 enabler item; correctly avoided inventing sub-decomposition) | `case-301-skill.md` |
| 302 (Cassandra SAI/CEP-7) | Baseline | 6/6 | `case-302-baseline.md` |
| 302 (Cassandra SAI/CEP-7) | With-skill | 6/6 | `case-302-skill.md` |
| 303 (Hudi metadata table) | Baseline (rerun, corrected fixture) | 10/11 (softly merged HUDI-2459+2460 into one slice, contrary to REQUIRED #8, while caveating the merge as its own inference) | `case-303-baseline-rerun.md` |
| 303 (Hudi metadata table) | With-skill | 11/11 | `case-303-skill.md` |

See `evals/task-composition/RESULTS.md`'s new "Real-world fixture iteration" section for the full case-by-case analysis, the case-301 finding where the with-skill run under-performed baseline, and answers to the ten evaluation questions.
