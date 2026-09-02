# Adversarial verification — Case P1 (MessageQueues.tsx), repeat run #2

**Review graded:** `evals/design-system-native-expression-review/runs-repeat/case-p1-skill.md`
**Grading key:** `evals/cloudscape-native-expression-review/grading/case-p1-message-queues.expected.md`
**Fixture:** `evals/cloudscape-native-expression-review/cases/case-p1-message-queues/fixture/src/pages/MessageQueues.tsx`
**Rubric:** `evals/cloudscape-native-expression-review/rubric.md`

All Cloudscape authority pages cited below were re-fetched live during this
verification pass (`curl` against the `.html.md` endpoints, not recalled from
training data): `patterns/resource-management/view/index.html.md`,
`.../view/table-view/index.html.md`, `.../view/card-view/index.html.md`,
`patterns/general/filter-patterns/index.html.md`,
`components/collection-select-filter/index.html.md`,
`components/cards/index.html.md`, `components/content-layout/index.html.md`,
`components/status-indicator/index.html.md`,
`components/pagination/index.html.md`. Every quotation below was checked
character-for-character against these fetched files, not against the
review's own transcription or my memory of the docs.

---

## Per-finding grading

### Finding 1 — Cards used for a 24-item comparison collection instead of Table
*(= grading key Candidate 1, MUST REPORT)*

- **Q1 (task supported by repo evidence):** Yes. The header `description`
  prop ("Compare message throughput and backlog age across queues to decide
  which need scaling attention.") and the file-header comment both state the
  comparison task directly. Not invented.
- **Q2 (authority says what's claimed):** Yes, verified live. `view.md`'s
  criteria table genuinely reads "9 or more resources in 99% of use cases"
  (Table) / "5 or less resources in 99% of use cases" (Card), and "Data that
  is displayed in columns (text, numerical, status, sparkline)" (Table) /
  "Data that can be displayed as visuals (charts, videos)" (Card). The
  sentence "Use a table if the resources share the same metadata, and your
  users will be comparing resources to determine which to take action on."
  is exact. `table-view.md`'s "The best data type for a table view is data
  that is structured, easily comparable, and sortable" is exact.
- **Q3 (four-point applicability test):** Passes. Both quantified criteria
  (24 items ≫ 9-item table threshold; all-columnar metadata, zero
  chart/image content) point the same direction, and the review correctly
  ties this to the page's own comparison-task language rather than a
  superficial pattern-exists match.
- **Q4 (preserves task semantics):** Yes — same four fields become columns,
  same items, same filter/pagination; no redesign.
- **Q5 (could current impl be equally valid?):** No — Cards fails both
  quantified thresholds outright; this isn't a coin flip.
- **Q6 (material to an FDE):** Yes — two independent, quantified criteria
  both clear their thresholds against this exact resource count and data
  shape.
- **Q7 (component/pattern-level, not implementation/UX):** Correctly scoped;
  boundary check is explicit and accurate.
- **Q8 (duplicated across component+pattern?):** No, correctly unified as one
  `combined selection + composition` finding.

**Grade: A.** Repository evidence checks out, authority genuinely says what's
claimed (two citation-fidelity nits below, not fabrications), applicability
test passes on all four points, task semantics preserved, clearly
component/pattern-level. An FDE surveying this page would plausibly swap
Cards for Table on this evidence alone.
**Case-level match:** matches designed intent (MUST REPORT candidate correctly reported, materiality/confidence appropriately high).

---

### Finding 2 — `ContentLayout` wrapping `Cards` instead of the pattern's `full-page` variant
*(= grading key's third, deliberately non-scoring ambiguity)*

- **Q2 (authority says what's claimed):** Yes, verified live —
  `card-view.md`'s "Don't" list reads verbatim: "Don't use the content
  layout component on this type of page. Instead, use the 'full-page'
  variant of the cards component to implement this pattern." The identical
  rule (with "table" substituted) is confirmed on `table-view.md`.
  `content-layout.md`'s "Provides page structure for expressive use cases."
  is exact.
- **Q9 (intent-dependent handling):** **Fails.** This file is a single
  bounded surface with no visible parent `AppLayout`/shell context. The
  grading key names this ambiguity explicitly and states the only
  unacceptable outcome is "reporting it as a confident, high-confidence
  violation-strength finding without naming the missing-context caveat."
  The review does exactly that: `Materiality: medium`, `Confidence: high`,
  `Authority strength: REQUIRED`, and nowhere does the applicability
  argument, "why it matters," or boundary check acknowledge that this
  single-file view cannot establish whether the page is a stand-alone
  top-level route or embedded in a larger shell that already resolves the
  chrome question. No hedge, no `intent-dependent` classification, no named
  caveat anywhere in the finding.

**Grade: D — overreach on genuinely missing intent.** The authority is
correctly quoted and the rule is real, but the finding asserts a confident,
required-strength violation without confronting the one piece of missing
context the grading key specifically calls out as needing acknowledgment.
This is not the case's central adjudication target, but it is exactly the
"real but separate missing-intent failure" the grading key names and asks
to be reported separately rather than folded into the Candidate 2 verdict.
**Case-level match:** does **not** match the tolerated outcomes (omitted /
named as suppressed-ambiguity / reported as `intent-dependent` with the
caveat) — this is the "confidently asserted without the caveat" outcome the
key marks unacceptable.

---

### Finding 3 — `TextFilter` alone vs. adding a collection select filter for `status`/`region`
*(= grading key Candidate 2, MUST SUPPRESS — the case's central adjudication target)*

- **Q2 (authority says what's claimed):** The individual quotes are real
  and verified verbatim (see citation table below): "If the common behavior
  of users is to filter a resource by only one or two properties, use the
  collection select filter," "A select filter helps users find specific
  items in a collection by choosing one or two properties," "Use a select
  filter if users need a maximum of two properties to find a specific item.
  If more than two are required, use a property filter instead," and "The
  collection is filtered as soon as the user selects a value from a select
  filter or enters text into the accompanying text filter" — all exact
  matches, live-verified.
- **Q3 / Q5 (applicability + could-current-be-equally-valid) — this is where
  the finding fails.** The review's own cited page, `filter-patterns.md`,
  carries a criteria table that the review **never quotes or engages with**:
  "Complexity of the resource | Simple resource (small set of properties)
  [Text filter] | Simple resource (small set of properties) [Collection
  select filter] | Complex resource (large set of properties) [Property
  filter]" — TextFilter and CollectionSelectFilter sit in the *identical*
  cell for this resource's complexity tier. The page distinguishes them only
  by *unresolved user goal* ("Find resources that match an exact text
  query" vs. "Find resources with overlapping, defined values"), a
  distinction this single-file fixture provides no evidence to resolve
  either way. The review's applicability argument (point 2) instead asserts
  the current `TextFilter` is only a "coincidental," "undiscoverable side
  effect, not a designed property filter" — i.e., it affirmatively argues
  the status quo is the *inferior*, accidental option, when the retrieved
  evidence places it as an equally-documented, deliberate fit for this exact
  complexity tier. Applicability point 4 asserts materiality ("an
  experienced Cloudscape implementer... would very likely add it") without
  ever confronting the same-tier equivalence its own cited criteria table
  establishes — this is precisely the SKILL.md anti-fundamentalism point 4
  failure the grading key names.
- **Q6 (material to an FDE):** The grading key is explicit that materiality
  is low here: no stated task friction (no comment/copy naming a filtering
  pain point — the fixture only asks for "narrow the list down to a specific
  status or region," which `TextFilter`'s cross-field substring match
  already fully services for two two-valued fields), and a working,
  doc-supported filter already exists. The review treats this as `high`
  materiality with `high` confidence — the opposite calibration the
  evidence supports.

**Grade: E — factually wrong / false underlying premise.** The individual
quotations are accurate, but the finding's central premise — that the
current `TextFilter`-only approach is a lesser, accidental fit that an
experienced implementer would restructure — is false on the review's own
cited authority: the filter-patterns criteria table documents `TextFilter`
as an equally correct, deliberate choice for this exact "simple resource"
complexity tier, not a coincidental one. This is rubric E's "the pattern
being rejected is actually documented as the correct fit ... or vice versa"
in its "vice versa" form: the option being downgraded (TextFilter) is
itself the one the docs treat as an equal, correct fit.

**Case-level match: FAILS.** This is the grading key's central adjudication
target, and the review reports it — unhedged, at `high`/`high`, as its own
freestanding Finding 3 (not folded into or hedged against Finding 1) — which
is the exact, disqualifying failure this case exists to detect. The
review does not append any "equally valid" self-acknowledgment to this
specific finding (it does correctly reason about equal-validity *elsewhere*,
in the Property-filter suppression bullet), so this is the plain unhedged
form of the failure rather than the "sharpest," self-contradicting form the
grading key describes as a variant — but the key is explicit that "any
response that reports this candidate — regardless of hedged confidence,
'medium' materiality" reproduces the failure. Reporting it at `high`/`high`
with an affirmative argument that the current approach is inferior is,
if anything, a more confident version of the disqualified failure, not a
lesser one.

---

## Suppressed section — spot check

- **Property filter suppression:** Correctly reasoned and consistent with
  live-verified text ("if more than two are required, use a property filter
  instead" — verbatim, minor lowercase edit to fit sentence flow, not a
  content change). Sound.
- **Card-view "Do" list per-resource details link:** Correctly classified
  `intent-dependent` with a named reason (no evidence of a details route in
  this bounded surface) — this is the correct handling pattern that Finding
  2 above should have used but didn't.
- **`CollectionPreferences` absence:** Correctly suppressed as an optional
  building block; not material to the core task. Sound.

The review demonstrably *knows how* to suppress on materiality/intent
grounds (it does so twice, correctly, in this section) — which sharpens
rather than excuses the failure to apply the same discipline to Finding 3.

---

## Citation-integrity table

| # | Quoted text (as it appears in review) | Cited source | Live-verified? | Verdict |
|---|---|---|---|---|
| 1 | "Number of resources in the data set \| 9 or more resources in 99% of use cases **[Table]** \| 5 or less resources in 99% of use cases **[Card]**" | `view.md` criteria table | Core values match exactly; bracketed `[Table]`/`[Card]` labels are the review's own addition, not literal source text | **Reformatted/embellished** — not strictly verbatim, but not a content distortion |
| 2 | "Metadata type \| Data that is displayed in columns (text, numerical, status, sparkline) **[Table]** \| Data that can be displayed as visuals (charts, videos) **[Card]**" | `view.md` criteria table | Same as above | **Reformatted/embellished** |
| 3 | "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on." | `view.md` | Exact match, `view.md` line 57 | **Verbatim, correct** |
| 4 | "The best data type for a table view is data that is structured, easily comparable, and sortable" | `table-view.md` | Exact match, line 193 | **Verbatim, correct** |
| 5 | "Tables enable users to quickly scan and sort columns, to compare metadata across many resources." | cited as `table-view.md` | Text is exact, **but it lives on `view.md` (the "View resources" page), not `table-view.md`** | **Verbatim text, misattributed source page** |
| 6 | "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." | `card-view.md` | Exact match, line 97 | **Verbatim, correct** |
| 7 | ContentLayout: "page structure for expressive use cases" | `content-layout.md` | Exact match, line 3 | **Verbatim, correct** |
| 8 | Cards `variant` "accepts exactly `\"container\" \| \"full-page\"`" | `cards.md` API | Not a literal doc quote (code-style paraphrase of documented variant behavior); substantively accurate — default renders header-in-container, "full-page" is the documented alternate | **Accurate paraphrase, not a verbatim claim** |
| 9 | "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter." | `filter-patterns.md` | Exact match, line 46 | **Verbatim, correct** |
| 10 | "A select filter helps users find specific items in a collection by choosing one or two properties" | `collection-select-filter.md` | Exact match, line 3 | **Verbatim, correct** |
| 11 | "Use a select filter if users need a maximum of two properties to find a specific item. If more than two are required, use a property filter instead" | `collection-select-filter.md` | Exact match, line 47 | **Verbatim, correct** |
| 12 | "The collection is filtered as soon as the user selects a value from a select filter or enters text into the accompanying text filter" | `collection-select-filter.md` | Exact match, line 30 | **Verbatim, correct** |
| 13 | (Suppressed section) "if more than two are required, use a property filter instead" | `collection-select-filter.md` | Exact match aside from sentence-initial capitalization lowered to fit embedding ("If" → "if") | **Verbatim, correct (trivial capitalization convention)** |
| 14 | StatusIndicator: "in a compact form that is easily embedded in a card, table, list, or header view." | `status-indicator.md` | Exact match, line 3 | **Verbatim, correct** |
| 15 | Pagination: "Pagination helps users with an extensive number of resources to navigate through them across multiple pages." | not URL-pinned; "documented building block" | Exact match, `table-view.md`/`card-view.md` (identical text both places) | **Verbatim, correct** |

**No fabricated or semantically-inverted quotations were found.** Every
quoted string traces to real Cloudscape prose. The defects found are: two
instances of a criteria table re-rendered with added interpretive bracket
labels not present in the source (cosmetic, content-preserving), and one
instance of a genuinely verbatim sentence attributed to the wrong page
(`table-view.md` cited, `view.md` actual). Neither defect changes any
finding's substance, but per the task brief these are graded separately
from — not folded into — the materiality verdicts above, and the citation
labeled "VERBATIM" should not be read as "these five words guarantee
correct sourcing" without the caveats noted.

---

## Fixture line-citation spot check

Per the task's instruction not to trust the review's line citations blindly:
QUEUES array (18–25), `sorting: {}` (line 41), `MessageQueue` interface
(9–16), and the `TextFilter`-only filter slot (89–95) all check out exactly
against the fixture. Two citations are loose but not substantively
misleading: "`<ContentLayout>` (lines 44–55)" actually opens at line 45
(line 44 is `return (`) and the element doesn't close until line 99 (the
cited range only covers the opening tag through the `Header` prop, not the
full element with `Cards` nested inside it through line 98); Finding 2's
compressed pseudo-code rendering similarly implies `<Cards .../>` and
`</ContentLayout>` sit near line 55 when they are actually at 56 and 99
respectively. These are off-by-a-few-lines looseness in a paraphrased JSX
sketch, not fabricated code, and don't affect any finding's correctness.

---

## Summary table

| Finding | Grade | Case-level match? | Core issue |
|---|---|---|---|
| 1. Cards→Table | A | Matches (Candidate 1 correctly reported, high/high) | None — well-evidenced, applicability test passes cleanly |
| 2. ContentLayout vs. full-page variant | D | Does not match tolerated outcomes | Confident, required-strength finding with no missing-context caveat on a deliberately ambiguous, single-surface question |
| 3. TextFilter vs. CollectionSelectFilter | E | **FAILS — central adjudication target reported, not suppressed** | Ignores/fails to confront the filter-patterns criteria table's same-tier equivalence; asserts the status quo is an accidental, inferior fit when the docs treat it as an equally deliberate one |

---

## Case-level verdict

**YES — this repeat run reproduces the "equally-valid candidate reported
instead of suppressed" failure.**

Finding 3 of this review is the grading key's Candidate 2 — `TextFilter`
alone vs. adding a `CollectionSelectFilter` for `status`/`region` — reported
as a standalone, unhedged finding at `Materiality: high` / `Confidence:
high`. The grading key states unambiguously: "Any response that reports
this candidate — regardless of hedged confidence, 'medium' materiality, or
an explicit self-acknowledgment that the current implementation is 'equally
valid' — reproduces the exact A1 Finding 2 failure this case exists to
detect." This review's version is not even hedged — it argues affirmatively
that the current `TextFilter` implementation is a coincidental, inferior fit,
without ever engaging the filter-patterns page's own criteria table, which
the review itself does not quote, placing `TextFilter` and
`CollectionSelectFilter` in the identical "Simple resource" cell. That is a
confident overreach on exactly the axis the case was built to probe, not a
borderline or partially-mitigated case.

This happened despite the review correctly reporting the real primary
finding (Candidate 1, Cards→Table, Grade A) and despite the review
demonstrating, twice, in its own Suppressed section, that it is capable of
applying the correct equal-validity/intent-dependent suppression logic. The
skill's materiality/anti-fundamentalism discipline was applied inconsistently
within the same run — engaged for the property filter and the
card-linking question, but not for the structurally identical
TextFilter-vs-CollectionSelectFilter question the case was designed around.

Separately, and not to be conflated with the Candidate 2 verdict per the
grading key's own instruction: Finding 2 (`ContentLayout`/`full-page`)
also fails, independently, by asserting a confident `REQUIRED`-strength
violation without naming the single-file missing-shell-context caveat the
key explicitly tolerates as ambiguous. This is a second, distinct
missing-intent defect in the same run, not a restatement of the Candidate 2
failure.

**Net: 1 of 2 scored candidates handled correctly (Candidate 1), the central
adjudication target (Candidate 2) failed, and the tolerated third ambiguity
was also handled in the disallowed way.** This run does not clear the bar
the case was designed to test.
