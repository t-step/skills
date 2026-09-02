# Grading key — Case A: FleetNodes.tsx (right components, wrong pattern)

## Designed intent

Every local Cloudscape mechanic in `FleetNodes.tsx` is mechanically
correct: `Table` + `useCollection` + `TextFilter` + `Pagination` +
`CollectionPreferences`, correct `ariaLabels`, `filteringAriaLabel`,
`trackBy`, sorting fields — nothing here belongs to
`cloudscape-implementation-audit`. The page's entire content is the
table, wrapped in `ContentLayout` with `Table variant="container"`. This
is a clean instance of the table-view pattern's own explicit rule (see
below) with none of the ambiguity the real `Identities.tsx` fixture has
(no error banner, no header action, no non-table content at all) —
deliberately less ambiguous than that real fixture so this case can be
adjudicated on its own.

## What a correct response looks like

**One material finding, `Type: pattern composition` (or `combined
component + pattern` if the response frames the `variant="container"` →
`variant="full-page"` swap as itself a component-prop-level change tied
to the pattern), high materiality.**

- Cites the table-view pattern page's own language: *"Don't use the
  content layout component on this type of page. Instead, use the
  'full-page' variant of the table component to implement this pattern"*
  and *"Use table view pattern for static data with multiple attributes
  displayed in a tabular format... structured, easily comparable, and
  sortable."*
- Applicability argument addresses why the exception ("if a table only
  has a few columns, use a bordered table inside content layout instead")
  does not apply here: 7 substantive columns, explicitly content-heavy,
  matches "large text and numerical data set."
- Authority strength: `REQUIRED` — this is a direct "Don't... Instead"
  pairing, not a soft preference.
- Native expression: `Table variant="full-page"` (typically paired with
  `AppLayout`'s `contentType="table"`, though that prop lives outside the
  reviewed file — a correct response should say so rather than silently
  assuming it, since the surface only shows the page component).
- Boundary check should distinguish this from implementation correctness
  (nothing here is an incorrect prop or a11y gap on the *chosen* variant —
  the variant/wrapper choice itself is what's wrong) and from general UX
  (this isn't "the page feels dense," it's a documented pattern rule).

## What would be wrong

- **Missed entirely** (silence): a real recall gap — this is the case's
  primary purpose, so a clean report here is the single most important
  negative signal this case can produce.
- **Reported at `REQUIRED` implementation-audit-style "violation"
  language while also citing implementation-level framing** (props,
  a11y, tokens) rather than pattern-composition framing: scope confusion
  between this skill and its sibling, even if the underlying observation
  is correct.
- **Additional, unrelated implementation-shaped findings** (e.g., a
  claimed a11y or styling defect): out of scope for this skill regardless
  of correctness; a response that reports them alongside the real finding
  should have them read as scope leakage, not bonus value.
- **Suppressed as low-materiality or "equally valid"**: given the
  fixture's deliberately unambiguous construction (7 columns, zero other
  page content), this would indicate a genuine applicability-reasoning
  gap, not appropriate caution — unlike Case D/E, where suppression is
  the *correct* answer.
