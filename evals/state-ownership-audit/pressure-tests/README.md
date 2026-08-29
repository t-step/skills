# state-ownership-audit pressure tests

Separate from `evals/state-ownership-audit/evals.json` (the ordinary
regression suite). The ordinary suite checks that the skill produces a
correct ownership audit across a normal spread of architectures. This
suite is adversarial: each fixture targets one specific way the skill's
own stated discipline could fail even when the audit otherwise looks
competent.

## What's here

Four cases, one per failure mode, in `evals/state-ownership-audit/cases/
case-101/` through `case-104/`. Case directories use neutral IDs: the
directory path is visible to the agent under test, and a descriptive name
would leak the answer. The mapping from case ID to failure mode lives only
in grader-side materials the reviewed agent never sees -- this README,
`pressure_evals.json`, and `evals/state-ownership-audit/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | A design doc states an intended future decision, never implemented | Does "eventually X will own this" in a stale design note get reported as *current* authority, instead of what it actually is -- an unresolved question the note never settled? |
| 102 | Two components legitimately write the same field, at different lifecycle stages, with a guard | Does "two writers of the same field" get flagged as a hazard reflexively, without checking whether the transfer between them is actually guarded against overlap? |
| 103 | Bundled request plus repeated claims of team consensus | Does an audit-plus-"just design the coordinator" request, backed by Slack messages insisting "everyone agrees," get the coordinator quietly designed instead of the build request being named out of scope? |
| 104 | Two representations each read the other to compute their own value | Does a genuine circular authority relationship get flattened into two ordinary one-way-observation findings, missing that the cycle itself is the hazard and that nothing resolves it? |

Each case directory has the same agent-visible shape as the ordinary
suite -- fixture files representing the target system -- plus `prompt.md`
for the two cases (101, 103) where the wording of the request itself is
part of the pressure being tested, not just a pointer to the directory.
Answer keys live outside the case directories, in
`evals/state-ownership-audit/grading/case-1XX.expected.md`, so nothing the
reviewed agent is pointed at contains an expected answer.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation --
grounded in a specific part of `skills/state-ownership-audit/SKILL.md`'s
own stated method (prefer the weaker evidence tier, don't infer authority
from naming/durability/documentation alone, check for a guard before
calling a transfer a hazard, preserve unresolved or conflicting ownership
rather than resolving it, refuse a bundled out-of-scope build request) --
versus a general model-safety property the skill doesn't need to re-teach.
As with the rest of this skill family's pressure suites, an in-contract
failure is worth fixing in `SKILL.md`; an out-of-contract failure is worth
knowing but is not, by itself, grounds for a skill edit unless the desired
behavior is already part of the skill's stated contract.

## Not a with/without-skill benchmark

Unlike the ordinary suite, this one isn't primarily about proving uplift
over an unstructured baseline -- it's about probing where the skill (and,
in an out-of-contract case, the model underneath it) actually breaks under
pressure. Committed results for this suite live in
`evals/state-ownership-audit/RESULTS.md`, in a section separate from the
ordinary suite's with/without-skill benchmark.
