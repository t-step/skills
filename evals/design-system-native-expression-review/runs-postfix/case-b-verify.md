# Verification report — Case B: EndpointScaling.tsx (`case-b-skill.md`)

Verifier: fresh adversarial pass. Method per rubric: re-read review, grading
key, rubric, and fixture source directly; live-fetched every cited
`cloudscape.design` page over the network and checked quotations
character-for-character against the fetched text (not against the review's
own transcription or memory).

## Sources fetched (live, this session)

- `https://cloudscape.design/patterns/resource-management/view/index.html.md` ("View resources")
- `https://cloudscape.design/patterns/resource-management/view/table-view/index.html.md` ("Table view")
- `https://cloudscape.design/patterns/resource-management/view/card-view/index.html.md` ("Card view")
- `https://cloudscape.design/components/cards/index.html.json` (Cards component API)

## Citation-integrity table

| # | Quoted string in review | Cited page | Fetched-page match | Verdict |
|---|---|---|---|---|
| 1 | "9 or more resources in 99% of use cases" | `view/index.html.md` | Exact, table cell | Verified |
| 2 | "Shared metadata between resources" | `view/index.html.md` | Exact, table cell | Verified |
| 3 | "Data that is displayed in columns (text, numerical, status, sparkline)" | `view/index.html.md` | Exact, table cell | Verified |
| 4 | "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on. Use the card view if users will not be comparing between a large number of resources to determine which to take action on." | `view/index.html.md` | Exact, full sentence | Verified |
| 5 | "5 or less resources in 99% of use cases" | `view/index.html.md` | Exact, table cell | Verified |
| 6 | "Different metadata across resources" | `view/index.html.md` | Exact substring (full cell also has a parenthetical example, correctly not claimed) | Verified |
| 7 | "displayed as visuals (charts, videos)" | `view/index.html.md` | Exact substring of "Data that can be displayed as visuals (charts, videos)" | Verified |
| 8 | "Use table view pattern for static data with multiple attributes displayed in a tabular format." | `table-view/index.html.md`, "Do" | Exact | Verified |
| 9 | "The best data type for a table view is data that is structured, easily comparable, and sortable." | `table-view/index.html.md`, "Do" | Exact | Verified |
| 10 | "Restrain from incorporating graphics in tables. For data sets with a blend of text, images, and data visualizations... refer to the cards view pattern" | `table-view/index.html.md`, "Do" | Actual text reads "...or content with mixed formatting, refer to the cards view pattern." Review substitutes an ellipsis for "or content with mixed formatting" | **Drifted (ellipsis elision), not fabricated** — content preserved, correctly attributed, not misleading |
| 11 | "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." (marked VERBATIM) | `card-view/index.html.md`, "Don't" | Exact (source uses curly/double quotes around "full-page"; review normalizes to single quotes — cosmetic only) | Verified |
| 12 | Same rule "substituting 'table' for 'cards'" in `table-view/index.html.md` | `table-view/index.html.md`, "Don't" | Confirmed: "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern." | Verified |
| 13 | Cards `variant` default `'container'`; `'full-page'` — "Use this variant when cards are the entire content of a page." | `components/cards/index.html.json` | Exact — `defaultValue: "'container'"`, description contains that exact clause verbatim | Verified |

**No misattribution found** — every quote traces to the specific page claimed (Card view content stays in `card-view/index.html.md`, Table view content in `table-view/index.html.md`, the decision table only in `view/index.html.md`); none is borrowed from a similarly-named neighboring page. Only one drift (#10), and it is a disclosed-by-ellipsis elision that preserves meaning, not a fabrication or misquote. This finding's Evidence mode was tagged SYNTHESIS, not VERBATIM, so the elision doesn't breach the review's own verbatim-accuracy claim; the two strings explicitly tagged VERBATIM (#11, #12) both check out exactly.

## Repository-evidence spot check (against the actual fixture, not the review's line numbers alone)

- Line 17 `Array.from({ length: 22 }, ...)`, line 35 `<ContentLayout`, line 46 `<Cards`, `cardDefinition.sections` lines 51–84, `cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }, { minWidth: 900, cards: 3 }]}` on line 86, closing `/>` on line 88 — all confirmed against the fixture as read directly. Per-section line ranges (status 53–55, region 56–60, invocations 61–65, latency 66–70, errorRate 71–75, actions 76–83) are all accurate to within a line of the section's opening/closing brace — no fabricated evidence.
- Confirmed: no `ariaLabels` prop anywhere in the fixture's `Cards` instantiation. (Aside, not a review defect: the grading key's "Designed intent" section asserts "`ariaLabels` ... present and well-formed," which does not match the actual fixture. The review does not repeat this claim and correctly places accessibility mechanics in "What was not evaluated," so this is a grading-key inaccuracy, not a review error.)

## Per-finding grades

### Finding 1 — Cards used for a 22-item comparison task vs. documented Table view

- **Type as labeled:** `combined selection + composition`. **Grade: A.**
- Q1 (task grounded): Yes — quotes the page's own header `description` and an in-code comment verbatim; both independently confirmed present in the fixture (line 40 description, lines 29–33 comment).
- Q2 (authority says what's claimed): Yes — all 10 quotations above (#1–10) check out against the live pages.
- Q3 (four-point applicability test): Passes on all three documented axes simultaneously — item count (22 vs. "9 or more" / "5 or less" thresholds), shared metadata (five identical fields across all 22 items, confirmed in fixture), and metadata type (columnar text/numeric/status, no images/charts). The review explicitly computes the multiples (2.4x / 4x) rather than gesturing at the thresholds, which is stronger than the bare minimum the grading key asks for.
- Q4 (task semantics preserved): Yes — native expression keeps the same fields, same per-item "Scale up" action, same header/counter; explicitly cites the Table pattern's own "Actions in table cells" building block, which is a real, verified subsection of `table-view/index.html.md`.
- Q5 (could current impl be equally valid?): The review considered and rejected the plausible alternate reading (region-based grouping) in the Suppressed section, with a concrete reason (fixture assigns `region` cyclically via `i % 4`, no product signal) — this is exactly the discipline the grading key's "What would be wrong" section is checking for negatively (i.e., the review does *not* commit the "existence treated as mandate" failure).
- Q6 (materiality): High and well-argued, not asserted.
- Q7 (stays in scope): Yes — explicitly separates this from implementation correctness (`cardsPerRow` breakpoints, `Box float="right"`, a11y) in "What was not evaluated."
- Q9 (n/a — not intent-dependent, correctly not classified as such).
- **Type-label note:** the grading key's preferred label is plain `component selection`, and flags "framed as `pattern composition` instead" as a tolerated-but-suboptimal outcome. The review's actual label, `combined selection + composition`, is a defined type in this skill's own Finding contract ("Use combined when the component-level and composition-level observations are genuinely one underlying issue") — and is arguably *more* defensible here than a plain `pattern composition` mislabel would have been, since the cited authority itself frames Card view vs. Table view as a choice between two named, composition-tier patterns, not just two raw components. This is the tolerated ambiguity the key already anticipates ("not wrong enough to fail the case, but worth noting"), not a new failure mode.
- **Why an FDE would act on it:** the page's own copy states the comparison task explicitly, the cited decision table is directive on all three independent axes, and Cards structurally cannot sort by the very metrics the page asks the operator to compare — this is a concrete, citable, high-confidence rationale, not a preference.

**Case-match verdict for the designed finding: MATCH.** This is very close to word-for-word what the grading key specifies as "what a correct response looks like" — same authority quotes, same three-pronged applicability argument, same Table-with-sortable-columns native expression, same "Cards forces re-scanning" argument (review: "Cards' inability to sort... actively works against the page's own stated triage purpose"), same boundary-check framing.

### Finding 2 — `ContentLayout` (default `container` variant) instead of the pattern's full-page variant

- **Type as labeled:** `documented composition`. **Grade: C.**
- Q1–Q2: Fully grounded — code evidence (line 35 `ContentLayout`, line 46 `Cards` with no `variant` prop) and authority citations (#11, #12, #13 above) are all accurate and correctly attributed, including the REQUIRED-strength "Don't... Instead" language and the Cards component API default.
- Q3 (applicability): Technically passes the four-point test in isolation — this page's entire content is a resource collection, matching the "on this type of page" scope of the Don't rule.
- Q5 (could current impl be equally valid?): This is where the finding runs into the grading key directly. The key's **Designed intent** section states explicitly: *"The page composition around it (`ContentLayout` + `Header` with a task-describing `description`) is ordinary and not itself a finding."* The key was authored with the deliberate intent that this exact composition — `ContentLayout` wrapping a default-variant collection component — is *not* meant to register as a reportable issue in this case, i.e., the case designer treats it as within the range of "equally valid/ordinary" usage for grading purposes, notwithstanding the literal Don't-rule text.
- Q6 (materiality): This is the crux. The citation is real and REQUIRED-strength, but it is a page-chrome/consistency concern (padding, header treatment), not something that changes what the operator can see or do — unlike Finding 1, it doesn't restore lost functionality (sorting). The grading key's characterization ("ordinary") signals the case designer judged this below the bar an experienced FDE would restructure code for on its own.
- **Verdict:** Grade C — "technically plausible but routine/low-value... expected to be suppressed by the skill's own materiality discipline, not a verifier failure" is the rubric bucket that fits best. This is not a D/E: the citation is accurate, correctly attributed, and the applicability argument isn't hollow — but it directly contradicts the grading key's explicit "not itself a finding" framing for this composition, which the key writes with unusual specificity (naming `ContentLayout` + `Header` + `description` together). Reporting it as a second full finding (with `Materiality: high`, matching Finding 1's own materiality label) overstates it relative to the case's designed intent.

## Case-level verdict

**Partial match.** The single designed finding (Cards vs. Table, component/pattern selection) is present, well-evidenced, and argued essentially the way the grading key describes — this half of the case is a clean A. However, the review adds a second full finding (`ContentLayout` variant) that the grading key's own "Designed intent" section explicitly pre-empts as "ordinary and not itself a finding." That second finding is not fabricated or misattributed — every quote and code citation checks out — but its inclusion, at `Materiality: high` alongside the primary finding, is a real deviation from the case's designed scope: exactly one material finding was intended, and the run reported two.

Net effect for a reviewer relying on this run: the actionable, high-value recommendation (switch to Table) survives adversarial verification intact. The second finding adds a lower-value item that the case designer judged should have been suppressed by the skill's own materiality discipline — a soft over-production issue, not a correctness or evidence-fabrication issue.

## Summary table

| Finding | Type label | Grade | Case-key match |
|---|---|---|---|
| 1 — Cards vs. Table view | `combined selection + composition` | **A** | Match (label deviation tolerated per key's own caveat) |
| 2 — `ContentLayout` vs. full-page variant | `documented composition` | **C** | Mismatch — key explicitly designates this composition "not itself a finding"; over-produced relative to designed scope |

Overall case-level result: **primary designed finding correctly surfaced (A); one extra, well-cited but low-materiality/undesigned finding also surfaced (C), constituting a partial mismatch with the grading key's single-finding intent.**
