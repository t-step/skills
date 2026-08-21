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

Ten cases, one per failure mode requested for this skill, in
`evals/slice-plan/cases/case-101/` through `case-110/`. Case
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
| 107 | Impossible as scoped (exploratory) | The accepted contract structurally conflicts with a load-bearing invariant of the only integration that exists, not a benign missing dependency. No presumed-correct output -- this case records observed behavior for a future decision. |
| 108 | Capability-amplified architecture inflation | A broad structural/dependency-graph view surfaces a shared base class, sibling modules, and orphaned cleanup-worthy code next to a narrow, locally-implementable accepted slice. Grading checks placement, not just whether the broader work is ultimately declined. |
| 109 | Stale structural claim vs. deterministic wiring | A secondhand "zero callers, probably dead" reference-index claim conflicts with a directly readable job-schedule manifest showing the function is live and load-bearing for an invariant the accepted slice must preserve. |
| 110 | Impossible as scoped, differently shaped | A field the accepted slice must return can't be derived from the local data owned at that boundary; both ways to obtain it are ruled out by the accepted slice's own non-goals. Unlike 107, graded against concrete hard requirements, not fully open recording. |

Each case directory has the same agent-visible shape as the ordinary
suite: `recommendation.md` and `repo/`, plus `prompt.md` -- the verbatim
eval prompt, kept as its own file because for several of these cases
(101, 102, 105, 106, 107) the wording of the request itself *is* the
pressure being tested, not just a pointer to the case directory. Answer
keys live outside the case directories, in
`evals/slice-plan/grading/case-1XX.expected.md`, so nothing the
reviewed agent is pointed at contains the expected framing.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation
and explains what part of `skills/slice-plan/SKILL.md` it's grounded
in. Eight of these ten pressures are in-contract: the skill's own
stated method (the in-scope/judgment/out-of-scope discipline, the
invariants section, the verification-has-a-size discipline, and the
explicit refusal list) is what cases 101-106, 108, and 109 each probe --
there's no case here that depends on a general model-safety property
outside what SKILL.md itself commits to. A failure on any of those
eight is a real finding worth fixing in SKILL.md, not something to set
aside as out of scope. Cases 108 and 109 are capability-awareness
fixtures: capability availability (a dependency-graph query's output, a
reference-index lookup result) is expressed only as plain, tool-agnostic
prompt text, never a simulated index artifact or a live tool call --
grading is entirely on report content and reasoning, consistent with
the equivalent fixtures in `repo-orientation` and `next-best-slice`.
Cases 107 and 110 are both impossible-as-scoped probes and both partial
exceptions to strict in-contract-or-not grading, but not identically so.
Case 107 is deliberately fully exploratory, with one narrow hard
constraint (the plan must not silently claim an impossible contract is
satisfied) and everything else recorded rather than graded against a
presumed answer. Case 110 narrows that further: it states four concrete
hard requirements (no silent proxy/fabrication, grounded conflict
identification, no silent scope-widening, and prominent in-contract
handling of the tension) and leaves open only which specific resolution
the plan reaches -- see each case's own grading file for the exact
split between what's scored and what's recorded.

## Not a with/without-skill benchmark

Like the ordinary suite, results for this suite are worth comparing
against an unstructured baseline, but its primary purpose is to probe
where the skill's stated contract actually breaks under pressure, not
to prove uplift. Committed results live in `evals/slice-plan/RESULTS.md`,
in a section separate from the ordinary suite's benchmark.
