# Verification — Case A: FleetNodes.tsx

Verifier method: read rubric.md, case-a-fleet-table.expected.md, both runs, and
the fixture (`src/pages/FleetNodes.tsx`); independently fetched every cited
Cloudscape page (table-view pattern, table component, filter-patterns,
property-filter, in-context-actions pattern, timestamps pattern,
collection-preferences component, progress-bar component) to confirm quotes
are accurate and not `llms.txt`-summary paraphrases.

## Headline result

**The skill-guided review missed the case's designed-intent finding
entirely.** Case A's sole purpose (per `case-a-fleet-table.expected.md`) is
to test recall of the `ContentLayout` + `Table variant="container"` vs.
`Table variant="full-page"` table-view pattern violation — the fixture was
built to make this "the single most important negative signal this case can
produce" if missed. `skill.md` contains no mention of `ContentLayout`,
`variant="container"`, `variant="full-page"`, or the table-view pattern's
"Don't use the content layout component on this type of page" rule anywhere
in its Findings, Suppressed, or Orientation-notes sections. It substitutes a
different, real, well-argued finding (TextFilter → PropertyFilter) as its
sole reported finding. **`baseline.md` found and correctly argued the actual
designed-intent finding** (its Finding #1), but buried it among four
additional findings, several of which leak into `cloudscape-implementation-audit`'s
territory — exactly the scope-confusion failure mode the grading key warns
against.

---

## Baseline findings

### Baseline #1 — Container table inside ContentLayout instead of full-page pattern
**Grade: A**

- Q1 (repo evidence): Confirmed. Lines 59–68: `ContentLayout` wrapping
  `Table variant="container"`, `Header variant="h1"`, 8 columns total (7
  data + actions).
- Q2 (authority accuracy): Confirmed verbatim against the live pages. The
  table-view pattern page does say "Don't use the content layout component
  on this type of page. Instead, use the 'full-page' variant of the table
  component," and the table component page does say the full-page variant
  "is for implementing the full page table view pattern... use it for
  presenting and managing a table with many columns," paired with
  `contentType="table"` on AppLayout.
- Q3 (applicability): Passes. The finding explicitly ties the 8-column,
  content-heavy, "nothing on the page besides the table" framing (drawn
  from the file's own header comment) to the docs' named scenario, which
  substantively (if not verbatim) forecloses the "few columns → bordered
  table in content layout" exception the grading key calls out.
- Q4 (task semantics preserved): Yes — swapping variant/wrapper only, no
  workflow redesign.
- Q5 (equally valid as-is?): No — this is a direct "Don't...Instead"
  pairing, not a soft preference; grading key rates authority strength here
  as REQUIRED.
- Q6 (materiality): High and correctly so — this is the exact pattern rule
  violation the case was built to test, and it forfeits real layout space
  (`contentType="table"`) on a dense operational table.
- Q7 (boundary): Clean — component/pattern-selection, not a prop bug or
  generic "feels dense" complaint.
- Minor gaps, not grade-affecting: doesn't literally quote the "few
  columns" exception clause to rule it out, and doesn't explicitly flag
  (as the grading key suggests an ideal response would) that
  `contentType="table"` lives on `AppLayout`, outside this file — it treats
  the pairing as documentation context rather than an assumed fact about
  unseen code, so this doesn't cross into invention.

**Why an FDE would act on it:** it's a documented "Don't...Instead" rule,
directly on point for this exact page shape, with a concrete, low-risk fix
(swap `variant` + wrapper) and a real cost to leaving it as-is (lost width
on a wide operational table).

### Baseline #2 — TextFilter for three finite categorical properties instead of PropertyFilter
**Grade: D**

- Q1: Confirmed — `status`/`region`/`instanceType` each have exactly 3
  distinct values in the fixture data (lines 24–26), `TextFilter` is the
  only filter wired (lines 139–145).
- Q2: Confirmed accurate against filter-patterns and property-filter pages
  ("more than two properties," "multi-select tokens for... discrete
  values," "State = Active, Pending, Canceled").
- Q3 (applicability — the driver of the grade): Fails to engage the other
  half of the docs' own gate. The filter-patterns page conditions the
  property-filter escalation on "complex products with **large collection
  of resources**," not on property-count alone. The fixture is 24 mock
  items — not obviously "large" — and the finding never raises or
  addresses this, presenting the recommendation as simply established.
- Q5: A live question the finding never poses — TextFilter over 24 items
  with 3 enumerable fields could plausibly still be "equally valid"
  Cloudscape usage under the docs' own scale framing; the finding doesn't
  rule this out.
- Q9: This is exactly the failure mode the question describes — a
  genuinely underdetermined point (is this collection "large" in the
  product's real intended scale, vs. the 24-item fixture?) is resolved by
  silent assertion rather than being named as an open question.
- Q6: Given the unaddressed scale gate, materiality is asserted more
  confidently than earned.

**FDE reaction:** likely pushback — "we have 24 nodes, why do we need
PropertyFilter" — which the finding as written has no answer for.

### Baseline #3 — CollectionPreferences omits column display preferences
**Grade: D**

- Q2: Accurate quote (collection-preferences docs do describe the column
  display preferences feature).
- Q3/Q6 (drivers): No documented threshold ties 8 columns to a requirement
  for `contentDisplayPreference` — the only numeric threshold that turned
  up in the docs (12 columns) gates an optional *text-filter-within-the-
  preferences-dialog* sub-feature, not whether column display prefs should
  exist at all. The "resizableColumns is already enabled, signaling
  columns don't comfortably fit" inference is weak — resizable columns is
  a routine width affordance, not evidence of overflow.
- Q7 (also a driver): This is a "which optional preference sub-props to
  pass on an already-correctly-chosen `CollectionPreferences`" question —
  prop-level configuration on a component whose selection is not in
  dispute. That's `cloudscape-implementation-audit` territory, not
  component/pattern selection.
- Q6: Routine, "nice to have" — the kind of finding the skill's own
  materiality discipline should suppress, per rubric's C description; here
  it's graded down further because of the Q7 boundary leak.

### Baseline #4 — Actions column not sticky
**Grade: D**

- Q1/Q2: Accurate — no `stickyColumns` prop set (lines 66–73); in-context-
  actions pattern page does recommend "enabling the sticky table column
  feature to maintain visibility of the available actions."
- Q7 (driver): The fix is `stickyColumns={{ last: 1 }}` — a missing prop
  on the Table component that is otherwise the correctly-selected
  component for this task. This is not a component/pattern choice; it's a
  configuration omission, squarely `cloudscape-implementation-audit`'s
  domain even though the citation is accurate and the underlying
  observation is real.
- Q6: Modest materiality — a prop addition, not a restructuring.

### Baseline #5 — "Launched" column: absolute string instead of documented timestamp pattern
**Grade: D**

- Q2: Quotes are accurate ("relative timestamps... recommend them for most
  use cases"; `<time>`/`datetime`/hover-title guidance for relative
  timestamps' absolute fallback).
- Q5 (driver): For an operator inventory table, an exact launch/provision
  timestamp is a plausible, commonly-seen legitimate choice in real AWS
  console tooling (audit/compliance relevance) — the docs say "most use
  cases," not "always," and the finding doesn't argue why this
  particular column is not the exception.
- Q7 (driver): The concrete "native expression" implied here (wrap in
  `<time>`, set `datetime`, add hover title) is accessibility/markup
  mechanics, not a component/pattern substitution — no distinct Cloudscape
  component is being swapped in, just a cell-formatting/a11y-affordance
  change. This is implementation-audit's domain.
- Not E: the citations aren't wrong and the code fact (`toLocaleString()`)
  is real — it's an overreach in framing/boundary, not a factual error.

---

## Skill findings

### Skill's sole reported finding — TextFilter → PropertyFilter (`combined component + pattern`)
**Grade: B**

- Q1/Q2: Same repository facts and same citations as baseline #2, both
  confirmed accurate.
- Q3/Q9 (why this beats baseline #2, but still not A): Unlike the
  baseline, this finding explicitly surfaces the exact gap that sinks
  baseline #2 — it names that the docs gate property-filter on "large
  collection of resources," that the fixture is only 24 items, and that
  the "large collection" reading is inferred from the page's own framing
  ("canonical inventory... backing the inference fleet") rather than
  concretely evidenced in the bounded surface. That is close to the Q9
  standard of naming the open question rather than silently asserting —
  but it still keeps "Confidence: high" and "Materiality: medium" instead
  of downgrading either in light of the acknowledged gap, so it doesn't
  fully split the difference the way a strict `intent-dependent`
  classification would.
- Q4: Preserves task semantics (filter mechanism swap only).
- Q6: Materiality correctly labeled "medium," not overstated.
- Q7: Explicit, correct boundary check ("component/pattern-selection
  question... not implementation-correctness... not general UX").
- Q8: Correctly filed as one unified `combined component + pattern`
  finding rather than split across levels.

**Why an FDE would plausibly act on it:** real, well-scoped, transparent
about its own weakest premise — a reasonable FDE could read this and either
implement it or ask the one clarifying question (is 24 nodes representative
of real scale?) the finding itself already surfaces, rather than being
blindsided by an unaddressed gap.

### Skill's suppressions (not findings — graded as calibration checks, no A–E letter)

- **Node ID column not linked to a details page** — correctly classified
  as intent-dependent: the fixture shows no in-app details page, and the
  existing external Console link is a plausible substitute for the "go see
  more" affordance the table docs otherwise recommend the first column
  provide. This is a model example of Q9 done right — names the ambiguity,
  the missing evidence, and declines to assert.
- **CPU/memory utilization as ProgressBar/gauge instead of plain text** —
  confirmed correct against the live progress-bar docs ("use a progress
  bar for operations... with a foreseeable point in time for completion";
  "Don't use a progress bar for indeterminate actions"). Steady-state
  utilization has no completion state, so ProgressBar doesn't apply;
  correctly suppressed for lack of a citable component substitute rather
  than waved through as a "finding." Baseline reaches the identical,
  correct conclusion in its closing "None found regarding" line.

### Skill's orientation notes
Spot-checked several (StatusIndicator mapping, inline-link Button for
in-context actions, no row-selection column, `counter` next to header,
filtering/pagination thresholds at 24 items) against fixture and docs —
each confirmation is accurate. These are validations, not findings, so they
carry no independent A–E grade, but their accuracy matters for the
case-level verdict below: nothing here is wrong, it's simply that none of
this — nor the sole reported finding — is the finding this case exists to
test for.

**Critical gap:** the "Macro-pattern choice (Table, not Cards or a custom
list)" orientation note confirms the *Table* component choice is correct
but never examines the *variant*/*wrapper* choice (`container` +
`ContentLayout` vs. `full-page`) at all. The review checked "is Table the
right macro pattern" and stopped one level short of "is this the right
Table variant for this composition" — precisely the question the fixture
was built to probe.

---

## Case-level verdict

| | Designed-intent finding present? | Verdict |
|---|---|---|
| **baseline.md** | Yes — Finding #1, graded A | **Matches** the case's designed intent, but imperfectly: the correct high-materiality finding is real and well-argued, but it's presented as one of five co-equal findings, four of which (D-graded) leak into implementation-audit territory (missing props: `stickyColumns`, `contentDisplayPreference`, `<time>`/`datetime` a11y markup) without any explicit boundary/scope discipline separating them from the pattern-level finding. This is exactly the "scope confusion between this skill and its sibling" failure mode the grading key calls out as a partial miss even when the underlying observation is correct. |
| **skill.md** | No | **Mismatch — the single most important negative signal this case can produce.** The skill-guided review shows strong scope discipline (explicit boundary checks, an explicit "what was not evaluated" section, honest caveat-naming on its one finding, well-calibrated suppressions) but never surfaces the `ContentLayout`/`variant="container"` vs. `variant="full-page"` violation anywhere — not in Findings, not in Suppressed, not in Orientation notes. It substitutes a different, real, competently-argued (B-grade) finding instead. Given this case's sole diagnostic purpose is recall of that one pattern rule, the skill run fails this case's central test despite otherwise-good hygiene. |

**Summary:** baseline "found the needle but buried it in hay that includes
several out-of-scope implementation nits"; skill "kept the hay clean but
never found the needle." Neither run should be scored as a clean pass on
this case's designed intent — baseline for scope dilution, skill for a
flat recall miss on the one thing the case was built to test.
