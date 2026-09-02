# design-system-native-expression-review — repeatability/adjudication round

**Run date:** 2026-09-02. **Branch:** `design-system-calibration-mui-generalization`.
**Repo SHA at start and throughout this round:** `ffcfd79666f6c9c6b8cc70d8cc0db2bee56c2b4b`
(unchanged — `git diff ffcfd79 HEAD -- skills/design-system-native-expression-review/SKILL.md`
is empty; no skill edit was made before, during, or after any run in this round).
**Skill file graded:** `skills/design-system-native-expression-review/SKILL.md`,
content identical to its state at commit `ffcfd79` throughout.

**Purpose:** the immediately preceding generalized regression
(`RESULTS.md` in this directory, classification **B**) produced four
regression signals against previously-validated behaviors, each a single
instance. Per this repo's own convention (iteration 3's precedent) and
per this task's explicit instruction, a suspected weakness becomes a
repeat trial before a wording change — not an immediate rewrite. This
round re-runs exactly the three implicated fixtures (Cloudscape Case P1,
MUI ntfy, MUI hk-independent-bus-eta) once more, fresh and independent,
specifically to separate one-run variance from a reproducible weakness.
**The skill was not modified before, during, or after this round.**

## 1. Method

- **Fixtures, authority, bounded surfaces:** identical to the immediately
  preceding round — same frozen fixture SHAs
  (`evals/design-system-calibration/SETUP.md`), same authority indexes
  (`evals/design-system-calibration/authority/{cloudscape-llms.txt,mui-material-llms.txt}`),
  same bounded-surface file sets.
- **Grading keys/rubric:** `evals/cloudscape-native-expression-review/grading/case-p1-message-queues.expected.md`
  (Cloudscape P1's pre-adjudicated MUST REPORT/MUST SUPPRESS candidates)
  and `evals/cloudscape-native-expression-review/rubric.md` (the generic
  9-question A–E rubric, "Cloudscape" read as "Material UI" for the two
  MUI fixtures, which have no pre-written grading key — same discipline
  the prior MUI rounds used).
- **Reviewer isolation:** three fresh `general-purpose` subagents, no
  fork, no shared context with this session, with each other, or with
  any prior run. Each received only the skill file, the design system
  and authority-source pointers, the bounded-surface file paths, and the
  generic baseline task framing — **never** the grading key, any prior
  run's output, any RESULTS file, or any statement of what failure this
  round exists to check for. This matches the task's explicit
  instruction not to tell the reviewing agent the expected answer or
  identify the previous failure it is being tested against.
- **Verifier isolation and knowledge:** three fresh `general-purpose`
  subagents, one per reviewer run, each told explicitly (as the task
  permits for verifiers) the purpose of this round and the specific
  prior-round failure shape to adjudicate for its fixture. Each verifier
  independently re-read the fixture directly (not trusting the review's
  line citations), independently live-fetched every cited authoritative
  page (`cloudscape.design`/`mui.com`, `.md` endpoints) and checked every
  quotation-marked claim character-for-character against the fetched
  text — never against memory or the review's own transcription.
- **Full raw run/verify transcripts:** committed at
  `runs-repeat/{case-p1,ntfy,hkbus}-{skill,verify}.md`. No file under
  `evals/cloudscape-native-expression-review/` or the prior
  `evals/design-system-native-expression-review/runs/` was read by any
  reviewer, and none was edited by this round.

## 2. The three fresh reviews — what each one did

| Fixture | This round's finding shape | vs. immediately preceding round |
|---|---|---|
| Cloudscape P1 | 3 findings: Cards→Table (A), `ContentLayout`/`full-page` variant (D — new, unhedged), TextFilter vs. CollectionSelectFilter for status/region (**E — the must-suppress candidate, reported unhedged**) | Same central failure (Candidate 2 reported), now unhedged rather than self-conceding; plus a *new*, independent missing-intent overreach on the previously-tolerated third ambiguity |
| MUI ntfy | 2 findings: Checkbox→Switch (A), DialogFooter→Alert (B); Popper/ClickAwayListener/Fade (EmojiPicker) demoted to a correctly-reasoned **orientation note**, not a finding | The specific Popper/Popover semantic-inversion citation failure did **not** recur; a *different*, non-load-bearing citation fabrication appeared in the new Alert finding |
| MUI hk-independent-bus-eta | 1 finding: Alert consolidation across four hand-rolled notice components (A); `RouteHeader`→`AppBar`/`Toolbar` **never raised at all**; `StopDialog` fullScreen sizing cleanly excluded to "what was not evaluated," no scope leak | AppBar question went from "unhedged and wrong" to "never investigated, silently absent" — a different failure mode on the same question; the props/CSS scope-leak from the prior round did **not** recur |

## 3. Per-behavior historical comparison

### 3a. P1 — equally-valid-candidate suppression (TextFilter vs. CollectionSelectFilter, status/region)

| Round | Skill state | Outcome |
|---|---|---|
| Iteration 3 (frozen, pre-morph, `cloudscape-native-expression-review`) — case built specifically for this axis | Unmodified, pre-morph | **PASS.** Candidate named in a "Suppressed" section with a real, evidence-grounded applicability argument (both view patterns' own "Filter" building block prescribes plain text filter as the reference component for this page type). |
| Generalized regression round 1 | Post-morph, `design-system-native-expression-review` | **FAIL.** Reported as Finding 2, `medium`/`high`, with a self-undermining "Why it matters" half-conceding the current approach already works, plus one fabricated `VERBATIM` quote. |
| **This repeat (round 2, post-morph)** | Post-morph, unchanged since round 1 | **FAIL — reproduces the exact failure, in its sharper, unhedged form.** Reported as Finding 3, `high`/`high`, with an affirmative argument that the current `TextFilter` is a "coincidental," "undiscoverable side effect" — i.e. the review argues the status quo is *inferior*, not merely that the alternative is *also valid*. The review's own cited authority (`filter-patterns.md`'s criteria table) places `TextFilter` and `CollectionSelectFilter` in the identical "Simple resource" complexity cell; the review never quotes or engages that table. Citations this round were individually accurate (no fabrication on this finding specifically) — the fabrication moved off this specific finding, but the core semantic failure (ignoring self-retrieved equivalence evidence) got *worse*, not better. |

**Cross-check — did the review demonstrate it *can* apply this discipline correctly, just not here?** Yes: in the same run's own Suppressed section, it correctly applies equal-validity/intent-dependent reasoning twice (Property Filter vs. Collection Select Filter; card-view details-linking). This sharpens rather than excuses the Candidate-2 failure — the discipline exists in the model's repertoire and simply wasn't applied to the one candidate the case is built around.

**Bonus, unplanned data point this round:** the previously-tolerated, explicitly non-scoring `ContentLayout`/`full-page`-variant ambiguity was *also* mishandled this round — asserted as a confident `REQUIRED`-strength finding with no missing-shell-context caveat, which the grading key explicitly marks as the one unacceptable outcome for that item. This is a second, independent missing-intent defect in the same run, not a restatement of the Candidate 2 verdict (per the grading key's own instruction to keep them separate) — but it is the same underlying shape (confident violation-strength assertion where the evidence doesn't license one), appearing twice in one report.

**Classification: CONFIRMED RECURRING WEAKNESS.** Two independent post-morph attempts on the exact case built to isolate this axis both fail it, one of them in a sharper form than before; the one available pre-morph data point on the identical case passed cleanly. This is not proof the *morph's specific wording changes* caused the regression (the anti-fundamentalism rule and "Missing intent" section were preserved in substance, only reworded for corpus-neutrality — see §5), but the outcome pattern (1-for-1 pre-morph, 0-for-2 post-morph, on the identical fixture) is itself real, actionable signal independent of root-cause attribution.

### 3b. ntfy — Popper/Popover reasoning and citation integrity

| Round | Skill state | Outcome |
|---|---|---|
| Pre-morph MUI round (frozen `cloudscape-native-expression-review` pointed at MUI) | Pre-morph | **PASS — Grade A, "strongest finding in the whole round."** Popper+ClickAwayListener+Fade → Popover reported, well-hedged (explicitly notes Popover's scroll-blocking is a legitimate counter-consideration inside an already-open Dialog), citations clean. |
| Generalized regression round 1 | Post-morph | **FAIL — Grade E.** Reported the same finding, but the citation is semantically inverted: claimed Popper "doesn't include built-in transition animations" when the live page states the opposite ("has built-in support for react-transition-group") and gives the *exact* `Popper`+`Fade`+`timeout={350}` pattern as its own worked example — the fixture's code, not a gap. |
| **This repeat (round 2, post-morph)** | Post-morph, unchanged since round 1 | **The inversion did not recur.** The item is now demoted to an "already-native" orientation note, not a finding. Its load-bearing citation ("Clicking away does not hide the Popper component... you can use the Click-Away Listener") is accurate, non-inverted, and — per the independent verifier — the *conclusion itself* is correct: Popper+ClickAwayListener+Fade is MUI's own documented, sanctioned composition for this need (the fixture's `Fade`/`timeout={350}` is a character-for-character match to MUI's own worked example), not a gap Popover uniquely fills. One weaker, non-load-bearing supplementary argument (conflating Popover's page-level scroll lock with the popover's own internal content scrolling) doesn't change the outcome. |

**Classification (Popper/Popover semantic-inversion specifically): LIKELY RUN VARIANCE, resolved on retry.** One pre-morph pass, one post-morph inversion failure, one post-morph clean pass with the correct conclusion reached via accurate citations — the inversion did not reproduce, on the same component, in the same corpus.

**However — citation fabrication as a category did not disappear; it moved.** This round's Finding 2 (DialogFooter→Alert, new this round, not present in the prior generalized round) contains one genuinely fabricated quote ("typically integrated into the page layout" — confirmed by the verifier to not exist anywhere on either the Alert or Snackbar page in any form) and one word-order quotation drift ("each with corresponding icon and color combinations" vs. the source's "...with corresponding icon and color combinations for each"). Neither is load-bearing (the underlying facts they gesture at are independently true and separately, accurately quotable elsewhere on the same pages), and neither is a semantic inversion or a conflation of unrelated sections — but this is a real, if smaller, recurrence of the broader "self-labeled VERBATIM is not self-verifying" failure mode the original morph regression (§5 of the prior `RESULTS.md`) named as a newly-discovered failure mode, now observed a second time on a different finding.

**Classification (VERBATIM self-verification, broader category): CONFIRMED RECURRING WEAKNESS, at reduced severity.** Rate this round: 1 fabricated + 1 drifted, both non-load-bearing, out of 13 checkable quotations in this run (vs. the prior round's 4 fabricated/inverted quotes across the same fixture, one of them load-bearing and outcome-reversing). This is real, measurable improvement in severity and load-bearingness, but not elimination.

### 3c. hk-bus-eta — AppBar/Toolbar applicability

| Round | Skill state | Outcome |
|---|---|---|
| Pre-morph MUI round | Pre-morph | **PASS — Grade A on Q9.** Reported `intent-dependent`, naming both plausible readings (RouteHeader should adopt AppBar per its per-screen "contextual action bar" documented use, vs. the current `Paper` composition already being correct *because* it avoids colliding with an as-yet-unconfirmed global app bar) and naming the exact resolving fact (does a global AppBar already exist in the app shell, outside the bounded surface). Did not assert a direction. The verifier independently checked `Root.tsx`/`Header.tsx` and confirmed a persistent global `Toolbar`-based `Header` does exist — substantively vindicating, not merely procedurally excusing, the hedge. |
| Generalized regression round 1 | Post-morph | **FAIL — Grade D.** Reported unhedged (`combined selection + composition`, high/high). The applicability argument explicitly claimed to have checked `App.tsx` and `Root.tsx` for a competing header and found none — but stopped one file short: `Root.tsx` renders `<Header/>`, and `Header.tsx` (same directory) is the same persistent global bare-`Toolbar` the pre-morph round's verifier had to find independently. Confident conclusion built on an incomplete absence check. |
| **This repeat (round 2, post-morph)** | Post-morph, unchanged since round 1 | **FAIL — a different, arguably worse failure mode: total silence.** `RouteHeader`→`AppBar`/`Toolbar` is never raised as a candidate anywhere in the report — not as a finding, not suppressed, not as an orientation note, not as `intent-dependent`. The review does examine `RouteHeader.tsx`'s `Paper` usage directly and affirmatively clears it ("a legitimate, documented customization... not a misuse of the component") without ever testing it against `AppBar`/`Toolbar` or checking for competing global chrome. The verifier found **zero evidence anywhere in this run of looking beyond the nine-file bounded surface for any finding** — the one investigative move that would settle this question (checking `App.tsx`→`Root.tsx`→`Header.tsx`) simply never happened. |

**Classification: CONFIRMED RECURRING WEAKNESS, manifesting differently each time.** Three data points, three distinct outcomes: (1) a correct hedge built on genuine, if partial, investigation, later vindicated; (2) a confident wrong answer built on an investigation that stopped one hop short of the truth; (3) no investigation of the question at all, plus an unrelated affirmative "checked and fine" verdict on the very component the missing question turns on. The pre-morph round did the necessary investigative work and reached (or at minimum earned) the right posture; neither post-morph attempt did. The verifier explicitly ranks this repeat's outcome as **the weakest of the three** — worse than an overconfident wrong answer, because at least that showed some investigative effort in the wrong place, whereas this run shows none.

**Important qualification per the task's causality-discipline instruction:** because the two post-morph failures take *different* forms (overreach from a partial check vs. total non-investigation), this is not evidence of one crisp, wording-fixable defect the way the P1 failure is (which reproduced in near-identical form both times). It is evidence that "does this run actually investigate surrounding application context before resolving or dropping an AppBar/Toolbar-shaped candidate" has failed twice, by two different mechanisms — a real, recurring outcome-level weakness, but one whose root cause is less cleanly isolated than P1's, and which this round's evidence alone does not license prescribing a specific wording fix for (see §6).

### 3d. hk-bus-eta — Dialog/fullScreen scope discipline

| Round | Skill state | Outcome |
|---|---|---|
| Pre-morph MUI round | Pre-morph | **PASS — cleanest possible scope discipline.** The `StopDialog.tsx` full-height `sx` sizing was fully excluded from any finding, named only in "what was not evaluated" as a props/hardcoded-CSS question on an already-correctly-chosen `Dialog` component. |
| Generalized regression round 1 | Post-morph | **FAIL — Grade D, scope leak.** Reported as `intent-dependent`, correctly executing the intent-dependent *procedure* (naming both readings, declining to pick one), but its stated "why it matters" leaned substantially on "hand-tuned pixel values instead of the dedicated `fullScreen` prop" — implementation mechanics folded into a composition-level finding, beyond the "supporting evidence only" allowance the skill's scope boundary permits. |
| **This repeat (round 2, post-morph)** | Post-morph, unchanged since round 1 | **The scope leak did not recur.** The `sx`-based sizing is again filed entirely under "what was not evaluated," described purely in props/CSS terms ("`Dialog` sizing achieved via `sx` targeting `.MuiPaper-root`... rather than the documented `fullScreen`/`maxWidth`/`fullWidth` props... not assessed"). No finding folds prop/CSS reasoning into a composition-level claim this round. |

**A genuine composition-level candidate exists on the same lines and was not investigated.** MUI's own "Full-screen dialogs" worked example (independently re-fetched and confirmed by the verifier) pairs the `fullScreen` prop with an `AppBar`/`Toolbar` title bar — authority that sits on the same documentation page as the `fullScreen` prop mechanics, and is a *stronger* on-point match for `StopDialog.tsx`'s `DialogTitle` icon row than the `DialogActions` alternative this run *did* consider and correctly reject. The review never raised the `AppBar`/`Toolbar`-for-the-title-row candidate at all, despite examining the same lines of code for a weaker alternative. Per the verifier: this "lands in the right place [no scope leak], but isn't demonstrated to be earned reasoning rather than an unexamined gap" — i.e., the correct *outcome* (no finding folding CSS-mechanics into composition) may be a product of not investigating far enough to reach the temptation, not of correctly resisting the temptation once found.

**Classification: LIKELY RUN VARIANCE for the scope-leak failure specifically (not reproduced on retry: 2 of 3 rounds clean, 1 leaked).** The distinct, adjacent recall gap (the `AppBar`/`Toolbar`-for-title-row composition candidate never investigated) is a different question from the one this axis was chartered to test (does implementation-mechanics reasoning leak into a composition finding) and should not be scored against it — but it is worth naming as a possible contributor to why this round happened to land clean (see §6).

## 4. Aggregate reading — what does *not* reduce to a percentage

Two of the four axes (P1 suppression, AppBar/Toolbar investigation) show a
**confirmed recurring weakness** at the outcome level across two
independent post-morph attempts, even though the AppBar failure changes
shape between attempts. Two axes (Popper/Popover inversion, Dialog
scope-leak) show a **single historical failure that did not reproduce on
retry** — best read as run variance, not a stable defect, though for
Dialog specifically the clean outcome may be partly attributable to
under-investigation rather than earned discipline (§3d).

Citation fabrication as a general category (distinct from the specific
Popper inversion) is smaller and less severe than the prior round but
did not disappear: this round contributed one new, non-load-bearing
fabricated quote and one word-order drift, both confined to a single
finding (ntfy Finding 2). Zero conflations and zero semantic inversions
were found across all three verified runs this round — a genuine,
measurable improvement on those two specific failure types, which were
present in the immediately preceding round.

## 5. Is any of this attributable to the morph specifically?

**No evidence in this round supports that attribution, and this round's
design does not license it either way with confidence.** The two
confirmed recurring weaknesses both involve reasoning behaviors
(equally-valid-candidate suppression; missing-intent investigation
depth) whose governing SKILL.md sections — the anti-fundamentalism rule,
the "Missing intent" section — were, per the skill's own "Lineage and
evidence" section, "preserved in substance, only reworded for
corpus-neutrality," not rewritten. The one available pre-morph baseline
on each of these exact fixtures/cases passed; the pre-morph skill's
broader history also contains one earlier instance of the equally-valid
failure shape (A1 Finding 2), later shown not to generalize across a
dedicated isolating case (iteration 3's P1 pass) — meaning this failure
shape is not new to the morph, but its *recurrence rate on this specific
case* went from 0-for-1 (iteration 3) to 2-for-2 post-morph, which is
itself the load-bearing fact regardless of whether the morph's wording
changes are the cause or an unrelated source of model-execution
variance is. This round cannot and does not distinguish between "the
corpus-neutral rewording weakened this specific discipline" and "this is
ordinary run-to-run reasoning variance that happens to have landed badly
twice in a row on the same case" — separating those two would require
further repeat trials specifically isolating the wording question (e.g.,
re-running the *frozen pre-morph* skill against the *same* P1 case
several more times to establish its own baseline variance rate), which
this task did not charter and this round did not perform.

**What this round does rule out:** systemic degradation of the
corpus-adaptive discovery mechanism or the generalized taxonomy itself.
All three fresh reviews this round used the generalized taxonomy
consistently and correctly (`component selection` / `documented
composition` / `combined selection + composition` / `intent-dependent`),
none invented a Cloudscape-shaped pattern tier for MUI, and the
Cloudscape run correctly identified and used the genuine pattern tier
that corpus has. Recommendation D's bar (systematic degradation
attributable to corpus-neutral generalization itself, with evidence
stronger than one failed rerun) is not met.

## 6. Classification summary

| Behavior | Classification |
|---|---|
| P1 — equally-valid candidate suppression | **Confirmed recurring weakness** (2-for-2 post-morph fails on the case built to isolate this axis; 1-for-1 pre-morph pass) |
| ntfy — Popper/Popover semantic inversion | **Likely run variance** (1 failure, did not reproduce on retry; correct conclusion reached via accurate citation this round) |
| ntfy/hk-bus — VERBATIM self-verification (broader citation-fabrication category) | **Confirmed recurring weakness, reduced severity** (present in both post-morph rounds; smaller, non-load-bearing this round vs. larger, load-bearing/outcome-reversing before) |
| hk-bus — AppBar/Toolbar missing-intent investigation | **Confirmed recurring weakness, insufficient evidence on root cause/exact shape** (2-for-2 post-morph fails, but via two different mechanisms — overreach, then total non-investigation — so the failure is real and recurring but not yet isolated to one crisp fixable defect) |
| hk-bus — Dialog/fullScreen scope leak | **Likely run variance** (1 failure, did not reproduce on retry; 2-for-3 across all rounds clean), with a caveat that this round's clean result may be partly explained by under-investigation rather than demonstrated discipline |

## 7. Is a wording change now empirically justified?

**For the P1 equally-valid-suppression axis: yes.** This is the
cleanest, most repeatable, most precisely isolated failure in this
round's evidence — the same case, reproduced twice post-morph with zero
pre-morph failures on record, and a review that demonstrably has the
correct discipline available in its own repertoire (it applies it
correctly to two adjacent candidates in the same report) but doesn't
apply it to the one candidate the case is built around.

**For the AppBar/Toolbar missing-intent-investigation axis: not yet, on
this round's evidence alone.** The failure is real and recurring at the
outcome level, but its shape differs each time (confident overreach vs.
total silence), which means a wording fix aimed at "don't overreach past
an incomplete absence check" would not obviously have prevented this
round's "never investigated" failure, and vice versa. Per this repo's
own precedent (the P1/P2 case-design approach used to isolate the A1
Finding 2 question before iteration 3), the next step for this axis
should be a dedicated isolating pressure case — one that removes the
"how deeply did this run choose to investigate" confound by making the
competing-global-chrome fact either trivially discoverable or
structurally undiscoverable, so investigation depth itself becomes the
measured variable — before proposing a specific wording change.

**For citation self-verification (VERBATIM discipline) generally: a
smaller version of the same signal as the prior round, now at reduced
severity.** Not this round's central target, but worth bundling into any
follow-up given it recurred a second time, in a new location, on a
different finding.

## 8. Smallest proposed follow-up (not implemented in this task)

Per the task's explicit instruction, **no skill edit was made in this
round**, and this section only names the smallest candidate the evidence
currently supports — implementing it is out of scope here.

**Recommendation: C — small reasoning-gate refinement**, targeted
specifically and only at the P1-shaped failure (an equally-valid
alternative surviving despite the review's own retrieved evidence of
equivalence), since it is the one failure this round isolates cleanly
enough to propose a specific, narrow rule for.

The smallest candidate rule the evidence supports: **before finalizing
any finding's materiality/confidence, if the finding's own cited
authority (a decision table, a "use X or Y" pairing, an explicit
complexity/fit-tier classification) places the current implementation
and the proposed alternative in the same documented fit tier — rather
than stating a directional preference between them — the finding must be
suppressed or reclassified `intent-dependent`, not reported as a
confident violation.** This targets the precise, demonstrated mechanism
of both P1 occurrences: the review's own retrieved filter-patterns
criteria table already states the equivalence; the failure is not a
missing citation, it's a citation that was fetched, is accurate, and was
not applied to the materiality/confidence decision it should have
governed.

This is deliberately narrower than (and should not be conflated with)
either: (a) the previously-proposed VERBATIM self-verification step
(recommendation B's candidate from the prior round, still separately
worth bundling given this round's smaller recurrence), or (b) a fix for
the AppBar/Toolbar missing-intent-investigation weakness, which this
round's evidence says needs a dedicated isolating case first, not a
wording guess.

**Do not implement either candidate in this task**, per the explicit
instruction governing this round.

## 9. Final recommendation

**C — small reasoning-gate refinement, scoped narrowly to the
equally-valid-candidate-suppression axis (§8), with two explicit riders:**

1. **Bundle the smaller VERBATIM self-verification step (B's candidate)
   into the same follow-up round**, since this round's evidence
   (one new fabricated quote, one drift, both non-load-bearing) shows
   the underlying mislabeling failure is smaller than before but not
   eliminated, and a combined follow-up round can re-test both at once
   using this round's same three fixtures.
2. **Do not yet propose a wording fix for the AppBar/Toolbar
   missing-intent-investigation weakness.** It is real and recurring at
   the outcome level (0-for-2 post-morph) but not yet isolated to one
   mechanism the way P1 is; per this repo's own convention, build a
   dedicated isolating case for it first (as iteration 3 did for A1),
   then repeat-test, before touching SKILL.md on this axis.

**Not A** (leave unchanged): the P1 axis is now confirmed recurring
across two independent post-morph attempts on the exact case designed to
detect it, with zero pre-morph failures on record — this is no longer a
single-instance signal.

**Not D** (reconsider the morph): nothing in this round's evidence
attributes either confirmed weakness to the corpus-neutral generalization
itself rather than to reasoning-discipline gaps that predate the morph
(P1's shape already existed pre-morph as A1 Finding 2) or to ordinary
model-execution variance this round's design cannot cleanly separate
from a wording effect (§5). The corpus-adaptive discovery mechanism and
the generalized taxonomy performed cleanly and consistently across all
three fresh runs this round, with no invented pattern tiers and no
taxonomy reversion.

**This report does not itself make any wording change.** Per this task's
explicit instruction, `skills/design-system-native-expression-review/SKILL.md`
was not edited before, during, or after this round.
