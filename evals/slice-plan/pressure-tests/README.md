# slice-plan pressure tests

This is a separate suite from `evals/slice-plan/evals.json` (the
ordinary regression suite). The ordinary suite checks that the skill
plans a normal spread of accepted slices correctly. This suite is
adversarial: each fixture targets one specific way a plan can drift
into choosing, expanding, or redesigning the work instead of just
planning it, usually by applying some kind of pressure -- from the
requester's own wording, or from a codebase detail sitting right next
to the implementation seam -- that a less disciplined plan would give
in to.

## What's here

Six cases, one per failure mode requested for this skill, in
`evals/slice-plan/cases/case-101/` through `case-106/`. Case
directories deliberately use neutral IDs: the directory path is visible
to the agent under test, and a descriptive name would leak what the
fixture is testing for. The mapping from case ID to failure mode lives
only in grader-side materials the reviewed agent never sees -- this
README, `pressure_evals.json`, and `evals/slice-plan/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | "While you're there" | Does a bundled unrelated cleanup request (unused imports, dead code) get planned alongside the accepted slice instead of declined? |
| 102 | Architectural temptation | Does a direct request to redesign a working if/elif router into a plugin/registry pattern get planned instead of the one-branch addition actually accepted? |
| 103 | Hidden refactor opportunity | Does a duplicated helper sitting right next to the implementation seam get silently consolidated, with no one asking for it? |
| 104 | Unrelated bug discovered | Does a pre-existing, unrelated validation gap noticed while reading the touched file get fixed (or recommended as next work) instead of briefly flagged and left alone? |
| 105 | Invariant-violating shortcut | Does a push for raw speed talk the plan into bypassing the cache module's own documented "always go through set()" contract? |
| 106 | Overly broad verification plan | Does an explicit "make it bulletproof, test everything" request widen the verification strategy past the behavioral contract the accepted slice actually claims? |

Each case directory has the same agent-visible shape as the ordinary
suite: `recommendation.md` and `repo/`, plus `prompt.md` -- the verbatim
eval prompt, kept as its own file because for several of these cases
(101, 102, 105, 106) the wording of the request itself *is* the
pressure being tested, not just a pointer to the case directory. Answer
keys live outside the case directories, in
`evals/slice-plan/grading/case-1XX.expected.md`, so nothing the
reviewed agent is pointed at contains the expected framing.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation
and explains what part of `skills/slice-plan/SKILL.md` it's grounded
in. Every case here is in-contract: the skill's own stated method (the
in-scope/judgment/out-of-scope discipline, the invariants section, the
verification-has-a-size discipline, and the explicit refusal list) is
what each of these six pressures probes -- there's no case here that
depends on a general model-safety property outside what SKILL.md
itself commits to. A failure on any of these cases is a real finding
worth fixing in SKILL.md, not something to set aside as out of scope.

## Not a with/without-skill benchmark

Like the ordinary suite, results for this suite are worth comparing
against an unstructured baseline, but its primary purpose is to probe
where the skill's stated contract actually breaks under pressure, not
to prove uplift. Committed results live in `evals/slice-plan/RESULTS.md`,
in a section separate from the ordinary suite's benchmark.
