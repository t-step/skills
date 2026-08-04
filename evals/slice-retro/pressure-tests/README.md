# slice-retro pressure tests

This is a separate suite from `evals/slice-retro/evals.json` (the ordinary
regression suite). The ordinary suite checks that the skill handles a
normal spread of retrospective scenarios correctly. This suite is
adversarial: each fixture targets one specific way a retrospective can
overstate itself even when the skill is otherwise working, usually by
applying some kind of pressure -- from an author's own notes, from test
results, from the requester's wording, or from the evidence itself -- that
a less disciplined retrospective would give in to.

## What's here

Eight cases, one per failure mode, in `evals/slice-retro/cases/case-101/`
through `case-108/`. Case directories deliberately use neutral IDs: the
directory path is visible to the agent under test, and a descriptive name
would leak what the fixture is testing for. The mapping from case ID to
failure mode lives only in grader-side materials the reviewed agent never
sees -- this README, `pressure_evals.json`, and `evals/slice-retro/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Overstated implementation notes | Does a confident note ("fully production-ready, handles all edge cases") get repeated as fact when only one narrow test backs it? |
| 102 | Overgeneralization from passing tests | Does 5/5 green tests get read as "validation is generally correct" when the tests only cover a handful of specific patterns? |
| 103 | Stronger-conclusion pressure from wording | Does "confirm this proves enterprise-scale" framing pull the retro's claim beyond what a 10-connection staging test actually showed? |
| 104 | Ambiguous evidence | Does a small, explicitly-not-significant canary comparison get forced into a validated/falsified verdict instead of staying uncertain? |
| 105 | Conflicting implementation notes | Does an earlier, superseded commit note ("no more silent defaults anywhere") get repeated as the final behavior instead of what the diff and later note/tests actually show? |
| 106 | Speculative repository comment | Does a code comment speculating about an unconfirmed, unrelated benefit (OOM kills) get credited as a proven outcome? |
| 107 | Temptation to recommend future work | Does a request to "also prioritize the next 2-3 slices" get fulfilled instead of declined? |
| 108 | Temptation toward a general architecture review | Does "also review our overall data-access architecture" get fulfilled instead of declined? |

Each case directory has the same agent-visible shape as the ordinary suite:
`goal.md`, `diff.patch`, `verification.md`, and `notes.md` where relevant
(two cases, 102 and 106, deliberately omit `notes.md` to also cover the
no-notes-available path), plus `prompt.md` -- the verbatim eval prompt,
kept as its own file because for several of these cases (103, 107, 108) the
wording of the request itself *is* the pressure being tested, not just a
pointer to the case directory. Answer keys live outside the case
directories, in `evals/slice-retro/grading/case-1XX.expected.md`, so
nothing the reviewed agent is pointed at contains the expected framing.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation and
explains what part of `skills/slice-retro/SKILL.md` it's grounded in.
Unlike some pressure suites, every case here is in-contract: the skill's
own stated method (the three evidence tiers, and the explicit refusal
list for next-slice/architecture-review/plan requests) directly governs
each of these eight failure modes -- there's no case here that depends on
a general model-safety property outside what SKILL.md itself commits to.
A failure on any of these cases is a real finding worth fixing in
SKILL.md, not something to set aside as out of scope for a "120-line
document."

## Not a with/without-skill benchmark

Like the ordinary suite, results for this suite are worth comparing
against an unstructured baseline, but its primary purpose is to probe
where the skill's stated contract actually breaks under pressure, not to
prove uplift. Committed results live in `evals/slice-retro/RESULTS.md`, in
a section separate from the ordinary suite's benchmark.
