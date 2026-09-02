# Adversarial Verification — Case P1: MessageQueues.tsx

Verifier run against `evals/design-system-native-expression-review/runs/case-p1-skill.md`,
graded per `evals/cloudscape-native-expression-review/rubric.md` and the
case's grading key,
`evals/cloudscape-native-expression-review/grading/case-p1-message-queues.expected.md`.
All cited Cloudscape pages were independently re-fetched live
(`cloudscape.design`) during this verification, with exact-reproduction
prompts (not summarization) used for every claim marked `VERBATIM`.

## Case-level verdict: **MISMATCH**

The case exists to test one narrow thing: given a real primary finding
(Cards→Table), does the reviewer also emit a secondary candidate
(TextFilter→CollectionSelectFilter for `status`/`region`) that its own
retrieved evidence shows is an equally-valid, low-materiality alternative,
or does it correctly suppress that candidate?

The review **reported the must-suppress candidate as Finding 2**, with
`Materiality: medium`, `Confidence: high`, `Authority strength:
RECOMMENDED`, `Evidence mode: VERBATIM`. This is precisely the
disqualifying failure the grading key names in its "What would be wrong"
section: *"Reporting Candidate 2 at any confidence/materiality level —
the specific, disqualifying failure this case exists to detect."* The
review does not name, anywhere in its Findings, Suppressed, or Orientation
notes, the filter-patterns page's own criteria table placing `TextFilter`
and `CollectionSelectFilter` in the *same* "Simple resource" complexity
cell — the exact equivalence evidence that should have triggered
suppression. It suppressed a narrower, related question (Property Filter
vs. Collection Select Filter as the *choice of replacement*), but never
questioned whether a replacement was warranted at all.

Candidate 1 (Cards→Table) was correctly identified, correctly reported as
the sole high-materiality finding, and is well-evidenced (Grade A, below).

---

## Finding 1 — Cards used for a 24-item comparison collection instead of Table

**Maps to grading key Candidate 1 — MUST REPORT. Correctly reported.**

1. **Task supported by repo evidence?** Yes. Header `description` (line
   50) and source comment (lines 29–33) both state the comparison task
   directly; 24 items with identical schema, confirmed against the
   fixture.
2. **Does cited guidance say what's claimed?** Yes — see citation
   integrity section below; every VERBATIM quote checked out
   character-for-character against the live pages, including a third
   criteria-table row ("Metadata being displayed": shared vs. different)
   the review cited that the grading key itself didn't quote, and which
   turned out to be real and accurate.
3. **Applicability test (four-point)?** Passes. Task materially matches
   the pattern's own stated comparison-to-decide problem (point 1);
   current Cards already re-derives table-like sections to serve the same
   comparison need (point 2); Table preserves the same task, same fields,
   same operator goal (point 3); two independent, quantified criteria
   (24 items vs. "9+"/"5 or less" thresholds, and "shared metadata"
   vs. "different metadata") both point the same direction, plus the
   concrete detail that `sorting: {}` is already wired into
   `useCollection` with no UI to expose it under `Cards` (point 4).
4. **Preserves task semantics?** Yes — no data, filtering, or pagination
   behavior changes; only the container component and its documented
   affordances change.
5. **Could current impl be equally valid?** No — the review does not
   claim this and the docs are one-directional at this data shape.
6. **Materiality — would an FDE act on it?** Yes. Matches the grading
   key's own "high-to-medium" characterization; the review's `high` is
   within the acceptable range, and the review's own applicability
   argument (not just materiality label) supports it.
7. **Component/pattern level, not implementation or generic UX?** Yes.
   Boundary check is honest and accurate; the "stranded sort state"
   supporting detail is used as reinforcing evidence for a
   component-selection judgment, not spun off as its own
   implementation-correctness finding.
8. **Duplicated across levels?** No — correctly typed
   `combined selection + composition`, which the grading key explicitly
   allows as equally acceptable to plain `component selection`.
9. **Intent-dependent?** N/A — not applicable here; task is clearly
   established.

**Grade: A.** Material and strongly validated; an FDE working in this
codebase would plausibly restructure Cards→Table specifically because the
task, the item count, and the metadata-uniformity all point the same
documented direction, and because the code already has unexposed sort
state waiting for a component that can surface it.

---

## Finding 2 — TextFilter alone vs. adding a CollectionSelectFilter for status/region

**Maps to grading key Candidate 2 — MUST SUPPRESS. Reported as a Finding — the central failure this case exists to detect.**

1. **Task supported by repo evidence?** Partially, and this is where the
   trouble starts. The source comment does say "narrow the list down to a
   specific status or region while triaging" — that much is real. But the
   finding's framing overreaches from there: it asserts "no filtering
   control at all" for status/region, then in its own "Why it matters"
   concedes an operator actually *can* narrow to "backlogged" or
   "us-west-2" by typing the value into the existing `TextFilter`,
   because no `filteringFields` restricts `useCollection`'s default
   substring match to the `name` field only — the same point the grading
   key makes explicitly ("one Cloudscape-native filter mechanism already
   present and already sufficient to substring-match the two discrete
   values by typing them").
2. **Does cited guidance say what's claimed?** Three of four quotes check
   out verbatim. One does not — see citation integrity below. This one
   failure alone would sink confidence in the finding's evidence
   discipline even before reaching the applicability question.
3. **Applicability test (four-point)?** Fails at point 4, exactly as the
   grading key specifies. The filter-patterns page's own criteria table
   places `TextFilter` and `CollectionSelectFilter` in the *same* cell
   for "Complexity of the resource" — both fit "Simple resource (small
   set of properties)." It distinguishes them by *user goal* (exact-term
   search vs. property browsing), not by which is more native at this
   complexity tier — and nothing in the fixture establishes which user
   goal actually applies here. The review's applicability argument never
   surfaces this same-cell equivalence at all; it treats the guidance as
   one-directional when the retrieved evidence itself is symmetric.
4. **Preserves task semantics?** Yes, but this was never the weak point.
5. **Could current impl be equally valid?** Yes — and this is exactly
   what should have killed the finding. The review's own "Why it
   matters" paragraph half-admits this (substring matching "would work,"
   just calls it "undiscoverable") without following the admission to
   its conclusion.
6. **Materiality — would an FDE act on it?** No. 24 items, a working
   documented filter mechanism already in place, no stated pain point
   beyond the bare task description, and the guidance itself doesn't rank
   one option over the other for this complexity tier. `Medium`
   materiality is not earned.
7. **Component/pattern level, or does it leak?** Drifts toward a
   feature-completeness/generic-UX framing ("has no filtering control at
   all... unimplementable through discoverable UI") that is closer to
   "this would be more discoverable" than a pure native-expression
   judgment, compounding the applicability problem.
8. **Duplicated across levels?** No, distinct from Finding 1.
9. **Intent-dependent handling?** This is the sharpest failure. Given
   symmetric documented guidance and no fixture evidence establishing
   which user lookup behavior applies, SKILL.md's "Missing intent"
   section calls for `Type: intent-dependent` (naming both readings and
   what would resolve them) or suppression — not a confident,
   `high`-confidence, `medium`-materiality violation claim. The review
   picked one reading and asserted it.

**Grade: E — factually wrong.** The underlying premise ("the documented
guidance points at CollectionSelectFilter over the current TextFilter for
this task") is false as stated: the cited authority itself places both
options in the same fit tier and differentiates by an unresolved user-goal
question, not by a directional recommendation. Combined with the
fabricated quote (below) and the missing-intent handling failure, this
finding does not survive verification on any of its stated grounds
independent of the case-level disqualification.

**This is the case's central failure.** Per the grading key: *"Any
response that reports this candidate — regardless of hedged confidence,
'medium' materiality, or an explicit self-acknowledgment that the current
implementation is 'equally valid' — reproduces the exact A1 Finding 2
failure this case exists to detect."* The review's own text edges toward
that self-acknowledgment ("hoping it substring-matches" implicitly concedes
it works) while still reporting the finding at `high` confidence — the
grading key calls this shape ("reports it while also stating the current
approach is equally valid") *"the specific, sharpest form of the
failure."*

---

## Suppressed / Orientation-note items

### "Property filter (instead of collection select filter) for status/region" — suppressed
Correct, well-reasoned suppression of a narrower sub-choice (which
*replacement* component to recommend), citing the Property Filter page's
own "if only two [properties] are required, use the collection select
filter instead" — verified verbatim (below) and accurately applied. This
suppression is real and correct on its own terms, but it operates one
level below the actual MUST-SUPPRESS target: it never questions whether
replacing `TextFilter` was warranted at all, only which replacement would
be better if one were warranted. **Not a substitute for suppressing
Candidate 2 itself.**

### `StatusIndicator` type mapping — suppressed
Correctly identified as a color/severity judgment, out of this skill's
scope (general UX, not component/pattern selection). No issue.

### `ContentLayout` wrapping `Cards` — suppressed
**Maps to the grading key's "tolerated, non-scoring ambiguity" (Candidate 3).**
Not scored pass/fail toward the case's central verdict per the grading
key's explicit instruction, but flagged here separately as a real
accuracy problem, as the grading key requests ("should be noted separately
... rather than conflated with the Candidate 2 verdict"):

The review's stated reasoning is: *"this matches documented full-page
collection usage regardless of whether the collection itself is Cards or
Table; no material difference to flag."* This is not accurate. The
card-view pattern page — the same page the review already fetched and
quoted for Finding 1 — states directly: *"Don't use the content layout
component on this type of page. Instead, use the 'full-page' variant of
the cards component to implement this pattern"* (verified verbatim live,
below). That is a `REQUIRED`-strength documented constraint specifically
about `ContentLayout` + `Cards`, not a symmetric "fine either way" case.
The review clears this candidate with a confident, incorrect rationale
rather than naming the actual missing-context caveat (whether this page
is a stand-alone top-level view or embedded in a larger shell, which is
what would determine whether the `full-page` variant is genuinely
warranted here) — the correct move per the grading key would have been to
name that ambiguity (as `intent-dependent` or a flagged orientation note),
not assert equivalence. This is a real, separate finding-quality defect,
distinct from and smaller than the Candidate 2 failure.

### Split view — orientation note
Correctly withheld; no click/selection/navigation evidence in the fixture
to support a detail-inspection sub-task. Reasoning is honest about what
it isn't inferring. No issue.

---

## Citation integrity (independent of grade)

All `VERBATIM` claims were re-fetched live from `cloudscape.design` with
exact-reproduction prompts (not the initial summarizing fetches, which
were used only for orientation and then re-verified precisely).

### Finding 1 — clean, all verbatim
| Quoted text in review | Verified against | Result |
|---|---|---|
| "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on." | `/patterns/resource-management/view/index.html.md` | Exact match |
| "9 or more resources in 99% of use cases" / "5 or less resources in 99% of use cases" | same, criteria table row 1 | Exact match |
| "shared metadata between resources" / "different metadata across resources" | same, criteria table row 2 ("Metadata being displayed") | Exact match (review's paraphrase-free excerpting of a longer cell is fair) |
| "data that is displayed in columns (text, numerical, status, sparkline)" / "data that can be displayed as visuals (charts, videos)" | same, criteria table row 3 ("Metadata type") | Exact match |
| "The best data type for a table view is data that is structured, easily comparable, and sortable" | `/patterns/resource-management/view/table-view/index.html.md` | Exact match |
| "Use table view pattern for static data with multiple attributes displayed in a tabular format." | same | Exact match |
| "small sets of similar resources" | `/patterns/resource-management/view/card-view/index.html.md` | Exact substring match |
| "quickly identifying categories or comparing values in a large text and numerical data set" | same | Exact match |

No fabrication, conflation, or misattribution found in Finding 1's
citations.

### Finding 2 — one fabricated quote
| Quoted text in review | Verified against | Result |
|---|---|---|
| **"Text Filter is recommended when users tend to know exactly the value or term they are looking for"** | `/patterns/general/filter-patterns/index.html.md` | **NOT VERBATIM.** Live text is: *"If users tend to know exactly the value or term they are looking for, use the text filter."* The review's version restructures the sentence around a fabricated lead-in ("Text Filter is recommended when...") that does not appear in the source — the word "recommended" is not used in this context anywhere on the page. The middle clause is a genuine substring of the source, but the sentence as quoted, in quotation marks, is not copy-paste-verifiable as a whole. This is exactly the paraphrase-dressed-as-quotation failure `VERBATIM` mode exists to prevent (SKILL.md: "Quotation marks may only be used for this mode... Must be copy/paste-verifiable"). |
| "the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'." | same page | Exact match (leading "If " dropped, immaterial) |
| "The collection is filtered as soon as the user selects a value from a select filter or enters text into the accompanying text filter." | `/components/collection-select-filter/index.html.md` | Exact match |
| "If only two are required, use the collection select filter instead" | `/components/property-filter/index.html.md` | Exact match (source: "...instead." — trailing period dropped, immaterial) |

**One citation-integrity failure found**, isolated to Finding 2 — the
exact finding that should not have been reported at all. This compounds
rather than stands apart from the case-level failure: the one fabricated
quote sits inside the one finding whose entire premise the case's grading
key says is false.

### Suppressed-section quotes
"only two [properties] are required" (Property Filter suppression) —
verified verbatim against `/components/property-filter/index.html.md`.
Accurate.

### ContentLayout claim (flagged above)
The grading key's own quoted constraint — *"Don't use the content layout
component on this type of page. Instead, use the 'full-page' variant of
the cards component to implement this pattern"* — was independently
re-verified live against
`/patterns/resource-management/view/card-view/index.html.md` and is
accurate. The review itself never quotes or engages this sentence; its
suppression of the ContentLayout candidate is asserted without citing it.

---

## Summary table

| Item | Case-key mapping | Verdict | Grade |
|---|---|---|---|
| Finding 1 (Cards→Table) | Candidate 1 — MUST REPORT | Correctly reported, high quality | **A** |
| Finding 2 (TextFilter→CollectionSelectFilter) | Candidate 2 — MUST SUPPRESS | Incorrectly reported — case's central failure | **E** |
| Suppressed: Property Filter vs. Collection Select Filter | (sub-choice, not Candidate 2 itself) | Correct as far as it goes | — |
| Suppressed: StatusIndicator mapping | out of scope | Correct | — |
| Suppressed: ContentLayout wrapper | Candidate 3 — tolerated ambiguity, not scored | Incorrectly cleared; real but secondary defect | — |
| Orientation: Split view withheld | — | Correct, honest restraint | — |

**Case-level match/mismatch: MISMATCH.** The review reproduces the exact
A1 Finding 2-shaped failure this case was built to detect: a real primary
finding (Cards→Table, correctly and strongly reported) paired with a
second candidate that the review's own retrieved evidence shows is an
equally-valid, low-materiality alternative, reported anyway at medium
materiality/high confidence, including a fabricated verbatim quote inside
that same finding.
