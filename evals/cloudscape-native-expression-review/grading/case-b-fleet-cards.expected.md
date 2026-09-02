# Grading key — Case B: EndpointScaling.tsx (wrong component, otherwise reasonable composition)

## Designed intent

`Cards` is used mechanically correctly (`cardDefinition`, `trackBy`,
`cardsPerRow`, `ariaLabels` all present and well-formed) — no
implementation defect to hang a finding on. The page composition around
it (`ContentLayout` + `Header` with a task-describing `description`) is
ordinary and not itself a finding. The only issue is the component
choice: 22 endpoints, all sharing identical numeric/status metadata, with
the header's own copy stating the task explicitly — *"Compare request
volume, latency, and error rate across endpoints to decide which ones
need to scale."*

## What a correct response looks like

**One material finding, `Type: component selection`, high-to-medium
materiality.**

- Cites the "View resources" pattern-family guidance: *"Use a table if
  the resources share the same metadata, and your users will be
  comparing resources to determine which to take action on"* / *"Table
  columns allow for the same metadata type to be displayed across all
  resources, and allow for easy scanning and comparison"* vs. card view's
  own stated fit — *"effective for glancing at small sets of similar
  resources"* / cards suit cases where "users will not be comparing
  between a large number of resources" and favor "non-columnar data, like
  charts or images."
- Applicability argument addresses both prongs directly: (a) this data
  is exactly the "same metadata type" case tables are for — five
  identical numeric/status fields, no images, no non-columnar content;
  (b) the task is explicitly comparison-and-action-driven, stated in the
  page's own copy, not inferred; (c) 22 is not "a small set."
- Native expression: `Table` (with sortable columns per metric, so a
  user can sort by error rate or latency directly) — this is the part of
  "why it matters" that should feel concrete: Cards forces re-scanning
  every card to find the worst performer, Table lets the user sort once.
- Boundary check: this is squarely component selection (Cards vs. Table
  for a collection-of-resources display), not implementation correctness
  (both would be equally "correctly implemented" as Cards or Table) and
  not generic UX ("cards feel cluttered" would be out of scope; "the
  task is comparison and the doc says tables are for comparison" is not).

## What would be wrong

- **Missed entirely**: recall gap — treating "Cards is a documented,
  valid component with a valid cardDefinition" as sufficient and stopping
  there, without asking whether it fits *this* task.
- **A finding that cites only "Table exists and could show this data"
  without engaging the comparison-task evidence or the collection-size
  evidence**: this is exactly the "component existence treated as
  mandate" failure mode this skill's anti-fundamentalism rule exists to
  prevent, even though the underlying recommendation happens to be
  correct — grade as D on applicability-reasoning grounds regardless of
  the right conclusion.
- **Framed as a `pattern composition` finding instead of `component
  selection`**: not wrong enough to fail the case, but worth noting — this
  is a same-family-of-patterns (view resources) component swap, not a
  composition-structure mismatch; the cleaner type label is `component
  selection`.
