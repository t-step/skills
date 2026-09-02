# design-system-native-expression-review — equally-valid-suppression isolation round

**Run date:** 2026-09-02. **Skill state:** unchanged (frozen) throughout this
round — `skills/design-system-native-expression-review/SKILL.md` was not
edited. No existing validated fixture or grading key was edited; this round
is entirely new fixtures, new grading keys, and one new results file.

**Purpose:** `RESULTS-POSTFIX.md` §3 left the equally-valid-candidate-
suppression axis in an unresolved state: four independent, diagnosis-driven
SKILL.md wording iterations all failed to make the skill suppress
`case-p1-message-queues`' Candidate 2 (`TextFilter` → add
`CollectionSelectFilter`), but the same round discovered that the P1
grading key's own factual premise — "the fixture shows no code, comment, or
header language establishing which lookup mode operators actually use" —
is false. `MessageQueues.tsx`'s own header comment plausibly resolves the
filter-patterns table's differentiating "user goals" row, meaning all four
observed failures may have been the model correctly reading a real (if
contestable) piece of evidence, not a reasoning defect. This round's charter
was to stop arguing about the old fixture and build cleaner instruments that
isolate the exact question, in both directions, without relitigating P1.

## 1. Why the previous P1 fixture was considered potentially compromised

`case-p1-message-queues/fixture/src/pages/MessageQueues.tsx` lines 29-33
carry a header comment: *"Operators can search by queue name, or narrow the
list down to a specific status or region while triaging."* The filter-
patterns page's criteria table ties `TextFilter` and `CollectionSelectFilter`
on "Complexity of the resource" and differentiates them only by a "User
goals" row phrased as two different user-behavior claims. `RESULTS-
POSTFIX.md`'s v4 trial cited exactly this comment as surface-level evidence
resolving which user goal applies to `status`/`region` — a legitimate,
non-fabricated reading of real fixture text, confirmed independently by both
a direct fixture read this round and the prior round's adversarial verifier.
Per the grading key's own MUST-SUPPRESS bar, this was still scored FAIL —
but a case whose own grading key misstates the fixture's evidentiary content
cannot cleanly distinguish "the skill has a suppression weakness" from "the
skill correctly used evidence its own grading key claimed didn't exist."
This round does not re-litigate that scoring; it retires P1 for this
specific axis and builds instruments that don't carry the same defect.

## 2. New fixtures and why each is a clean instrument

All four fixtures live under
`evals/design-system-native-expression-review/cases/case-{e1,e2,n1,n2}-*/`,
each with a `fixture/` (synthetic, single-file bounded surface + minimal
`package.json`/`package-lock.json` pinning `@cloudscape-design/
components@3.0.900`) and a `prompt.md`. Grading keys live under
`evals/design-system-native-expression-review/grading/case-{e1,e2,n1,n2}-
*.expected.md`. Every authoritative quote below was independently
live-fetched from `cloudscape.design` on 2026-09-02, both while building the
grading keys and again during grading (see §7).

**Case E1 — `ApiKeys.tsx` (explicit equivalence, TextFilter vs.
CollectionSelectFilter).** A direct re-instrument of the retired P1
Candidate 2, with the confound surgically removed: a `Table` (not `Cards`,
so no Cards/Table finding can arise and dilute isolation) of 16 API keys,
two low-cardinality columns (`environment`, `status`), one `TextFilter`, a
single neutral header description ("Manage API keys for this account."),
and **zero comments anywhere in the file**. Cloudscape's `/patterns/general/
filter-patterns/` criteria table ties `TextFilter`/`CollectionSelectFilter`
on "Complexity of the resource," differentiated only by an unresolved "User
goals" row — re-verified live, character-for-character identical to what
the P1-era evals recorded. Pressure-tested against the fixture-quality
checklist: repo evidence is a bare title + 4 neutral column headers;
authoritative evidence is the live-verified tie; the identified
opposite-direction reading (treating column cardinality itself as evidence
of a filtering "goal") is explicitly named and rejected in the grading key,
since cardinality is already priced into the tied "Complexity" row and
re-using it under "User goals" double-counts the same fact; the verdict is
grounded in SKILL.md's own frozen "same-tier equivalence controls point 4"
text, not a judgment call; and item 5 (would removing a comment change the
result) is trivially **no** — there is no comment to remove, which is
exactly the property the retired P1 case lacked.

**Case E2 — `CreateBackupSchedule.tsx` (non-obvious equivalence,
RadioGroup vs. Tiles).** A materially different instrument from E1 — no
single "same cell" sentence settles it. Cloudscape's `/patterns/general/
selection/` page carries **two separate criteria tables**: a "Boolean
selection criteria" table that ties `RadioGroup` and `Tiles` on every row
for a plain on/off choice ("Selection": both "takes effect at form
submission"; "Additional metadata": both "can be included for both the on
and off options"), and a separate "Single selection criteria" table
(general 2-7-option case) that differentiates them by metadata richness.
The fixture is a "Create backup schedule" form with a two-option, plain-
text, submission-gated `RadioGroup` ("Retention policy") carrying no
metadata of any kind — deliberately shaped so the *boolean* table is the
one that actually governs it, and even under the general table's own logic
`Tiles`' stated rationale ("Use for selections that require additional
metadata to compare mutually exclusive options," confirmed live on the Tiles
component page, `/components/tiles/`) doesn't apply, since no metadata
exists to compare. Two independent lines of defense against a wrongly-
reported finding, by design. No comment exists in the fixture; item 5 is
again trivially no.

**Case N1 — `AccountSettings.tsx` (inverse control, Checkbox vs. Toggle).**
Both components are officially supported; Cloudscape's own "Boolean
selection criteria" table states a concrete, directional, checkable
criterion on its "Selection" row: `Checkbox` "takes effect at form
submission" vs. `Toggle` "results in an immediate change." The fixture
wires two `Checkbox` controls whose `onChange` handlers call `setState`
*and* fire an immediate `fetch(..., { method: 'PATCH' })` — with **no
`<form>` element, no `Button` of any kind, and no other commit/confirm
mechanism anywhere in the file**. This is structural, code-level evidence,
independent of any comment (there is none). The opposite reading
("the fetch could be optimistic, the real save might be elsewhere") is
named and foreclosed by the fixture's total absence of any deferred-commit
affordance. Item 5 is again trivially no — the finding rests on code
structure, not prose.

**Case N2 — `CreateEnvironment.tsx` (composition inverse control,
optional).** Tests the same discipline at the composition level.
Cloudscape's `/patterns/resource-management/create/` page gives a numeric,
directly-countable Length threshold: single-page create fits "Between 2 and
15 fields... or up to 5 groups"; multipage create (`Wizard`) fits "More
than 16 fields... or more than 5 groups." The fixture is a single-page
`Form` with 20 fields across 6 `Container` groups, all directly visible (no
`ExpandableSection`), independently clearing *both* thresholds. No comment
in the fixture; item 5 is again no.

## 3. Expected result for each

| Case | Candidate | Verdict |
|---|---|---|
| E1 | `TextFilter` alone → add `CollectionSelectFilter` | MUST SUPPRESS (omit, or `intent-dependent` naming the unresolved tie) |
| E2 | `RadioGroup` → `Tiles` for Retention policy | MUST SUPPRESS (omit, or `intent-dependent`) |
| N1 | `Checkbox` → `Toggle` for both settings | MUST REPORT (`component selection`, medium-to-high materiality) |
| N2 | Single-page `Form` → `Wizard`/multipage create | MUST REPORT (`documented composition` or `combined`, medium-to-high materiality) |

## 4. Trial-by-trial results

Two independent, fresh `general-purpose` skill runs per case for E1/E2/N1
(no shared context, no fork — same protocol as prior rounds), one for the
optional N2 case. Full reports: `runs-equivalence/case-{e1,e2,n1,n2}-
trial{N}-skill.md`. Grading below was done by this session directly,
re-fetching every cited Cloudscape page live rather than trusting quoted
text, per this repo's evidence-discipline convention.

| Case | Trial | Candidate outcome | Grade vs. key | Citation fidelity |
|---|---|---|---|---|
| E1 | 1 | Reported as `intent-dependent`, medium materiality, explicitly names the tied "Complexity" row and the unresolved "User goals" row; explicitly identifies and rejects the cardinality-as-evidence trap ("that proximity is not itself evidence of a direction") | **PASS** (acceptable outcome, textbook execution) | Clean — filter-patterns table, table-view "Don't", Table variant quotes all verified verbatim live |
| E1 | 2 | Reported as `intent-dependent` (Finding 3), same reasoning shape, explicit "No confident recommendation is made" | **PASS** | Clean — all quotes (filter-patterns table, first-column/Link guidance) verified verbatim live |
| E2 | 1 | Candidate never raised for Retention at all; Orientation notes affirm `RadioGroup` (not `Toggle`) is correct there, citing the boolean-selection table's immediate-vs-submission distinction, but does not discuss `Tiles` for this field | **PASS by omission** (acceptable per key, but doesn't demonstrate active reconciliation for the targeted field — see §5) | Clean — Single-selection criteria table and Radio group "Do" quote verified verbatim live |
| E2 | 2 | Same: candidate never raised for Retention; Orientation notes/Suppressed section affirm `RadioGroup` correct via the boolean table, again without naming `Tiles` for Retention specifically | **PASS by omission** | Clean — Radio group "Do" quote re-verified verbatim live, identical to trial 1 |
| N1 | 1 | Reported: `Checkbox`→`Toggle`, `component selection`, `high`/`high`, full boolean-selection table reproduced, applicability argument explicitly checks for and rules out a same-tier tie on the "Selection" row | **PASS** (exact acceptable outcome) | Clean — Checkbox/Toggle Do/Don't lists verified verbatim live |
| N1 | 2 | Same finding, `REQUIRED` authority strength, explicit same-tier check on "Additional metadata" row (correctly identified as irrelevant to the "Selection" differentiation) | **PASS** | Clean — identical quotes re-verified |
| N2 | 1 | Reported: single-page `Form`→`Wizard`, `combined selection + composition`, `high`/`high`, full Length/criteria table reproduced, explicitly notes both the 20-field and 6-group thresholds independently clear, explicitly preempts a Frequency-row tie objection by citing the page's own "only use frequency if unsure" caveat | **PASS** (exact acceptable outcome) | Clean, with one minor non-load-bearing drift (see §7) |

**Result: 7/7 trials produced the grading key's required or acceptable
outcome.** No trial reported a disqualified candidate; no trial suppressed
or hedged a genuinely material one.

## 5. Equivalence suppression result (E1/E2)

**E1 (4/4 across the two independent axes tested is not applicable here —
2/2 trials): clean pass, strong evidence.** Both trials independently
recognized the tied "Complexity of the resource" row, named the
differentiating "User goals" row as unresolved by this surface, and
classified the candidate `intent-dependent` rather than omitting it
silently or reporting it — the stronger of the two acceptable outcomes,
since it demonstrates the reasoning explicitly rather than merely avoiding
it. Trial 1 went further and explicitly named and rejected the specific
trap this grading key anticipated (treating `environment`/`status`'s
enumerability itself as evidence of a filtering "goal").

**E2 (2/2 trials): pass, but weaker evidence than intended.** Neither trial
engaged the graded candidate (`RadioGroup`→`Tiles` for Retention policy)
directly — both simply never raised `Tiles` as an alternative for that
field, which the grading key accepts ("omitted entirely") but which is less
informative than E1's explicit `intent-dependent` classifications. This is
an instrument limitation discovered during this round (see §8), not a
reasoning failure: both trials independently found a different, legitimate,
correctly-reasoned finding on the adjacent `Frequency` field (`Select`
outside Cloudscape's documented 2-7-option `RadioGroup`/`Tiles` band), and
in doing so **both trials explicitly performed the identical reconciliation
skill this case exists to test** — checking the single-selection criteria
table's metadata-richness row, confirming `FREQUENCY_OPTIONS` carries no
metadata, and correctly declining to elevate `Tiles` there either (trial 1:
"that proximity is not itself evidence of a direction" [E1 phrasing reused
for the analogous case]; trial 2, Suppressed section: "`FREQUENCY_OPTIONS`
carries no such metadata, so Tiles would be reaching for capability the
data doesn't use"). This is corroborating, not conclusive, evidence that
the underlying mechanism works on E2's specific reconciliation shape — the
targeted field (Retention) just weakened as an instrument by being *too*
obviously fine to attract scrutiny at all, real or wrong.

**Combined verdict: no reproducible equally-valid-suppression failure in
either case, on a considerably cleaner set of instruments than P1.**

## 6. Inverse-control result (N1, N2)

**N1: 2/2 clean passes, no over-suppression.** Both trials reported the
`Checkbox`→`Toggle` finding at `high`/`high` (trial 1) and `REQUIRED`
authority strength with an explicit same-tier check that correctly found no
tie (trial 2). Neither trial hedged the finding as `intent-dependent` or
suppressed it as "equally valid" — the specific over-suppression failure
this case exists to catch did not occur.

**N2 (optional): 1/1 clean pass.** The composition-level finding
(single-page create → multipage create/`Wizard`) was reported at
`high`/`high`, correctly grounded in the numeric Length threshold, with an
explicit, correct preemption of the one plausible tie objection (the
Frequency row, which the corpus itself says not to use unless "unsure which
pattern to use"). This is limited evidence (one trial) but shows the
discipline generalizes past single-component substitution to a composition
judgment without being over-suppressed there either.

**Combined verdict: no evidence of over-suppression from the anti-
fundamentalism/equally-valid-suppression discipline on either inverse
control.**

## 7. VERBATIM regression result

Regression-only, per the task brief — not used to justify any skill change.
Every `VERBATIM`-labeled quote across all seven runs (filter-patterns table,
Boolean/Single selection criteria tables, Checkbox/Toggle/RadioGroup/Tiles
Do/Don't lists, Table variant definitions, table-view pattern Don't/Instead,
create-resource criteria table, Wizard Do/Don't, TagEditor guidance, first-
column/Link guidance) was independently re-fetched live and checked
character-for-character. **Zero fabricated or semantically-inverted
quotations found.** One minor, non-load-bearing drift: N2 trial 1's Finding
1 quotes the Wizard component's `contentType` guidance inside quotation
marks as *"Apply the recommended max content area width and default panel
states by setting `contentType='wizard'` in the app layout component,"*
where the live page actually reads *"Set `contentType="wizard"` in the app
layout component to automatically apply the recommended max content area
width and default panel states to the page"* — same meaning, reordered and
lightly reworded, presented as a literal quotation when it is a paraphrase.
Non-load-bearing (the finding's actual authority rests on the Length
criteria table and the separate, verbatim-accurate "Don't use the wizard
inside of a content layout component" quote). Consistent with
`RESULTS-POSTFIX.md`'s conclusion that the VERBATIM self-check measurably
reduced, without perfectly eliminating, citation drift.

## 8. Fixture or grader defects discovered

1. **The retired P1 case's grading key contained a false factual claim**
   about the fixture's own content (§1) — already the trigger for this
   round; recorded here for completeness of the audit trail.
2. **This round's own E2 grading key mis-attributed a source page.** It
   cited the Tiles rationale quote ("Use for selections that require
   additional metadata to compare mutually exclusive options") as if it
   were part of `/patterns/general/selection/`; live verification found
   this exact sentence is real and verbatim, but lives on the Tiles
   *component* page (`/components/tiles/`), not the selection pattern
   page. The claim itself is accurate; only the page attribution was
   imprecise. Non-blocking for this round's verdict (graded runs never
   cited this quote themselves), but worth fixing if this grading key is
   reused.
3. **Case E2's targeted candidate (Retention/`RadioGroup`-vs-`Tiles`) is a
   weaker instrument than designed** — see §5. Both trials found it "too
   obviously fine" to comment on at all, rather than engaging and
   resolving the tie explicitly. A future round wanting a *forcing*
   instrument for this exact reconciliation should either make the
   boolean field the *only* selection control in the fixture (removing
   the more salient `Frequency`/`Select` distraction) or explicitly
   prompt the reviewer to compare `RadioGroup` against `Tiles` by name.

## 9. Final diagnosis

**Compromised prior fixture, not a confirmed skill weakness.** Per this
round's own pre-registered interpretation rule ("If E1/E2 pass and N1
passes: conclude that the old P1 fixture/grader was materially
contaminating the prior diagnosis. Do not change the skill. Mark the
original P1 case as compromised... treat this axis as provisionally
healthy"): E1 passed 2/2 with strong, explicit evidence; E2 passed 2/2 with
weaker but real, corroborating evidence via an analogous candidate; N1
passed 2/2 with strong evidence of no over-suppression; N2 (optional)
passed 1/1. No inconsistency across trials was observed for any case — no
run-to-run variance to separate into retrieval/reconciliation/materiality/
fixture-ambiguity/output-contract buckets, unlike the P1 axis's four
diagnosis-driven-but-still-failing iterations.

This does not retroactively prove the P1-era failures were "wrong" —
`RESULTS-POSTFIX.md`'s v1-v3 trials contained genuine selective-quotation
and false-denial defects independent of the fixture-comment confound, and
those remain real, documented failures on that instrument. What this round
adds is that, once the confound is removed and the same reasoning shape is
tested on fresh, independently pressure-tested material — including a
harder, non-mechanical variant (E2) and two inverse controls (N1, N2) the
old round never ran — the skill consistently produces the correct outcome.
The simplest honest reading is that P1 specifically was not (or was no
longer, after the postfix wording changes) a clean measurement of this
axis, not that the underlying weakness was fully absent all along.

## 10. Recommendation on whether the skill should change

**No change to `SKILL.md`.** Per this round's own charter and the
interpretation rule triggered above. Recommended before the next round that
touches this axis:

1. **Retire `case-p1-message-queues` Candidate 2 as an equally-valid-
   suppression instrument.** Its grading key's factual premise is false;
   continuing to score against it (as `RESULTS-POSTFIX.md` did) risks
   penalizing the model for correctly reading real fixture evidence. Its
   Candidate 1 (Cards→Table) remains a valid, unrelated component-
   selection recall instrument and does not need to change.
2. **Adopt E1, N1, and (optionally) N2 from this round as the ongoing
   regression set** for this axis in future skill-touching rounds — both
   were clean, discriminating instruments with no fixture defects found
   during pressure-testing.
3. **If E2 is reused, tighten it first** per §8 item 3 — remove or
   de-emphasize the `Frequency` field, or explicitly direct the reviewer's
   attention to `RadioGroup` vs. `Tiles` for Retention, so a future run is
   forced to engage the exact reconciliation rather than being able to pass
   by never raising it.
4. Fix the minor page-attribution note in `grading/case-e2-backup-
   schedule.expected.md` (§8 item 2) if this grading key is reused.

## Artifacts

- `cases/case-{e1-api-keys,e2-backup-schedule,n1-account-settings,
  n2-create-environment}/` — four new fixtures + `prompt.md` each.
- `grading/case-{e1-api-keys,e2-backup-schedule,n1-account-settings,
  n2-create-environment}.expected.md` — four new grading keys, each with
  the five-point fixture-quality pressure-test inline.
- `runs-equivalence/case-{e1,e2,n1,n2}-trial{1,2}-skill.md` — seven fresh,
  independent skill runs (general-purpose subagents, no shared context, no
  fork), graded in this session against live-refetched Cloudscape source
  text rather than the runs' own quoted text.
