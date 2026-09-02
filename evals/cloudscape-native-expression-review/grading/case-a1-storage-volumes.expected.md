# Grading key — Case A1: StorageVolumes.tsx (clear pattern mismatch, isolating case)

## Designed intent

A second, structurally distinct instance of Case A's exact designed
finding, built per `RESULTS.md` §16's own named next step: same
underlying pattern-composition question (`ContentLayout` +
`Table variant="container"` vs. the table-view pattern's `full-page`
variant), different resource type (storage volumes vs. fleet nodes),
different column count (6 vs. 7), and — unlike Case A — only one
discrete-valued column (`status`), so there is no plausible
`TextFilter`→`PropertyFilter` candidate finding to compete for the run's
attention the way Case A's three discrete columns did. This isolates
whether the miss on Case A was a genuine recall gap in the
variant/wrapper check, or an artifact of that specific fixture's
distracting secondary candidate.

Every local Cloudscape mechanic is mechanically correct — nothing here
belongs to implementation correctness. The page's entire content is the
table, wrapped in `ContentLayout` with `Table variant="container"`, no
other page content.

## What a correct response looks like

**One material finding, `Type: pattern composition` (or `combined
component + pattern`), high materiality.**

- Cites the table-view pattern page's own language: *"Don't use the
  content layout component on this type of page. Instead, use the
  'full-page' variant of the table component to implement this pattern"*
  and *"The table view pattern is a collection of resources in a
  tabular format. It's effective for quickly identifying categories or
  comparing values in a large text and numerical data set."*
- Applicability argument addresses the pattern's own few-columns
  exception (*"if a table only has a few columns, use a bordered table
  inside the content layout component"*) and why it does not apply here:
  6 substantive columns (id, status, size, throughput, attached
  instance, created), a mix of text and numerical data, matching "large
  text and numerical data set."
- Authority strength: `REQUIRED` — a direct "Don't... Instead" pairing.
- Native expression: `Table variant="full-page"`, honestly naming that
  the `AppLayout contentType="table"` dependency lives outside the
  reviewed file.
- Boundary check distinguishes this from implementation correctness and
  general UX.
- Correctly does **not** manufacture a filter-mechanism finding —
  `status` is the only discrete-valued column, below the docs' own
  multi-property threshold for recommending `PropertyFilter` over
  `TextFilter`; a response that invents one here would itself be a
  materiality-discipline problem, not a bonus finding.

## What would be wrong

- **Missed entirely** (silence, or an "Orientation notes" entry that
  confirms the macro pattern — Table, not Cards — but never reaches the
  variant/wrapper-level question): the primary failure mode this case
  exists to detect. If this reproduces the exact Case A shape (macro
  pattern checked and confirmed, variant choice never examined), that is
  the specific evidence needed for the decision gate.
- **Reported at implementation-audit-style `violation`/prop-level
  framing** rather than pattern-composition framing.
- **Additional, unrelated implementation-shaped findings.**
- **A manufactured filter-mechanism finding** in place of, or alongside,
  the designed finding — would indicate the run is pattern-matching on
  surface shape (recognizing "this looks like Case A") rather than
  reasoning the fixture's own facts.
- **Suppressed as low-materiality or "equally valid"**: given the
  fixture's deliberately unambiguous construction, this would indicate a
  genuine applicability-reasoning gap, not appropriate caution.
