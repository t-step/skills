# Checkmate — Incidents page: MUI component-choice review

Scope reviewed (pinned commit, `bluewave-labs/Checkmate`, unmodified): `client/src/Pages/Incidents/index.tsx`, `utils.ts`, `Components/IncidentTable.tsx`, `Components/DialogResolution.tsx`, `Components/CardDetails.tsx`, `Components/CardSummary.tsx`, `Components/DialogIncidentDetails.tsx`, `Components/ControlsIncidentFilter.tsx`.

## Inferred user task

This is an operator's incident console for an uptime/monitoring product: the user lands here to see, at a glance, whether anything is currently down (active-incident count and the most recently affected monitors), then triages by filtering a paginated history of incidents by monitor and resolution type, opens a single incident to read its full timeline/status/resolution detail in a focused view, and — for incidents the automated checker hasn't already closed — manually resolves an active incident with an optional free-text comment. The five building blocks are: summary/status cards, a filter bar, a two-part (active + resolved) paginated table, a read-only detail view, and a confirmation dialog for the resolve action.

## Findings

### 1. `CardDetails.tsx` uses layout `Grid` to hand-build what is a data table (label/value rows), not a page layout

**Where:** `client/src/Pages/Incidents/Components/CardDetails.tsx`, lines 59–93 (Overview section), 99–146 (Analysis section), and 155–202 (Resolution Details section). Each section is a `Grid container` whose children are `Grid size={2}`/`size={10}` (or `size={6}`/`size={4}`) pairs, each pair being a field label (`Cell` → `Typography`) followed by its value — repeated for Status, Monitor, URL, Started At, Status Code, Downtime, Message, Resolved At, Resolution Type, Resolved By, Comment.

**MUI documentation:** `https://mui.com/material-ui/react-grid.md` — "The `Grid` component is a *layout* grid, not a *data* grid... [it] works well for a layout with a known number of columns." MUI's own framing explicitly separates layout structuring from data-structure display.

By contrast, `https://mui.com/material-ui/react-table.md` states core `Table` is meant to "display information in a way that's easy to scan, so that users can look for patterns and insights," and has "a close mapping to the native `<table>` elements" — i.e., it's the component meant for exactly this kind of enumerable, scannable field/value listing. (Not recommending `@mui/x-data-grid` here — that's a separate, commercially licensed package and out of scope; the fit here is plain `@mui/material` `Table`/`TableRow`/`TableCell`, or alternatively `List`/`ListItem`/`ListItemText` using the `primary`/`secondary` pattern documented at `https://mui.com/material-ui/react-list.md` — "you can leverage the `primary` and `secondary` properties of `ListItemText` to present hierarchical information—such as a label paired with descriptive or supplemental content.")

**Why it matters:** `Grid` gives no semantic association between a label cell and its value cell (no row grouping, no `<th>`/`<td>` relationship even at the visual-abstraction level) and forces manual column-span bookkeeping (`size={2}`/`size={10}` in one section, `size={6}`/`size={4}` in another, inconsistent between the two) for a shape of data (17 label/value pairs across 3 sections) that `Table` or `List` model directly and MUI's own Grid docs say Grid isn't for.

### 2. Categorical incident attribute ("resolutionType": manual/automatic) rendered as manually colored `Typography` rather than `Chip`, inconsistent with how the adjacent `status` column is already handled

**Where:** `client/src/Pages/Incidents/Components/IncidentTable.tsx`, lines 129–150 — the `resolutionType` column renders `<Typography variant="body2" color={... warning.main : success.main} textTransform="capitalize">{row.resolutionType}</Typography>`. The same file's `status` column (lines 95–111), two rows above it, already uses the design-system's `ValueLabel` chip-like element for the same kind of categorical value (active/resolved). Also present at `client/src/Pages/Incidents/Components/CardDetails.tsx`, lines 170–181, where `resolutionType` is rendered as plain, uncolored `Cell`/`Typography` text in the detail dialog.

**MUI documentation:** `https://mui.com/material-ui/react-chip.md` — "Chips are compact elements that represent an input, attribute, or action." `resolutionType` (manual vs. automatic) is precisely an *attribute* of the incident record, the exact category Chip's own doc names.

**Why it matters:** The table already establishes a visual convention — categorical/state values get a pill-style label (`ValueLabel`) — for `status`. `resolutionType` is the same kind of data (a small enum describing how the incident record got here) but is expressed with raw colored text in the table and as plain unstyled text in the detail dialog, so the same underlying data concept is represented three different ways across two files. `Chip` is the component MUI ships specifically for compact attribute display and would let this value be expressed the same way `status` already is, consistently, in both places.

### 3. `SummaryCardActiveIncidents` hand-rolls an icon+color+message severity indicator that matches `Alert`'s documented purpose

**Where:** `client/src/Pages/Incidents/Components/CardSummary.tsx`, lines 85–124. The component picks `theme.palette.error.main` or `theme.palette.success.main`, pairs it with a `TriangleAlert`/`CircleCheck` icon in a colored `Box`, and shows a short status message ("N active incidents" / none) — entirely by hand, with the success/error branching done manually (`hasActive ? ... : ...`).

**MUI documentation:** `https://mui.com/material-ui/react-alert.md` — "Alerts give users brief and potentially time-sensitive information in an unobtrusive manner," supporting severity states "`success` (default), `info`, `warning`, and `error`," each with "corresponding icon and color combinations for each."

**Why it matters:** This is close to a textbook match for `Alert`'s documented use case: a brief, colored, iconed, severity-driven status message ("things are fine" vs. "things are on fire") is exactly what `Alert`'s `severity` prop is built to express, including the icon-and-color pairing this component currently reproduces by hand (manually selecting between `error.main`/`success.main` and `TriangleAlert`/`CircleCheck`).

### 4. `SummaryCardStats`'s icon/label/value rows are a hand-built version of the icon+text list-row pattern `List` documents

**Where:** `client/src/Pages/Incidents/Components/CardSummary.tsx`, lines 19–45 (`SummaryItem`) and 206–236 (`SummaryCardStats`, which renders three `SummaryItem`s: total incidents, most-affected monitor, avg. resolution time). Each row is a manually composed `Stack` (`direction="row"`, `justifyContent="space-between"`) holding an icon + label on the left and a bold value on the right.

**MUI documentation:** `https://mui.com/material-ui/react-list.md` — "Lists are a continuous group of text or images. They are composed of items containing primary and supplemental actions, which are represented by icons and text," with `ListItemIcon` + `ListItemText` shown as the documented way to pair an icon with label/value content in a row.

**Why it matters (hedged):** This is a weaker match than findings 1–3: MUI's `ListItemText` `primary`/`secondary` pattern is documented for stacked label+description text, not strictly for a label-left/value-right layout, so `List` is a plausible native fit rather than a precise one. Still, three fixed icon+label+value rows stacked vertically is exactly the shape `List`/`ListItem`/`ListItemIcon`/`ListItemText` (with a trailing element for the value) are built to express, and using them would remove the need to hand-manage row height (`minHeight: 32`) and spacing that `List` handles by convention.

### 5. Resolution-type filter (`all`/`manual`/`automatic`) is a small, fixed, always-visible exclusive choice rendered as a `Select` dropdown

**Where:** `client/src/Pages/Incidents/Components/ControlsIncidentFilter.tsx`, lines 9 (`resolutionTypes = ["all", "manual", "automatic"]`) and 57–72, where these three fixed values are rendered as `MenuItem`s inside a `Select`, requiring a click-to-open interaction to see or change which of the three is active.

**MUI documentation:** `https://mui.com/material-ui/react-toggle-button.md` — "A group should share a common container. The `ToggleButtonGroup` controls the selected state of its child buttons," with exclusive selection meaning "selecting one option deselects any other."

**Why it matters (hedged):** MUI's Toggle Button docs don't explicitly state "prefer this over `Select` for small filter sets" — I could not find that comparison in the fetched documentation, so this is suggestive rather than proven. But the shape of this data (exactly 3 fixed, always-relevant values, no search/scroll needed, one always selected) is the shape `ToggleButtonGroup`'s exclusive-selection mode is documented for, and using it would let the current selection be visible at a glance instead of hidden behind a closed dropdown — consistent with what the doc describes as the group's job (visibly showing/controlling which single child button is selected).

## Not flagged

`DialogResolution.tsx` and `DialogIncidentDetails.tsx` both go through a project-local `Dialog` wrapper (`@/Components/inputs`), whose internal composition is outside the reviewed file set, so I can't assess what MUI primitives it does or doesn't use under the hood. At the level visible here, using a modal, decision-oriented dialog for a destructive "resolve incident" confirmation (`DialogResolution.tsx`) matches MUI's own framing of `Dialog` — "Dialogs inform users about a task and can contain critical information, require decisions" (`https://mui.com/material-ui/react-dialog.md`) — so no finding there. I considered whether the active/resolved incident split (`index.tsx`, lines 187–235, two `IncidentsTable`s shown simultaneously) is a `Tabs` opportunity, but both tables are intentionally visible at once rather than being alternate views of one task, so recommending `Tabs` would be a workflow-shape judgment rather than a grounded component-fit claim, and I left it out per the instruction to avoid generic UX/workflow critique.
