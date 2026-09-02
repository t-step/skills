# cloudscape-native-expression-review — iteration 3 results

**Run date:** 2026-09-01. **Frozen baseline:** commit `2745d97` ("chore:
retire cloudscape-implementation-audit as an active skill"), on branch
`worktree-design-system-calibration-eval-setup`. `SKILL.md` remains
byte-identical to that commit throughout this iteration
(`git diff 2745d97 HEAD -- skills/cloudscape-native-expression-review/SKILL.md`
is empty). This iteration adds two new cases and their grading keys
(commit `647ff0e`), runs the unmodified skill against them, and verifies
the results — no skill wording was edited to produce, accommodate, or
respond to anything this iteration observed.

This is a **precision-focused, single-issue verification iteration**, not
a broad re-run and not a redesign. Iteration 2 (`RESULTS-ITERATION-2.md`)
closed its own chartered question (whether Case A's recall miss was a
genuine gap — it wasn't) but incidentally surfaced one new, real,
adversarially-confirmed defect: A1 Finding 2, a self-hedged,
admittedly-equally-valid secondary finding reported anyway alongside a
correct primary finding. Iteration 2 explicitly declined to act on a
single instance and named the next experiment needed: an isolating case
that separates "does the reviewer correctly recognize an alternative as
equally valid" from "does it still report it anyway once a strong
primary finding is already on the page." This iteration builds that
case, plus its logical mirror (does a real, independent secondary
finding survive once a primary is already found, or does discipline tip
into under-recall instead), and adjudicates both.

## 1. Frozen skill state

- SHA at start of this iteration: `c18c53c` (iteration 2's final commit).
- SHA after freezing the two new pressure cases: `647ff0e`.
- `skills/cloudscape-native-expression-review/SKILL.md`: unchanged across
  both commits and unchanged from `2745d97` throughout. No skill edit was
  made before, during, or after any run in this iteration.

## 2. P1 and P2 designs

Full case-by-case rationale: `cases/case-p1-message-queues/prompt.md`,
`cases/case-p2-security-groups/prompt.md`, and their grading keys
(`grading/case-p1-message-queues.expected.md`,
`grading/case-p2-security-groups.expected.md`). Both fixtures were
validated against `inspect_surface.py` and `resolve_versions.py` before
freezing (both fully resolve `@cloudscape-design/components@3.0.900` /
`collection-hooks@1.0.60`, matching every prior case in this eval).

- **P1 (`MessageQueues.tsx`) — real primary + seductive equally-valid
  alternative.** A `Cards`-based, 24-item collection view whose header
  copy states an explicit comparison-to-decide task (mirroring Case B's
  already-validated finding shape, on a fresh resource type and a fresh
  citation path — the "View resources" pattern-family criteria page's
  quantified 9-vs-5-item and columnar-vs-visual thresholds — rather than
  reusing Case B's file). Embedded in the same fixture: two discrete,
  low-cardinality columns (`status`, `region`) that recreate A1 Finding
  2's decision shape on fresh material — the filter-patterns page's own
  criteria table places `TextFilter` and `CollectionSelectFilter` in the
  identical "Simple resource" complexity cell, meaning the retrieved
  evidence itself, not just low column count, establishes equivalence.
  Deliberately *not* built by copying A1's fixture: different primary
  axis (component selection vs. A1's pattern composition), different
  resource domain, different secondary framing (2 discrete columns in an
  explicitly-tied complexity tier, vs. A1's single discrete column with
  no such explicit tie).
- **P2 (`SecurityGroups.tsx`) — real primary + genuinely independent
  material secondary.** A stand-alone, `ContentLayout`+
  `Table variant="container"` resource-inventory table (the same
  validated finding shape as Case A1, on a fresh resource type and
  column set) *plus* a hand-rolled `<input type="checkbox">` multi-select
  mechanism (driving a "Delete selected" bulk action) standing in for
  `Table`'s own documented `selectionType="multi"` — a second,
  independent axis (selection mechanism, not page layout) with no
  documented "equally valid" escape hatch the way P1's filter axis has,
  chosen specifically so materiality could not be argued away.

Both designs include a named, explicitly non-scoring distractor (P1: the
card-view pattern's own `ContentLayout`-vs-`full-page` "Don't...Instead"
rule, which also applies to `Cards` and could surface as an unintended
third candidate; P2: the same `status`-column filter-mechanism
temptation P1 tests directly) — named in advance in the grading keys so
neither could be misread as an unplanned confound after the fact.

## 3. Grading keys

Both grading keys pre-adjudicate every candidate as **MUST REPORT**,
**MUST SUPPRESS**, or a named **non-scoring distractor**, per the task
brief's requirement, with citations independently verified live before
freezing (`/patterns/resource-management/view/index.html.md`'s criteria
table for P1 Candidate 1; `/patterns/general/filter-patterns/index.html.md`'s
criteria table for P1 Candidate 2; the table-view pattern page for P2
Candidate 1, reusing A1's already-verified citations; `/components/table/index.html.md`'s
selection-type documentation and `/patterns/general/actions/index.html.md`
for P2 Candidate 2). Full text: `grading/case-p1-message-queues.expected.md`,
`grading/case-p2-security-groups.expected.md`.

## 4. Raw frozen-skill behavior

Each run is a fresh, isolated `general-purpose` subagent with no shared
context with this session or with each other (same methodology as
iterations 1–2). Full committed writeups: `runs/case-p1-skill.md`,
`runs/case-p2-skill.md`.

- **P1:** One finding reported — Cards → Table, `combined component +
  pattern`, high materiality/confidence, argued via the two individual
  pattern pages' purpose statements rather than the grading key's own
  preferred quantified criteria table (a different but independently
  valid citation path). The MUST-SUPPRESS filter candidate was
  explicitly named in a "Suppressed" section with a real applicability
  argument (both view patterns' own "Filter" building block prescribes
  plain text filter as the reference component for this exact page
  type) rather than reported hedged as "equally valid."
- **P2:** Two findings reported, fully independent — Finding 1: hand-rolled
  checkbox selection vs. `Table`'s `selectionType="multi"`
  (`component selection`, high/high), argued in component-vocabulary
  terms with a concrete, doc-grounded behavioral consequence (selection
  not reset across sort/filter/pagination); Finding 2: `ContentLayout`+
  `container` vs. `full-page` (`combined component + pattern`, high
  materiality/medium confidence, self-hedged for the pattern's
  undocumented "few columns" threshold rather than overclaimed). Neither
  finding referenced the other as a precondition for its own materiality.
  The `status`-column filter distractor was not manufactured into a
  third finding.

## 5. Verifier results

Independent, fresh verifier subagents per case, each re-fetching every
cited `cloudscape.design` URL live rather than trusting quotation marks,
per `rubric.md`. Full writeups: `runs/case-p1-verify.md`,
`runs/case-p2-verify.md`.

| Case | Finding | Grade | Note |
|---|---|---|---|
| P1 | Finding 1 (Cards → Table) | **A** | One real, separate defect: folds the non-scoring `ContentLayout`/`full-page`-for-cards distractor into itself at unhedged `REQUIRED` strength without naming the missing-surrounding-shell-context caveat — a genuine missing-intent gap, but orthogonal to this case's central target (see §9). |
| P1 | Suppressed filter candidate | **Correctly suppressed** | Verifier confirms no A1 Finding 2 recurrence — real, evidence-grounded suppression, not silence and not a hedged report. |
| P2 | Finding 1 (checkbox selection) | **A** | Stayed on component-vocabulary ground throughout; did not drift into a11y/keyboard-mechanics critique of the existing checkboxes, the specific hazard this case named. |
| P2 | Finding 2 (`ContentLayout`/`full-page`) | **A** | Engaged the pattern's own "few columns" carve-out directly and self-hedged confidence to `medium` for an undocumented threshold rather than overclaiming — good epistemic discipline, not a materiality problem. |

## 6. Did the A1 Finding 2 failure pattern recur?

**No.** On P1 — the case built specifically to recreate its decision
shape — the frozen, unmodified skill visibly recognized the seductive
surface-level match (the code's own "narrow the list down to a specific
status or region" phrasing is a closer, more explicit textbook match to
the collection-select-filter example than anything in A1's fixture) and
then reasoned its way to a named, evidence-grounded suppression rather
than reporting a hedged "equally valid" finding. No trace of "found one
candidate, kept looking for a second, reported it anyway despite
hedging" appeared in either run's suppressed-candidate reasoning.

Per the task's own decision gate — "a skill change is justified if...
the reviewer explicitly acknowledges equivalence or low materiality but
emits it anyway... the same 'candidate should have self-suppressed'
behavior appears again" — **that behavior did not appear again.** A1
Finding 2 stands as a single, isolated instance across three iterations'
worth of findings, not a repeatable pattern.

## 7. Citation-fidelity findings

Neither run fabricated a citation, invented a URL, or misattributed a
claim's substance. Both runs showed the same *minor* category of defect
observed in iteration 2's Case A1 (never a fabrication or meaning
inversion, always a formatting/completeness liberty):

- **P1:** two instances — two adjacent bulleted list items merged into
  one quoted sentence without a break marker; a section heading and its
  body text stitched together with an em dash. Both textually accurate,
  neither meaning-altering.
- **P2:** three instances — a trailing clause ("...to maximize the
  available space") silently dropped from a quote without an ellipsis
  marking that specific trim; a four-item bulleted list rendered as
  comma-separated prose inside quotation marks; two adjacent same-topic
  bullets ellipsis-joined (the most defensible of the three, bordering
  on acceptable convention).

Per the task's explicit instruction — "do not fail an otherwise good
recommendation solely because prose could be phrased more elegantly, but
do grade fabricated/misattributed quotations as a real evidence-quality
defect" — none of these five instances rises to a disqualifying defect:
all are word-preserving formatting liberties (list-to-prose
reformatting, heading/body stitching, one narrow, honestly-adjacent
trim), not inventions or inversions. **Neither verifier downgraded any
finding's grade for these**, consistent with the rubric's own
instruction to flag citation fidelity separately from the materiality
judgment. This is a real, mild, continuing pattern across iterations
(A1's iteration-2 defect was more severe — two clearly fabricated
verbatims dressed as literal text) but does not, on this iteration's
evidence, escalate or recur at A1's severity.

One incidental correction for the record: P2's own grading key
misattributed a "table inside a container with other content" quote to
the Container variant heading; live verification shows that sentence
actually lives under the Borderless variant. This is an error in the
grading key's own supporting citation, not in either agent run, and does
not affect either finding's grade.

## 8. Skill change made

**None.** `skills/cloudscape-native-expression-review/SKILL.md` remains
byte-identical to the frozen baseline (`2745d97`) throughout this
iteration. Per the task's decision gate, a change was to be made only if
the A1 Finding 2 pattern recurred; it did not.

## 9. Regression results

Not run. Per this repo's `AGENTS.md` eval-expectations convention and
the task brief's own instruction, a regression set is required only "if
the skill changes." Since no change was made, iteration 1's seven-case
results (`RESULTS.md`) and iteration 2's three-case results
(`RESULTS-ITERATION-2.md`) stand unmodified and still describe the
current, unchanged skill.

One new, single-instance, orthogonal observation surfaced incidentally
during this iteration's own verification (not requiring regression
testing to notice, since it was caught directly by P1's verifier): P1
Finding 1 folds the fixture's deliberately-tolerated
`ContentLayout`/`full-page`-for-`Cards` ambiguity into its high-confidence,
`REQUIRED`-strength finding without naming the missing-surrounding-shell-
context caveat SKILL.md's "Missing intent" section calls for. This is a
real, adversarially-confirmed gap — but it is orthogonal to this
iteration's chartered question (candidate suppression, not missing-intent
hedging on a layout question), a single instance, and the same
epistemic shape as A1 Finding 2 and the original Case A miss before it:
per this repo's own precedent for treating one incidental miss as
insufficient grounds for a rewrite (`RESULTS.md` §16,
`RESULTS-ITERATION-2.md` §4), it is recorded here as a second named,
isolated limitation rather than acted on. If a future iteration is
chartered to test missing-intent hedging on layout/variant recommendations
specifically, this observation is the concrete starting point.

## 10. Did the skill over-suppress P2?

**No.** Both of P2's independently-adjudicated MUST-REPORT candidates
were reported as genuinely separate findings, each carrying its own
complete Finding-contract block (Type, Materiality, Confidence, evidence,
applicability argument, boundary check), with neither referencing the
other as a precondition for its own materiality. The one candidate that
was folded/suppressed (the header-counter format reflecting selection
count) was correctly identified as a downstream symptom of Finding 1,
not an independent third finding — proper materiality discipline, not
under-recall. The tolerated `status`-column filter distractor was not
manufactured into a spurious third finding either. Finding one real,
strong issue did not crowd out, dilute, or absorb a second, genuinely
independent one.

## 11. Final verdict

**PROMOTION-READY**, on this iteration's chartered question, with two
named, isolated limitations carried forward for the record (not
disqualifying, per the task's own standard that "PROMOTION-READY does
not require zero historical mistakes"):

1. **A1 Finding 2** (iteration 2) — a self-hedged, equally-valid
   secondary finding reported anyway. This iteration's evidence
   (P1, built specifically to recreate this decision shape) shows the
   failure **did not generalize**: the frozen, unmodified skill
   correctly suppressed a fresh, comparably tempting instance of the
   identical shape with real, evidence-grounded reasoning.
2. **P1 Finding 1's missing-intent-caveat omission** (this iteration,
   §9) — a new, single-instance, orthogonal observation: an unhedged
   `REQUIRED`-strength claim on a candidate this file's own scope cannot
   fully resolve. Real and worth tracking, but not a recurrence of any
   previously-identified pattern, and not itself demonstrated as
   repeatable.

Neither limitation is a repeatable pattern on the evidence gathered so
far; both are single, named instances consistent with this eval's own
precedent for what does and does not justify a skill rewrite. The
central, chartered question this iteration exists to answer — does the
skill sometimes correctly recognize an alternative as equally valid or
low-materiality, then fail to suppress it before emitting the finding —
is answered **no** on this round's evidence: recognition and suppression
were the same act in both the P1 run and its verifier's independent
review, and P2 confirms this discipline does not come at the cost of
under-reporting a second, genuinely independent, materially-earned
finding.

Not KEEP-WITH-KNOWN-LIMITATION as a downgrade from PROMOTION-READY: that
verdict language was iteration 2's own hedge specifically because A1
Finding 2 was untested against a dedicated isolating case at the time.
That gap is now closed, with a clean result. The task brief's own
framing anticipated exactly this outcome ("Final verdict should likely
be PROMOTION-READY unless some new material problem appears") and no new
*material* problem appeared — only two small, named, non-recurring
observations, tracked above rather than allowed to silently disappear
into an unqualified verdict.

Not ITERATE: no repeatable pattern was demonstrated on the axis this
iteration was chartered to test (the opposite was demonstrated, twice —
once via correct suppression, once via correct independent retention),
and every other property validated across iterations 1–2 (boundary
discipline, missing-intent handling, anti-cargo-culting, combined
component+pattern reasoning, baseline comparison) is untouched by this
iteration's narrow scope and stands as previously reported.

Not RETIRE: nothing in three iterations' cumulative evidence supports
discarding this skill.

## 12. Promotion recommendation

This skill remains the sole active Cloudscape design-system calibration
skill (`cloudscape-implementation-audit` was retired at commit
`2745d97`). On the cumulative evidence across all three iterations — 100%
A/B findings across iteration 1's seven cases, iteration 2's targeted
recall-isolation success, and this iteration's clean pass on the one
remaining named concern — **this skill is ready for a deliberate
promotion decision** (copying it from `skills/` into
`plugins/software-engineering/skills/` per this repo's own promotion
convention), which was the single open item blocking that consideration
going into this iteration.

**This report does not itself initiate promotion.** That is a separate,
deliberate action per this repo's `AGENTS.md` ("Promotion from `skills/`
into the plugin tree is deliberate and one skill at a time, not
automatic"), and per this task's own explicit instruction not to
promote, publish, or modify the skill as part of this evaluation.
