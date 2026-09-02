# cloudscape-implementation-audit — iteration 2 results

**Run date:** 2026-09-01. **Baseline:** iteration-1 commit `4068dd7`
("feat: add cloudscape-implementation-audit experimental skill + eval"),
on branch `worktree-design-system-calibration-eval-setup`, treated as
frozen and read-only until this iteration's one documented change (see
"Exact skill change made"). Main stayed untouched throughout — all work
happened in this pre-existing worktree/branch.

This is a **targeted pressure-test iteration**, not a redesign. Iteration
1 (`RESULTS.md`) produced 10 candidate findings (6 A / 4 B / 0 C / 0 D /
0 E) and an **ITERATE** verdict, leaving two unresolved questions this
round exists to answer:

1. **Boundary behavior** — when the reviewer hits a material issue whose
   real explanation belongs to component-selection, pattern, or
   experience-level guidance, does it silently omit the issue or
   explicitly signal that a higher-level review may be warranted?
2. **Recall** — is the skill's precision discipline suppressing useful,
   in-scope findings an unguided baseline would catch?

Every run cited below is a fresh, isolated `general-purpose` subagent
(no fork, no shared context between runs) — the same methodology
iteration 1 used. Full raw transcripts are local artifacts under
`runs/iteration-2/*.md` (gitignored per `evals/*/runs/*/`, same
convention as `runs/iteration-1/`); `runs/2026-09-01-iteration-2-runs.md`
and this file are the committed, auditable record every claim below
traces back to.

## 1. Iteration-1 baseline used

Commit `4068dd7`. `skills/cloudscape-implementation-audit/SKILL.md` at
that commit is the "frozen iteration-1 skill" referenced throughout
sections 3 and 5–6 below, before this round's one edit (section 4).

## 2. Pressure cases created, and why each is diagnostic

Full design rationale: `PRESSURE-ITERATION-2.md`. Summary:

- **Case 4 — `Endpoints.tsx` (boundary pressure case).** A synthetic
  resource-table page where every local Cloudscape mechanic (`Table`,
  `useCollection`, `Modal`, `KeyValuePairs`) is built to be
  textbook-correct, but the `Modal` opened per row displays what reads as
  the endpoint's full detail set (9 fields) — a shape Cloudscape's own
  pattern documentation assigns to "details page" or "split view," not
  `Modal`. Modal's own docs don't forbid this outright (no tabs, no
  expanded sections, no chained modal — every hard "Don't" is respected),
  so there's no clean implementation-level violation to hang a finding
  on; the tension is genuinely pattern/product-intent-level. Diagnostic
  because it's adjudicable: `grading/case-4-boundary-endpoints.expected.md`
  states in advance what a correct response looks like (A/B/C per the
  task brief's framing), unlike iteration 1's real fixtures where no one
  decided the "correct" answer in advance.
- **Case 5 — `InstanceDetailsModal.tsx` (recall, composition
  constraint).** A `Modal` containing `Tabs` — Modal's own docs state,
  under "Don't": *"Avoid tabs, or expanded sections in modal which
  overload the interface."* Chosen because it requires fetching Modal's
  actual usage-guidelines page rather than pattern-matching from general
  Cloudscape familiarity, and because the *correct fix* is
  implementation-level (stop nesting Tabs) while an *incorrect* fix
  ("move this to a details page") would smuggle case 4's exact failure
  mode into the fix itself — testing boundary discipline on the
  remediation, not just defect detection. A second, correctly-scoped
  `Modal` (`RenameInstanceModal`) in the same file is the false-positive
  control.
- **Case 6 — `TeamsPage.tsx` (recall, app-owned accessibility
  mechanics).** Three `Table` instances: one with `selectionType="multi"`
  and a fully correct `ariaLabels` prop, one with the same selection type
  and no `ariaLabels` at all, one with no selection. Table's own
  accessibility guidelines state: *"Provide alternative text for row
  selection controls (for single, multi, or group selection) through
  `allItemsSelectionLabel` and `itemSelectionLabel`."* Chosen as a second
  recall category distinct from case 5's, with a genuine false-positive
  test built in (three tables, only one should be flagged).
- **Real-fixture rerun** — `Identities.tsx` from
  `aws-samples/sample-bedrock-spend-budget-guardrails` at the same pinned
  SHA (`588b62598a842896583d1ef516ae38597e00dc4e`) iteration 1 used, to
  see whether any skill change generalizes back to the messier real case
  that originally exposed the boundary ambiguity (iteration 1's baseline
  flagged `ContentLayout`+`Table variant="container"` vs. the full-page
  Table-view pattern; iteration 1's skill run stayed silent on it).

## 3. Frozen iteration-1 results on the pressure cases

- **Case 4, v1** (`runs/iteration-2/skill-i1-case-4-boundary-endpoints.md`):
  2 findings — `CollectionPreferences` composed with no `onConfirm`
  (violation) and `TextFilter` missing `filteringAriaLabel` (recommended
  alignment). **Neither was intended** — see the correction note below.
  "What was not evaluated" named "Component selection" and "Pattern
  composition" only as generic boilerplate categories, with no specific
  engagement with the Modal/details-page tension.
- **Case 4, v2** (corrected fixture,
  `runs/iteration-2/skill-i1-case-4-boundary-endpoints-v2.md`): 2 findings
  — missing `enableKeyboardNavigation` and an unconfigured `filtering.noMatch`
  state. This time "What was not evaluated" specifically named *"whether
  a `Modal` is the right way to show endpoint details versus a split
  panel"* — a genuine, if brief, acknowledgment of the designed tension —
  but folded into the same generic bucket, with no evidence, materiality,
  or structured signal attached.
  **Fixture correction note:** the v1 fixture had two unintended real
  bugs (`CollectionPreferences` with no `onConfirm`/state, `TextFilter`
  with no `filteringAriaLabel`) that I introduced by construction error,
  not by design. Both were legitimate, well-cited findings — good
  evidence of real skill recall — but they gave the reviewer's attention
  somewhere concrete to land before ever reaching the pattern question,
  contaminating the boundary read. I fixed both (added `useState`
  +`onConfirm` wiring; added `filteringAriaLabel="Filter endpoints"`) and
  reran (v2). Both runs are reported because both are informative: **in
  two independent reads of the same designed tension, across two
  different sets of accompanying local defects, the frozen skill never
  produced a dedicated, evidenced signal about the Modal/pattern
  question** — at best a passing clause inside boilerplate.
- **Case 5** (`runs/iteration-2/skill-i1-case-5-recall-modal-tabs.md`): 1
  finding — Tabs nested in `InstanceDetailsModal`, classified
  `recommended alignment`, materiality high, citing Modal's verbatim
  "Don't" line. Correctly left `RenameInstanceModal` alone.
- **Case 6** (`runs/iteration-2/skill-i1-case-6-recall-table-selection.md`):
  1 finding — missing `ariaLabels` on the Pending-invites table,
  classified `recommended alignment`, materiality high. Correctly left
  the Members and Audit-log tables alone.

Adversarial verification of cases 5 and 6 (fresh verifier per rubric.md):
**both graded A** (`runs/iteration-2/verify-i1-case-5-recall-modal-tabs.md`,
`verify-i1-case-6-recall-table-selection.md`). Case 5's verifier
independently judged the "Recommended" (not "Required") authority-strength
call defensible given Modal's "Avoid" (not "Don't"-absolute) phrasing.
Case 6's verifier confirmed zero false positives on the other two tables.

**Reading for the two open questions, frozen skill only:** recall — 2/2
planted defects found, correctly characterized, zero false positives.
Boundary — 0/2 reads produced a dedicated signal; the tension was either
absent (v1) or a passing generic mention (v2). This is the evidence base
that justified the one skill change below.

## 4. Exact skill change made

Added one new section, **"## Escalation"**, to
`skills/cloudscape-implementation-audit/SKILL.md` (between "Materiality"
and "Report"), plus a matching **"## Escalations"** slot in the "Report"
template between "Findings" and "Suppressed," and one forward-pointer
sentence at the end of "How this composes" in "Scope boundary." Full text
is in the file; summary of the contract:

- Two hard gates before writing one: (a) concrete implementation +
  Cloudscape evidence that the concern sits above the implementation
  layer, not just "this could arguably also be considered higher up";
  (b) no implementation-level finding, at any classification, honestly
  resolves it.
- Exactly four fields: **Boundary reached** (component selection /
  pattern-or-experience / product-intent dependent), **Trigger evidence**,
  **Why no implementation finding**, **Suggested next review** (category
  name only — never a component, pattern, or restructuring
  recommendation).
- Escalations don't count as findings, aren't classified
  violation/alignment/concern/unresolved, and should be rare — the
  section explicitly warns that escalating more than one thing per
  review is a signal of misuse, not thoroughness.

**Rationale:** justified directly by section 3 — two independent reads
of a designed boundary tension produced zero dedicated signal, replaying
iteration 1's own unresolved case-1 ambiguity. This is the single edit
made this iteration; no other section of SKILL.md was touched, and no
deterministic tooling changed (section 9).

## 5. Recall results, before vs. after

| Case | Frozen skill | Iteration-2 skill | Verifier |
|---|---|---|---|
| Case 5 (Modal+Tabs) | 1 finding, correct | Same finding, unchanged (`runs/iteration-2/skill-i2-case-5-recall-modal-tabs.md`) | A (both rounds) |
| Case 6 (Table selection a11y) | 1 finding, correct | **3 findings** — same ariaLabels finding, plus 2 new: "selection wired to no consuming action" and "missing selection counter" (`skill-i2-case-6-recall-table-selection.md`) | ariaLabels: A. Counter: **A**. Selection-no-action: **D** (see section 8) |
| Real fixture — `DetailPage.tsx` (case 2) | 4 findings (Container nesting, `Header variant="h1"`, `TextContent`, native-anchor) | **5 findings** — Container nesting, `TextContent`, native-anchor unchanged; **recovered** the breadcrumbs-slot finding baseline caught and iteration-1's skill missed; added a new `BreadcrumbGroup` `ariaLabel` finding; **lost** the `Header variant="h1"` finding (not reproduced this round) | Not independently re-verified this round (budget; see "What this does not prove") — reviewed directly, both new findings cite `AppLayout`'s documented `breadcrumbs` slot and `BreadcrumbGroup`'s dev-guide `ariaLabel` guidance respectively, with boundary checks that correctly stay at the composition-slot level |
| Real fixture — `Form.tsx`/`FormContent.tsx` (case 3) | 3 findings + 1 `unresolved` (disabled-vs-readOnly split two ways, submit-button-disabled anti-pattern, deprecated `statusIconAriaLabel`) | **3 findings** — disabled-vs-readOnly (same, re-split), a compound-field readOnly gap (same); **new**: the `Select`/`Tiles`/`RadioGroup` `""`-vs-`null` contract violation, now traced through `FormContent`'s actual initial state to confirm it's reachable on first render (iteration 1's skill explicitly suppressed this exact signal for insufficient runtime-consequence evidence — see iteration-1 `RESULTS.md`'s case-3 "meaningful no-findings"); **missing** this round: the submit-button-disabled finding and the deprecated-prop `unresolved` item | Not independently re-verified this round |
| Real fixture — `Identities.tsx` (case 1) | 2 findings (Modal `closeAriaLabel`, monospace/code) | **2 findings** — monospace/code (broader: now also catches two native `<code>` elements the iteration-1 finding didn't cite); **new**: `ContentLayout`/`Table` full-page-variant finding; **lost**: the Modal `closeAriaLabel` finding | Monospace: **A**. ContentLayout/full-page: **D** (see section 6) |

**Reading:** recall genuinely improved in three of four cases — case 6
gained a real new finding (counter, A-graded), case 2 recovered a
previously-named gap (breadcrumbs-slot), case 3 promoted a
previously-suppressed signal to a properly-evidenced finding by doing the
reachability work iteration 1's run didn't. But recall is **not
monotonic**: case 2 lost a previously-verified A-grade finding
(`Header variant="h1"`), case 3 lost two previously-reported items, and
case 1 lost the `closeAriaLabel` finding. None of this is attributable to
the one-line SKILL.md edit (the touched section has nothing to do with
Modal ARIA labels or Header variants) — it's evidence that **a single
fresh run of this skill has real run-to-run variance**, a caveat that
applies to iteration 1's numbers too and is worth stating plainly rather
than only implicitly.

## 6. Boundary-pressure results, before vs. after

**Case 4 (the designed boundary case), with escalation now available**
(`runs/iteration-2/skill-i2-case-4-boundary-endpoints.md`): 3 findings
(sortable-column `ariaLabel`, `enableKeyboardNavigation`, `noMatch` —
all real, all independently verified A/A/B, no overreach), **0
escalations**. "What was not evaluated" again named "whether a `Modal`
is the right way to show endpoint details versus a split panel" —
verbatim, almost identically to the v2 frozen-skill run — but still only
as a passing clause, never elevated to the new Escalation section despite
it now existing. **The escalation mechanism did not fire on the case it
was built for**, on any of three independent reads (v1, v2, v2 +
escalation).

**Real fixture — `Identities.tsx`, the central result.** The
iteration-2 run produced a `violation`-classified Finding 1: replace
`ContentLayout` + default `Table` variant with `variant="full-page"`,
citing the table-view pattern page's *"Don't use the content layout
component on this type of page. Instead, use the 'full-page' variant of
the table component"* as REQUIRED authority. Its own "Escalations"
section explicitly considered and rejected escalating this, reasoning
that the page already *is* a single full-page table, so the pattern
page's rule is "a concrete rule already in play," not "recomposing the
page into a different pattern."

A dedicated adversarial verifier (`runs/iteration-2/verify-i2-case-1-identities.md`)
was asked to independently judge exactly this boundary question — not
just apply the standard rubric — and graded Finding 1 **D (overreach)**.
Its reasoning, which I find persuasive on independent reading of the same
sources: the finding collapses "the page's content happens to be
table-shaped" into "the page is a declared instance of the table-view
pattern," which is precisely the shape-match trigger `SKILL.md`'s scope
boundary warns against ("propose restructuring... just because such a
pattern exists"). Recommending `variant="full-page"` plus coordinating
`AppLayout`'s `contentType` is functionally identical to what a
component-selection/pattern reviewer would say. The citation is a
*pattern* page (retrieval priority 4), used here at REQUIRED strength for
a layout/variant choice — priority 4 is worded to *"establish a concrete
implementation rule already in play,"* and stretching a page-composition
recommendation to REQUIRED strength off a pattern citation is more than
that carve-out was meant to license. Most tellingly, the finding's own
proposed fix admits half of it (`AppLayout`'s `contentType`) lives
outside the audited files — itself evidence the concern doesn't fully
resolve at the implementation layer being judged. Finding 2 (monospace/
`<code>` vs. `Box` code variants) verified cleanly, **A**.

**This is the decisive result on the boundary question.** Not silence
this time (iteration 1's central ambiguity — "did it correctly withhold
the finding, or never generate it?" — doesn't apply here), and not a
correct escalation either. The frozen skill's core reasoning, even with
an explicit escalation outlet available and explicitly invoked in its own
deliberation, argued itself into an overreach on the flagship real
fixture where this question mattered most.

## 7. Escalation candidates and verifier judgments

**Total escalations produced across all 6 iteration-2 runs (case 4, case
5, case 6, `Identities.tsx`, case 2, case 3): zero.** The mechanism never
fired — not spuriously (good for precision) and not on the case built for
it, nor on the real fixture where its own deliberation explicitly reached
for it and talked itself out of it (bad for the boundary-awareness
question this iteration exists to answer).

Applying the task brief's 5 escalation-specific verifier questions to the
one case where escalation was genuinely live (`Identities.tsx`):

1. *Is there genuinely material evidence above the implementation
   layer?* Yes, per the verifier's own read — the pattern-level "is this
   correctly composed as this app's instance of the table-view pattern"
   question is real.
2. *Is the implementation audit unable to resolve it without changing
   jurisdiction?* Yes — the verifier's own strongest point is that half
   the proposed fix reaches outside the audited files.
3. *Did the escalation avoid prescribing the higher-level answer?* N/A —
   no escalation was produced; a `violation` at REQUIRED strength was
   produced instead, which is a stronger prescriptive claim than an
   escalation would have been permitted to make.
4. *Would the signal have helped an FDE decide whether another review is
   warranted?* Plausibly yes, more honestly than the `violation` that was
   actually reported.
5. *Material enough to surface?* Yes.

So on the one case that mattered, the honest answer to "should this have
escalated" is yes — and it didn't, despite explicitly considering it.
**Diagnosis, not a re-tuning:** the escalation gate's second condition
("no implementation finding, at any classification, honestly resolves
it") is exactly where the reasoning failed — the reviewer judged its own
candidate finding as resolving the tension, and the verifier's read is
that judgment was wrong. A self-attestation gate is only as reliable as
the self-critique behind it, and this round's evidence is that it isn't
reliable enough yet. Per the task brief's explicit instruction not to
silently tune after seeing results, **no further SKILL.md edit was made
this round** — this is recorded as a concrete, evidenced input for a
future iteration's smallest next step (section 12), not acted on now.

## 8. Regression results

| Fixture | Iteration-1 result | Iteration-2 result | Regression? |
|---|---|---|---|
| Case 5 (synthetic) | 1 finding, A | Same finding, unchanged | None |
| Case 4 (synthetic, v2-equivalent) | 2 findings, no grade recorded (only escalation-run graded) | 3 findings — A, A, B | None; escalation-run's 3 findings independently verified clean |
| `DetailPage.tsx` (case 2, real) | 4 findings, 4/4 A | 5 findings; new ones reviewed directly (not independently re-verified) and read as clean, correctly-scoped composition-slot findings | No overreach observed; recall gain, with the caveat noted in section 5 |
| `Form.tsx` (case 3, real) | 3 findings + 1 unresolved, 2A/2B | 3 findings; not independently re-verified this round | No overreach observed on direct reading; the promoted Select/Tiles/RadioGroup finding is unusually well-evidenced (traced through actual initial state) |
| `TeamsPage.tsx` (case 6, synthetic) | 1 finding, A | 3 findings — **D, A, A** | **Yes — a genuine, newly-discovered D-grade.** The "selection wired to no consuming action" finding cites a real Table usage-guideline quote (*"Only use selection if the user can take action on the items in the collection"*) but the verifier's independent judgment is that the underlying diagnosis is a general workflow/product-completeness judgment dressed in an accurate citation — the same shape `SKILL.md`'s own "General UX judgment" exclusion list names ("number of primary actions," "workflow design"). The finding's careful hedge on the *fix* ("a product decision this audit can't resolve from the code alone") doesn't relocate the *diagnosis* to the implementation layer. This is a real failure mode iteration 1's narrower 3-fixture battery never exercised — not caused by this round's SKILL.md edit (unrelated section), but genuinely newly surfaced by this round's pressure cases doing their job. |
| `Identities.tsx` (case 1, real) | 2 findings, A/A | 2 findings — **D, A** | **Yes — see section 6.** The most consequential single result of this iteration. |

**Explicit checks against the task brief's named regression risks:** no
run flagged every custom component, no run escalated an ambiguous choice
(0 escalations total, so this specific risk is trivially absent), no run
treated component existence alone as criticism, no run reported pattern
guidance as an implementation violation *except* the one Identities.tsx
case documented above (which is exactly this failure mode, caught by
adversarial verification rather than avoided), no run emitted generic UX
observations as findings *except* the one case-6 finding documented above,
D/E findings did increase (0→2 D, 0 E) across the expanded evidence base
— reported honestly rather than smoothed over — and no run buried its
report in "review this elsewhere" notes (0 escalations, if anything the
opposite risk materialized). A clean audit with no findings and no
escalations remains structurally possible under the new report template
(nothing in the addition requires a non-empty Escalations section) — not
separately re-tested this round since none of the six runs produced one,
but the template's "None." default is unchanged from the Suppressed
section's existing pattern.

## 9. Deterministic tooling

**No changes made, and none were needed.** Both `inspect_surface.py` and
`resolve_versions.py` ran unmodified against three brand-new synthetic
fixtures (cases 4, 5, 6) and the real fixture rerun, correctly reporting
native-element/style facts, JSX inventories, and resolved-vs-unresolved
package versions in every run, including correctly reporting case 3's
fixture as a genuinely unresolved semver range (no lockfile) — exactly
the "fact, not a guess" behavior iteration 1 already validated. This
iteration's failures were entirely in reasoning (the boundary judgment,
the case-6 scope-creep), not in evidence-gathering; per the task brief,
this confirms no tooling expansion is justified.

## 10. Comparison with unguided baseline

Not re-run this round — the task brief scoped this iteration to the
boundary and recall questions specifically, not a re-litigation of the
skill-vs-baseline comparison iteration 1 already established. Where this
round's evidence intersects that comparison: iteration-1's baseline (case
2) is the one that originally caught the breadcrumbs-slot finding the
frozen skill missed and iteration-2's rerun recovered — a direct,
concrete instance of "closing a recall gap baseline had already
demonstrated," which is a real, if narrow, win for the skill's continued
differentiated value.

## 11. Decision-criteria assessment

**Precision.** Does the 0 D/E behavior hold? **No, not across the full
iteration-2 evidence base.** Aggregating this round's newly-verified
findings (case 4: A,A,B; case 6: D,A,A; `Identities.tsx`: D,A — 9
findings, 6 A / 1 B / 2 D / 0 E) with iteration 1's original 10 (6 A / 4
B / 0 D / 0 E) gives **12 A / 5 B / 2 D / 0 E across 19 adversarially
verified findings** — 89% A/B, 0% E (no factually-wrong finding has ever
been produced across either round), but no longer 0% D. Both D-grades are
genuine, specific, well-characterized overreach instances, not vague
unease — that is itself evidence the pressure-testing and verification
process is working as intended, not evidence the skill has gotten worse.

**Recall.** Does the skill reliably catch the targeted implementation
defects? **Yes, on the two purpose-built recall cases** — both planted
defects found, correctly characterized, correctly scoped fixes, zero
false positives, both A-graded. On real fixtures, recall improved on net
(section 5) but is not monotonic and has real run-to-run variance
independent of any skill change.

**Boundary discipline.** Does it continue refusing component/pattern/UX
prescriptions? **Mostly, with one confirmed exception.** 7 of 8 case-6
findings-worth-checking and the case-4/case-5 findings all passed
boundary review cleanly; the `Identities.tsx` Finding 1 and case-6's
"selection wired to no consuming action" finding are two concrete,
verified counter-examples this round's pressure specifically surfaced.

**Boundary awareness.** Can it recognize material higher-level issues
without silently presenting an incomplete review? **Partially, and this
is the least resolved dimension.** The mechanism exists, is documented
narrowly, never fired spuriously — but in the one case it was most
directly relevant and was explicitly considered, the self-critique behind
the gate failed. "Silent" is no longer the right word for what happened
on `Identities.tsx` (the run visibly engaged with the question) — but the
outcome, an unwarranted `violation`, is arguably worse than the silence
iteration 1 produced on the same underlying tension.

**Escalation precision.** Are escalation signals rare and useful rather
than noisy? **Rare: yes (0/6). Useful: not demonstrated this round** —
zero data points of a correct escalation to evaluate usefulness against.

**Baseline value.** Does the skill remain meaningfully better than an
unguided Cloudscape review? **Yes.** Every finding this round carries the
same structured, verifiable evidence contract iteration 1 established;
recall gains recovered real gaps baseline had already shown existed
(breadcrumbs-slot); the promoted `Select`/`Tiles`/`RadioGroup` finding in
case 3 is more rigorously evidenced (traced through actual reachability)
than baseline's original version of the same signal. This dimension is
not in question this round.

## Verdict

**ITERATE.**

Not RETIRE: recall on both purpose-built pressure cases was clean and
verified, real recall gaps against baseline closed on two of three real
fixtures, and the skill's evidence-and-verification discipline continues
to produce a materially more checkable artifact than an unguided review.

Not KEEP: this round's central, most carefully-designed test — the
flagship real fixture where the boundary question already mattered most
in iteration 1 — produced a confirmed, adversarially-verified overreach,
with the reviewer's own escalation deliberation talking itself into the
wrong answer rather than either the right finding or the right silence.
A second, independent D-grade appeared on a purpose-built recall case
that iteration 1's narrower battery never exercised. Two D-grades against
19 total verified findings is not proof of a broken skill, but it is
concrete, evidence-backed shortcoming this repo's convention treats as
pressure to add, not grounds to declare the boundary question solved.

**Given ITERATE, this explicitly does NOT justify starting a separate
higher-level reviewer** (`cloudscape-component-selection-review` or
similar) — if anything, this round's evidence argues more strongly
against it than iteration 1's did: the one case that most needed a
higher-level review to exist didn't cleanly hand off to one via
escalation; it produced a confident, specific, wrong answer instead. That
is a reason to hold this layer's own reasoning to closer scrutiny before
building on top of it, not a reason to build the next layer.

## 12. Smallest justified next step

**Do not re-tune SKILL.md's Escalation section immediately** based on a
single observed failure — per the task brief's own discipline, one edit
cycle was made and evaluated this round; further wording changes chasing
this specific result risk fitting the fixture rather than the underlying
judgment failure.

Two concrete, narrowly-scoped candidates for a **future** iteration,
neither committed to here:

1. **A targeted pressure case for the escalation gate's self-critique
   failure specifically** — construct 2–3 more cases shaped like
   `Identities.tsx` (a real, defensible pattern-page "Don't...Instead"
   citation that *could* license either an implementation finding or an
   escalation) and test whether a structural change — e.g., requiring the
   Boundary check to explicitly answer "would the complete fix touch
   anything outside the audited files" — changes the outcome, before
   editing the prose that failed this round.
2. **A targeted pressure case for the case-6 D-grade shape** — "a
   component's own docs state a usage precondition (`X` requires `Y`),
   and the surface violates the precondition" is a citation shape that
   can encode either a genuine implementation defect (Modal+Tabs, case 5)
   or a general product/workflow judgment (case 6's selection-with-no-
   action). Whether this distinction is teachable via a short addition to
   the "General UX judgment" exclusion examples, or whether it requires
   a different mechanism, is unresolved and worth its own narrow test
   before touching SKILL.md again.

Both are diagnostic questions, not proposed fixes — consistent with this
round's own finding that pressure-testing before rewriting is what
surfaced real, previously-invisible failure modes in the first place.

## What this round proves / does not prove

**Proves, on this round's evidence:** the frozen skill's recall on two
purpose-built, adjudicable pressure cases is genuinely strong and
verified; a narrow, well-specified escalation mechanism can be added
without introducing any observed spurious escalation; the deterministic
tooling generalizes cleanly to new fixtures with zero changes; and — the
central result — this skill's boundary discipline has at least one
concrete, adversarially-confirmed failure mode on a real fixture, not
merely a theoretical risk.

**Does not prove:** that the escalation mechanism is worthless (n=0
correct-escalation data points either way); that the case-6 D-grade
generalizes beyond this one citation shape; that the lost findings in
sections 5/8 (Header-h1, closeAriaLabel, submit-button-disabled,
deprecated-prop) reflect anything other than ordinary single-run
variance — each was previously verified once, in one run, and this round
did not re-verify their absence as a deliberate suppression versus a
draw-to-draw miss. As in iteration 1: one round, one model, a small
number of fixtures — suggestive, not statistically powered.
