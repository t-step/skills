# cloudscape-native-expression-review — eval design

This eval is separate from `evals/cloudscape-implementation-audit/` — a
different reasoning problem (component selection + pattern composition,
not implementation mechanics), evaluated as its own experiment. It shares
the same umbrella authority snapshot and fixture setup recorded in
`evals/design-system-calibration/SETUP.md`.

**A note on historical paths:** the documents in this eval (and in
`evals/design-system-native-expression-review/`) reference
`skills/cloudscape-native-expression-review/SKILL.md`,
`skills/cloudscape-implementation-audit/SKILL.md`, and
`evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md` as they
existed when those documents were written. None of those paths exist in
this repository's current tree. Those references are left as originally
written — they are a historically truthful record, not revised to look
current — and frozen, byte-identical copies of the files they cite are
preserved under [`archive/`](archive/README.md), with exact source commit
SHAs. The active, maintained skill is
`skills/design-system-native-expression-review/`.

## Shape of this eval

Unlike the sibling implementation-audit eval (three real, unmodified
fixtures with no answer key, because no one decided in advance what
"correct" looks like), this eval needs *adjudicable* cases to answer its
central open question — whether component selection and pattern
composition are genuinely one reasoning operation, and whether the
skill's applicability discipline holds under targeted pressure. That
requires cases with a known, author-decided intended answer:

- `cases/case-a-*/` through `cases/case-f-*/` — six purpose-built
  synthetic fixtures, one per required pressure case (A–F from the task
  brief), each with a `prompt.md` (the exact framing given to both the
  baseline and skill runs) and a `fixture/` tree of real, self-contained
  `.tsx` files.
- `cases/case-real-identities/` — a pointer case (no copied fixture; see
  its `prompt.md`) into the same real, pinned-SHA
  `sample-bedrock-spend-budget-guardrails` repo and the same
  `Identities.tsx` surface `cloudscape-implementation-audit` already
  reviewed. Reused deliberately: iteration 2 of that sibling eval produced
  an adversarially-confirmed **D-grade overreach** when the
  implementation-level skill tried to recommend `variant="full-page"`
  over `ContentLayout` + `Table variant="container"` — a pattern-level
  call it has no business making. This is exactly this skill's job
  instead. Whether this skill reaches the same substantive recommendation
  *without* the D-grade — correctly scoped, correctly authorized — is the
  single most direct real-world validation this eval can offer.
- `grading/case-{a..f}.expected.md` — isolated grading keys (never inside
  `cases/`, per this repo's eval-isolation convention) stating, per case,
  what a correct response looks like and why each case is diagnostic.
  There is deliberately no grading key for the real-fixture case — nobody
  decided its "correct" answer in advance, same as the sibling eval's real
  fixtures; its adjudication is `rubric.md` plus the D-grade precedent
  above, not a pre-written key.
- `rubric.md` — the adversarial verification rubric used to grade every
  candidate finding a skill run produces (A–E), adapted from the sibling
  eval's rubric with this skill's own applicability-specific verification
  questions.
- `runs/*.md` — hand-curated, committed writeups of each run (baseline,
  skill, verification). Full raw transcripts are local, gitignored
  (`evals/*/runs/*/`, per this repo's `.gitignore`).
- `RESULTS.md` — the numeric/qualitative summary and verdict.

## Freeze discipline

Per the task brief: the skill's design, the six pressure cases, and their
grading keys were authored and validated for adjudicability *before* any
baseline or skill run against them, and before the real-fixture rerun.
`skills/cloudscape-native-expression-review/SKILL.md` was not edited after
seeing any run's output. If a later iteration edits it, that is recorded
as a new iteration with the observed failure that justified it, per this
repo's `AGENTS.md` eval-expectations convention — never a silent tune.

## What "passing" means here

No expectation count to hit. Per case, the question is whether the
skill's candidate findings match the case's intended diagnostic answer
(a real, material, correctly-scoped finding on A/B/C; a correctly
suppressed or absent finding on D/E/F) and whether those findings survive
adversarial verification. Across the whole suite, the question is
comparative: does the skill's reasoning procedure produce findings that
are more precise, more material, better evidenced, more resistant to
cargo-cult pattern-matching, and more successful at unifying component and
pattern reasoning into one recommendation than an unguided baseline given
the same fixture and the same authoritative Cloudscape material — and do
those findings survive adversarial verification. See `RESULTS.md` for the
actual judgment.
