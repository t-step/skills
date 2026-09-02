# Adversarial verification — Case A3: Endpoints.tsx

Verifier: independent, no prior context beyond the files listed in the task.
Cloudscape pages were re-fetched directly (raw `index.html.md` via `curl`,
not paraphrased WebFetch summaries, after the first WebFetch pass produced
lossy paraphrases that were unsafe to quote-check against) for:
`components/table`, `patterns/resource-management/view/table-view`,
`components/text-filter`, `components/property-filter`,
`patterns/general/filter-patterns`. Fixture `package.json`/`package-lock.json`
were also inspected to check the review's version-resolution claim, and the
fixture directory was listed to confirm the bounded surface really is the
single file (relevant to Finding 3).

---

## Finding 1 — Full-page resource table wrapped in `ContentLayout`/`variant="container"` instead of the full-page table view pattern

**Grade: A**

Walkthrough of the nine questions:

1. **Task inference supported by evidence, not invented.** The review's
   top-level "Inferred user task" and Finding 1's own "User task" field cite
   the route/page name, the header counter, the "Create endpoint" action,
   the 6-column set, the 26-row count, and (correctly, as verified below)
   the *absence* of any router import or navigation affordance. This is
   fixture-specific, not boilerplate.
2. **Cited authority checks out verbatim.** Re-fetched raw markdown
   confirms every quote:
   - Table docs, Variant section: "This table variant has its own visual
     container with shadows and borders. Use this variant to feature a
     table in a stand-alone container with its own hierarchy... when using
     a table on a details page" (container) and "This variant is for
     implementing the full page table view pattern. Use it for presenting
     and managing a table with many columns within a stand-alone page"
     (full page) — exact matches.
   - Table docs, Header/Collection title: "Use the h1 variant of the header
     component with the full page table. Use the h2 variant of the header
     component with the container table." — exact match.
   - Table View pattern, Don't list: "Don't use the content layout
     component on this type of page. Instead, use the 'full-page' variant
     of the table component to implement this pattern." and "Don't use the
     table view pattern for tables that aren't overly content-heavy.
     Instead, if a table only has a few columns, use a bordered table
     inside the content layout component" — exact matches (the review's
     ellipsis elides only the immaterial "...with the default app layout
     content max-width" clause).
   - Pattern problem statement: "a collection of resources in a tabular
     format. It's effective for quickly identifying categories or comparing
     values in a large text and numerical data set" — exact match, and the
     review's applicability argument quotes it correctly.
3. **Four-point applicability test genuinely passes**, not merely asserted:
   task matches the pattern's stated problem (large text/numerical
   comparison, not a details-page adjunct); current implementation already
   solves the same listing/filtering/paginating problem; the proposed
   `Table variant="full-page"` swap preserves the identical task; and the
   materiality case is unusually strong because the review identifies a
   second, independent piece of corroborating evidence — the fixture
   already uses `Header variant="h1"` (the full-page signal) while wrapping
   it in `Table variant="container"` (the details-page signal), which is a
   genuine internal inconsistency in the code, not something the review
   invented.
4. **Task semantics preserved.** The proposed native expression keeps the
   same header, counter, description, and primary action; only the wrapper
   and table variant change.
5. **No documented "equally valid" escape hatch.** This is a REQUIRED-
   strength "Don't ... Instead" pairing naming this exact composition, not
   a matter of preference the current code could defensibly claim.
6. **Materially actionable.** An explicit prohibition plus a self-
   contradicting h1/container pairing is exactly the kind of thing a
   Cloudscape-fluent implementer restructures rather than notes as a
   preference.
7. **Genuinely component/pattern-level.** The finding is about which of two
   documented table compositions (and which page wrapper) fits this page's
   role — not implementation mechanics or generic UX. No leakage.
8. **Correctly unified**, not split into duplicate component- and
   pattern-level findings — `Type: combined component + pattern` is used
   deliberately, consistent with SKILL.md's guidance against artificial
   splitting.
9. N/A (not `intent-dependent`).

**On the specific test this case was designed for** (genuine task inference
vs. page-shape pattern matching): the reasoning is genuine. It engages
fixture-specific numbers (six columns, 26 rows), explicitly works through
the "few columns" exception with reference to *this* column count rather
than asserting content-heaviness in the abstract, and surfaces the h1/
container mismatch — a piece of evidence unique to this file's actual code
that could not have been copy-pasted from a generic template. It also does
not fall into the trap the grading key specifically calls out: it never
treats the header description/action as evidence *for* keeping
`ContentLayout`; instead, in "Native expression" and in "Orientation notes"
(the "Create endpoint" button placement is separately confirmed as already
matching the documented global-actions-in-header convention), it explicitly
argues the header content already belongs to the full-page pattern's own
header building block. This matches the grading key's "ideal" answer shape
even though the review doesn't cite the exact building-block sub-line
("Actions - optional: Actions in the header — refer to global actions") by
name in Finding 1 itself (it's substantively present via the Orientation
notes item).

**One completeness gap, not a substance problem:** SKILL.md's Finding
contract requires an explicit `Authority strength` label
(`REQUIRED`/`RECOMMENDED`/`OPTIONAL`/`INFERRED`) on every finding. Finding 1
never writes this label as its own field (Finding 3 does, parenthetically).
The cited "Don't ... Instead" quote makes the strength unambiguously
REQUIRED in substance, so this doesn't change the grade, but it is a literal
contract-compliance omission worth flagging.

Why an FDE would act on it: it's a named, explicit "don't do this, do this
instead" rule being violated on the account's canonical endpoint inventory,
corroborated by an internal h1/container inconsistency already present in
the code — not a stylistic nudge.

---

## Finding 2 — `TextFilter` where the column set matches Cloudscape's `PropertyFilter` profile

**Grade: B**

1. Task inference reasonable and grounded in the actual column shape
   (`status`, `region`, `model` as small discrete-valued columns).
2. Citations check out against the re-fetched raw pages: text-filter Don't
   — "Don't use a text filter for collections that have a large set of
   values; use the property filter instead" (exact match). Property-filter
   Do list — "Use multi-select tokens for properties with discrete values
   or finite sets of numeric values. For example, *State = Active,
   Pending, Canceled*" (exact match, confirmed in the raw fetch at
   `## General guidelines / ### Do`). Filtering-patterns page criteria
   table (simple vs. complex resource) also checks out.
3. **Applicability is real but weaker than Finding 1's.** There's a small
   tension the review surfaces honestly but doesn't fully resolve: the
   text-filter "Don't" is keyed to a collection having "a large set of
   values," but this fixture's discrete columns each have only 3 distinct
   values (3 statuses, 3 regions, 3 models) — a small, finite set, which is
   arguably a different scenario from "a large set of values" than the one
   that Don't clause is warning about. The stronger, more precisely-on-
   point support is actually a different citation the review does use
   correctly — property-filter's own "discrete values/finite sets" Do-item
   and its separate "more than two properties" threshold (not quoted by
   the review, but independently confirmed here: "Use a property filter
   pattern if users need more than two properties to find a specific item.
   If only two are required, use the collection select filter instead" —
   3 discrete properties clears that bar). So the underlying recommendation
   holds up, but the specific "large set of values" citation is a slightly
   loose fit for this fixture's actual small value-cardinality, which is
   the kind of imprecision that should cost some confidence.
4. Native expression (`PropertyFilter` with `tokenType="enum"` for
   status/region/model plus free text for `id`) preserves the same
   filtering task exactly.
5. **The current `TextFilter` has real documented cover.** The table-view
   pattern's own "Filter - optional" building block illustrates a generic
   text filter for this exact pattern slot: "Text filter helps users with
   an extensive number of table rows to quickly find one or several
   resources with a matching query" (confirmed verbatim in the raw fetch).
   The review surfaces this counter-evidence itself and argues the
   component-level guidance is more specific and controlling — a fair
   argument, but it means this finding sits closer to "a documented,
   defensible reason the code already does this" than Finding 1 does,
   which had no such competing authority.
6. Plausibly actionable for an FDE, but with 26 rows and only three small
   enum columns, this reads as a real improvement rather than a must-fix —
   consistent with `Materiality: medium-high` as self-labeled (not `high`).
7. Genuinely component-selection, no drift into implementation or generic
   UX.
8. Correctly kept as its own separate finding (not an artificial split of
   Finding 1 — different underlying concept, filter component vs. table
   variant).
9. N/A.

Why an FDE would plausibly act on it: three independently-filterable enum
columns plus a `failed` status value is close to the textbook property-
filter profile the docs give as their own worked example, even if the
"large set of values" citation specifically is a stretch.

---

## Finding 3 — First (identifier) column doesn't navigate to a details view

**Grade: B**

1. Task framing (whether an endpoint is individually addressable) is
   plausible and explicitly tied to the `failed`/`updating` status values
   observed in the data.
2. Citation checks out: Table docs, Columns/Do — "Use the first table
   column for unique identifiers of the items that are represented in the
   table (for example: name, id, and ARN). Also use the first table column
   for users to navigate to a details page that shows more information
   about the item." (exact match, confirmed in raw fetch). Correctly
   labeled `RECOMMENDED` (a "Do," not a "Don't... Instead" prohibition) —
   this is the one finding that does write out the authority-strength
   label explicitly.
3. Applicability is honestly incomplete by design — the finding states
   plainly that the bounded file can't establish whether a details route
   exists, which is verified accurate: the fixture directory contains only
   this single file (confirmed by listing
   `evals/cloudscape-native-expression-review/cases/case-a3-endpoints/fixture/src`),
   and the file itself has no router import, `Link`, `onClick`, or `href`
   on the `id` cell (confirmed by re-reading the file, lines 77–84).
4. N/A in the decisive sense — the finding explicitly declines to assert
   which native expression is correct pending missing evidence, which is
   the correct move for genuinely unresolvable intent per SKILL.md's
   "Missing intent" section.
5. The current plain-text cell is honestly acknowledged as possibly already
   correct if no details page exists.
6/7. In scope (a documented column-role convention), correctly not
   overreaching into "add a Link here" as a confident recommendation.
8. Correctly kept separate from Finding 1 (different underlying concept:
   row-level navigation affordance vs. page-level variant/wrapper).
9. **This is the question this finding exists to test, and it passes
   cleanly**: it names both plausible readings (terminal summary table vs.
   entry point to a details page), names what would resolve it (whether an
   endpoint details route exists elsewhere in the app), and explicitly
   declines to guess — "Reporting a confident 'add a Link here'
   recommendation would guess at product intent the evidence doesn't
   establish." This is textbook correct `intent-dependent` handling, not a
   guess dressed up as caution.

Why it's `B` rather than `A`: by construction an `intent-dependent` finding
is non-decisive — useful to keep in a review as a flagged ambiguity, but not
a finding an FDE acts on today. That's a `B` outcome under the rubric's own
definition, not a flaw in execution.

---

## Case-level verdict: **match**

The grading key names Finding 1 as this case's primary designed target:
one material `pattern composition`/`combined` finding, reached by inferring
the task from route/copy/actions/data (no comment exists in this fixture,
unlike A/A1) rather than by page-shape matching, correctly working through
the few-columns exception and correctly not treating the header
description/action as evidence for keeping `ContentLayout`. The review's
Finding 1 satisfies every element of that description, with citations that
check out against freshly re-fetched Cloudscape pages and reasoning that is
visibly tied to this fixture's specific numbers and specific internal
inconsistency (h1 header + container table) — not a copy-pasted conclusion
from Case A/A1. None of the "what would be wrong" failure modes in the
grading key occurred: the finding was not missed, not suppressed as
low-materiality, and not asserted via silent page-shape pattern-matching
without stated inference.

The two additional findings (2 and 3) are real, correctly-cited, in-scope
findings that the case's grading key doesn't require but also doesn't
penalize — they don't contradict or dilute the primary designed finding,
and Finding 3 in particular is a clean demonstration of the skill's
`intent-dependent` discipline working as intended on a genuinely
ambiguous point.

## Summary of grades
- Finding 1: **A**
- Finding 2: **B**
- Finding 3: **B**
- Case-level verdict: **match**
