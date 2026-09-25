# Freeze manifest -- R4 severity/tier-floor intervention (2026-09-24)

**Base commit tested against:** `63af571d7f8273d45224abcc1d220f792930e9a5`
(`fix(identity-authority-audit): route unresolved existence-questions out
of Findings`) plus one uncommitted working-tree edit to
`skills/identity-authority-audit/SKILL.md` (see "The intervention"
below) -- this experiment measures that edit, not yet a committed SHA.

## What is frozen here

- `frozen/skill/SKILL.md` -- the **post-intervention** skill: identical
  to `skills/identity-authority-audit/SKILL.md` as of this experiment,
  i.e. the case-102-stability-rerun's frozen `SKILL.md` plus exactly one
  new paragraph inserted immediately before the HIGH/MEDIUM/LOW severity
  list in Review mode (see "The intervention"). No other line changed.
- `frozen/skill/references/framework-signals.md`,
  `frozen/skill/references/organization-profile-template.md` -- byte-
  identical to the live repo and to the prior stability-rerun's frozen
  copies; not touched by this intervention.
- `frozen/cases/case-102/*.py`, `frozen/cases/case-102/context.md` --
  byte-identical to `evals/identity-authority-audit/cases/case-102/` and
  to the prior stability-rerun's frozen copies (verified with `diff -r`
  before this run). Not edited.
- `frozen/grading/case-102.expected.md` -- byte-identical to
  `evals/identity-authority-audit/grading/case-102.expected.md` and to
  the prior stability-rerun's frozen copy (verified with `diff`). Not
  edited.
- `frozen/grading/RUBRIC.md.source-review-findings-fix` -- copy of
  `../2026-09-24-review-findings-fix/RUBRIC.md`, the rubric whose case-102
  section (R1-R7, F1-F3, T3) this experiment grades against, unedited.
- `prompts/case-102-with-skill.md` -- the exact run prompt: the prior
  stability-rerun's frozen prompt
  (`../2026-09-24-case-102-stability-rerun/prompts/case-102-with-skill.md`)
  with only its embedded `SKILL.md` block replaced by the post-
  intervention `SKILL.md` above (verified by `diff`: the only changes are
  the one new paragraph and one blank-line spacing correction around it;
  the case evidence, task context, and run instructions are byte-for-byte
  unchanged from the prior experiment's prompt).

See `CHECKSUMS.sha256` (generated after all files above were placed, not
regenerated afterward) for exact SHA-256 hashes of every frozen file.

## The intervention

One paragraph inserted into `skills/identity-authority-audit/SKILL.md`,
in Review mode, immediately before the existing HIGH/MEDIUM/LOW severity
bullet list (after "Within Confirmed and Likely findings only, a coarse
consequence class may help a reader triage, and nothing finer than
this:"). Full text of the inserted paragraph:

> The same floor applies here, not only to tier: a severity level's own
> wording can quietly reassert the exact exploitability the paragraph
> above just excluded from Confirmed. HIGH's "reachable... without
> appropriate authorization" is itself an exploitability claim -- don't
> reach for it on the strength of a Confirmed structural fact alone when
> reachability is exactly what's unresolved. Pick the level whose own
> definition matches only what's actually confirmed (often MEDIUM's
> "missing defense in depth"), or keep HIGH by carrying the finding at
> Likely instead, where the tier itself already carries that inference. A
> Confirmed tier and an unearned HIGH are not a shortcut around naming the
> same uncertainty twice -- they're the uncertainty being paid for once
> and spent twice.

Nothing else in `SKILL.md` was changed. No fixture, grading key, or the
Findings/Open-questions admission rule itself (the two paragraphs
immediately above the edit point) was touched.

## Regression-check additions (Phase 4)

After the 5-run case-102 targeted validation passed at 4/5, the following
were added for the regression subset -- none touch case-102's own frozen
files above:

- `frozen/cases/case-105/`, `frozen/cases/case-108/`, `frozen/cases/case-109/`,
  `frozen/cases/case-112/` -- byte-identical copies of
  `evals/identity-authority-audit/cases/case-1{05,08,09,12}/`, unedited.
- `frozen/grading/case-105.expected.md`, `case-108.expected.md`,
  `case-109.expected.md`, `case-112.expected.md` -- byte-identical copies
  of the live grading keys, unedited.
- `prompts/case-105-with-skill.md`, `case-108-with-skill.md`,
  `case-109-with-skill.md`, `case-112-with-skill.md` -- built the same
  way as `case-102-with-skill.md`: the post-intervention `SKILL.md` and
  both references verbatim, followed by that case's own `context.md` and
  evidence files verbatim, followed by the identical "Instructions for
  this run" block. Each case's own evidence is otherwise untouched.

See "Regression subset selection" in `RESULTS.md` for why these four
cases were chosen. `CHECKSUMS.sha256` was regenerated after these
additions and covers all of `frozen/` and `prompts/`.

## Isolation method (identical to the prior stability rerun)

Each of the 5 trials is a freshly spawned, independent subagent with no
shared context with this session, each other, or any prior run. Each
subagent receives only the frozen prompt's full text (case evidence and
post-intervention skill text are self-contained in the prompt) and is
instructed not to call any tool. No run sees the grading key, sibling
outputs, or any prior experiment's summary. Each run's raw response is
saved unedited to `runs/r4-floor-NN.md`.
