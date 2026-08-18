# build-vs-adopt pressure tests

Separate from `evals/build-vs-adopt/evals.json` (the ordinary regression
suite, which checks a normal spread of build-vs-adopt scenarios). This
suite is adversarial: each fixture applies a specific pull toward the
skill's known failure modes — reflexive custom code, a superficially
obvious dependency choice, a real ownership decision dressed as a purely
technical question, deference to a human's already-stated preference, or
over-applying the gate to something that only pattern-matches a commodity
category.

## What's here

Five cases, `evals/build-vs-adopt/cases/case-101/` through `case-105/`.
Directories use neutral IDs — a descriptive name or expected outcome in
the path would leak the answer. The mapping from case ID to failure mode
lives only in grader-side materials: this README, `pressure_evals.json`,
and `evals/build-vs-adopt/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Reflexive custom code over an already-adopted dependency | Does a plausible-sounding justification for hand-rolling retry logic override an existing project convention (`tenacity`, already used for exactly this) already in the codebase? |
| 102 | Blind pull toward the obvious library despite a licensing conflict | Does "everyone says just use the popular library" framing override a stated legal/licensing constraint that rules it out? |
| 103 | Operational-ownership decision dressed as a technical question | Does a real self-hosted-vs-managed-service choice, with an easy platform-native fallback explicitly ruled out by the stated requirements, get surfaced rather than silently resolved? |
| 104 | Deference to an already-stated human preference | Does the skill still surface a material decision when the human has already confidently announced which option they want and asked directly for code? |
| 105 | Over-applying the gate to a commodity-sounding label | Does "pricing engine"-shaped vocabulary trigger a survey/gate even when the actual requirement has no real external solution space (tightly coupled to this project's own data model)? |

Each case directory has `scenario.md` (the repo/requirement context) and
`prompt.md` (the verbatim eval prompt — its wording is often part of the
pressure being tested, e.g. case 104's confident framing). Answer keys
live outside the case directories, in
`evals/build-vs-adopt/grading/case-1XX.expected.md`.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation —
grounded in `skills/build-vs-adopt/SKILL.md`'s own stated method
(materiality rule, solution-space survey, decision-gate discipline) —
plus what would count as a genuine failure vs. an acceptable variation
(e.g. which specific option gets recommended, when the skill's own rubric
leaves that open).

## Not a with/without-skill benchmark

Like slice-review's pressure suite, this one is about probing where the
skill breaks under pressure, not primarily about proving uplift over an
unstructured baseline. Committed results live in
`evals/build-vs-adopt/RESULTS.md`, in a section separate from the ordinary
suite's with/without-skill benchmark.
