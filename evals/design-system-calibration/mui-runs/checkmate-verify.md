# Adversarial verification: Checkmate Incidents page (baseline vs. skill-assisted)

Verifier re-read both write-ups, the rubric (Cloudscape-authored, applied here with
"Material UI" / "MUI docs" substituted), `SKILL.md`, all 8 bounded fixture files, plus
two files outside the bounded set that either review leaned on as evidence
(`Components/design-elements/StatusLabel.tsx`, `Components/actions-menu/index.tsx`).
Every MUI doc URL cited in either review was re-fetched (both via WebFetch and raw
`curl` against the `.md` endpoint) and every quoted string was grepped against the raw
markdown for verbatim presence — not just paraphrase plausibility.

## Citation audit (both reviews)

All URLs cited in both reviews resolve and are on-topic. Per-quote results:

| Review | Quote | Verbatim in cited page? |
|---|---|---|
| Baseline F1 | "The `Grid` component is a *layout* grid, not a *data* grid... works well for a layout with a known number of columns" | **Yes**, exact (react-grid.md L33, L14) |
| Baseline F1 | Table: "display information in a way that's easy to scan..." / "close mapping to the native `<table>` elements" | **Yes**, exact (react-table.md L15, L106) |
| Baseline F1 | List: "you can leverage the `primary` and `secondary` properties of `ListItemText` to present hierarchical information—such as a label paired with descriptive or supplemental content" | **FABRICATED.** No occurrence of "leverage," "hierarchical," or "descriptive or supplemental" anywhere in react-list.md. The page's only `primary`/`secondary` content is example code (`<ListItemText primary="Photos" secondary="Jan 9, 2014" />`) and an empty-description props table row. This sentence does not exist on the page in any form. |
| Baseline F2 | Chip: "compact elements that represent an input, attribute, or action" | **Yes**, exact (react-chip.md L12) |
| Baseline F3 | Alert: "Alerts give users brief and potentially time-sensitive information in an unobtrusive manner" / severity list | **Yes**, exact (react-alert.md L18, L56) |
| Baseline F5 | ToggleButtonGroup: "controls the selected state of its child buttons" / "selecting one option deselects any other" | **Yes**, exact (react-toggle-button.md L16, L22) |
| Baseline (not-flagged) | Dialog: "inform users about a task and can contain critical information, require decisions" | **Yes**, exact (react-dialog.md L13, truncated but not misleading) |
| Skill F1 | Chip: "Chips are compact elements that represent an input, attribute, or action" | **Yes**, exact |
| Skill F1 | Chip: color prop conveys states/categories, quoted as *"convey different states or categories"* | **FABRICATED.** No occurrence of "categories" or "states" anywhere in react-chip.md. The `color` and `icon` prop rows in the API table have empty description cells; no prose on the page makes this claim in these or similar words. The underlying inference (color prop values include `'error'`/`'success'`, which do map to semantic states) is reasonable, but it is presented in quotation marks as if lifted from the doc, and it isn't. |
| Skill suppressed | Select: "advanced" (combobox/multiselect/autocomplete/async) | **Yes**, exact (react-select.md L62) |
| Skill orientation | DataGrid: "designed for use-cases focused on handling large amounts of tabular data... more rigid structure... more powerful features" | **Yes**, exact (react-table.md paraphrase region confirmed) |
| Skill orientation | Menu: IconButton-triggered pattern | Not directly quoted; paraphrase, confirmed by example in react-menu.md |

**Verdict: one fabricated quotation in each review.** Baseline's is in a *reported*
finding (F1, Grid→Table/List) but is redundant — the finding's real weight rests on the
Grid quote (verified genuine) and the accurate Table quote; the List misquote is
decorative, not load-bearing. The skill run's fabrication is more consequential: it sits
inside the **cited MUI evidence** for its *only* reported finding, in a field the
Finding contract requires to state "the exact authoritative source... and the specific
guidance it establishes." Presenting a paraphrase as a direct quotation there is exactly
the failure mode the rubric's Q2 exists to catch, even though the finding survives on
its other (real) evidence.

## Per-candidate grading — skill-assisted review

### Finding 1: Chip vs. hand-rolled ValueLabel/colored-Typography — **Grade B**

Walking the nine questions:

1. **User task supported by evidence** — yes, matches the route/data shape (status,
   resolutionType fields visibly present across all cited files).
2. **Does cited authority say what's claimed** — partially. The purpose-statement quote
   is genuine and on-point. The "convey different states or categories" quote is
   fabricated (see citation audit). The underlying prop facts (color accepts
   `'error'`/`'success'`, icon prop exists) are true even though not stated in prose on
   the page — confirmed against the props table (react-chip.md L698-709).
3. **Four-point applicability test** — passes cleanly. Task match is real (categorical
   attribute, at-a-glance), current code solves the identical problem, proposed swap
   preserves semantics, and it recurs enough (3× ValueLabel + 1× raw Typography) to be
   more than a one-off.
4. **Preserves task semantics** — yes.
5. **Could current code be equally valid MUI usage?** — this is where the finding is
   weaker than its self-assigned "high/high" rating admits. `ValueLabel` is not an
   isolated hack: it lives in `StatusLabel.tsx` alongside three siblings
   (`StatusLabel`, `ColoredLabel`, `DockerStateLabel`) that implement the same
   dot+border+Typography convention for monitor status and Docker state elsewhere in
   the app (confirmed by reading the file). That is a deliberate, actively-maintained,
   app-wide design-system layer, not a one-page reimplementation. The skill's own
   *sibling* suppressed candidate (BaseBox-as-Card) explicitly credits this exact
   "established, app-wide convention" argument as a reason to suppress a swap — but the
   Chip finding, built on the same `BaseBox`-derived component family, does not apply
   that same reasoning to itself. This is an internal inconsistency in the run's own
   standard, not just a close call.
6. **Materiality — would an FDE actually restructure?** — plausible, but the more likely
   first move for a working engineer is "make `resolutionType` use the existing
   `ValueLabel`, like `status` already does" (a zero-MUI-impact consistency fix), not
   "replace the app's shared status-label component with `Chip` on this one page." The
   finding's "Why it matters" acknowledges the inconsistency is the real cost but jumps
   straight to a component swap as if it's the only fix, without weighing the
   in-place-consistency alternative.
7. **Leaking into implementation/UX** — no, cleanly component-selection.
8. **Duplicated across levels** — no, single combined finding, correctly not split.
9. **Intent-dependent** — n/a.

**Repository-evidence completeness gap:** the finding claims the pattern "recurs at
least four times... using two different bespoke implementations" and cites four sites
(`IncidentTable.tsx` status + resolutionType, `CardDetails.tsx` status,
`CardSummary.tsx` latest-incidents status). It misses a **third** implementation that
baseline's parallel finding catches: `CardDetails.tsx:170-181`'s `resolutionType` field
is rendered as *plain, uncolored* `Cell`/`Typography` (verified by reading the file —
no `color` prop at all on that `Cell`), distinct from both the `ValueLabel` pill and the
colored `Typography` in the table. This is inside the bounded 8-file surface the skill
run was scoped to and is squarely on-topic for the exact claim being made, so its
absence is a real evidence gap, not an out-of-scope omission.

Net: real finding, correct core observation, well-formed under the Finding contract's
structure — but overstated confidence given (a) the fabricated supporting quote, (b) an
un-reckoned-with tension with its own suppression reasoning elsewhere in the same
report, and (c) an incomplete repository-evidence count relative to what baseline
found in the same files. **B — useful but non-decisive**, not the "A" its self-assigned
high/high rating implies.

### Suppressed candidate: monitor filter `Select` vs. `Autocomplete` — **correctly suppressed**

Verified against react-select.md and react-autocomplete.md: Select is documented as
fine for "straightforward scenarios," Autocomplete is positioned for combobox/async/
multiselect needs, and neither page states an option-count threshold. The suppression
reasoning matches what the docs actually say (no fabrication, no overreach). This is
exactly the kind of C-grade candidate the skill's own materiality bar is supposed to
catch and correctly did — not a verifier failure to find fault with.

### Suppressed candidate: `BaseBox`-as-card vs. `Card` — **correctly suppressed**

Sound reasoning (no documented "don't use Box, use Card" pairing; `BaseBox` is an
established app-wide convention). As noted under Finding 1 above, this same
cross-app-consistency logic, applied consistently, would have tempered rather than
inflated the confidence of the Chip finding — the run reasons well here but doesn't
carry the reasoning across to the one place it most needed to.

### Suppressed candidate: `CardDetails.tsx` Grid key/value layout vs. `List` — **outcome defensible, reasoning incomplete**

The stated reasoning only weighs List (imperfect fit — `ListItemText` primary/secondary
is documented for stacked label+description text, not label-left/value-right rows,
which the run correctly notes). But it never engages the angle baseline's parallel
finding used — Grid's own "layout grid, not a data grid" framing — nor considers
`Table` as a candidate at all. Having independently graded baseline's version of this
same candidate (see below), I judge the *outcome* here (suppress) as substantively
defensible: `Table`'s documented problem is scanning multiple rows for patterns, and a
single incident's field/value listing is a categorically different shape (one record,
not many), so neither `Table` nor `List` is a clean fit — this is a case where nothing
in MUI's vocabulary cleanly covers a "description list," and the skill's high
materiality bar is right to stay quiet rather than force a fit. But the recorded
rationale is thinner than the candidate deserved.

### Orientation notes — factually confirmed, one scope inconsistency

All five orientation-note claims were checked against the actual code and cited docs
and hold up:

- Table vs. DataGrid — confirmed (server-driven pagination/filtering present in
  `index.tsx`; DataGrid doc language re: "large amounts of tabular data" verified).
- Menu via IconButton — confirmed accurate **but the underlying evidence
  (`Components/actions-menu/index.tsx`'s actual `IconButton`+`Menu` composition) lives
  outside the 8 bounded files**, exactly the situation baseline explicitly flagged and
  declined to assess for `DialogResolution`/`DialogIncidentDetails`'s own wrapper. The
  skill run asserts a confirmed match without naming that it reasoned past the
  boundary; I independently read `actions-menu/index.tsx` and the claim happens to be
  true, but the run's own methodology is inconsistent about when it will and won't peek
  past the bounded surface, and doesn't flag it either way here.
- Both Dialog notes — confirmed against `DialogResolution.tsx`/`DialogIncidentDetails.tsx`.
- `Select` for the 3-value filter — confirmed, and well-grounded (see recall-gap
  discussion below).

Version-resolution claims (`@mui/material` 7.3.7, `@mui/icons-material` and `@mui/lab`
both absent from the bounded surface) were independently re-derived from
`package.json`/`package-lock.json` and grep — all accurate.

## Chip finding: is the skill run's version genuinely more rigorous than baseline's?

Mixed, not a clean win for the skill run:

- **Structure/discipline:** skill's version is more rigorous in form — explicit
  Type/Materiality/Confidence/Applicability-argument/Boundary-check fields, and it
  independently opened `StatusLabel.tsx` to characterize *how* `ValueLabel` is built
  (confirmed accurate: `BaseBox` + 7px dot + `Typography`, verified by reading the
  file), which baseline doesn't do — baseline treats `ValueLabel` as a black box
  ("chip-like element").
- **Evidence completeness:** baseline's version is more complete — it catches a third
  inconsistent treatment (`CardDetails.tsx`'s uncolored `resolutionType` text) that
  skill's finding misses entirely, despite that file being in skill's own bounded set
  and cited elsewhere in the same finding for the *status* field.
- **Citation integrity:** a wash — each review has exactly one fabricated quotation,
  and skill's fabrication is more consequential because it sits inside the sole
  evidence block for the run's only reported finding.

So: better argument scaffolding, weaker on both completeness and citation fidelity
where it matters most. Call it a draw with different failure modes, not a validation
that the skill discipline produced a strictly stronger finding.

## Recall-gap question: baseline's other 4 findings

| Baseline finding | Skill run's treatment | Verdict |
|---|---|---|
| F1 — Grid→Table/List (`CardDetails.tsx`) | Considered and suppressed (as Grid-vs-List only) | Adequate discipline, thin reasoning (see above) — not a gap |
| F2 — Chip (resolutionType/status) | Reported (skill's own Finding 1) | Recalled |
| F3 — Alert for `SummaryCardActiveIncidents` | **Not mentioned anywhere** — not a finding, not suppressed, not an orientation note | **Genuine recall gap** |
| F4 — List for `SummaryCardStats` icon/label/value rows | Not mentioned | Not a gap — baseline itself hedges this as its weakest finding; correctly falls below the skill's materiality bar |
| F5 — ToggleButtonGroup for resolution-type filter | Explicitly considered and **rejected** via an orientation note ("uncontested, correct fit") | Recalled and correctly resolved — a point in the skill's favor |

**F3 (Alert) is the one real gap**, and it's worth being precise about why it counts as
a gap rather than a defensible omission. `CardSummary.tsx` — the exact file containing
`SummaryCardActiveIncidents` — is demonstrably read closely by the skill run (it's
cited at line 160-164 for a *different* function in the same file, two functions below
`SummaryCardActiveIncidents`). The candidate is not weak on its face: `Alert`'s
documented purpose ("brief and potentially time-sensitive information," severity prop
with paired icon+color for exactly `success`/`error`) is a strong shape-and-problem
match to a hand-rolled `hasActive ? error : success` branch with a paired icon — this
clears the four-point applicability test at least as well as, arguably better than, the
Chip finding the run did report (it's a purpose-statement match, not just an existence
match). It is genuinely arguable whether it would survive to a final grade of A once
weighed against the counter-consideration that `Alert` is typically a transient,
dismissible, page/section-level banner and this is a persistent dashboard KPI tile
(same "different problem, same shape" trap the skill's anti-fundamentalism rule warns
about) — a careful pass might reasonably suppress or hedge it. But the skill run shows
no evidence of having weighed it at all: unlike the Grid/List and BaseBox/Card
candidates, which were explicitly named and given suppression rationale, F3 has zero
trace in the report. That absence — not a documented "considered and rejected" call —
is what makes this a recall gap rather than disciplined pruning.

**Overall verdict on the generalization question:** the skill run's narrower output is
*mostly* appropriate discipline, not recall failure — it correctly reported the
strongest candidate (Chip, albeit overstated), correctly and better-groundedly rejected
the weakest hedge in baseline's set (ToggleButtonGroup, with real documentation baseline
itself admitted it lacked), and reached a defensible (if thinly reasoned) suppression on
the Grid/List candidate. But it is not *entirely* discipline — one plausible,
high-materiality candidate (Alert) that sat inside a file the run demonstrably read
closely was never engaged at any level (finding, suppressed, or orientation), which is
a coverage gap in applying the skill's own procedure, not a materiality judgment the
procedure would have made correctly if it had been applied.

## Summary of citation problems (both reviews)

- Baseline F1: fabricated List quote ("leverage... hierarchical information...") — not
  load-bearing to the finding's core argument, but presented as verbatim and isn't.
- Skill F1: fabricated Chip quote ("convey different states or categories") — sits
  inside the evidence block for the run's only reported finding.
- No other fabrications found; every other quoted string in both reviews was confirmed
  verbatim against the raw `.md` source, including all orientation-note and
  suppressed-candidate citations in the skill run.
