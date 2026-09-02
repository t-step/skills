# Adversarial verification — Case P1 (MessageQueues.tsx), review `case-p1-v3-skill.md`

**Verifier scope:** review under test, grading key, rubric, live fixture, live-fetched
Cloudscape source pages. No prior conversation context assumed.

## 0. Overall case-level verdict

**FAIL**, per the grading key's own explicit, non-negotiable bar.

Finding 2 in the review ("No dedicated control for the page's own stated 'narrow by
status or region' task; TextFilter alone doesn't natively cover it") **is** the grading
key's Candidate 2 (`TextFilter` alone vs. adding a `status`/`region` collection select
filter). The review reports it as a full Finding — Materiality: medium, Confidence:
high, with a "Why it matters" and a "Native expression" recommending the code be
changed. The grading key states without qualification:

> "Any response that reports this candidate — regardless of hedged confidence, 'medium'
> materiality, or an explicit self-acknowledgment that the current implementation is
> 'equally valid' — reproduces the exact A1 Finding 2 failure this case exists to
> detect."

The review clears the recall requirement (Candidate 1 / Finding 1 is present, well
supported — see below), and its citation fidelity is excellent throughout. But because
the disqualifying condition ("reports Candidate 2 at any confidence level") is met, the
case is a fail regardless of argument quality. See §4 for why the review's argument is
nonetheless the strongest defensible version of this failure mode, and §5 for a specific
problem I found in the grading key's own stated rationale that does not change this
verdict but should be corrected.

## 1. Per-finding grade table

| Finding | Rubric grade | Case-level match vs. grading key | Key driver |
|---|---|---|---|
| Finding 1 — Cards+ContentLayout vs. full-page Table | **A** | MATCH (Candidate 1, MUST REPORT) | Q1 (task from verbatim `Header description`), Q2/Q3 (all cited criteria confirmed live, both quantified rows point the same direction, no equalizing row), Q4 (Table preserves the same 4-column comparison task), Q5 (three independent "Don't use ContentLayout" rules rule out "equally valid"), Q6 (24 items, shared metadata, purely columnar — an FDE would act), Q8 (correctly unified as one `combined selection + composition` finding rather than split across component/pattern levels) |
| Finding 2 — TextFilter alone vs. add CollectionSelectFilter for status/region | **D** | MISMATCH (this is Candidate 2, MUST SUPPRESS) | Q5 fails: the review's own applicability argument concedes the narrowing goal is "today... reachable as a side effect of TextFilter's whole-item substring match" — i.e., it names the current implementation as already functionally adequate, then recommends restructuring anyway. Q6 fails: 2-value enums, 24 items, no stated friction/pain point, criteria table ties both filters on "Complexity of the resource" (both "Simple resource"). Q3 is weak: the differentiation the review leans on ("User goals" row) is real, but doesn't establish that the *current single control* fails the task, only that a *purpose-built* control would be marginally better — which is exactly the "equally valid alternative" shape the grading key's cited SKILL.md materiality bar rules out. |

## 2. Citation-integrity table

All quotations the review marks as verbatim were checked against a fresh, direct
`WebFetch` of the live cited page (not against memory, and not against the review's own
paraphrase). Straight vs. curly quote-mark rendering differences are noted but not
counted as fidelity failures.

| # | Review's quoted text | Cited page | Live-fetch result | Verdict |
|---|---|---|---|---|
| 1 | View/Table/Card criteria table (3 rows × 3 cols) | `patterns/resource-management/view/index.html.md` | Table reproduced identically, all cells match | VERBATIM ✓ |
| 2 | "Use a table if the resources share the same metadata... Use the card view if users will not be comparing..." | same | Matches (two source sentences correctly joined) | VERBATIM ✓ |
| 3 | Table view "Don't": "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern." | `patterns/resource-management/view/table-view/index.html.md` | Confirmed on second, more literal fetch: exact match (curly vs straight quotes only) | VERBATIM ✓ |
| 4 | Card view "Don't", same shape, "cards component" | `patterns/resource-management/view/card-view/index.html.md` | Exact match | VERBATIM ✓ |
| 5 | Content layout "Don't": "Don't use the content layout component for productive use cases such as resources creation, view, edit, and delete." | `components/content-layout/index.html.md` | Exact match; "view" link confirmed pointing to the same View-resources pattern page | VERBATIM ✓ |
| 6 | Filtering-patterns criteria table (4 rows × 3 cols) | `patterns/general/filter-patterns/index.html.md` | Table reproduced identically, all cells match | VERBATIM ✓ |
| 7 | "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'." | same | Exact match (confirmed on literal-text re-fetch; first fetch had truncated the "For example" clause via model summarization, not a review error) | VERBATIM ✓ |
| 8 | Collection select filter "Do": "Use a select filter if users need a maximum of two properties to find a specific item. If more than two are required, use a property filter instead." | `components/collection-select-filter/index.html.md` | Exact match | VERBATIM ✓ |
| 9 | Property filter "Do": "Use a property filter pattern if users need more than two properties to find a specific item. If only two are required, use the collection select filter instead." | `components/property-filter/index.html.md` | Exact match | VERBATIM ✓ |
| 10 | Collection select filter "Displaying results": "The collection is filtered as soon as the user selects a value from a select filter or enters text into the accompanying text filter." | same | Exact match | VERBATIM ✓ |
| 11 | Orientation note, StatusIndicator: "communicates the state of a resource ... in a compact form that is easily embedded in a card, table, list, or header view" | `components/status-indicator/index.html.md` | Exact match either side of the review's ellipsis; elided clause ("either in its entirety or a particular facet of a resource") is a legitimate, honestly-marked ellipsis, not a fidelity violation | VERBATIM ✓ |

**Result: 11/11 checked quotations verbatim.** No fabricated or misattributed quotation
found anywhere in the review. Citation fidelity is a clean pass and is **not** the basis
for the case-level fail.

## 3. Fixture line-citation accuracy

Checked directly against `MessageQueues.tsx` (not trusted from the review):

| Review citation | Actual content at those lines | Accurate? |
|---|---|---|
| Lines 29–33 (code comment, user task) | Exact 5-line comment block, word-for-word as quoted | Yes |
| Line 50 (Header `description`) | `description="Compare message throughput and backlog age across queues to decide which need scaling attention."` | Yes |
| Lines 18–25 (`QUEUES` array) | `const QUEUES: MessageQueue[] = Array.from(...)` through closing `}));` | Yes |
| Lines 44–101 (ContentLayout→Cards block) | `<ContentLayout` opens at 45 (JSX return starts 44), file ends at 101; close enough to be a fair span citation for "the entire page" | Yes (minor, immaterial rounding) |
| Lines 63–87 (card sections) | `cardDefinition={{` at 63 through closing `}}` at 87 | Yes |
| Lines 12–13 (`status`/`region` union types) | Exact match | Yes |
| Lines 89–95 (`TextFilter` block) | Exact match | Yes |
| Lines 36–39 (`useCollection` filtering config) | Exact match | Yes |

No line-citation fabrication or drift found.

## 4. Is Finding 2 a legitimate reading of the fixture, or a rationalization?

The task brief specifically asks me to weigh whether the review's argument — that the
fixture's own comment resolves "which user goal applies to which field," on top of the
documented tie in "Complexity of the resource" — is a legitimate reading or an
unsupported rationalization dressed in the corpus's own equivalence language.

**My assessment: it is a legitimate, evidence-grounded reading of the fixture, but it
does not clear the rubric's materiality bar, and the review's own text contains the
tell.**

- The comment at lines 29–33 does genuinely map cleanly onto the filter-patterns table's
  "User goals" row: "search by queue name" ≈ "find resources that match an exact text
  query" (Text filter); "narrow the list down to a specific status or region" ≈ "find
  resources with overlapping, defined values" (Collection select filter) — and the
  comment even names "status" as one of the two properties, echoing the doc's own "For
  example: by 'status' or 'type'" continuation almost exactly. This is not invented; it
  is a real, close correspondence, and the review's citation of it is fair.
- But establishing *which user goal exists* is a different question from establishing
  *that the current single control fails to serve it materially*. The review's own
  applicability argument, point (2), states the narrowing goal is "today... reachable as
  a side effect of TextFilter's whole-item substring match (typing 'healthy' or
  'us-east-1')." That sentence is the review conceding, in its own words, that the
  current implementation already accomplishes the stated task for two 2-value enums on a
  24-item list — which is functionally the "equally valid alternative" the grading key's
  cited SKILL.md materiality section says must not be reported. The review reframes this
  concession as "not through the documented mechanism," which is a real but *procedural*
  objection (purity/discoverability of the specific widget), not a *task-failure*
  objection (the operator genuinely cannot accomplish the goal). Rubric Q6 asks whether
  an FDE would *plausibly restructure the code* over this, not whether a more
  textbook-correct widget exists — and for a tied complexity tier, low cardinality
  (2 values × 2 fields), and no stated friction/pain point in the fixture, the honest
  answer is no.
- So: legitimate reading of the evidence, rationalized past the materiality bar. The
  finding is "well-argued overreach," which is exactly what the rubric's D grade is for
  ("treats component or pattern existence as a mandate without establishing
  applicability").

## 5. Does the grading key's own "no comment establishes lookup mode" premise hold up?

**No — as a literal factual claim it does not hold up, and I want to flag this clearly.**

The grading key's Candidate 2 section states:

> "the fixture shows no code, comment, or header language establishing which lookup mode
> operators actually use, only that the page's task is comparison across the full list
> ... not targeted lookup by either name or property."

The fixture directly contradicts the first half of this sentence. Lines 29–33 read (word
for word, confirmed by direct read of the fixture, not trusted from either document):

> "Message Queues: every queue in the account, side by side, so an operator can compare
> throughput and backlog age across all of them at once to decide which need scaling
> attention right now. Operators can search by queue name, or narrow the list down to a
> specific status or region while triaging."

This is comment language that explicitly names two distinct lookup modes — name search
and status/region narrowing — not merely the comparison task. I confirmed via `git log
--follow -p` that both the fixture and the grading key were introduced in the same
commit (`647ff0e7`, 2026-09-01), so this is not a case of the fixture being edited after
the key was written; the comment was present when the key's author wrote the "no
comment" sentence. The review under test correctly caught this comment and used it
(consistently with how the grading key's *own* Candidate 1 section treats the `Header`
`description` as non-inferred, verbatim task evidence) — the review's Finding 2 "User
task" field cites it accurately.

**Why this doesn't flip my case-level verdict:** the grading key's suppression argument
is not built on that one sentence alone. It has a second, independent leg — the
materiality/equivalence argument (tied "Complexity of the resource" cell, TextFilter
already functionally sufficient for two 2-value enums, no stated friction, 24 items is
not a large collection) — that does not depend on "no lookup-mode evidence exists" and
stands on its own under the rubric's Q5/Q6. Even granting that the comment *does*
establish operators want both lookup modes, that only shows a *goal* exists; it does not
show the *existing single control* fails to serve it, which is what materiality requires
per SKILL.md's cited "an experienced Cloudscape practitioner would plausibly restructure
the code" bar — and the review's own text (§4 above) concedes the existing control
already reaches the goal by substring match. So: the grading key contains a real,
checkable inaccuracy in one supporting sentence, but its ultimate MUST-SUPPRESS verdict
survives on the independent materiality leg. I'd recommend the grading key's author
correct or soften that specific sentence (e.g., "the comment names the goal but doesn't
establish that the existing control fails to serve it") rather than leave it as a
flatly-false "no comment exists" claim, since a future adversarial pass that only checks
that one sentence could wrongly credit a candidate response for citing evidence the key
claims doesn't exist.

## 6. Suppressed section and tolerated ambiguity

- **PropertyFilter suppression (review's "Suppressed" section):** correctly suppressed,
  and named explicitly (the stronger form the grading key prefers). The stated reasoning
  — Property filter's own "Do" text plus the "Complex resource" tier — matches confirmed
  live source text. No issue.
- **`ContentLayout`+`Cards` vs. `full-page` cards-variant ambiguity (grading key's
  "tolerated, non-scoring" item):** the review does not surface this as a separate
  confident finding. It is effectively subsumed by Finding 1's recommendation to move to
  a full-page `Table` entirely (which independently resolves the "don't use
  ContentLayout" issue for whichever component is chosen). This is one of the grading
  key's explicitly "acceptable outcomes" (omitted entirely). No penalty.

## 7. Summary

- **Citation fidelity:** clean pass, 11/11 verbatim, no fabrication, fixture line cites
  accurate.
- **Finding 1:** A grade, matches Candidate 1 exactly, MUST REPORT satisfied.
- **Finding 2:** D grade — legitimate but overreaching reading of real evidence; is
  Candidate 2; reported at high confidence, which the grading key treats as an automatic,
  non-negotiable disqualifying failure regardless of argument quality.
- **Case-level verdict: FAIL**, per the grading key's stated bar ("Reporting Candidate 2
  at any confidence/materiality level — the specific, disqualifying failure this case
  exists to detect").
- **Grading key defect found:** the "no code, comment, or header language establishing
  which lookup mode operators actually use" sentence in the key's Candidate 2 section is
  factually inaccurate against the actual fixture (the comment at lines 29–33 does
  establish both lookup modes) — confirmed the fixture and the key were authored in the
  same commit, so this isn't a drift artifact. This does not change the case verdict,
  because the key's independent materiality/equivalence argument holds regardless, and
  the review's own text concedes the functional-equivalence point the materiality bar
  turns on — but the key's wording should be corrected so a future grading pass isn't
  misled by a checkable false premise.
