# Adversarial Verification Report — Case P2: SecurityGroups.tsx

## Finding 1 (run) — Hand-rolled checkbox selection vs. `Table`'s native `selectionType="multi"` — corresponds to grading key **Candidate 2**

**Grade: A — material and strongly validated.**

Rubric walk-through:

1. **User task supported by repo evidence?** Yes. The in-file comment ("let an operator pick a batch of unused groups and delete them in one action"), the `checkedIds: Set<string>` state, `toggleOne`/`toggleAllOnPage`, and the `Delete selected (${checkedIds.size})` button are all directly cited with line numbers (40, 55–81, 111–129) and check out exactly against the fixture. `inspect_surface.py`'s claimed fact — exactly two raw `<input type="checkbox">` elements at lines 113 and 122 — matches the fixture precisely.
2. **Does the cited authority say what's claimed?** Yes, on all three sources cited (see Citation Fidelity section below for verbatim-level detail). The "controlled state" contract, the `Multi` selection type description ("Use for collections that support bulk actions"), the "make sure selection is also controlled by the hook" client-side guidance, the "reset item selection across pagination, sorting, filtering..." guideline, the "Don't show the number of selected items if nothing has been selected" rule, and the collection-hooks dev guide's `selection: {}` / `selectionType="multi"` / `collectionProps.selectedItems` worked example are all real and substantively as described.
3. **Four-point applicability test.** Task match: the observed task (checkbox multi-select feeding a bulk "Delete selected" action) is exactly the documented "collections that support bulk actions" scenario the `Multi` selection type names — not a superficial shape match. Current implementation solves the identical problem via a hand-rolled parallel mechanism. Proposed native expression preserves the same task (same rows selectable, same delete goal) — it is a mechanism swap, not a redesign. Material: there is no documented alternative that sanctions hand-rolled checkbox state as an equally valid pattern for this job.
4. **Preserves task semantics?** Yes, explicitly and correctly argued.
5. **Could the current code be equally valid Cloudscape usage?** No — and the run correctly establishes this rather than assuming it: `useCollection` is called with no `selection` option, `Table` receives no `selectionType`/`selectedItems`/`onSelectionChange`, so this isn't "a different but sanctioned selection mechanism," it is Cloudscape's own selection concept reinvented outside Cloudscape's own machinery.
6. **Materiality — would an FDE act on it?** Yes, and unusually concretely: the run identifies a real behavioral defect that follows directly from the bespoke implementation — selection isn't reset across sort/filter/pagination the way the docs require, meaning an operator could fire "Delete selected" against security groups no longer visible on screen. On a page whose entire purpose is bulk-deleting security groups, this is the kind of concrete, safety-relevant consequence an FDE restructures code over, not a stylistic preference.
7. **Genuinely component-level, not implementation-correctness or generic UX?** Yes — and this is the specific discipline the grading key calls out as the case's real hazard. The finding's boundary check states plainly: "not about whether the current checkboxes are individually well-built... a component-vocabulary question, not implementation correctness." The "Why it matters" section names missing free features (shift-click/shift-space range selection, `allItemsSelectionLabel`/`itemSelectionLabel`, `isItemDisabled`) as *evidence supporting the component-selection argument* (what native adoption gets you for free), not as an a11y/keyboard-mechanics critique of the existing raw checkboxes. This correctly avoids drifting into `cloudscape-implementation-audit`'s domain, which is exactly the failure mode the grading key warns is distinct from Case P1's.
8. **Duplicated across component+pattern?** No, cleanly typed `component selection`, standalone.
9. **Intent-dependent?** Not applicable here — correctly not invoked.

**Why an FDE would act on it:** it identifies a genuine, uncontroversial reimplementation of a first-class Cloudscape mechanism paired with a concrete correctness/safety consequence (stale selection surviving sort/filter/page changes) on a page whose sole purpose is bulk deletion — exactly the kind of finding that gets prioritized in a real review, not filed as a style note.

One caveat, not enough to move the grade: `isItemDisabled` is named as a "feature you get for free" but does not appear verbatim (or at all) in the specific Table guidelines page fetched in this session — it is a real, well-known Cloudscape `Table` prop consistent with the doc's own "Inactive items should not be selected" rule, but I could not independently confirm the prop name against the fetched material. It is not presented inside quotation marks as a literal citation, so this is a minor unverified-supporting-detail note, not a citation-fidelity violation.

---

## Finding 2 (run) — `ContentLayout` + `Table variant="container"` vs. `Table variant="full-page"` — corresponds to grading key **Candidate 1**

**Grade: A — material and strongly validated.**

Rubric walk-through:

1. **User task supported by evidence?** Yes — the file's own comment ("Nothing on the page besides the table") plus the fact that `ContentLayout`'s only child is a single `Table` is directly cited and verified accurate against the fixture (line range cited as 84–185 is off by one line at the tail — the actual closing sequence is `</ContentLayout>` / `);` / `};` around lines 184–186 — a trivial line-count imprecision, not a substantive error).
2. **Does the cited authority say what's claimed?** Yes. The table-view pattern's "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant..." and its "few columns" carve-out are both verbatim-exact against the live page. The Table docs' "Container" variant description is verbatim-exact. The "Full page" variant description is substantively accurate but has one non-verbatim trailing clause (see Citation Fidelity below).
3. **Four-point applicability test.** Task match: a dedicated, sole-purpose, full-page resource-inventory table — precisely the table-view pattern's stated problem, not a shape-only match. Current implementation solves the same problem via the explicitly discouraged `ContentLayout` + `container` composition. Native alternative (`full-page` variant, header moved into `Table`'s own header slot) preserves the identical task, columns, filter/sort/pagination, and even the same header content/actions. Materiality: this rests on a direct, explicit "Don't X, instead do Y" pairing — about as strong as this skill's evidence bar gets.
4. **Preserves task semantics?** Yes, explicitly and correctly argued — same columns, same actions, only page-structure changes.
5. **Could this be equally valid Cloudscape usage?** The run correctly engages the one documented escape hatch — the pattern's own "few columns" carve-out permitting `container` + `ContentLayout` — and reasons through it rather than ignoring it: 7 columns spanning text/id/two numeric counts/status/timestamp reads as "content-heavy," not "a few columns." The run honestly flags that no numeric threshold is documented and downgrades its own self-reported confidence to `medium` rather than overclaiming — this is appropriate epistemic discipline (rubric Q9's spirit, applied even outside a strict `intent-dependent` case), not a materiality-undermining hedge, since the finding still asserts `high` materiality and the applicability reasoning itself is sound and matches the grading key's own resolution of this carve-out almost exactly.
6. **Materiality — would an FDE act?** Yes — `REQUIRED`-strength "Don't...Instead" language is cited correctly and is about as material a signal as this skill's evidence discipline recognizes.
7. **Component/pattern-level, not implementation/UX?** Yes — boundary check is explicit and clean: "a judgment about which documented page-composition variant... matches the page's own stated shape... not a critique of how either variant is implemented... not a redesign."
8. **Duplicated across component+pattern?** No — correctly typed `combined component + pattern`, consistent with SKILL.md's own instruction that a single issue spanning both levels (a page-composition/variant choice) should be unified rather than artificially split into two findings.
9. **Intent-dependent?** Not applicable — correctly not invoked.

**Why an FDE would act on it:** the recommendation rests on the pattern page's own explicit "Don't...Instead" prohibition, preserves the exact same page and task, and names a concrete downstream cost (losing `contentType="table"` AppLayout space/behavior optimizations) — the kind of documented, low-risk-to-fix structural change a Cloudscape-fluent engineer would make on sight.

---

## Citation-Fidelity Section

All three cited cloudscape.design URLs were re-fetched live via `curl -s -A "Mozilla/5.0"` and returned substantive, real markdown content (not a client-rendered shell):

- `https://cloudscape.design/components/table/index.html.md` (1068 lines returned)
- `https://cloudscape.design/get-started/dev-guides/collection-hooks/index.html.md` (384 lines returned, including the exact worked example the run describes: `selection: {}` passed to `useCollection`, `selectionType="multi"` on `Table`, `collectionProps.selectedItems`, and the `` selectedItems.length ? `(${selectedItems.length}/${allItems.length})` : `(${allItems.length})` `` header-counter code — all confirmed present verbatim in the fetched page)
- `https://cloudscape.design/patterns/resource-management/view/table-view/index.html.md` (315 lines returned)

No fabricated URL, no dead link, no client-shell substitution.

Quote-by-quote verbatim check:

**Fully verbatim (exact match on the live page):**
- "The selection and sorting state of table component are controlled." + "For the selection state, set the `selectedItems` property and `onSelectionChange` event listener." — exact, adjacent sentences correctly ellipsis-joined.
- "Allows multiple items to be selected at a time by using checkboxes for each item." + "Use for collections that support bulk actions." — exact, two consecutive bullets under the same `Multi` heading, correctly ellipsis-joined.
- "When you are using collection hooks, make sure that the selection is also controlled by the hook." — exact.
- "Don't show the number of selected items if nothing has been selected." — exact.
- "Use the 'full-page' variant of the table component for this pattern." — exact.
- Both "Don't" bullets on `ContentLayout`/table-view (the explicit prohibition and the "few columns" carve-out) — exact, word-for-word.
- "This table variant has its own visual container with shadows and borders. Use this variant to feature a table in a stand-alone container with its own hierarchy. For example: when using a table on a details page." (Container variant) — exact.
- "Selection configuration. If you want to use the selection feature with default settings, provide an empty object." — exact.

**Minor, real fidelity defects (per the rubric's instruction to flag these separately from the materiality judgment):**

1. **Trimmed clause presented as continuous quotation.** The run's "Full page" variant quote ends: *"...Use this variant in conjunction with `contentType="table"` on the App Layout."* The live page actually says: *"Use this variant in conjunction with the `contentType="table"` property on the App Layout to maximize the available space."* The words "the," "property," and "to maximize the available space" were dropped without any ellipsis marking this specific trim (the run's ellipsis appears earlier, before this sentence, correctly marking a different omission — but this final clause is silently edited after that ellipsis). The substance is not inverted, but this is non-verbatim text inside quotation marks and should be flagged as an evidence-quality defect.
2. **Bulleted list reformatted into comma-separated prose inside quotation marks.** The run's Table-view "Selection - optional" quote renders the doc's four-item bulleted list ("- Table sorting / - Pagination / - Preferences / - And as soon as they are no longer visible on the page") as an inline sentence: *"Selection is overwritten by: Table sorting, Pagination, Preferences, and as soon as they are no longer visible on the page."* The words are all present and correct, but the format was silently converted from a list to prose while still enclosed in quotation marks — a second instance of the same category of defect as (1), lower severity since no wording was altered or dropped.
3. Similarly, in Finding 1's Table-docs quote, "reset item selection across pagination, sorting, filtering, page size changes... Always include the number of selected items in the header item counter" joins two adjacent, thematically identical bullets under the same "Selection" sub-heading in the "Do" list via ellipsis. This is the most defensible of the three instances (adjacent bullets, same topic, ellipsis present) and borders on acceptable convention rather than a defect, but is noted for completeness.

None of these three instances invert or fabricate what the cited material actually says, and none affects the underlying materiality/applicability judgment for either finding — per the rubric's explicit instruction, they are flagged here as evidence-quality defects but do not downgrade either finding's grade.

**Distractor check:** the grading key's own text misattributes a "place a table inside a container with other content, such as key-value pairs" quote to the "Container" variant — that sentence is actually documented under the **Borderless** variant, not Container. This is an error in the grading key's supporting citation, not in the run: the run's own "Container" quote is the correct, verbatim, live-page text for that heading. This does not affect grading the run and is noted only for completeness.

---

## Case-Level Verdict

**Both MUST-REPORT candidates were reported, as genuinely independent findings, with no folding and no crowding-out.**

- Candidate 1 (`ContentLayout`+`container` vs. `full-page`) appears as the run's **Finding 2**, fully argued on its own evidence and citations.
- Candidate 2 (hand-rolled checkboxes vs. `selectionType="multi"`) appears as the run's **Finding 1**, fully argued on its own evidence and citations, with a complete, independent Finding-contract block (Type, Materiality, Confidence, User task, Repository evidence, Cloudscape evidence, Applicability argument, Current/Native expression, Why it matters, Boundary check).
- Neither finding is a sub-clause of the other; neither references the other as a precondition for materiality. The only cross-reference is a *suppressed* item (the header counter format) that the run correctly identifies as a downstream symptom of Finding 1 rather than an independent third finding — this is proper materiality discipline, not folding of Candidate 1/2 into each other.
- The specific hazard this case is designed to catch — Finding 2 (checkbox selection) drifting into implementation-correctness/a11y-nitpick framing — did **not** occur. The boundary check and "Why it matters" section both stay on component-vocabulary ground and explicitly disclaim critiquing the checkboxes' individual construction.
- The tolerated, non-scoring `status`-column filter-mechanism distractor was **not** manufactured as a separate finding; the run's Orientation notes confirm `TextFilter` as native without singling out `status` for a select-based filter argument. Per the grading key this does not affect the verdict, but is noted as required.

**Overall: case-level match with designed intent — full, correctly-structured recall of both independent MUST-REPORT candidates, modulo the minor citation-fidelity defects noted above.**
