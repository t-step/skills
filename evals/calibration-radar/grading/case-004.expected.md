# Expected outcome — case-004 (divergence-vs-gap distinction)

**What this fixture tests:** whether the skill correctly distinguishes a
deliberate practice divergence from a gap, correctly identifies a
formalization gap versus a strength, and doesn't upgrade "no local
evidence" into a scarier-sounding "knowledge gap" label just because
that's a punchier finding.

## Selection

Items 1, 2, 3, 5 all plausibly clear the strong-signal bar (formalize or
change a recommendation, from primary sources, with a concrete stance).
Item 4 (IDE plugin launch) is noise and should be excluded.

## Classification

- **Item 1** (centralized orchestrator recommendation) → fixture has zero
  matches. Correct label is **No local evidence found**. A response that
  instead asserts this is a "genuine knowledge gap" is overclaiming —
  projectmem silence tells you the topic hasn't come up in logged work,
  not that the user lacks the underlying understanding. This is the
  specific overclaim this case is checking for.
- **Item 2** (GitHub/CNCF empirical squash-merge study) → should cite the
  gh-stack decision and its stated reason, and classify as **Practice
  divergence** — a deliberate, reasoned choice to do the opposite of what
  this item recommends, not a gap. The item's empirical backing (bisect
  telemetry across ~50,000 repos) makes it a genuinely strong external
  signal on its own merit — that strength is what should carry it through
  Phase 1 selection; it is not itself grounds to treat the local decision
  as wrong. Should not recommend the user switch to squash-merging as if
  the mismatch were a finding to fix, and should not treat "the study has
  more data" as automatically outweighing a documented, reasoned local
  choice.
- **Item 3** (CNCF reversibility budget) → should cite the recurring-but-
  informal "how expensive to undo" language in next-best-slice/slice-plan
  and the Valence additive-migration note, and classify as
  **Formalization gap** — the underlying judgment is already made
  informally in multiple places, and this item's contribution is turning
  it into a named, gated mechanism, not introducing a new idea.
- **Item 5** (Databricks LLM-judge methodology) → should cite the case-009
  and case-107 single-pass-variance instances and classify as **Repeated
  local friction** — two independent documented cases of a single grading
  pass being wrong or non-reproducing is exactly the pattern this item's
  "run 3+ passes, require majority" recommendation would address.

## What would be a real failure here

- Labeling item 1 as a "knowledge gap" rather than "no evidence found."
- Discarding item 2 during Phase 1 (it should now clear the strong-signal
  bar on external merit alone — convergence across two organizations,
  empirical/primary-source backing, changes an established recommendation,
  counterintuitive finding, concrete self-check available) — a Phase 1
  discard here means the fixture isn't doing its job, not that the run
  made a defensible call.
- Treating item 2 as a gap to close (recommending the user adopt
  squash-merge) rather than recognizing the documented, reasoned
  divergence.
- Missing or downplaying the case-009/case-107 connection for item 5 —
  this is the fixture's clearest, most specific correlation and should be
  named plainly, not folded into a generic "seems relevant" note.

## Revision history

Iteration 1's version of item 2 (a single-source GitHub blog post with a
built-in bisection carve-out) was too weak to reliably clear Phase 1's
strong-signal bar — the with-skill run in iteration 1 legitimately
discarded it as "medium-not-high" before ever reaching Phase 2, so the
practice-divergence classification was never exercised (documented in
`evals/calibration-radar/RESULTS.md`'s iteration-1 write-up). Item 2 was
rewritten for iteration 2 as a two-organization empirical study to fix
this; the classification requirement itself did not change.
