# Verification — Case F: QuotaRequests.tsx

Verifier method: read rubric.md, grading key, both reviews, and the fixture
source (`QuotaRequests.tsx`, 137 lines). Independently re-fetched every cited
Cloudscape URL with a JS-rendering browser (Playwright, reading
`document.body.innerText` after the SPA's client-side tab router settled —
plain WebFetch/defuddle only returned the pre-render shell for this site, so
those citations were confirmed against the rendered page instead) to check
whether the quoted language is real and complete, not just present.

Pages independently re-read: Modal usage, Table usage, Split panel usage
(partial — Secondary panels page covers the same "primary component" line),
Split view pattern, Secondary panels pattern, Delete patterns, Resource
details pattern, Table view pattern.

## Fixture ground truth

`QuotaRequests.tsx`: a `Table` (`variant="full-page"`, 3 rows, 5 columns, no
sort/filter/pagination) with a per-row "View" `Button` (`variant="inline-link"`)
that opens a `Modal` showing all 6 fields of the selected request via
`KeyValuePairs`, plus a conditional `Withdraw request` footer button when
`status === 'pending'`. The file's own comment (lines 58-63) states nothing
else links to an individual request and there is no per-request route. This
matches both reviews' "inferred user task" sections.

---

## Baseline findings

### Baseline Finding 1 — Modal → Split panel

**Grade: E — factually wrong.**

Driving questions: **2, 3, 5** (primary), **9** (secondary).

The individual quotes baseline pulls are real (verified verbatim on the
Split panel/Secondary panels/Resource-details/Split-view pages), but the
conclusion misrepresents what the guidance collectively says. The Split
view pattern page's own "Key UX concepts" section — not quoted by
baseline — states directly:

> "Split view is not a replacement of details page ... Always use details
> pages to display full resource details of a single resource. A split
> view should never replace details pages in the service information
> architecture."

and its objectives are explicitly "resource identification within a group
of similar resources," "monitoring," and "troubleshooting" across
resources — none of which describe "review the complete field set of one
already-selected request." The Resource-details pattern page reinforces
this: split view is framed as providing "a subset of resource details"
*alongside* a full details page, not as a replacement for a full-detail
view. The Modal here already shows the complete 6-field record of one
resource (i.e., the details-page-shaped case), so converting it to a
Split panel is precisely the move Cloudscape's own docs say not to make.
This is not a case of "the docs contain another example dressed as a
recommendation" (Q3 fails) — it's the docs affirmatively rejecting the
proposed direction (Q5: the current Modal usage is at minimum equally
valid, arguably better-supported).

This also lands on the grading key's explicitly named trap: "misreading
this as resembling Case E's rejected split-view temptation ... factually
wrong regardless of directional confidence." Baseline's finding is exactly
that misreading. It also never engages with the case's actual
missing-intent question (transient vs. persistent/addressable resource) —
it asserts a specific architectural change with full confidence throughout
(Q9 fails independently of the factual error).

An FDE would not act on this — and if they looked up the cited split-view
page themselves (one hop past baseline's quotes), they'd find the page
arguing against the exact change being proposed.

### Baseline Finding 2 — Withdraw action → dedicated confirm modal

**Grade: D — overreach / weak applicability.**

Driving questions: **1, 3, 6** (primary), **2** (secondary).

The Delete-patterns quotes are accurate (verified verbatim), but applying
"delete with simple confirmation" criteria to "withdraw a pending quota
request" is an unestablished analogy. The delete-pattern criteria table is
about running infrastructure, cascading breakage, and backend
recreate-cost ("the resource takes hours on the backend to spin up") —
none of which the fixture supports for a quota-request record; the "cost
to redo (re-filing the request)" framing is invented, not evidenced (Q1).
Separately, the "Never launch another modal from within a modal" citation
doesn't actually describe a problem with the *current* code (which has one
modal, not a nested pair) — it's the finding's own proposed fix (open a
second confirm modal) that would need to avoid nesting, so the citation is
aimed at the wrong target (Q2 concern, secondary). Modal's own usage docs
list "Use an action button to act on the entire contents of a modal. For
example: Save, Delete, Done, Cancel" as a documented Do — meaning a single
conditional footer action living in a view modal is already
Cloudscape-normal, undercutting the premise that this needs restructuring
(Q6). The finding is also structurally dependent on Finding 1's
already-invalid Split-panel premise ("Once finding 1 moves..."), compounding
the applicability problem. An FDE would not restructure a 3-item fixture's
single conditional button into a second confirmation modal on this basis.

### Baseline Finding 3 — Sticky header + `awsui-h1-sticky` for full-page table

**Grade: C — technically plausible but routine/low-value.**

Driving question: **6** (materiality), confirming **2** (citation accurate).

Verified verbatim on both the Table usage page ("We suggest enabling the
sticky header and using the 'awsui-h1-sticky' variant of the header with
this variant...") and the Table-view pattern page ("Enabling a sticky
header is optional, but recommended, for these potentially lengthy list
pages"). The citation is accurate and the guidance is real component/pattern-level
material (not implementation minutiae — it's a named building block of the
Table-view resource-management pattern). But baseline itself correctly
flags that the general sticky-header trigger criteria (30+ items, 5+
columns, sortable columns) don't apply to this 3-row, unsorted, 5-column
sample, and the pattern page's own qualifier — "potentially lengthy list
pages" — signals this is exactly the kind of low-materiality catch the
skill's discipline should suppress at this fixture's scale. Correct, but
not something an FDE restructures a 3-row table over.

### Baseline case-level verdict

**Mismatch — failed the case.** The centerpiece finding (1) is a confident,
undiscussed recommendation to restructure the surface, built on cherry-picked
quotes that omit the source page's own explicit disclaimer against the exact
move being proposed. Baseline never surfaces the transient-vs-persistent
ambiguity that is this case's actual design point; it treats the "correct"
answer as self-evident and argues for one specific architectural direction
(Split panel) throughout, then stacks a second, weakly-applicable finding on
top of it. Only Finding 3 is a legitimate, if low-value, catch.

---

## Skill-guided findings

**Findings: None** (skill's own header). Two candidates are named and
explicitly suppressed rather than reported; several are logged as
"Orientation notes" (non-findings).

### Skill — Suppressed candidate: Split view instead of Modal

**Assessed as correctly suppressed — high-quality calibration (would be
A-grade reasoning if reported as a finding rejecting the alternative).**

Driving questions: **2, 3, 9**.

The quoted "Key UX concept" line ("Always use details pages to display
full resource details of a single resource. A split view should never
replace details pages...") is verified verbatim accurate — this is the
exact passage that invalidates baseline's Finding 1. The applicability
reasoning (split view's objectives are group identification/monitoring/
comparison, not single-item full-record review) is sound and matches the
page's own stated "Objectives" section. This is precisely the correct,
well-evidenced rejection of the trap the grading key names.

### Skill — Suppressed candidate: Details page instead of Modal

**Assessed as correctly suppressed, and substantively addresses the
missing-intent question even without the literal label
`intent-dependent`.**

Driving question: **9**.

The reasoning ("no per-request route, nothing else links to an individual
request... adopting a details page would mean inventing routing/IA this
task doesn't have") names the alternative reading (persistent/addressable
resource) and explains precisely why current evidence doesn't support
acting on it — functionally equivalent to naming "what evidence would
resolve it" as the grading key asks, even though it frames the decision as
"out of scope" rather than using the word "intent-dependent." Combined
with the Split-view suppression above, the two entries together name both
plausible readings from the grading key (transient/resolved-and-forgotten
via Modal vs. persistent/addressable via a details or split-view
treatment) and decline to assert either with unsupported confidence — the
explicitly sanctioned correct outcome.

### Skill — Orientation notes (non-findings, spot-checked)

- Table `full-page` variant as primary surface — accurate, standard usage.
- `Button variant="inline-link"` instead of `Link` for "View" — correct
  call: no route exists to navigate to, so a non-navigating action control
  is the right primitive, consistent with the fixture's own no-route
  comment.
- Modal + KeyValuePairs framed as "not a documented deviation" — this
  reads as a claim about docs-compliance, not a confident product verdict;
  read alongside the two suppressions immediately above (which do engage
  the alternative reading), this does not cross into the "confidently
  asserting Modal is correct with no acknowledgment of the alternative
  reading" trap the grading key warns against. One caveat: the supporting
  claim that the Table-view pattern page "explicitly leaves the
  detail-viewing mechanism open to the implementer" slightly overstates
  the source — the page simply doesn't address per-row detail-viewing
  mechanics at all (no building block covers it), rather than explicitly
  declaring it an open choice. Minor imprecision, not consequential since
  this is an orientation note, not an acted-upon finding.
- `StatusIndicator` type mapping (`pending`→`in-progress`,
  `approved`→`success`, `denied`→`error`) — matches documented status-type
  semantics; trivial, uncontroversial.
- "What was not evaluated" section correctly scopes out the
  withdraw-confirmation-step question as implementation/UX mechanics
  rather than component/pattern selection (Q7 boundary respected).

### Skill case-level verdict

**Match — correctly handled the case.** The skill considered exactly the
two live alternatives (Split panel, Details page), verified their
applicability against the real pattern pages rather than treating pattern
existence as a mandate, found both wanting given the evidence the fixture
actually provides, and reported zero findings while transparently
documenting what was considered and why it was suppressed — the outcome
the grading key calls "acceptable and correct," executed with more
rigor than the minimum (silent suppression) would have required.

---

## Summary table

| # | Source | Finding | Grade | Driving Qs |
|---|--------|---------|-------|------------|
| 1 | baseline | Modal → Split panel | **E** | 2, 3, 5, 9 |
| 2 | baseline | Withdraw action → dedicated confirm modal | **D** | 1, 3, 6, 2 |
| 3 | baseline | Sticky header + `awsui-h1-sticky` | **C** | 6, 2 |
| — | skill | Split view — suppressed | (correct suppression, A-quality reasoning) | 2, 3, 9 |
| — | skill | Details page — suppressed | (correct suppression, addresses missing intent) | 9 |
| — | skill | Findings: None | case-level **match** | 9 |

**Case-level verdict:** baseline **mismatch/failed** (confident, factually
contradicted recommendation on genuinely missing intent, plus a dependent
overreaching second finding); skill **match/passed** (correct suppression
of both directional temptations with accurate, verified citations, zero
confident findings reported).
