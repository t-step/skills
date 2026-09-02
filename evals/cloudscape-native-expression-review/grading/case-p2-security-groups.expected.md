# Grading key — Case P2: SecurityGroups.tsx (real primary + genuinely independent material secondary)

## Designed intent

This case is the mirror image of Case P1: given a real, established
primary finding, does the reviewer correctly retain a *second*,
genuinely independent finding that clears every materiality/
applicability gate on its own — or does finding one strong issue cause
the reviewer to either stop looking (under-recall) or pad the report
with a weaker, look-alike extra (P1's failure mode)? Two candidates are
pre-adjudicated below; both must independently earn their place. A third
distractor is named and explicitly not part of the scored verdict.

## Candidate 1 — `ContentLayout` + `Table variant="container"` instead of the Table view pattern's `full-page` variant

**Verdict: MUST REPORT.**

Structurally identical in shape to Case A1's designed finding (frozen,
adversarially A-graded on that case) — a fresh resource type (security
groups, not storage volumes), a fresh column set (7 columns: select,
name, VPC, inbound rules, outbound rules, status, created), same
mechanically-valid-but-non-native composition: the entire page content
is `ContentLayout` wrapping `Table variant="container"`.

- **Type:** `pattern composition` or `combined component + pattern`,
  materiality high.
- **Repository evidence:** the file's own comment states the page's sole
  job is listing every group and letting an operator pick a batch of
  unused ones to delete; `ContentLayout` wraps a single
  `Table variant="container"` with no other page content (the entire
  return value).
- **Cloudscape evidence** (verified live at
  `/patterns/resource-management/view/table-view/index.html.md` and
  `/components/table/index.html.md`, matching Case A1's already-verified
  citations): "Don't use the content layout component on this type of
  page. Instead, use the 'full-page' variant of the table component to
  implement this pattern" (with the same "few columns" carve-out, which
  does not apply here: 7 substantive columns, mixed text/numeric/status
  data — "It's effective for quickly identifying categories or comparing
  values in a large text and numerical data set.").
  - Container variant: "Use this variant to place a table inside a
    container with other content, such as key-value pairs" — does not
    describe this page, which has no other content.
  - Full-page variant: "Use it for presenting and managing a table with
    many columns within a stand-alone page."
- **Applicability argument a correct response must make:** the same
  four-point test A1's Finding 1 satisfied — task match (stand-alone
  resource-view page), current implementation solves the same problem
  via the discouraged composition, native expression preserves the same
  task (same columns, same filter/sort/paginate, only page-structure
  changes), and material (direct "Don't...Instead" pairing, no
  documented exception applies at 7 columns).
- **Boundary check:** page-structure/component-selection judgment
  grounded in an explicit "don't/instead" directive, not implementation
  mechanics or general UX.

## Candidate 2 — hand-rolled `<input type="checkbox">` selection instead of `Table`'s built-in `selectionType="multi"`

**Verdict: MUST REPORT — independently of Candidate 1.**

This is the case's central adjudication target: a second, genuinely
material finding on a different axis of the same component (selection
mechanism, not page layout), which must survive on its own evidence
rather than being crowded out once Candidate 1 is already established,
or folded into Candidate 1 as padding.

- **Type:** `component selection`, materiality high.
- **Repository evidence:** the table defines its own `select` column by
  hand — a raw `<input type="checkbox">` per row and one in the header
  for "select all," both driving local `useState<Set<string>>` state
  (`checkedIds`, `toggleOne`, `toggleAllOnPage`) — paired with a header
  `Button` reading `` `Delete selected (${checkedIds.size})` ``. `Table`
  never receives `selectionType`, `selectedItems`, or
  `onSelectionChange`; the component's own selection mechanism is never
  invoked at all. `inspect_surface.py` independently confirms this as
  fact (`native_interactive_elements`: two raw `input` tags at the two
  checkbox call sites), not a matter of interpretation.
- **Cloudscape evidence** (verify live at `/components/table/index.html.md`
  and `/patterns/general/actions/index.html.md`):
  - Table's own documented selection feature: "Multi — Allows multiple
    items to be selected at a time by using checkboxes for each item...
    Use for collections that support bulk actions." This is the
    component's own named mechanism for exactly this job — checkbox-based
    multi-select feeding a bulk action — not an adjacent or superficially
    similar feature.
  - Selection-state contract, same page: "The selection and sorting
    state of table component are controlled... For the selection state,
    set the `selectedItems` property and `onSelectionChange` event
    listener." The fixture's hand-rolled `Set<string>` state is not this
    contract — it is a parallel, uncoordinated reimplementation of the
    same concept, disconnected from `Table`'s own row/selection wiring
    (pagination, sorting, and filtering changes are not reconciled
    against it the way the controlled-selection contract requires).
  - Actions pattern page: "If an action can be triggered on multiple
    resources in bulk, it should be listed as a global action" — exactly
    the "Delete selected" button already present, currently wired to a
    hand-built selection set instead of the pattern's own paired
    mechanism.
- **Applicability argument a correct response must make:** (1) the
  observed task — pick a batch of resources, delete them in one action —
  is precisely the "collections that support bulk actions" job `Table`'s
  own Multi selection type names; (2) the current hand-rolled checkboxes
  solve the same problem, just by reinventing a first-class Cloudscape
  concept rather than adopting it; (3) switching to `selectionType="multi"`
  preserves the identical task (same rows selectable, same bulk-delete
  goal) — this is not a redesign; (4) material because there is no
  documented alternative that sanctions hand-rolled selection as an
  equally valid pattern the way text-filter-vs-collection-select-filter
  is for a simple resource (this is not an "equally valid" case — the
  bespoke concept isn't itself Cloudscape usage, native or otherwise, of
  anything the component ships for this job) — this should independently
  register as clearing every "Anti-fundamentalism rule" gate at least as
  cleanly as Candidate 1, not as a weaker afterthought.
- **Boundary check:** this is a component-selection judgment — a bespoke,
  hand-rolled UI concept (manual checkbox state) where Cloudscape ships a
  purpose-built mechanism for the identical job (`Table`'s `selectionType`
  contract) — explicitly named as in-scope by SKILL.md's own "In scope"
  bullet ("a bespoke, hand-rolled UI concept where Cloudscape ships a
  more semantically appropriate component for the same job"), not a
  correctness/a11y-implementation nitpick about the raw `<input>`
  elements themselves (that framing — missing ARIA roles, keyboard
  semantics of a hand-rolled checkbox — would be
  `cloudscape-implementation-audit`'s domain and must not be how this
  finding is argued, even though it is real supporting color).

**A response that finds only Candidate 1 and stays silent on Candidate 2
is an under-recall failure on this case's own central target** — the
opposite failure from Case P1, and the one this case exists to check for
directly. **A response that reports Candidate 2 as a sub-clause or
"why it matters" aside inside Candidate 1's finding, rather than a
distinct finding, blurs a genuinely independent issue and should be
graded down on structure**, per SKILL.md's own instruction not to force
one recommendation into an artificial single finding, applied in
reverse: these two are not one underlying issue at two abstraction
levels (unlike Case C's designed `combined` finding) — they are two
unrelated concepts (page layout; selection mechanism) that happen to sit
in the same file.

## A tolerated, non-scoring distractor — `status` (2 values) as a filter-mechanism candidate

`status` (`active`/`unused`) is a second discrete-valued column, similar
in shape to Case P1's `status`/`region` pair, and could tempt the same
TextFilter-vs-collection-select-filter reasoning P1 tests directly. This
case does not pre-adjudicate that candidate one way or the other — it is
present incidentally, not as this case's test target. Report or
suppression of a filter-mechanism candidate here should be noted in any
writeup but must not affect this case's own pass/fail verdict, which
turns entirely on Candidates 1 and 2 above.

## What would be wrong, summarized

- **Missing Candidate 1** — recall failure on a previously-validated
  finding shape.
- **Missing Candidate 2, or folding it into Candidate 1 as an aside**
  — the specific failure this case exists to detect: treating a
  genuinely independent, materially-earned second finding as
  unnecessary once a first one is already reported.
- **Reporting Candidate 2 at implementation-audit framing** (e.g., "the
  checkboxes are missing ARIA attributes") instead of component-selection
  framing (the app never adopted `Table`'s own selection mechanism at
  all) — a boundary-discipline failure distinct from, but adjacent to,
  P1's overreach failure.
- **Fabricated or non-verbatim quotation** presented inside quotation
  marks as literal source text for either finding — graded separately
  under citation fidelity, never folded into the materiality verdicts
  above.
