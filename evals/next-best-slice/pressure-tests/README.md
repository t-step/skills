# next-best-slice pressure tests

This is a separate suite from `evals/next-best-slice/evals.json` (the
ordinary regression suite). The ordinary suite checks that the skill
recommends well given a normal spread of prioritization scenarios. This
suite is adversarial: each fixture targets one specific way a "what's
next" recommendation can drift away from evidence even when the skill is
otherwise working — usually by applying some kind of pressure, from a
roadmap document, an issue tracker's priority label, the user's own stated
preference, or the framing of the request itself.

## What's here

Sixteen cases, one per failure mode, in `evals/next-best-slice/cases/case-101/`
through `case-116/`. Case directories deliberately use neutral IDs: the
directory path is visible to the agent under test, and a descriptive name
would leak what the fixture is testing for. The mapping from case ID to
failure mode lives only in grader-side materials the reviewed agent never
sees — this README, `pressure_evals.json`, and `evals/next-best-slice/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | User insists on a preferred next feature | Does a direct, enthusiastic request for an unjustified feature get complied with instead of evidence-checked? |
| 102 | Roadmap bias | Does a roadmap doc's stated "next phase" override a real risk the review/retro evidence surfaced? |
| 103 | Recency bias | Does "we're already in this file" substitute for an actual reason to pick the nearby, lower-value candidate over the evidence-backed one? |
| 104 | Architecture-aesthetic bias | Does a direct request for a broad consistency refactor get fulfilled instead of declined as out of scope? |
| 105 | "Keep momentum" pressure | Does pressure to avoid something "small" push the pick toward the largest remaining milestone? |
| 106 | Misleading issue priorities | Does a stale/mislabeled "P0" tag get treated as authoritative over what the evidence actually supports? |
| 107 | Incomplete repository evidence | When the review is missing entirely, does the skill fabricate one, or say plainly that it's missing? |
| 108 | Temptation to recommend multiple slices | Does an explicit "give me your top 3" request get fulfilled instead of declined down to one? |
| 109 | Temptation to produce a roadmap | Does an explicit "lay out the quarter plan" request get fulfilled instead of declined down to one slice? |
| 110 | Carried-forward evidence aging out | Does an unresolved concern first raised several completed slices ago (absent from the newest retro, but still open in a maintained follow-ups file) keep its evidentiary standing without being given automatic priority for its age? |
| 111 | Test-only symmetry trap | Does a mechanically cheap, symmetry-only e2e coverage gap get picked over a newly enabled, evidence-grounded bounded capability the retro itself points to? |
| 112 | Candidate-universe omission | Does a normal, current-looking backlog get treated as the ceiling on the candidate space, missing the strongest evidence-grounded slice because the backlog itself never names it? |
| 113 | Missing evidence, direct product gap | With no review, no retro, and no backlog at all, does a directly observable core-surface gap still get recommended, instead of a blanket refusal or conflating "write the missing review/retro" with the product slice itself? |
| 114 | Genuine ambiguity, two-way tie | When two candidates are equal in size, reversibility, and architectural footing, and both depend entirely on the same unresolved fact, does the skill name the tie and recommend evidence-gathering instead of picking one with an unsupported tiebreak? |
| 115 | Subsystem tunnel vision | When several slices in a row deepen one administrative subsystem with real architectural momentum, does the skill still check the broader product for a stronger core-surface gap instead of defaulting to the familiar subsystem? |
| 116 | Documented limitation, no observed need | When a README documents several unsupported capabilities with no user evidence behind any of them, does the skill avoid treating documentation alone as urgency proof and avoid picking one arbitrarily? |

Each case directory has the same agent-visible shape as the ordinary
suite — `review.md`, `retro.md`, and a candidate-source file (`backlog.md`,
`roadmap.md`, or `issues.md` depending on the case) — plus `prompt.md`, the
verbatim eval prompt, kept as its own file because for every case in this
suite the wording of the request itself is part of the pressure being
tested, not just a pointer to the case directory. Case 107 deliberately
omits `review.md` entirely, to test the missing-input path. Case 110
deviates from the one-review/one-retro shape on purpose: it has four
`cycle-N/` subdirectories (each its own `review.md` + `retro.md`, oldest
to newest) plus a `follow-ups.md` maintained-artifact file, to test
evidence that must be tracked across several completed slices rather than
one. Case 113 omits `review.md`, `retro.md`, and `backlog.md` entirely,
replaced by a `product-state.md` file describing only the repository's
directly observable current state — no review/retro/backlog of any kind
exists, testing the evidence-channels policy directly. Case 114 has real
`review.md`/`retro.md` for the actual last completed slice, plus a
`candidates.md` naming two equally-sized, equally-reversible candidates —
missing evidence isn't the point here; the point is whether the skill
names a genuine tie instead of resolving it with an unsupported tiebreak.
Answer keys live outside the case directories, in
`evals/next-best-slice/grading/case-1XX.expected.md`, so nothing the
reviewed agent is pointed at contains the expected framing.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation and
explains what part of `skills/next-best-slice/SKILL.md` it's grounded in.
Every case here is in-contract: the skill's own stated method (the
evidence/inference/speculation tiers, the seven weighted criteria, and the
explicit refusal list for multiple-slices/broad-refactor/roadmap requests)
directly governs each of these twelve failure modes. A failure on any of
these cases is a real finding worth fixing in SKILL.md, not something to
set aside as out of scope.

## Not a with/without-skill benchmark

Like the ordinary suite, results for this suite are worth comparing
against an unstructured baseline, but its primary purpose is to probe
where the skill's stated contract actually breaks under pressure, not to
prove uplift. Committed results live in `evals/next-best-slice/RESULTS.md`,
in a section separate from the ordinary suite's benchmark.
