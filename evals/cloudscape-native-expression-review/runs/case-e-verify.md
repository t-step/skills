# Verification — Case E: Certificates (list + details)

Fixture verified against: `cases/case-e-certificates/fixture/src/pages/CertificatesTable.tsx`,
`.../CertificateDetails.tsx`. Cloudscape authority verified live via rendered pages
(static WebFetch failed to render Cloudscape's tabbed component pages — JS-rendered
SPA — so Table/Link/BreadcrumbGroup/Button/Collection-select-filter/Split-panel usage
tabs were confirmed via a real browser (Playwright); Patterns pages such as
filter-patterns, collection-hooks dev guide, and the Details page pattern rendered
statically and were cross-checked the same way).

## Central diagnostic question: split view / SplitPanel

**Neither review mentions split view, `SplitPanel`, or the split-view pattern
anywhere** — not as a recommendation, not as an explicit rejection. I searched both
files for "split" and "panel" in that sense; no hits in either.

Confirmed via the live Split panel component usage page (`Don't` list): *"Don't use
the split panel to replace the details page."* This is the real doc language behind
the grading key's premise — the temptation is genuinely a documented anti-pattern, so
a review that recommended it would be flatly wrong (grade E territory), and a review
that explicitly named and rejected it would be the strongest possible outcome for this
case.

**Case-level verdict — both runs: SILENT (weaker than the ideal, but not wrong).**
Per the grading key, silence is "not wrong on its face... but weaker evidence... than
an explicit rejection." Neither run recommended split view (so neither is a
false-positive failure, no D/E on this specific axis), but neither earns the stronger
credit of a visible, auditable rejection either.

- **Baseline**: no structural equivalent of an "orientation notes" section at all;
  nothing in the review shows split view was ever considered. Weakest form of
  silence — indistinguishable from never having looked.
- **Skill**: has an "Orientation notes" section that does real, evidenced pattern-
  fit checking — it explicitly confirms `CertificateDetails.tsx` matches the Details
  page building blocks A–G, and explicitly checks the nested table item counts (3, 2,
  3) against the Details page pattern's own "more than 10 items → use Details page as
  a hub" threshold (confirmed live: real quote). That is the *right kind* of
  diligence this case is designed to reward, and it directly rules out one adjacent
  temptation (hub pattern) with citation — but it never names split view/`SplitPanel`
  specifically, so it does not claim the strongest possible credit either. Better
  process, same technical verdict as baseline on this exact axis.

## Baseline findings

### 1. Row navigation as `Button`+`onClick` instead of `Link` on the row-header cell — **B**

- **Repo evidence (Q1):** Confirmed exact — `CertificatesTable.tsx` lines 55-56
  (`isRowHeader: true`, `cell: (c) => c.domain`, plain text) and lines 66-75 (separate
  `actions` column, `Button variant="inline-link" onClick={() => navigate(...)}`, no
  `href`).
- **Cited authority (Q2):** The Link component's `onClick`/`onFollow` quote is
  **verified word-for-word** via the live API tab: *"Called when the user clicks on
  the link. Do not use this handler for navigation, use the onFollow event
  instead."* The specific "playground source" row-header code snippet
  (`<Link href="#">{item.name}</Link>` with `isRowHeader: true`) could not be
  independently reproduced — the Playground tab renders as an async live demo that
  did not resolve to inspectable text — but the *same underlying claim* (first
  column should carry the identifier and the navigation entry point) is
  independently confirmed via the Table Usage tab's real "Do" list: *"Use the first
  table column for unique identifiers... Also use the first table column for users to
  navigate to a details page..."* So the substantive claim holds even though the
  specific citation is unverifiable as stated.
- **Applicability / semantics (Q3, Q4):** Passes — same destination, same task,
  genuinely the documented first-column convention.
- **Scope (Q7):** This is where it loses ground. The finding's header names a
  component swap (Button → Link), which is legitimately pattern/composition-level,
  but the "why it matters" section argues almost entirely from anchor-semantics/
  accessibility mechanics (Ctrl/Cmd+click, middle-click, right-click "copy link
  address", status-bar URL preview) — and the review itself calls Finding 4 "the
  mirror image of Finding 1," explicitly framing both as the same onClick-vs-onFollow
  issue. That reasoning is `cloudscape-implementation-audit` territory, not
  component/pattern selection, even though the recommended fix (use `Link`) is
  correctly pattern-shaped.
- **FDE verdict:** A real, actionable comment an FDE would likely act on, but for
  reasons that are half pattern-selection, half implementation-mechanics — weaker
  than the skill's version of the same underlying issue (see skill Finding 1), which
  keeps the reasoning cleanly at the composition level.

### 2. `TextFilter` only, despite a closed-enum `status` — **B**

- **Repo evidence (Q1):** Confirmed — `Certificate.status` is a 3-value enum,
  `TextFilter` is the only filter used.
- **Cited authority (Q2):** Both quotes verified live and exact: filter-patterns page
  — *"If the common behavior of users is to filter a resource by only one or two
  properties, use the collection select filter. For example: by 'status' or
  'type.'"*; Collection select filter's own Usage tab — *"Use a select filter for
  commonly used properties and values"* / *"Property: Status; Values: Error,
  Loading, Pending, Stopped, and Success."*
- **Applicability (Q3):** Real gap — a closed 3-value status enum is exactly what
  `CollectionSelectFilter` is for. But two things weaken the case: (a) the claim that
  "show me what's expiring/expired" is "the primary triage query" is an inference
  about user behavior not directly evidenced in the fixture (no comment or copy
  establishes this priority — it's plausible, not established); (b) the same
  Collection select filter page's own "Don't" list — *"Don't use filtering if the
  majority of your users operate on small collections of resources (fewer than five
  resources)"* — is directly relevant to this 4-row fixture and is never addressed,
  even though the skill review reasoned through the analogous threshold question for
  a different feature (filtering/pagination on the same table) and treated the mock
  data size as non-dispositive. Baseline doesn't do that reasoning here, so the
  applicability argument is incomplete on its own terms.
- **FDE verdict:** Real and useful, additive (not a replacement) recommendation, but
  not fully decisive — the confidence in "primary query" is somewhat asserted rather
  than evidenced, and the small-collection caveat from its own cited page goes
  unaddressed.

### 3. `noMatch` dead-code override via static `empty` prop — **D**

- **Repo evidence (Q1):** Confirmed exact and technically correct — `{...collectionProps}`
  spreads first (line 43), a literal `empty="No certificates"` prop appears later in
  the same JSX element (line 79) and wins, permanently discarding whatever
  `collectionProps.empty` resolves to (including the `noMatch` copy configured at
  lines 35-39). This is a real, material functional bug — filtering to zero results
  will show "No certificates" instead of "No matching certificates."
- **Cited authority (Q2):** collection-hooks dev guide quotes on `empty`/`noMatch`/`collectionProps`
  confirmed accurate.
- **Scope (Q7):** This is squarely a props-ordering / API-usage mechanics bug — a
  JSX spread-then-override mistake — not a component or pattern selection question.
  It belongs to `cloudscape-implementation-audit`'s domain, not this skill's mandate.
  Being real and material doesn't rescue it from being out of scope for a
  component/pattern-alignment review; the citations give it a patina of
  pattern-level grounding (Table view pattern's "zero results state" language) but
  the underlying defect is pure implementation mechanics.
- **FDE verdict:** An FDE would fix this, but it's not the kind of finding this
  review type should be surfacing — it dilutes the report's focus.

### 4. Breadcrumb `href` without `onFollow` — **D**

- **Repo evidence (Q1):** Confirmed exact — `CertificateDetails.tsx` lines 36-42, no
  `onFollow` wired to the `react-router` navigation used elsewhere in the same
  surface.
- **Cited authority (Q2):** Confirmed word-for-word via the live BreadcrumbGroup API
  tab — *"Called when the user clicks on a breadcrumb item. Do not use this handler
  for navigation, use the onFollow event instead."* / onFollow's description matches
  too.
- **Scope (Q7):** Same issue as Finding 3 — this is an event-handler wiring/API-usage
  defect (which prop to bind to the router), not a question of whether `BreadcrumbGroup`
  is the right component (it is — confirmed against the Details page pattern's
  building block A) or whether the breadcrumb pattern applies. Out of scope for
  component/pattern-level review; `cloudscape-implementation-audit`'s domain.
- **FDE verdict:** Real, correctly cited, would get fixed — but it's a mechanics bug
  wearing a Cloudscape citation, not a pattern-alignment finding.

## Skill findings

### 1. "View details" navigation belongs on the identifier column, not a separate Actions column — **A**

- **Repo evidence (Q1):** Confirmed exact, same lines as baseline's Finding 1.
- **Cited authority (Q2):** Both citations verified live and accurate: Table Usage
  tab "Do" list — *"Use the first table column for unique identifiers... Also use
  the first table column for users to navigate to a details page that shows more
  information about the item"* and *"Use the primary link variant instead of the
  secondary link variant in table cells... to help users distinguish links from
  other text content in adjoining cells"*; Button Usage tab — *"Inline link... Use
  this so as not to impact the height of the table row... For example: A download
  button placed in table cells within the actions column in a table."* All
  quoted accurately, not stretched.
- **Applicability (Q3):** The review lays out its own explicit four-point argument
  (task match, current code already solves substantially the same problem, fix
  preserves the same destination, materiality/collision with the Actions column's
  documented purpose) — this is exactly the discipline the rubric's applicability
  test asks for, done visibly rather than asserted.
- **Semantics preserved (Q4):** Yes — same route, same identifier, only the
  column/component changes.
- **Equally-valid alternative (Q5):** Addressed and rejected with a real reason
  (today's Actions column exists solely to hold a navigation link with no other
  action content, which collides with the Button/inline-link doc's own stated
  purpose for that column).
- **Materiality (Q6):** High — this is the kind of "first column" convention
  violation an FDE reviewing any Cloudscape table would flag.
- **Scope discipline (Q7):** The review includes an explicit "Boundary check" line
  distinguishing this from an implementation defect and from generic UX opinion —
  correctly self-polices the exact boundary that both of baseline's D-graded
  findings failed to observe.
- **No duplication (Q8):** Correctly filed as one `combined component + pattern`
  finding rather than splitting the column-selection and Button-vs-Link angles into
  two findings.
- **FDE verdict:** Materially real, tightly scoped, well-evidenced — an experienced
  FDE would plausibly restructure this column on the strength of the cited "Do"
  guidance alone.

## Suppressed items and orientation notes (skill run) — not graded as findings, noted for calibration

These were correctly *not* reported, and the reasoning behind each is sound:
- Attached-resources-as-own-resource-links: correctly withheld as intent-dependent
  (can't establish from this bounded surface whether an ALB details route exists) —
  good instance of Q9 discipline (name the ambiguity, don't guess).
- Filtering/pagination/sorting on a 4-item table: correctly suppressed against the
  Table page's own real "more than five items" threshold (confirmed live), with an
  explicit, reasonable rationale for not over-reading mock-data size as the true
  fleet size.
- `awsui-h1-sticky` header variant: correctly identified as implementation/props-level
  and out of scope — this is precisely the self-policing baseline's Findings 3 and 4
  needed and didn't apply to themselves.
- Breadcrumb missing a "service name" tier: correctly deferred as outside the bounded
  two-file surface.

The orientation notes' confirmation that `CertificateDetails.tsx` matches the Details
page building blocks A–G, and that none of its three nested lists cross the
"hub pattern" item-count threshold, were both checked against real, live-rendered
doc text and are accurate.

## Summary

| Source | Finding | Grade | Key driver |
|---|---|---|---|
| baseline | Row nav: Button→Link | B | real + cited accurately, but reasoning leans into a11y/implementation mechanics (Q7) |
| baseline | TextFilter → CollectionSelectFilter | B | real + cited accurately, but "primary query" claim under-evidenced and own cited small-collection caveat unaddressed (Q1/Q3) |
| baseline | noMatch dead-code override | D | real bug, but pure props-ordering mechanics — out of scope (Q7) |
| baseline | Breadcrumb missing onFollow | D | real bug, but pure event-wiring mechanics — out of scope (Q7) |
| skill | Identifier column should carry nav | A | evidenced, applicability test shown explicitly, correctly scoped, no duplication |

**Case-level verdict:** Both runs avoid the false-positive failure mode (neither
recommends split view), so neither is a D/E on the central axis. Neither, however,
produces the explicit, citation-backed rejection the grading key treats as the
strongest possible response — both are "silent" on split view specifically. The
skill run's silence is better-supported by visible, correct adjacent reasoning
(Details-page-as-hub threshold check) that suggests the same discipline would likely
have caught and rejected split view had it been prompted to consider it; baseline
shows no comparable evidence of having looked at all. On the findings that *are*
reported, the skill run is cleaner and more disciplined about staying at the
component/pattern level (1-for-1 A), while baseline mixes two real, well-cited
findings that overreach into implementation-mechanics territory (2x D) with two
weaker-but-real pattern-level findings (2x B).
