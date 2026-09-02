# Grading key — Case P1: MessageQueues.tsx (real primary + seductive equally-valid alternative)

## Designed intent

This case isolates one narrow question from the eight open items in
`RESULTS-ITERATION-2.md` §4/§11: given a real, material primary finding,
does the reviewer also emit a secondary candidate that its own evidence
shows is an equally-valid, low-materiality alternative — the exact shape
of the observed A1 Finding 2 overreach — or does it correctly suppress
that candidate once it recognizes the equivalence? This is not a recall
test and not a general-applicability test; both are considered settled
by prior iterations and are explicitly out of scope for this case's
adjudication.

Two candidates are pre-adjudicated below. A third, orthogonal ambiguity
(named in "A tolerated, non-scoring ambiguity") is deliberately present
and must not be scored either way on its own.

## Candidate 1 — `Cards` used for a 24-item, explicitly comparison-driven collection instead of `Table`

**Verdict: MUST REPORT.**

- **Type:** `component selection`, materiality high-to-medium (matching
  the precedent set by Case B's own grading key for the structurally
  identical judgment).
- **Repository evidence:** the header's own `description` states the
  task directly: "Compare message throughput and backlog age across
  queues to decide which need scaling attention." 24 items, all sharing
  identical metadata (`status`, `region`, `messagesPerSecond`,
  `oldestMessageAgeSec`) — no images, no charts, no non-columnar content.
- **Cloudscape evidence** (verified live at
  `/patterns/resource-management/view/index.html.md`, the "View
  resources" pattern-family criteria page):
  - Criteria table: "Number of resources in the data set — Table view: 9
    or more resources in 99% of use cases; Card view: 5 or less
    resources in 99% of use cases." 24 clears the table threshold and
    fails the card threshold outright.
  - Criteria table: "Metadata type — Table view: Data that is displayed
    in columns (text, numerical, status, sparkline); Card view: Data
    that can be displayed as visuals (charts, videos)." All four of this
    page's data fields are exactly the table-typed kind; none are
    chart/image content.
  - Prose: "Use a table if the resources share the same metadata, and
    your users will be comparing resources to determine which to take
    action on. Use the card view if users will not be comparing between
    a large number of resources to determine which to take action on."
    — this page's own header copy names exactly the comparison-to-decide
    task this sentence describes.
  - Prose: "Tables are optimized for displaying metadata that can fit
    into data cells, and can be sorted and compared. Cards are optimized
    for displaying non-columnar data, like charts or images."
- **Applicability argument a correct response must make:** (1) task
  materially matches the pattern's own stated comparison-to-decide
  problem, named in the page's own copy, not inferred; (2) current Cards
  implementation solves the same "let an operator see all queues at
  once" problem, just through the discouraged component for this volume
  and data shape; (3) `Table` preserves the identical task — same four
  metrics, same operator goal — only the display component changes; (4)
  material because two independent, quantified criteria (item count,
  metadata type) both point the same direction, and the header's own
  language matches the criteria table's comparison-task language
  directly, not superficially.
- **Boundary check:** this is a component-selection judgment (Cards vs.
  Table for a collection-of-resources display), not implementation
  correctness and not generic UX ("cards feel busy" would be out of
  scope; "the task is comparison and the criteria table says tables are
  for comparison, at this item count" is not).

A correct response may type this `component selection` or `combined
component + pattern`; either is acceptable, consistent with Case B's own
precedent.

## Candidate 2 — `TextFilter` alone vs. adding a `status`/`region` collection select filter

**Verdict: MUST SUPPRESS.**

This is the case's central adjudication target — built specifically to
recreate the decision shape of A1 Finding 2 on fresh material, not to
copy it. `status` (2 values: healthy/backlogged) and `region` (2 values:
us-east-1/us-west-2) are both discrete, low-cardinality columns — exactly
the "one or two properties" zone the filter-patterns doc names as the
collection select filter's fit, and exactly the kind of surface-level
match a reviewer that has just found one real issue might go looking for
a second one on.

It must be suppressed because the retrieved evidence itself establishes
equivalence, not because the alternative is undocumented or the column
count is too low to notice:

- **Cloudscape evidence** (verified live at
  `/patterns/general/filter-patterns/index.html.md`): the page's own
  **criteria table** places `TextFilter` and `CollectionSelectFilter` in
  the *same* cell for "Complexity of the resource": both are listed as
  fitting a "Simple resource (small set of properties)." The page does
  not rank one over the other for a simple resource — it distinguishes
  them by *user goal* ("Find resources that match an exact text query"
  vs. "Find resources with overlapping, defined values"), not by which
  one is more native for this complexity tier.
  - Exact quote: "If the common behavior of users is to filter a
    resource by only one or two properties, use the collection select
    filter. For example: by 'status' or 'type'."
  - Exact quote: "If users tend to know exactly the value or term they
    are looking for, use the text filter."
  - Both conditions are speculative user-behavior claims this file
    cannot evidence either way — the fixture shows no code, comment, or
    header language establishing which lookup mode operators actually
    use, only that the page's task is comparison across the full list
    (already fully addressed by Candidate 1's `Table` recommendation),
    not targeted lookup by either name or property.
- **Materiality:** 24 items, one Cloudscape-native filter mechanism
  already present and already sufficient to substring-match the two
  discrete values by typing them, no stated task friction (no comment or
  copy naming a filtering pain point, unlike A1's "find unattached or
  errored volumes" — this fixture deliberately omits that kind of cue).
  An FDE would not plausibly restructure a working, doc-supported filter
  for this reason alone.
- **Applicability test (SKILL.md "Anti-fundamentalism rule"):** point 4
  fails outright — the difference is not material enough that an
  experienced Cloudscape practitioner would plausibly restructure the
  code over it, because the retrieved evidence places both options in
  the same documented fit tier for this resource's complexity.

Any response that reports this candidate — regardless of hedged
confidence, "medium" materiality, or an explicit self-acknowledgment
that the current implementation is "equally valid" — reproduces the
exact A1 Finding 2 failure this case exists to detect. A response that
reports it while *also* stating the current approach is equally valid is
the specific, sharpest form of the failure (SKILL.md's own "Apply a high
materiality bar" section names "an equally valid alternative" as
something that must not be reported, making this a self-contradicting
finding, not merely a borderline one).

Correctly suppressing this candidate should ideally appear as a named
"Suppressed" entry (the stronger form, as seen correctly done for
`PropertyFilter` in the actual A1 run) — but silent omission is also an
acceptable pass, since SKILL.md permits omitting candidates that
wouldn't be useful to name.

## A tolerated, non-scoring ambiguity — `ContentLayout` wrapping `Cards` vs. the card-view pattern's `full-page` variant

The card-view pattern page (`/patterns/resource-management/view/card-view/index.html.md`)
itself states: "Don't use the content layout component on this type of
page. Instead, use the 'full-page' variant of the cards component to
implement this pattern" — the same "Don't...Instead" shape A1's Finding
1 was built around, this time for `Cards`. This file's single-surface
scope cannot establish whether this page is the app's stand-alone
top-level view or embedded in a larger shell (no surrounding app-layout
context is provided), which is exactly the ambiguity the actual Case B
skill run (`runs/case-b-skill.md`) encountered on the same shape of
fixture and correctly suppressed as secondary/unresolvable from one
file.

**This candidate is not scored pass/fail on its own** — it is orthogonal
to what this case tests (candidate-suppression discipline once a primary
finding is already established, not recall or general applicability,
per this case's explicit charter). Acceptable outcomes: omitted
entirely; named as a suppressed/orientation-note ambiguity (Case B's
precedent); or reported as `intent-dependent` naming the missing
surrounding-shell context. **Not acceptable:** reporting it as a
confident, high-confidence violation-strength finding without naming the
missing-context caveat — that would be a genuine, scorable
missing-intent failure (SKILL.md's "Missing intent" section), but a
distinct one from this case's central target, and should be noted
separately in any writeup rather than conflated with the Candidate 2
verdict.

## What would be wrong, summarized

- **Missing Candidate 1 entirely** (recall failure — not this case's
  primary target, but still a failure if it occurs).
- **Reporting Candidate 2** at any confidence/materiality level —
  the specific, disqualifying failure this case exists to detect.
- **Confidently asserting** the `ContentLayout`/full-page-cards
  candidate without naming the missing-context caveat — a real but
  separate missing-intent failure, not this case's central target.
- **Fabricated or non-verbatim quotation** presented inside quotation
  marks as literal source text for any finding — graded separately under
  citation fidelity, per the task brief, never folded into the
  materiality verdict above.
