# Adversarial Verification: Case B — EndpointScaling.tsx (fleet cards)

Verifier grading `evals/design-system-native-expression-review/runs/case-b-skill.md` against
`evals/cloudscape-native-expression-review/rubric.md` (nine questions, applied with "Cloudscape"
read as "the design system under review") and the designed intent in
`evals/cloudscape-native-expression-review/grading/case-b-fleet-cards.expected.md`.

All cited Cloudscape pages were fetched live (WebFetch, cloudscape.design) on 2026-09-02 and
checked against every VERBATIM-quoted string in the review. Fixture claims were checked directly
against `EndpointScaling.tsx`.

---

## Finding 1 — Cards → Table (component selection)

**Grade: A**

### Nine questions

1. **Repo evidence supported, not invented.** Confirmed against the fixture: 22-item `ENDPOINTS`
   array, identical shape (`id, region, status, invocationsPerMin, latencyP99Ms, errorRatePct`)
   (line 17), `Cards` with `cardDefinition.sections` exposing all five fields plus an action
   (lines 46-87), `cardsPerRow` capped at 3 columns at any viewport (line 86), and the header
   `description` quoted exactly as it appears at line 40 ("Compare request volume, latency, and
   error rate across endpoints to decide which ones need to scale."). All accurate.
2. **Cited authority genuinely says what's claimed — for the load-bearing citation, yes; for one
   corroborating citation, no (fabricated — see Citation Integrity below).** The View Resources
   decision table and "Use a table if the resources share the same metadata, and your users will
   be comparing resources to determine which to take action on" sentence are both confirmed
   verbatim and are, by themselves, fully sufficient to support the applicability argument.
3. **Four-point applicability test passes cleanly.** Task match, same-problem-today, task
   preservation, and materiality (22 vs. documented "9 or more" table threshold and "5 or less"
   card threshold; uniform shared metadata; all-columnar data types) are all addressed explicitly
   and correctly, not merely asserted.
4. **Native expression preserves task semantics.** Table changes scan structure only — same data,
   same per-row action, same operator decision.
5. **No documented reason the current Cards usage is equally valid here** — the decision table's
   three factors (size, metadata sharing, data type) unanimously favor Table; correctly ruled out.
6. **Materiality is real.** An FDE would plausibly restructure this; it matches the case's designed
   intent almost exactly, including the specific "why it matters" framing (re-scanning cards vs.
   sorting a column).
7. **Correctly scoped to component selection**, not implementation or generic UX — boundary check
   is honest and accurate. Minor imprecision: the finding is typed `combined selection +
   composition`, but nothing inside Finding 1 itself argues a distinct *composition*-level claim
   (the composition-level material lives entirely in Finding 2). The grading key explicitly flags
   this exact mislabeling risk and recommends the cleaner label `component selection` for this
   case. Not disqualifying, but worth correcting.
8. Not applicable — no duplicated component/pattern split within this finding.
9. Not applicable — not `intent-dependent`.

### Why an FDE would plausibly act on it

The page's own header copy states the comparison task in the design system's own decision-table
language for Table ("comparing resources to determine which to take action on"), the dataset size
and metadata uniformity trip every documented Table criterion and fail every documented Card
criterion simultaneously, and the fix is a like-for-like component swap that changes nothing about
what data is shown or what action is taken.

### Case-B match

Yes — this is essentially the designed-intent answer: right conclusion, right primary citation, a
correctly-executed four-point applicability argument, and a concrete "why it matters" (sort once
vs. rescan every card).

---

## Finding 2 — ContentLayout + Cards → Cards `variant="full-page"` (documented composition)

**Grade: C**

### Nine questions

1. **Repo evidence supported.** `ContentLayout` wraps `Cards` as sole content (lines 35-45, 89);
   no `variant` prop is passed, so it defaults to `"container"`. Accurate.
2. **Cited authority genuinely says what's claimed — confirmed clean, no fabrication found here**
   (see Citation Integrity below). Both the "Don't use the content layout component... Instead,
   use the 'full-page' variant" pairing and "Card collection should not be used for page layout
   purposes" are verbatim-confirmed on the Card view pattern page, and the `variant` prop's
   `"full-page"` description ("Use this variant when cards are the entire content of a page") is
   verbatim-confirmed on the Cards component page.
3. **Applicability test is procedurally addressed**, but rests on a premise the report's own
   Finding 1 undermines: the "Don't" rule cited here is scoped specifically to *Card view* pages.
   If Finding 1 (Cards → Table) is adopted — which this same report argues for at high
   materiality/high confidence — this page is no longer a Card view page at all, and no
   equivalent "don't wrap Table in ContentLayout" prohibition was found or claimed. The finding
   itself concedes this in its own "Why it matters" paragraph but does not adjust materiality
   downward in response.
4. Native expression (drop `ContentLayout`, use `Cards variant="full-page"`) does preserve task
   semantics **if Cards remains the chosen component** — but that "if" is exactly what Finding 1
   argues against.
5. **No documented reason the current composition is equally valid** — genuinely a real,
   explicit, REQUIRED-strength documented violation, taken in isolation.
6. **Materiality is the weak point.** Would an FDE reading this report *and* Finding 1 restructure
   the code because of Finding 2? Only by first rejecting Finding 1. Since Finding 1 is the
   stronger, better-supported, higher-priority recommendation in the same report, a rational
   reader adopts it and Finding 2's fix becomes moot before it's ever applied. Reporting this at
   `materiality: high` alongside Finding 1, rather than as contingent/subordinate or suppressing
   it, overstates its practical value in the context of this specific report.
7. Correctly scoped to composition (page-wrapper choice), not implementation or UX, in isolation.
8. Not a level-duplication of Finding 1 (different underlying issue: page-layout wrapper vs.
   collection-display component) — so Q8 doesn't disqualify it directly, but the interaction
   between the two findings is exactly the kind of scenario the "prefer one to three strong
   findings" materiality discipline exists to catch before publication.
9. Not applicable — not `intent-dependent`.

### Verdict

Real, citation-accurate finding, correctly reasoned *in isolation*, but its materiality is
substantially undercut by the report's own higher-priority Finding 1 — the review notices this
tension explicitly but doesn't act on it (no materiality downgrade, no explicit "contingent on
Finding 1 not being adopted" framing, no suppression). This is the kind of finding the skill's own
"prefer one to three strong findings over exhaustive commentary" / high-materiality-bar guidance is
meant to catch before it reaches the report. Graded C: technically plausible and correctly cited,
but not the kind of thing that should move an FDE's actual decision in a report that also contains
Finding 1.

### Case-B match

Not designed in — the grading key's "correct response" is explicitly **one** material finding
(the Table/Cards component-selection call). Finding 2 is not wrong on its citations, but its
presence, at equal high-materiality billing, is an over-report the case's designed intent did not
anticipate and the skill's own materiality discipline should have suppressed or demoted.

---

## Suppressed item — "multi-select + bulk global action"

Correctly suppressed. The review's own reasoning (introducing multi-select bulk scaling would
change the interaction model — act on N endpoints at once — rather than natively re-express the
existing single-endpoint "Scale up" task) is exactly the product-redesign scope boundary the skill
defines. No grade needed; this is a good call and matches the skill's discipline.

## Orientation notes

All three checked and confirmed accurate:

- `StatusIndicator` quote — "easily embedded in a card, table, list, or header view" — confirmed
  verbatim against the StatusIndicator component page.
- "Global actions (buttons) should be included in the header, not in each card." — confirmed
  verbatim against the Card view pattern page, and correctly applied (per-resource "Scale up" is
  not a global action, so this rule doesn't indict the current design).
- `Header` composition note is a reasonable, low-stakes affirmative call; nothing to verify beyond
  what's visible in the fixture, which matches.

---

## Citation Integrity (independent of letter grades)

Every VERBATIM-tagged quote in the review was checked against the live cloudscape.design page it
cites. No SYNTHESIS-tagged claims appear in this review (both findings self-label VERBATIM, not
SYNTHESIS), and no PARAPHRASE/INFERRED claims are dressed in quotation marks.

**Confirmed accurate (copy/paste-verifiable), Finding 1:**
- View Resources decision table (all three rows/columns) — confirmed on
  `.../patterns/resource-management/view/index.html.md`.
- "Use a table if the resources share the same metadata, and your users will be comparing
  resources to determine which to take action on." — confirmed verbatim, same page.
- Table view: "It's effective for quickly identifying categories or comparing values in a large
  text and numerical data set." — confirmed verbatim on `.../table-view/index.html.md`.
- Card view: "Use cards to display non-columnar, yet comparable data." — confirmed verbatim.
- Card view: "Surface only relevant and repeatable information across resources. Treat it as a
  quick reference for each resource." — confirmed verbatim, both sentences, same page.

**FABRICATED — Finding 1, Authority evidence:**
- The review attributes to the **Table view** page: *"Table columns allow for the same metadata
  type to be displayed across all resources, and allow for easy scanning and comparison of similar
  metadata."* Independent verification found **no occurrence of the word "metadata" anywhere on
  the Table view page** (`.../table-view/index.html.md`) — confirmed by two separate targeted
  fetches, one of which explicitly enumerated every sentence containing "metadata" or "sort" and
  returned zero "metadata" hits. This quote does not exist on the cited page. It is presented
  inside a bullet explicitly labeled `Evidence mode: VERBATIM`, in quotation marks, which per
  SKILL.md's Finding contract is reserved for text that "must be copy/paste-verifiable against
  that source." **This is a fabricated citation.**

**FABRICATED/CONFLATED — Finding 1, Native expression:**
- The review writes: "the docs note multi-column sort is meant for 'analyz[ing] data across
  multiple dimensions simultaneously'" (quotation marks in the original, with a bracket-edited verb
  form signaling an attempted direct quote). The actual Table view page contains two *separate*
  sentences: "Multi-column sort is useful when users need to analyze multi-dimensional data." and,
  elsewhere, "Table view of all user resources sorted by multiple columns simultaneously with
  explicit priority ordering." The phrase "across multiple dimensions simultaneously" is not a
  verbatim or near-verbatim rendering of either sentence — it is a conflation of "multi-dimensional
  data" from one sentence and "simultaneously" from an unrelated sentence about sort-priority
  ordering, stitched into a new phrase and presented with quotation marks. **This is a fabricated/
  conflated citation** dressed as verbatim.

**Confirmed accurate, Finding 2:**
- "Don't use the content layout component on this type of page. Instead, use the 'full-page'
  variant of the cards component to implement this pattern." — confirmed verbatim on the Card
  view pattern page (curly vs. straight quotes around "full-page" is a formatting non-issue, not a
  substance issue).
- "Card collection should not be used for page layout purposes." — confirmed verbatim, same page.
- Cards `variant` prop: allowed values `"container" | "full-page"`, and "Use this variant when
  cards are the entire content of a page." — confirmed verbatim (quoted as a fragment, matches
  substring exactly) on the Cards component reference.

**Confirmed accurate, Orientation notes:**
- StatusIndicator "easily embedded in a card, table, list, or header view" — confirmed verbatim.
- "Global actions (buttons) should be included in the header, not in each card." — confirmed
  verbatim (same string also independently verified for Finding 2's context).

### Summary of citation-integrity failures

Two fabricated/conflated quotes, **both inside Finding 1**, both self-labeled `VERBATIM`:

1. A quote about "table columns... same metadata type... easy scanning and comparison of similar
   metadata" attributed to the Table view page — that page contains no occurrence of "metadata" at
   all. Fabricated.
2. A quote about multi-column sort "analyz[ing] data across multiple dimensions simultaneously" —
   assembled by conflating two unrelated sentences on the Table view page into a phrase neither
   sentence contains. Fabricated/conflated.

Neither fabrication is load-bearing: Finding 1's applicability argument stands fully on the
independently-verified View Resources decision table and its "Use a table if..." sentence, which
alone satisfy the four-point applicability test. But both fabrications sit inside a bullet
explicitly marked `VERBATIM`, which the skill's own Finding contract defines as requiring the text
to be "copy/paste-verifiable against that source" — this is exactly the failure mode
(`design-system-native-expression-review`'s lineage notes) this skill's evidence-mode discipline
was built specifically to eliminate relative to its Cloudscape-only predecessor. Its presence here,
even in non-load-bearing corroborating bullets, is a real regression against that stated design
goal and should be corrected before this review is trusted as a citation-integrity exemplar.

Finding 2 and the Orientation notes are citation-clean — every VERBATIM string checked was found
exactly as quoted.

---

## Case-level verdict

**Partial match to designed intent.**

- The core, intended finding — Cards should be Table, because the task is explicit multi-metric
  comparison across 22 uniform resources and the design system's own View Resources decision table
  unanimously says so — was correctly identified, correctly argued through the four-point
  applicability test, and matches the grading key's "what a correct response looks like" almost
  point for point (decision-table citation, applicability reasoning on task/size/metadata-type,
  sortable-column native expression, correct boundary check). This is the behavior the case was
  designed to elicit, and the review produced it.
- Two things keep this from a clean match: (a) Finding 1's Type label (`combined selection +
  composition`) is imprecise in exactly the way the grading key warned against — the grading key's
  preferred label is plain `component selection`, since nothing in Finding 1 argues a genuine
  composition-level claim; and (b) the review over-reported by adding Finding 2, a citation-
  accurate but practically-moot second finding whose own stated rationale is undercut by Finding
  1's adoption — a case the designed intent did not call for and the skill's materiality
  discipline should have suppressed or demoted rather than reported at equal high materiality.
- Independently, two fabricated/conflated VERBATIM citations were found inside Finding 1's
  corroborating evidence (see above) — not load-bearing for the core conclusion, but a real
  citation-integrity failure in a review this skill is specifically designed to keep clean.

Net: the review reached the right primary conclusion for the right core reasons, but did not fully
match the designed intent's shape (over-reported a second, contingent finding; imprecise type
label) and contains citation fabrication that a stricter, citation-first read should not let pass
uncorrected.
