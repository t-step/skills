# Adversarial verification — Case P1 (MessageQueues.tsx)

**Review graded:** `evals/design-system-native-expression-review/runs-postfix/case-p1-skill.md`
**Grading key:** `evals/cloudscape-native-expression-review/grading/case-p1-message-queues.expected.md`
**Fixture:** `evals/cloudscape-native-expression-review/cases/case-p1-message-queues/fixture/src/pages/MessageQueues.tsx` (re-read directly, 101 lines)
**Live sources fetched** (raw `.html.md`, not paraphrased through a summarizer):
- `/patterns/general/filter-patterns/index.html.md`
- `/patterns/resource-management/view/index.html.md`
- `/patterns/resource-management/view/card-view/index.html.md`
- `/patterns/resource-management/view/table-view/index.html.md`
- `/components/status-indicator/index.html.md`

## Case-level verdict (headline)

**FAIL — Candidate 2 must-suppress failure reproduced.** The review's Finding 3
reports `TextFilter` vs. adding a `CollectionSelectFilter` for `status`/`region`
as a high-materiality, high-confidence finding. The grading key's Candidate 2
is unambiguous: this must be suppressed, and it is not — regardless of
confidence framing. This is the specific failure mode Case P1 was built to
detect.

Candidate 1 (Cards → Table) is correctly reported and well-supported —
**PASS**, matches the grading key's MUST REPORT verdict closely.

The tolerated ambiguity (`ContentLayout` vs. full-page `Cards`, Finding 2) is
reported at high confidence/high materiality **without** the missing
surrounding-shell-context caveat the grading key says is required to make
that an acceptable outcome. This is a real, separate missing-intent failure —
noted here per the grading key's own instruction to keep it distinct from
the Candidate 2 verdict, and it does not change the case's primary
pass/fail (which is driven by Candidate 2).

---

## Per-finding grade table

| Finding | Rubric grade | Case-level match | Driving questions |
|---|---|---|---|
| Finding 1 — Cards vs. Table (Candidate 1) | **A** | MATCH (MUST REPORT, correctly reported) | Q1 PASS, Q2 PASS, Q3 PASS, Q4 PASS, Q6 PASS, Q7 PASS |
| Finding 2 — ContentLayout vs. full-page variant (tolerated ambiguity) | **D** | Not itself scored pass/fail per the key, but lands in the key's "not acceptable" bucket — confident violation-strength claim, no missing-context caveat | Q9 FAIL (asserts confident answer on genuinely-missing intent instead of naming the shell-context ambiguity) |
| Finding 3 — TextFilter vs. CollectionSelectFilter (Candidate 2) | **D** (overreach; see note) | **MISMATCH — MUST SUPPRESS violated** | Q3 FAIL, Q5 FAIL, Q6 FAIL (materiality asserted "high" despite the cited page's own criteria tying the two options at this resource's complexity tier) |

**Note on Finding 3's grade:** every individual quoted fragment the review
pulls from the filter-patterns page is, on its own, accurate (see citation
table below) — the failure is not that the review invented what the docs
say, but that it retrieved a 4-row criteria table, quoted from the "User
goals" row (which reads as differentiating), and never engaged with the
adjacent "Complexity of the resource" row in the same small table, which
ties the two components together for this exact resource shape. That is an
applicability/overreach failure (rubric Q3/Q5: "does this treat
partial/documented support as a mandate without establishing genuine
applicability"), not a fabrication of what any single sentence says — hence
D rather than E on the per-finding rubric. Whether the underlying candidate
should have been suppressed is a separate, case-level judgment (below),
independent of the per-quote grade.

---

## Citation-integrity table (every VERBATIM-tagged quotation, checked character-for-character against the live-fetched `.html.md`)

| # | Finding | Quoted string in review | Source page | Verified? |
|---|---|---|---|---|
| 1 | F1 | Criteria table: "Number of resources in the data set / 9 or more... / 5 or less...", "Metadata being displayed / Shared metadata... / Different metadata...", "Metadata type / Data that is displayed in columns... / Data that can be displayed as visuals..." | `/patterns/resource-management/view/index.html.md` | **Match**, with one trivial deviation: source row label is `Metadata*` (with a footnote asterisk); review drops the asterisk. No content distortion. |
| 2 | F1 | "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on. Use the card view if users will not be comparing between a large number of resources to determine which to take action on." | same page | **Exact match.** |
| 3 | F2 | "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." | `/patterns/resource-management/view/card-view/index.html.md`, Don't list | **Match** (review discloses stripping markdown link brackets around "content layout" and "cards"; wording otherwise identical). |
| 4 | F2 | Same sentence with "table" substituted for "cards" | `/patterns/resource-management/view/table-view/index.html.md`, Don't list | **Match**, same disclosed bracket-stripping. |
| 5 | F3 | "If users tend to know exactly the value or term they are looking for, use the text filter." | `/patterns/general/filter-patterns/index.html.md` | **Exact match** (link bracket around "text filter" stripped, disclosed). |
| 6 | F3 | "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter." | same page | **Exact match.** |
| 7 | F3 | "For example: by 'status' or 'type'." | same page | **Match** — source uses double quotes (`"status"`/`"type"`), review renders single quotes because the string is nested inside an outer double-quoted span. Content unchanged; acceptable nesting convention. |
| 8 | F3 | "Find resources that match an exact text query" (Text filter, User goals row) | same page, criteria table | **Exact match.** |
| 9 | F3 | "Find resources with overlapping, defined values" (Collection select filter, User goals row) | same page, criteria table | **Exact match.** |
| 10 | F3 | "if a select filter has two properties, the operator is always and" | same page | **FAIL — not verbatim, effectively fabricated.** No such sentence exists on the page. The nearest source material is two separate sentences: "Display operators when at least two filters are defined... By default, the operator is always set to 'and' for the collection select filter, and can be modified only in the property filter." The review compresses/paraphrases these into a single string and presents it inside quotation marks as literal source text, under a finding whose "Evidence mode" is declared VERBATIM. This is a citation-fidelity violation, to be scored separately per the task brief (not folded into Finding 3's materiality grade above). |
| — | Orientation notes | "communicates the state of a resource... in a compact form that is easily embedded in a card, table, list" | `/components/status-indicator/index.html.md` | **Match** — legitimate ellipsis-truncated quote (skips "either in its entirety or a particular facet of a resource-" and the trailing ", or header view"); retained text is word-for-word accurate. Not tagged VERBATIM but checked for completeness. |
| — | Orientation notes | "display the pagination even if the resources set fits in one page" | `/patterns/resource-management/view/card-view/index.html.md` | **Match** (source: "Display the pagination even if the resources set fits in one page." — capitalization lowered to fit the review's sentence, standard practice). |

**Attribution check:** every citation in Findings 1–3 points to the page it actually quotes from; no cross-page misattribution found.

---

## The central question: did Finding 3 engage with the "Complexity of the resource" row?

**No.** The filter-patterns criteria table fetched live is:

```
|  | Text filter | Collection select filter | Table property filter |
| --- | --- | --- | --- |
| Complexity of the resource | Simple resource (small set of properties) | Simple resource (small set of properties) | Complex resource (large set of properties) |
| User goals | Find resources that match an exact text query | Find resources with overlapping, defined values | Find resources with multiple combinations of values |
| Selection of values | - | Single selection of a value for each property | Multiple selection of values for each property |
| Operators | - | "And" operator | "And", "Or", "Not", "And not" and "Or not" operators |
```

Row 1 ("Complexity of the resource") places `TextFilter` and
`CollectionSelectFilter` in the **identical cell** — "Simple resource (small
set of properties)" — for both. This fixture's `MessageQueue` type (6
fields, 2 of which are the finite-valued `status`/`region`) is squarely a
simple resource by this table's own framing, so both filter options are
tied at the complexity dimension. The table only differentiates by *user
goal* (row 2), which is exactly, and only, the row the review quotes.

The review's Finding 3 "Authority evidence" quotes two prose sentences and
then explicitly frames the criteria table as something that "further
contrasts user goals," quoting the two User-goals cells verbatim — but never
names "Complexity of the resource," never quotes that row, and never
states that the two options are tied at this resource's complexity tier.

**Selective quotation, not failed retrieval.** The Complexity row and the
User-goals row the review does quote are adjacent rows in the same
4-row, single markdown table on one short page (68 lines total, table
spans lines 29–34 of the fetched source). It is not plausible that a
fetch of this page returned the User-goals row's cells character-for-character
while omitting the immediately adjacent Complexity row — the whole table is
a single retrieval unit. The far more likely account, given the review
demonstrably had the table's other cells in hand, is that the row was
retrieved and then not engaged with in the write-up: the equalizing
evidence was in front of the reviewer and left out of the finding, not
missed by a narrow or partial fetch. This is precisely the "selective
retrieval that omitted the equalizing evidence" framing named in the task
brief, and it is exactly the shape of failure the grading key's Candidate 2
section is built to catch: quoting the differentiating language while
silently dropping the tying language from the same source.

Compounding this: applicability point (4) in Finding 3 ("Two finite-valued
properties is precisely the collection select filter's stated scope...")
leans on the fabricated "operator is always and" quote (citation item #10
above) rather than on anything that actually addresses whether the
difference is material at this resource's documented complexity tier — the
one dimension on which the source page itself says there is no difference.

---

## Summary of what would be wrong (per the grading key) vs. what the review did

- Missing Candidate 1 entirely → **did not happen** (Finding 1 present, well-supported, grade A).
- Reporting Candidate 2 at any confidence/materiality level → **did happen** (Finding 3, materiality high, confidence high). This is the case's disqualifying failure.
- Confidently asserting the ContentLayout/full-page-cards candidate without naming the missing-context caveat → **did happen** (Finding 2 has no shell-context hedge), a real but separate missing-intent failure per the grading key, noted here distinctly from the Candidate 2 verdict.
- Fabricated or non-verbatim quotation inside quotation marks presented as literal source text → **did happen once** (citation item #10, Finding 3's "operator is always and" string), scored separately under citation fidelity as instructed.

## Bottom line

Case P1 fails at its central adjudication target: Finding 3 reproduces the
A1 Finding 2 overreach shape the case was designed to detect — a
component-selection candidate reported at high confidence despite the
reviewer's own cited authority tying the two options together on the one
dimension (resource complexity) that would make the difference material.
Finding 1 is a clean, well-evidenced pass. Finding 2 is a secondary,
separately-scoped missing-intent problem (confident claim, no
shell-context caveat) that does not affect the primary verdict but should
not be silently absorbed into it.
