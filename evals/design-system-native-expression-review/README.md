# design-system-native-expression-review — eval home

This is the eval home for the **active** skill,
`skills/design-system-native-expression-review/SKILL.md` — a deliberate,
evidence-driven generalization of two frozen predecessors:

- `evals/cloudscape-native-expression-review/` — the original,
  Cloudscape-only skill's own eval: six purpose-built pressure cases (A–F,
  plus P1/P2 added in iteration 3), grading keys, and adversarially-
  verified run results. Preserved verbatim as historical evidence; its
  `SKILL.md` references (`skills/cloudscape-native-expression-review/...`)
  describe that frozen, pre-morph skill, not the active one.
- `evals/design-system-calibration/` — the shared fixture/authority
  workspace (`SETUP.md`), plus the MUI generalization round
  (`MUI-GENERALIZATION-NOTES.md`, `MUI-RESULTS.md`, `mui-runs/`) that
  pointed the *frozen, unmodified* Cloudscape-only skill at Material UI to
  test whether its reasoning operation was corpus-neutral. That round's
  central finding — the reasoning architecture (scope fence, anti-
  fundamentalism rule, missing-intent handling) transferred, but citation
  fabrication/conflation rose from 1-in-7 findings to 3-in-6 — is what
  this skill's morph specifically targets.

## What changed in the morph

See `skills/design-system-native-expression-review/SKILL.md`'s own
"Lineage" section for the full account: corpus-adaptive
authority discovery (no assumed Cloudscape-shaped hierarchy), a
corpus-neutral finding taxonomy (`component selection` / `documented
composition` / `combined selection + composition` / `intent-dependent`),
and an explicit evidence-mode discipline (`VERBATIM` / `PARAPHRASE` /
`SYNTHESIS` / `INFERRED`) layered onto the existing authority-strength
scale. The reasoning procedure itself — bounded-surface scope, establish-
task-first, the implementation-correctness scope fence, the anti-
fundamentalism rule, the missing-intent escape hatch — was deliberately
preserved, not rewritten.

## This directory

- `runs/*-skill.md` — six fresh regression runs of the *generalized*
  skill: three reused Cloudscape pressure cases (`case-b`, `case-c`,
  `case-p1`, chosen to cover component-selection precision, the validated
  combined-finding case, and the equally-valid-suppression trap) and the
  same three pinned MUI fixtures the prior round used (Checkmate, ntfy,
  hk-independent-bus-eta — "hkbus" in filenames).
- `runs/*-verify.md` — one independent adversarial verifier per run,
  re-fetching every cited page live and re-reading the fixture code,
  never trusting the reviewing run's own quotation marks.
- `RESULTS.md` — the regression verdict, citation-integrity comparison,
  and A/B/C/D classification.

Per this repo's eval-isolation convention, the Cloudscape cases' grading
keys (`evals/cloudscape-native-expression-review/grading/*.expected.md`)
were read only by verifiers, never by the reviewing runs themselves.

## Repeatability/adjudication round

`RESULTS-REPEAT.md` and `runs-repeat/*.md` record a second, independent
repeat of exactly three fixtures from the round above (Cloudscape P1,
MUI ntfy, MUI hk-independent-bus-eta) — the three that produced the four
regression signals `RESULTS.md` §5–§7 named as needing repeat evidence
before any wording change. No skill edit was made before, during, or
after either round. See `RESULTS-REPEAT.md` for the per-behavior
historical comparison, classification (confirmed recurring weakness /
likely run variance / insufficient evidence), and the resulting
recommendation.

## Post-fix refinement round

`RESULTS-POSTFIX.md` and `runs-postfix/*.md` record the first round that
actually edits `SKILL.md`, targeting the two axes `RESULTS-REPEAT.md`
confirmed as ready for a wording change: equally-valid-candidate
suppression (Cloudscape P1) and VERBATIM self-verification. The
AppBar/Toolbar axis was deliberately left untouched per that round's own
recommendation. The VERBATIM fix measurably worked across every fixture
retested. The equally-valid-suppression gate did **not** achieve
suppression on the P1 isolating case across four independent,
diagnosis-driven iterations — see `RESULTS-POSTFIX.md` §3 for the full
per-trial mechanism breakdown and a verified complication in the P1
grading key itself. Read `RESULTS-POSTFIX.md` before assuming this axis
is resolved; it isn't.

## Equivalence isolation round

`RESULTS-EQUIVALENCE.md` and `cases/case-{e1,e2,n1,n2}-*/`,
`grading/case-{e1,e2,n1,n2}-*.expected.md`, `runs-equivalence/*.md` record
a follow-up round that retires `case-p1-message-queues` Candidate 2 as an
equally-valid-suppression instrument (its grading key's premise that the
fixture supplies no resolving evidence is false — see `RESULTS-POSTFIX.md`
§3 and `RESULTS-EQUIVALENCE.md` §1) and replaces it with four purpose-built,
independently pressure-tested fixtures: two clean equivalence cases (E1, E2)
and two inverse controls testing for over-suppression (N1, an optional N2).
The skill was **not** edited during this round. Result: 7/7 fresh trials
produced the required or acceptable outcome, with no fabricated citations —
this round's diagnosis is that the prior P1-based finding was contaminated
by a compromised instrument, not a confirmed reproducible skill weakness.
Read `RESULTS-EQUIVALENCE.md` for the full trial-by-trial evidence,
fixture-defects discovered, and recommendation.

## Distillation round

`RESULTS-DISTILLATION.md` and `runs-distillation/*.md` record a
deliberate distillation pass on `SKILL.md` itself, not a further
behavioral iteration: the reasoning operation was treated as
provisionally validated by the equivalence-isolation round above, and
this round's job was to make the skill smaller and less shaped by its
own eval history while regression-testing that the validated reasoning
survived. `SKILL.md` shrank from 522 to 477 lines — mostly removal of
maintainer/historical narrative (now consolidated in this README and the
`RESULTS*.md` files below rather than duplicated in the runtime skill)
and a significant trim of the same-tier-equivalence paragraph that had
grown overfit to the retired P1 case. **E1, N1, and (optionally) N2 are
the ongoing canonical regression set for the equally-valid-suppression
axis** going forward; `case-p1-message-queues` Candidate 2 remains
retired/compromised for that axis exactly as described above — this
round did not revisit or restore it. Regression trials on the distilled
skill passed on E1 (suppression), N1 (report), and two strong prior
positive findings (Cloudscape Case C, MUI hk-bus-eta's
`RouteUpdateNotice`→`Alert`); N2 produced a mixed 1-of-2 result flagged
as an open item for a future round, not yet a confirmed regression. Read
`RESULTS-DISTILLATION.md` for the full line-by-line accounting, before/
after text, and trial-by-trial evidence.

## Closeout round

`RESULTS-CLOSEOUT.md` and `runs-closeout/*.md` record the follow-up round
that resolved the distillation round's one open item: five fresh,
independent N2 trials against each of the distilled and pre-distillation
`SKILL.md` versions (identical fixture, grading key, and protocol; no
skill edit before, during, or after). Both versions failed N2 once in five
fresh trials, via two distinct and unrelated failure mechanisms — an
authority-retrieval gap on the distilled skill, a materiality/reconciliation
misjudgment on the original — which this round classifies as run variance,
not a distillation regression. `SKILL.md` was **not** edited in this round.
See `RESULTS-CLOSEOUT.md` for the full trial-by-trial evidence, failure-
mechanism classification, and final recommendation (keep the distilled
skill; retain N2 as an accepted-variance case).
