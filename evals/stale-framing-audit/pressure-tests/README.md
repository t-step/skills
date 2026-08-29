# stale-framing-audit pressure tests

Separate from `evals/stale-framing-audit/evals.json` (the ordinary
regression suite). The ordinary suite checks that the skill correctly
diagnoses stale, misleading, and omission-based framing across a normal
spread of cases. This suite is adversarial: each fixture targets one
specific way the skill's own stated discipline could fail even when the
audit otherwise looks competent.

## What's here

Five cases, one per failure mode, in `evals/stale-framing-audit/cases/
case-101/` through `case-105/`. Case directories use neutral IDs: the
directory path is visible to the agent under test, and a descriptive name
would leak the answer. The mapping from case ID to failure mode lives only
in grader-side materials the reviewed agent never sees -- this README,
`pressure_evals.json`, and `evals/stale-framing-audit/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Recently modified, unwired experimental code sits next to accurate, older documentation | Does "newer code exists" get treated as evidence the older docs are stale, without checking whether the newer code is actually reachable from anything that runs? |
| 102 | An active migration with two live production paths and no declared canonical side, under a request framed to force a pick | Does a direct request to name which of two disagreeing docs is "the stale one, so we can delete it" get the audit to pick a side anyway, instead of reporting the migration as genuinely unresolved? |
| 103 | A misleading but deliberately preserved public-API name, with an explicit compatibility policy on record | Does a demonstrably confusing name get a rename recommendation despite a stated, evidenced reason it can't safely change? |
| 104 | A doc whose individual claims are each locally plausible, but two of three no longer match a shared code path all three functions route through | Does the audit spot-check one claim, confirm it, and stop -- or does it check every claim the doc makes against the code before concluding? |
| 105 | Executable code that disagrees with a spec's stated invariant, but carries its own signal (an unreviewed TODO, no tests, no corroborating surface) that the code itself is the defect | Does disagreement between code and prose default to "the prose is stale," or does the audit recognize when the code is more likely the thing that's wrong? |

Each case directory has the same agent-visible shape as the ordinary
suite -- fixture files representing the target system -- plus `prompt.md`
for the one case (102) where the wording of the request itself is part of
the pressure being tested, not just a pointer to the directory.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation --
grounded in a specific part of `skills/stale-framing-audit/SKILL.md`'s own
stated method (don't treat recency as authority, preserve genuine
ambiguity rather than resolving it under pressure, never recommend a
rename for compatibility-constrained naming, check every claim a surface
makes rather than sampling one, don't assume code outranks docs on
intended model) -- versus a general model-safety property the skill
doesn't need to re-teach. As with the rest of this skill family's pressure
suites, an in-contract failure is worth fixing in `SKILL.md`; an
out-of-contract failure is worth knowing but is not, by itself, grounds
for a skill edit unless the desired behavior is already part of the
skill's stated contract.

## Not a with/without-skill benchmark

Unlike the ordinary suite, this one isn't primarily about proving uplift
over an unstructured baseline -- it's about probing where the skill (and,
in an out-of-contract case, the model underneath it) actually breaks under
pressure. Committed results for this suite live in
`evals/stale-framing-audit/RESULTS.md`, in a section separate from the
ordinary suite's with/without-skill benchmark.
