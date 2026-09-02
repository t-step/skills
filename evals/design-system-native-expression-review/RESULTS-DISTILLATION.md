# design-system-native-expression-review — distillation round

**Run date:** 2026-09-02. **Skill edited:** `skills/design-system-native-expression-review/SKILL.md`. **Purpose:**
this is not a behavioral-iteration round. The reasoning operation is
considered provisionally validated by the equivalence-isolation round
(`RESULTS-EQUIVALENCE.md`: E1 2/2, N1 2/2, N2 1/1, VERBATIM clean across
all seven runs). This round's job was to make SKILL.md smaller, cleaner,
and less shaped by the specific history of its evals, while
demonstrating — via regression, not assertion — that the validated
reasoning is preserved.

## 1. Size

| | Lines | Words |
|---|---|---|
| Original SKILL.md | 522 | 4,020 |
| Distilled SKILL.md | 477 | 3,613 |
| Change | −45 (−8.6%) | −407 (−10.1%) |

This is a deliberately modest reduction. Per the task's own instruction,
this round did not optimize for minimum token count — it removed
maintainer/historical narrative and one significantly overfit paragraph,
while leaving the core reasoning procedure, finding contract, and every
explicitly-required preserved behavior intact, sometimes verbatim.

## 2. What was removed, shortened, moved, or merged

### 2a. "Lineage and evidence" → "Lineage" (43 lines → 17 lines)

The original section narrated, in the runtime skill file, the full
history of the Cloudscape-only predecessor, the MUI generalization
experiment, prior citation-fabrication rates, and the
`cloudscape-implementation-audit` skill's role in shaping the scope
boundary. None of that is runtime-actionable — an LLM executing this
skill does not need the MUI-round citation-fabrication percentages to
review a page correctly.

**Kept:** the two runtime-relevant *design decisions* that history
produced (corpus-adaptive authority discovery instead of an assumed
hierarchy; the evidence-mode label on every finding) and a pointer to
`evals/design-system-native-expression-review/README.md` and its
`RESULTS*.md` files for the full account. **Moved:** all of the
percentages, round-by-round narrative, and the `cloudscape-
implementation-audit` backstory already live in
`evals/design-system-native-expression-review/README.md` (updated below)
and the individual `RESULTS*.md` files — nothing was deleted from the
repository, only removed from the file an LLM re-reads on every
invocation.

**Why this was believed safe:** this is squarely category (1) of the
decision rule — "removes purely historical/maintainer material from
runtime context." No instruction, invariant, or guardrail lived only in
the deleted prose; every design decision it explained is still stated,
just without the narrative justification for *why* the decision was
made historically.

### 2b. "How this composes" merged into "Out of scope" (a standalone
subsection folded into a fourth bullet)

The original had a freestanding "How this composes" paragraph after the
Out-of-scope bullet list, restating that implementation correctness is
out of scope (already bullet 1) and adding one genuinely new point —
that cross-surface/multi-page synthesis is also out of scope. Restating
implementation correctness a second time, in a new subsection, is
duplicated instruction; the one new point (cross-surface synthesis) did
not need a separate subsection to say it.

**Kept:** the cross-surface-synthesis point, as a fourth `Out of scope`
bullet, phrased to also carry forward the "don't freelance either layer"
warning. **Cut:** the restatement of implementation correctness (already
covered by bullet 1) and the "review that also freelances... is harder
to trust" framing sentence, whose substance is preserved by the bullet
now sitting alongside the other three out-of-scope categories.

**Why this was believed safe:** category (2) — genuine duplication
removed, the one non-duplicated invariant (cross-surface synthesis is
out of scope) preserved and relocated rather than deleted.

### 2c. Same-tier equivalence paragraph (32 lines → 12 lines)

This is the paragraph the task brief specifically flagged as likely
overfit to the retired P1 case's failure mechanism (decision-table rows,
property counts, the "different row of the same table" loophole closed
in the postfix round's v4 edit). See §5 below for the full before/after
text and the regression evidence for this specific change — E1, N1, and
N2 trial 2 all exercised this exact paragraph and it held.

### 2d. Finding contract's "Authority evidence" full-table field (small
wording change, see §6)

Loosened from "reproduce the whole table" to "include enough of it...
explicitly disclose any row that qualifies, equalizes, or contradicts."
See §6 for the reasoning and regression evidence — this is the change
this round is least confident about, and it's flagged as unresolved
rather than confirmed safe.

### 2e. Minor prose trims

- Step 2 (script usage): shortened the `inspect_surface.py` and
  `resolve_versions.py` explanatory paragraphs by roughly a third,
  keeping every caveat that appears validated by eval history (the
  "handles both deep subpaths and barrel imports" note; the "an
  unresolved semver range... name that" note) and cutting sentence-level
  restatement.
- Finding contract's `Boundary check` field definition was shortened to
  cross-reference "Scope boundary" (where the instruction to perform the
  check already lives) instead of restating the same one-sentence
  requirement a second time.
- The intro's second paragraph dropped a self-referential pointer
  ("Splitting them here would force artificial, premature boundaries
  this skill's own evaluation exists to test — see 'Lineage and
  evidence,' below...") since the evidence it pointed to moved out of
  the runtime file; the underlying claim (don't split component and
  composition reasoning) is unchanged and unshortened.

### 2f. What was deliberately left unchanged

Per the task's own instruction not to touch what can't be demonstrated
safe to simplify: the "Applicability argument" and "Why it matters"
fields (found materially distinct in every report read from this
skill's own eval history — one is the four-point-test checklist, the
other is the consequence statement); `Authority strength`; the VERBATIM/
PARAPHRASE/SYNTHESIS/INFERRED definitions (validated, positive evidence
per `RESULTS-POSTFIX.md` §4); the "Missing intent" section; the "Report"
template; the four-point anti-fundamentalism test itself; and the entire
five-step core reasoning procedure's structure.

## 3. Runtime history moved out of SKILL.md

All of the following now live only in
`evals/design-system-native-expression-review/README.md` (and the
`RESULTS*.md` files it links), not in the runtime skill file:

- The Cloudscape-only predecessor's full evaluation summary (bounded-
  surface scope, the anti-fundamentalism rule, applicability-before-
  availability, suppression of equally-valid alternatives — all still
  true and still enforced by the current text, just not re-narrated).
- The MUI generalization round's specific citation-fabrication rates
  (1-in-7 → 3-in-6) and which specific rule wording transferred cleanly.
- The `cloudscape-implementation-audit` predecessor's role in informing
  the scope boundary and anti-fundamentalism rule.
- The morph regression round's case-by-case grades, the post-fix
  round's four P1 trial mechanisms, and the equivalence-isolation
  round's fixture-design rationale — these were already only in
  `RESULTS*.md`, not duplicated in SKILL.md to begin with.

## 4. Eval lineage update

Per the task's instruction, `evals/design-system-native-expression-
review/README.md` is updated (see the "Distillation round" section added
there) so that:

- E1 is named as the canonical equivalence regression case.
- N1 is named as the canonical component-level inverse control.
- N2 is named as the canonical composition-level inverse control.
- `case-p1-message-queues` Candidate 2 remains explicitly retired/
  compromised for the equally-valid-suppression axis — this round did
  not touch that retirement, restore it, or relitigate it. Its historical
  failures (`RESULTS-POSTFIX.md` §3) remain recorded, unedited.

No historical result file was modified to look cleaner. `RESULTS.md`,
`RESULTS-POSTFIX.md`, and `RESULTS-EQUIVALENCE.md` are untouched.

## 5. Same-tier equivalence rule: treatment and regression evidence

**Before (32 lines)** included: the reconciliation requirement ("whether
or not you end up quoting it"); the tie → suppress/`intent-dependent`
rule; an explicit rejection of "a different row of the same table" as a
license to pick a direction; a compact restatement of the fixture-
resolution check; and the non-default-preference escape hatch.

**After (12 lines)**, reproduced in full:

> **Same-tier equivalence controls point 4.** Before finalizing point 4,
> reconcile the *complete* authoritative material you retrieved for this
> candidate — not only the excerpt you plan to quote. If that material
> places the current and proposed expressions in the same suitability
> tier (a tied decision-table cell, fit-tier classification, or unranked
> "use X or use Y" pairing) rather than stating a directional preference
> between them, point 4 fails: suppress the candidate or classify it
> `intent-dependent`. A nearby differentiating clause — another row of
> the same table, a different page's "use X if Y" — does not by itself
> overturn a tie your own retrieval surfaced, including when that clause
> differentiates by an unresolved user intent or behavior ("if users
> tend to..."); that describes two different intents, not a direction.
> Check whether *this bounded surface's own code, comments, or copy* —
> never a property of the data itself, like a column's cardinality, and
> never the authority page — resolves which intent applies. If it
> doesn't, this is a "Missing intent" candidate: classify
> `intent-dependent` or suppress it, don't pick a direction because one
> reading sounds more specific than the other. This is not a default
> preference for the current implementation — when the surface itself
> resolves the intent, or evidence genuinely independent of the tied
> material establishes a task-specific advantage, the finding still
> stands.

Every invariant identified as load-bearing in the original was kept: (a)
reconcile the complete authority regardless of what you plan to quote,
(b) tie → no default direction, (c) a nearby differentiating clause
doesn't override a tie unless the *surface itself* resolves it, (d) the
"cardinality is not evidence of intent" trap named compactly instead of
across several sentences, (e) the non-default-preference escape hatch.

**Regression evidence this paragraph still governs correctly:**

- **E1** (distilled skill, 1 trial): the exact candidate this paragraph
  exists to catch (`TextFilter` alone vs. adding `CollectionSelectFilter`)
  was correctly suppressed, citing the tied "Complexity of the resource"
  cell and naming the unresolved "User goals" row — the required
  suppress/`intent-dependent` outcome.
- **N1** (distilled skill, 1 trial): the inverse — a *stated directional*
  criterion (Checkbox/Toggle "Selection" row) — was correctly reported,
  not suppressed, confirming the paragraph's escape hatch (a real
  directional criterion still produces a finding) survived the trim.
- **N2** (distilled skill, 2 trials): trial 2 correctly reported the
  Wizard finding, explicitly checking for and ruling out a same-tier tie
  ("only the 'Sub-resource create' row ties both... not the one this
  finding relies on"). Trial 1 did *not* fail via this paragraph's
  mechanism (no "different row of the same table" argument, no tie
  claim at all) — see §8 for what actually happened there.

## 6. Full-table reconciliation vs. full-table reproduction

**Before:** "reproduce the whole table here — every row, not only the
row(s) that support the finding's direction."

**After:** "include enough of it here that a reader can audit the tier/
direction question without re-fetching it, and explicitly disclose any
row that qualifies, equalizes, or contradicts the finding's direction.
Never quote a differentiating row while silently omitting one that ties
the current and proposed approaches in the same tier."

**Reasoning this was worth testing:** `RESULTS-POSTFIX.md` §3's own
before/after trial history shows full-table reproduction (added at trial
v3) did not, by itself, stop the deeper failure — trial v3 reproduced the
whole table, correctly named the tie, and *still* argued past it using a
different row. What actually closed that specific loophole was the
same-tier-equivalence paragraph's "different row" instruction (added at
v4), not the reporting requirement. That's evidence the reasoning
requirement (reconcile the whole table) is what's load-bearing, and the
reporting requirement (print the whole table) is a blunt enforcement
mechanism for the specific failure of *dropping* an equalizing row while
keeping a differentiating one — which "explicitly disclose any row that
qualifies, equalizes, or contradicts" targets more precisely without
forcing verbatim reproduction of irrelevant rows on a large table.

**Regression evidence:** every distilled-skill trial that cited a
decision/criteria table (E1's filter-patterns table, N1's Boolean-
selection table, both N2 trials' Length/Complexity/Error-handling rows,
Case C's building-block citations) disclosed the full relevant table or
the specific tying/qualifying rows in every instance — no selective
quotation that dropped an equalizing row was observed in five distilled-
skill reports and two comparison reports read closely for this round.

**Verdict on this specific change: adopt, but flag as the least-tested
simplification in this round.** It was exercised correctly in every
trial run, but the sample (5 distilled reports) is smaller than what
would be needed to rule out the specific selective-quotation failure
this field exists to prevent recurring under different phrasing. A
future round touching this axis should specifically try to reproduce
v3's "acknowledged-but-argued-past" shape against the new wording before
treating this as fully settled.

## 7. Finding contract fields: changed vs. retained

**Changed:**
- `Authority evidence` — full-table reproduction loosened to full-table
  *disclosure* of qualifying/equalizing/contradicting rows (§6).
- `Boundary check` — field definition shortened to cross-reference
  "Scope boundary" instead of restating the one-sentence requirement.

**Retained, no changes attempted (no safe simplification demonstrated):**
`Finding`, `Type`, `Materiality`, `Confidence`, `User task`, `Repository
evidence`, `Evidence mode` (all four sub-definitions), `Applicability
argument`, `Current expression`, `Native expression`, `Why it matters`,
`Authority strength` and its interaction paragraph, the closing "a
native-expression finding does not need to be a violation" paragraph.

No field was removed. No field was merged. `Applicability argument` and
`Why it matters` were specifically investigated per the task's request
(are they materially distinct in successful runs?) — in every report
read across this round and prior rounds, `Applicability argument` reads
as the four-point-test checklist and `Why it matters` as the consequence
statement; they are not interchangeable in practice, so they were left
separate.

## 8. Trial-by-trial regression results

All trials: fresh `general-purpose` subagents, no shared context, given
either the distilled SKILL.md (at a scratch path with its own copy of
the unmodified `scripts/`) or the original, committed SKILL.md, and the
exact bounded fixture. Full reports committed at
`runs-distillation/*.md`.

| Case | Skill version | Trials | Required outcome | Result |
|---|---|---|---|---|
| E1 (equivalence) | distilled | 1 | suppress/`intent-dependent` on TextFilter→CollectionSelectFilter | **PASS** — suppressed, correctly reasoned, citing the tied row and the unresolved "User goals" differentiator |
| N1 (component inverse) | distilled | 1 | report Checkbox→Toggle | **PASS** — reported at high/high, VERBATIM, full criteria row disclosed |
| N2 (composition inverse) | distilled | 2 | report single-page Form→Wizard | **1/2 PASS** — trial 2 passed cleanly (high/high, VERBATIM, correct tie-check); trial 1 did not report the required finding (see below) |
| N2 (composition inverse) | **original, unmodified** | 1 (this round) + 1 (prior round) | report single-page Form→Wizard | **2/2 PASS** — this round's comparison trial matches the prior round's single trial exactly (high/high, VERBATIM) |
| Case C (Cloudscape strong positive) | distilled | 1 | reproduce the unified `combined selection + composition` KeyValuePairs/tab-placement finding | **PASS** — reproduced designed intent exactly, matching two prior A-grade rounds |
| hkbus (MUI strong positive) | distilled | 1 | reproduce `RouteUpdateNotice`→`Alert` finding | **PASS** — reproduced at high materiality, matching the one finding that has reproduced exactly across every prior round (frozen, morph, postfix); additionally showed clean scope discipline on the Dialog/fullScreen question (properly `intent-dependent`, no bundling of implementation mechanics — a shape that regressed in a past round on the *original* skill) |

**E1 additional observation (not the primary axis, flagged not
confirmed):** the distilled trial reported three findings beyond the
core suppression test (Table variant, column order, Badge-for-
environment). Two of these (Table variant, column order) are consistent
with what the *original* skill's own two baseline trials on this same
fixture also reported — those two baseline trials themselves disagree
substantially with each other (different `Type` labels, different
materiality, a different second/third finding each), establishing that
this fixture is not deterministic under the unmodified skill either. One
discrepancy is worth naming: the distilled trial reported "Badge for
environment" as a finding, where both original baseline trials
explicitly suppressed that exact candidate as an "equally-valid
stylistic alternative." This is a single instance on each side, on a
fixture whose own baseline already shows this much run-to-run variance —
not treated as a confirmed regression, but named here rather than
omitted, per this repo's evidence-discipline convention.

## 9. VERBATIM verification results

Per the task's instruction, VERBATIM citations were independently
re-fetched live (not graded against the run's own quoted text) for the
load-bearing claims in each report:

| Source | Quoted claim | Live re-fetch result |
|---|---|---|
| Cloudscape "Selection in forms" (Boolean selection criteria, Selection row) | Checkbox/Toggle cells, N1 | **Exact match**, character-for-character |
| Cloudscape "Create resource" decision table (Length row) | Modal/Single-page/Multipage cells, N2 trial 2 | **Exact match** |
| MUI Alert page introduction | "Alerts display brief messages..." , hkbus Finding 1 | **Exact match** |
| Cloudscape "Filter patterns" criteria table (Complexity of the resource row) | Text filter/Collection select filter cells, E1 | **Exact match** |
| Cloudscape "Details page with tabs" (Details summary container building block) | "serves as a summary that is always visible...", Case C | **Exact match** |

**Zero fabricated or drifted VERBATIM quotations found** in this
spot-check sample (5 load-bearing citations across 5 different reports
and 3 different source pages). This is a spot-check, not an exhaustive
per-quote audit of every citation in every report (that would mean
re-fetching several dozen individual sentences) — consistent with this
round's resource scope, but named explicitly so it isn't read as a
complete audit.

## 10. Simplification attempted and reverted, or flagged unresolved

**Nothing was reverted outright in this round.** One simplification is
flagged, not reverted, because the evidence is ambiguous rather than
clearly negative:

**N2's mixed result (§8).** One of two distilled-skill trials failed to
report the required Wizard finding. Its failure mechanism does not trace
to either of the two changes made in this round's most-edited section
(the same-tier-equivalence paragraph or the full-table-disclosure
field): the failing trial did not invoke a "different row of the same
table" argument (the specific failure mode the same-tier-equivalence
paragraph exists to close), and it did fully disclose the qualifying
Multipage-create tier language rather than selectively omitting it (the
specific failure mode the full-table field exists to close). Instead, it
introduced a genuinely new rationalization — that the surface's own
heavy use of field defaults evidences a "one-click to create" intent
that should override the Length decision table's numeric thresholds —
which is not a same-tier-equivalence argument at all; it is a case of
one real piece of authority (a Key UX concept elsewhere on the same
pattern page) being weighed against another (the Length table) without
either being tied. Two comparison trials on the *original, unmodified*
skill (this round's fresh trial, plus the prior round's single trial)
both passed cleanly on this exact fixture, which is suggestive that the
distilled skill regressed something — but the sample is 1-fail-of-2
distilled vs. 2-of-2 original, on a fixture whose only pre-distillation
evidence was a single trial to begin with. Per this repo's own
evidence-discipline convention (a suspected weakness becomes a repeat
trial before a rewrite, not an immediate edit), this is reported as an
**open item requiring a repeat trial in a future round**, not treated as
either a confirmed regression or a false alarm. No new rule was added to
SKILL.md in response to this single instance, per the task's explicit
instruction not to compensate for an ambiguous signal with a new,
more-complicated rule.

## 11. Final recommendation

**Adopt the distilled SKILL.md.** Rationale:

- Every case explicitly required by the task's regression protocol —
  E1's suppression, N1's report, one strong Cloudscape positive (Case
  C), one strong MUI positive (hkbus) — passed cleanly, in most cases
  reproducing the exact designed intent or matching the strongest prior
  grade.
- Citation fidelity was clean in every spot-checked instance across five
  different reports and three different source pages.
- The two most substantive content changes (same-tier equivalence
  paragraph, full-table field) were each specifically exercised by the
  regression trials and held.
- The one mixed result (N2, 1-of-2 distilled trials) is real and is
  reported honestly rather than hidden, but its failure mechanism is not
  attributable to a specific text this round removed or shortened, and
  the comparison evidence (2-of-2 on the original skill, including one
  trial run in this same round under identical conditions) is not yet
  strong enough — on this repo's own stated evidence bar — to justify
  either reverting a specific change or adding a new rule in response to
  a single instance.

**This is not a claim that N2 is fully resolved.** A future round should
specifically re-run N2 (both skill versions, 2+ trials each) before
either closing this open item or acting on it — consistent with this
repo's convention of treating single-instance signals as evidence to
watch, not evidence to act on unilaterally.

## Artifacts

- `runs-distillation/case-e1-distilled-skill.md`
- `runs-distillation/case-n1-distilled-skill.md`
- `runs-distillation/case-n2-trial1-distilled-skill.md`,
  `case-n2-trial2-distilled-skill.md`,
  `case-n2-original-skill-comparison.md`
- `runs-distillation/case-c-distilled-skill.md`
- `runs-distillation/hkbus-distilled-skill.md`
- `skills/design-system-native-expression-review/SKILL.md` — updated in
  place (522 → 477 lines); scripts unchanged.
