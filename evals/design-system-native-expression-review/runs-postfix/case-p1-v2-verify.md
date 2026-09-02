# Adversarial verification — case-p1-message-queues, v2 skill run

**Review graded:** `evals/design-system-native-expression-review/runs-postfix/case-p1-v2-skill.md`
**Grading key:** `evals/cloudscape-native-expression-review/grading/case-p1-message-queues.expected.md`
**Fixture:** `evals/cloudscape-native-expression-review/cases/case-p1-message-queues/fixture/src/pages/MessageQueues.tsx` (re-read directly; all line-number claims in the review checked against it)
**Cloudscape pages live-fetched and read in full:** `/patterns/general/filter-patterns/`, `/components/collection-select-filter/`, `/components/text-filter/`, `/patterns/resource-management/view/`, `/patterns/resource-management/view/table-view/`, `/patterns/resource-management/view/card-view/`, `/components/status-indicator/` — all as `index.html.md`, fetched with `curl` directly (no summarizing intermediary) so every quoted string below is checked character-for-character against the fetched file.

---

## 1. The central factual question: does the filter-patterns criteria table contain equalizing language?

The review's Finding 2, Applicability argument point (4), states:

> "there's no equalizing language in the filtering-patterns table suggesting text filter alone is an equally valid choice once structured property narrowing is the stated goal — the table differentiates by user goal..."

**This claim is FALSE.** The live-fetched criteria table at `/patterns/general/filter-patterns/index.html.md` reads:

```
|  | Text filter | Collection select filter | Table property filter |
| --- | --- | --- | --- |
| Complexity of the resource | Simple resource (small set of properties) | Simple resource (small set of properties) | Complex resource (large set of properties) |
| User goals | Find resources that match an exact text query | Find resources with overlapping, defined values | Find resources with multiple combinations of values |
| Selection of values | - | Single selection of a value for each property | Multiple selection of values for each property |
| Operators | - | "And" operator | "And", "Or", "Not", "And not" and "Or not" operators |
```

The **"Complexity of the resource" row places `Text filter` and `Collection select filter` in the identical cell** — "Simple resource (small set of properties)" — verbatim, word for word, both cells. That *is* equalizing language for exactly the dimension ("small set of properties" / "two properties") the review's own Finding 2 uses to argue materiality. The review quoted the *User goals* row (which does differentiate) but never quoted, and explicitly denied the existence of, the *Complexity of the resource* row it sits directly above in the same table — the row that undercuts its own materiality argument.

This is not a minor citation slip. It is the exact overreach the grading key was built to detect: MessageQueue's `status` and `region` are both simple, low-cardinality properties — precisely the tier where the design system's own table says *both* components fit equally, differentiated only by unresolved user-behavior goals ("if users tend to know exactly the value... use text filter" vs. "if the common behavior... is to filter by one or two properties... use collection select filter") that this single-file fixture cannot evidence either way (no code, comment, or header language establishes which lookup mode operators actually use). The review's applicability point (4) — the crux of its "this is material" argument — is built on a false premise about what its own cited source says.

## 2. Citation-integrity table

All quotations below were checked against the raw fetched markdown, not a paraphrase.

| # | Review's quote | Attributed to | Verified against live fetch | Verdict |
|---|---|---|---|---|
| 1 | "9 or more resources in 99% of use cases" / "5 or less resources in 99% of use cases" | `view/index.html.md` | `Number of resources in the data set` row — exact match | VERBATIM confirmed |
| 2 | "Shared metadata between resources" / "Different metadata across resources" | `view/index.html.md` | Exact match (review omits page's own parenthetical example after "resources," which is fine — not claimed as full sentence) | VERBATIM confirmed |
| 3 | "Data that is displayed in columns (text, numerical, status, sparkline)" / "Data that can be displayed as visuals (charts, videos)" | `view/index.html.md` | Exact match | VERBATIM confirmed |
| 4 | "Use a table if the resources share the same metadata... to take action on." | `view/index.html.md` | Exact match, full sentence pair | VERBATIM confirmed |
| 5 | "Use table view pattern for static data with multiple attributes displayed in a tabular format. The best data type for a table view is data that is structured, easily comparable, and sortable." | `table-view/index.html.md`, "Do" | Both sentences verbatim, but source renders them as **two separate bullets**; review concatenates into one quoted run without a bullet break. Wording itself is character-exact. | VERBATIM text, minor structural merge (not a fabrication) |
| 6 | "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern." | `table-view/index.html.md`, "Don't" | Exact match | VERBATIM confirmed |
| 7 | Same "Don't...Instead" pairing "also appears verbatim" in card-view, substituting "cards" for "table" | `card-view/index.html.md` | Confirmed: "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." | VERBATIM confirmed |
| 8 | "Table view of all user resources sorted on a certain data set by the user. Each individual table column can be sorted in ascending or descending order," | `table-view/index.html.md`, "Sort" | Exact match; source ends the sentence with a period, review's embedded quote splices a comma to join the next clause | VERBATIM text, trivial punctuation splice |
| 9 | "User goals" row: "Find resources that match an exact text query" / "Find resources with overlapping, defined values" | `filter-patterns/index.html.md` | Exact match | VERBATIM confirmed |
| 10 | "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'." | `filter-patterns/index.html.md` | Exact match | VERBATIM confirmed |
| 11 | "Use a select filter if users need a maximum of two properties to find a specific item. If more than two are required, use a property filter instead." | `collection-select-filter/index.html.md`, "Do" | Exact match | VERBATIM confirmed |
| 12 | "Use a select filter for commonly used properties and values." | `collection-select-filter/index.html.md`, "Do" | Exact match | VERBATIM confirmed |
| 13 | "The collection is filtered as soon as the user selects a value from a select filter or enters text into the accompanying text filter" | `collection-select-filter/index.html.md`, "Displaying results" | Exact match (correctly truncated before the following sentence) | VERBATIM confirmed |
| 14 | "Use the text filter to provide basic filtering in a collection" | `text-filter/index.html.md`, "Do" | Exact match (correctly truncated before "The most common use cases are...") | VERBATIM confirmed |
| 15 | "communicates the state of a resource... in a compact form that is easily embedded in a card, table, list, or header view" | `status-indicator/index.html.md` | Exact match with legitimate ellipsis eliding "either in its entirety or a particular facet of a resource" | VERBATIM confirmed, ellipsis correctly signaled |
| 16 | "there's no equalizing language in the filtering-patterns table suggesting text filter alone is an equally valid choice" | Review's own analytical claim about `filter-patterns/index.html.md` (not in quotation marks as literal source text) | **FALSE** — see §1 above; the "Complexity of the resource" row is exactly this equalizing language | **Factually incorrect characterization of cited source** |

All page attributions are correct (every quoted string traces to the page named). No fabricated quotation was found presented inside quotation marks as literal source text — the one substantive failure is item 16, a false *characterization* of what the source does/doesn't contain, which is the load-bearing premise of Finding 2's materiality argument.

## 3. Per-finding grade table (rubric's nine questions)

### Finding 1 — Cards vs. Table (= Candidate 1, designed verdict: MUST REPORT)

| Q | Answer |
|---|---|
| 1. Task supported by repo evidence? | Yes — header `description` prop (fixture line 50) states the comparison task verbatim; review cites it correctly. |
| 2. Cited authority says what's claimed? | Yes — all four quoted table rows/prose fragments verified verbatim (§2, items 1–8). |
| 3. Four-point applicability test passes? | Yes — task matches the pattern's own stated comparison-to-decide problem in the page's own header copy (not inferred); current Cards implementation solves the same "see all queues" problem; Table preserves the identical task; two independent quantified criteria (item count, metadata type) both point the same direction. |
| 4. Native expression preserves task semantics? | Yes — same four fields, same filter/pagination affordances, same 24 items; only the presentational component changes. |
| 5. Could current impl be equally valid? | No — 24 items clears the "9+" Table threshold and fails the "5 or less" Cards threshold outright; all criteria point one direction, no tie found on this dimension (unlike Finding 2). |
| 6. Materially would an FDE restructure? | Yes — plausible; the already-wired but inert `sorting: {}` is a concrete signal a practitioner would notice. |
| 7. Component/pattern-level, not implementation/UX? | Yes — boundary check correctly scoped. |
| 8. Improper duplication across levels? | No — correctly unified as one `combined selection + composition` finding, matching SKILL.md's stated preference and the grading key's allowance of either type. |
| 9. intent-dependent handling? | N/A for the core Cards-vs-Table judgment — but see flag below. |

**Grade: A** for the core Cards-vs-Table judgment — matches Candidate 1's designed evidence and applicability argument almost point for point, citations verified verbatim, materially correct. An FDE would plausibly act on this: two independent, quantified, unambiguous criteria (item count, metadata type) both fail the Cards side of the threshold, and the header's own copy names the comparison task directly.

**Flag (not scored against Candidate 1, per the grading key's own instruction to note separately):** Finding 1's "Native expression" folds in, with the same high confidence as the rest of the finding, a second and separate claim — "no `ContentLayout` wrapper, per the pattern's own 'Don't'" — addressing the grading key's "tolerated, non-scoring ambiguity" (whether this file is a standalone top-level view or sits inside a larger app-layout shell). The review never names this missing-context caveat anywhere in the document (confirmed via full-text search: no mention of "shell," "app layout," "standalone," "embedded," or `intent-dependent` anywhere in the review). Per the grading key: "reporting it as a confident, high-confidence violation-strength finding without naming the missing-context caveat... would be a genuine, scorable missing-intent failure... a distinct one from this case's central target." That failure is present here, embedded inside an otherwise-correct Finding 1, and should be recorded as a real defect distinct from the Candidate 1/2 verdicts.

### Finding 2 — TextFilter alone vs. adding CollectionSelectFilter (= Candidate 2, designed verdict: MUST SUPPRESS)

| Q | Answer |
|---|---|
| 1. Task supported by repo evidence? | Partially — `status`/`region` cardinality is real and correctly cited (fixture lines 12–13), but the task's own copy never names a filtering *pain point* for these two properties (no comment/copy says users struggle to find queues by status or region) — the grading key names this absence explicitly as deliberate. |
| 2. Cited authority says what's claimed? | **No, not fully** — the "User goals" row quote (item 9, §2) is accurate, but the finding's load-bearing materiality claim (item 16) misstates what the same table's "Complexity of the resource" row says. The cited page does *not* say what the finding's own applicability argument claims it says. |
| 3. Four-point applicability test passes? | **No** — point 4 fails. The retrieved evidence, correctly read, places `TextFilter` and `CollectionSelectFilter` in the same documented fit tier for this resource's complexity; the review asserts the opposite. |
| 4. Native expression preserves task semantics? | Yes, nominally — adding CollectionSelectFilter alongside TextFilter doesn't redesign the product — but this is moot given the point-3 failure. |
| 5. Could current impl be equally valid? | **Yes** — this is exactly what the "Complexity of the resource" row establishes, and what the review's own applicability argument affirmatively (and incorrectly) denies. |
| 6. Materially would an FDE restructure? | No — 24 items, one already-present, doc-supported filter mechanism sufficient to substring-match two discrete values, no stated task friction. The grading key is explicit that an FDE would not plausibly restructure for this reason alone. |
| 7. Component/pattern-level, not implementation/UX? | Correctly scoped as component-level, but that scoping doesn't rescue the applicability failure. |
| 8. Improper duplication? | No. |
| 9. intent-dependent handling? | Not applicable — but arguably *should* have been: given the table's own tie and the speculative, unresolvable "user goals" distinction, `intent-dependent` (or suppression) was the correct classification, not a confident `high`/`high` finding. |

**Grade: E — factually wrong.** The underlying premise of the finding's materiality argument (that the cited authority contains no equalizing language) is false; the cited page, read in full, is exactly what the grading key predicted a correct reviewer would find and use to suppress this candidate. This reproduces the case's designed disqualifying failure: Finding 2 reports Candidate 2 at `Materiality: high`, `Confidence: high`, with a specific, incorrect denial of the table's tie as its stated justification.

Per the grading key's escalation clause: this does **not** reach the "sharpest form" of the failure (an explicit self-acknowledgment inside the finding that the current approach is "equally valid") — the review never states TextFilter-alone is equally valid within Finding 2 itself. But it is functionally adjacent: the Orientation notes section separately states "`TextFilter` itself, for the name-search part of the task, is valid... on-label usage," and Finding 2's own cited source (which the review partially quoted) says the opposite of what the review claims about it. This is the ordinary form of the MUST-SUPPRESS failure, compounded by a citation-integrity defect on the exact fact that should have triggered suppression.

## 4. Case-level verdict

**Candidate 1 (Cards vs. Table): correctly reported, MUST REPORT satisfied.** Grade A on the core judgment, with one separately-scored missing-intent lapse (the un-hedged ContentLayout/full-page-variant claim folded into the same finding) that the grading key treats as real but orthogonal.

**Candidate 2 (TextFilter alone vs. CollectionSelectFilter): NOT correctly suppressed.** The v2 skill run reproduces the exact A1 Finding 2 failure shape this case exists to detect — it reports the candidate as a named, high-materiality, high-confidence finding, and the applicability argument it uses to justify doing so rests on a demonstrably false claim about the cited Cloudscape source (denying equalizing language that in fact exists, verbatim, in the same table the finding already partially quotes).

**Overall: FAIL on this case's central adjudication target.** The report does not achieve the pass condition (silent omission or a named "Suppressed" entry for Candidate 2, per the grading key). Candidate 1 alone being handled well does not offset this, since the rubric and grading key are explicit that reporting Candidate 2 at any confidence/materiality level is "the specific, disqualifying failure this case exists to detect," independent of Candidate 1's quality.

### Summary of what would be wrong (per grading key's own checklist), applied here

- Missing Candidate 1 entirely — did not occur (correctly reported).
- Reporting Candidate 2 at any confidence/materiality level — **occurred** (`high`/`high`, named "Finding 2").
- Confidently asserting the ContentLayout/full-page-cards candidate without naming the missing-context caveat — **occurred**, inside Finding 1, a real but separate missing-intent failure.
- Fabricated or non-verbatim quotation — **not found**; all sixteen quoted/cited fragments checked verbatim against live-fetched source text, with the one substantive defect being a false *characterization* of source content (item 16) rather than a fabricated quotation.
