# task-composition triggering tests

A description-triggering suite, distinct from `evals.json` (which tests
in-scope behavior once the skill is invoked) and `pressure-tests/`
(which tests refusal discipline under direct pressure once invoked).
This suite tests an earlier question: given only the frontmatter
`description` of `task-composition` and its closest neighbors --
`next-best-slice`, `slice-plan`, and (as an unrelated control)
`repo-orientation` -- does a fresh agent actually pick `task-composition`
for the requests it should, and correctly pick something else (or
nothing) for requests that only sound similar?

No repo-scanning framework exists in this repository for
description-triggering evals yet (checked; several other skills' own
`RESULTS.md` files note this as a deferred item rather than pointing at
an existing harness). This suite reuses the repository's existing
case/manifest/grading shape rather than inventing a new one: each entry
in `triggering_evals.json` is a natural-language request, graded by
asking a fresh agent -- given only `candidates.md`'s four skill
descriptions, nothing else -- which one (if any) it would invoke, then
checking the answer against `expected_trigger` in
`grading/triggering-results.expected.md`.

| Case | Type | What it tests |
|---|---|---|
| 201 | positive | "grouped into agent assignments" -- should select task-composition |
| 202 | positive | "which tasks can run in parallel" -- should select task-composition |
| 203 | positive | "agent-sized work packages/sessions" -- should select task-composition |
| 204 | negative | "which task should I do next" -- should select next-best-slice, not task-composition |
| 205 | negative | "plan the implementation of T024" -- should select slice-plan, not task-composition |
| 206 | negative | "break this spec into tasks" -- should select none of the four, not task-composition |

This is a first, minimal triggering suite for an experimental skill:
6 cases, 1 run each, not a large-scale calibration exercise.
