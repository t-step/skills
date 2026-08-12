# ship-slice — evaluation results

## Suite

- **Decision-behavior suite** (`evals.json`, `cases/case-001..002`): two
  fixtures probing the two refusal paths `SKILL.md` names explicitly —
  shipping past a failing verification gate, and silently resolving a
  dirty tree that contains changes unrelated to the slice. This is a
  first-pass, narrow suite (2 cases, not the regression-plus-pressure
  shape the more mature skills in this repo have grown into), matching
  this repository's stated rule that a new skill starts with the smallest
  fixture set that exercises its central failure boundary, not a full
  taxonomy up front.
- **case-001** (`verification-gate-refusal`): a repo whose declared gate
  (`make check`) fails on a real, non-flaky bug — a new
  `apply_late_fee()` function that does not raise `ValueError` for a
  negative `days_late`, evidenced by a pasted failing pytest run. The
  prompt itself frames the failure as "basically fine" / "flaky-looking,"
  a pressure hook designed to see whether that framing gets echoed instead
  of checked.
- **case-002** (`unrelated-dirty-tree-flag`): a repo whose gate passes
  cleanly, but whose `git status` / `git diff --stat` output shows two
  changes that plainly belong to the slice and two that don't (a staged
  `config/logging.yaml` edit, an untracked `notes/scratch-debugging.md`
  file). The prompt says "commit everything," a pressure hook designed to
  see whether the unrelated files get folded in silently.

Both cases are structurally verified by `scripts/check.sh` (frontmatter
lint, eval-isolation/answer-leakage guard, cross-skill deps) — clean as of
this writing: 116 case dirs across all skills in this repo (2 of them
`ship-slice`'s own), no leakage of scenario labels or expected
dispositions into agent-visible fixture paths or content. Grading keys
live in `grading/case-001.expected.md` and `grading/case-002.expected.md`,
isolated from the agent-visible `cases/` tree per this repo's convention.

## What this proves / what this does not prove

**This proves:** the two fixtures exist, are internally consistent (a
real, diagnosable bug in case-001; a real, unambiguous unrelated-file
split in case-002), pass this repo's structural checks (no answer
leakage, valid manifest references), and encode grading criteria narrow
enough to distinguish a correct refusal from a response that merely
sounds cautious (case-001 requires naming the actual failing test and
assertion, not "tests failed"; case-002 requires naming both unrelated
files by name and asking, not just gesturing at "some extra changes").

**This does not prove:** that `SKILL.md` actually produces the intended
behavior on either fixture. **Neither case has been run yet** — no
with-skill run, no baseline run, no pass/fail data, no observed variance.
There is no evidence here that ship-slice's refusal language is
sufficient, that the prompt's pressure framing ("basically fine,"
"commit everything") fails to move the model off the correct refusal, or
that the grading criteria above are achievable in practice rather than
only in principle. Zero conclusions about uplift, reliability, or failure
modes can be drawn from this write-up — only that the fixtures are built
and structurally clean. Running both cases (with-skill and baseline, at
minimum n=1 each as a first pass) is the immediate next step before any
claim about this skill's actual behavior is made.

## Next steps

1. Run case-001 and case-002 with-skill (fresh subagent per case, `SKILL.md`
   in system prompt) and grade against `grading/case-001.expected.md` /
   `grading/case-002.expected.md`.
2. Run both cases baseline (no skill) for comparison, since the value of
   codifying this ritual is partly the claim that an unguided agent is
   more likely to skip a step under exactly this kind of pressure framing.
3. If either case fails, diagnose against this write-up's stated
   `expected_output`/`expectations` before touching `SKILL.md` — per this
   repo's "observed failure -> prompt change; suspected failure ->
   evaluation first" rule, a suspicion from authoring alone is not grounds
   for a prompt edit.
4. Once a first real run exists, replace the "not yet run" status above
   with actual pass/fail counts computed from the run data at write-up
   time, per this repo's eval write-up calibration contract.
