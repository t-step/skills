# Adversarial verification: case-real (Identities.tsx, sample-bedrock-spend-budget-guardrails)

Verifier method: read the rubric, both reviews, and the three fixture files in full;
independently re-fetched and confirmed every cited Cloudscape page via a rendered
browser (component/pattern docs are client-rendered SPAs — a plain HTML fetch only
returns the one-line component blurb, so citations were checked against the
`?tabId=usage` rendered text, not the SPA shell). No grading key exists for this
case; grades below are argued from the rubric's nine questions and the cited
authority text actually fetched.

Live source confirmations obtained (verbatim unless noted):
- Table View pattern: *"Don't use the content layout component on this type of
  page. Instead, use the 'full-page' variant of the table component to implement
  this pattern."* / converse: *"Don't use the table view pattern for tables that
  aren't overly content-heavy. Instead... use a bordered table inside the content
  layout component."* — confirmed.
- Content Layout usage guidelines (`/components/content-layout/?tabId=usage`):
  *"Don't use the content layout component for productive use cases such as
  resources creation, view, edit, and delete."* — confirmed, exact.
- Table usage guidelines (`/components/table/?tabId=usage`), Variant → Full page:
  *"This variant is for implementing the full page table view pattern. Use it for
  presenting and managing a table with many columns within a stand-alone page. We
  suggest enabling the sticky header and using the 'awsui-h1-sticky' variant of
  the header with this variant... Use this variant in conjunction with the
  contentType="table" property on the App Layout..."* — confirmed, exact,
  including the real `awsui-h1-sticky` enum value.
- Modal usage guidelines: *"Keep the text short and interactions to a minimum. Try
  to avoid scrolling content."*; *"Use a modal primarily to confirm or cancel a
  choice. For example, deleting a resource."*; intro line *"It prevents interaction
  with the main page content, but keeps it visible with the modal as a child
  window in front of it."* — confirmed, exact.
- Split View pattern: objectives include *"Users need to quickly check or compare
  relevant resource details to troubleshoot an issue"* (troubleshooting) and *"By
  default, it's closed on page load and opens automatically on resource
  selection."* — confirmed, exact.
- Filter patterns page: *"For complex products with large collection of
  resources, use the property filter so that users can combine multiple
  properties, values, and operators."* and *"If the common behavior of users is to
  filter a resource by only one or two properties, use the collection select
  filter. For example: by 'status' or 'type'."* — confirmed, exact.
- Table View pattern, Pagination building block: *"Pagination helps users with an
  extensive number of resources to navigate through them across multiple
  pages... Display the pagination even if the resources set fits in one page."* —
  confirmed, exact; and Table usage guidelines: *"Only use filtering, pagination,
  and sorting if there are more than five items in the table"* — confirmed, which
  matters below because it makes these building blocks conditional on volume, not
  unconditional.
- DateRangePicker guidance cited only in the skill's "Orientation notes" (not a
  graded finding) could not be independently re-confirmed — the live site's
  client router repeatedly redirected away from that page mid-fetch across
  several attempts. Since it's an orientation note, not a finding, this does not
  affect any grade below, but is flagged as unverified.

Fixture facts confirmed directly from the three files: `Identities.tsx` is a
single `ContentLayout` wrapping one 8-column `Table` (`variant="container"`,
`resizableColumns`, `stickyColumns={{first:1,last:1}}`, `wrapLines`,
`stickyHeader`) with no `filtering` key on `useCollection` and no `pagination`
prop; row actions are "Create budget" (navigates to `/budgets?principal=...`) and
"Activity" (opens `PrincipalActivityModal`, a `Modal size="large"` rendering the
shared, unbounded `ActivityTable`).

---

## Baseline findings

### Baseline Finding 1 — No filter control on a multi-property, potentially large table

**Grade: B**

- Q1: Supported. Table has 8 columns, `useCollection` has `sorting` only, no
  `filtering` key, no filter slot on `<Table>` — verified directly against lines
  80–87 and the `columnDefinitions` block.
- Q2: Citations confirmed exact (table-view Filter building block; filter-patterns
  selection-criteria prose, including the "by 'status' or 'type'" example that
  maps well onto this table's Type/Account/SSO columns).
- Q3/Q6: Applicability is plausible, not certain. The code comments do describe
  "multi-account installs" and "wildcard admins viewing many accounts" (lines
  194–197), which supports discrete-property filtering being useful, but nothing
  in the fixture establishes an actual row count — and the Table usage guidelines
  say these features should only be used "if there are more than five items,"
  making this conditional rather than unconditional. The finding itself
  appropriately hedges ("optional-but-expected") rather than overclaiming.
- Q7: Clean — pattern-level (filter slot choice), not implementation mechanics.

Why an FDE would plausibly act: reasonable if principal counts are actually large,
but the finding doesn't establish that they are, so it reads as a good backlog
item rather than a must-fix — B, not A.

### Baseline Finding 2 — ContentLayout + `variant="container"` instead of `full-page` table variant

**Grade: A** — see the dedicated scoping discussion below; this is the finding
that must be checked against the sibling eval's D-graded overreach.

- Q1: Supported — the page is exactly one `ContentLayout` wrapping one 8-column
  `Table`, with `resizableColumns`/`stickyColumns`/`wrapLines` present and
  commented as viewport-overflow workarounds (lines 139–142) — verified directly.
- Q2: Both cited pages confirmed to say exactly what's claimed, verbatim (Table
  View pattern's "don't... instead" rule, and its converse for few-column tables).
- Q3: The applicability argument, though one sentence, correctly applies the
  pattern's own two-sided test (content-heavy → full-page; few columns →
  ContentLayout+bordered) to concrete evidence (8 columns, workaround props) —
  this is a real applicability argument, not "the docs contain another example."
- Q4: Native alternative (`Table variant="full-page"`) preserves identical data,
  columns, actions — no redesign.
- Q5: Table docs' own "Container" variant description ("feature a table in a
  stand-alone container with its own hierarchy, e.g. a details page") doesn't fit
  this page (Identities is a top-level resource list, not a details page nested in
  a container), which weakens the "equally valid alternative" counter-argument.
- Q7: Clean — pattern/variant selection, not implementation correctness (the
  finding doesn't touch prop misuse or a11y mechanics).
- Weakness relative to the skill's version: doesn't mention that a full
  realization also requires coordinating `AppLayout`'s `contentType="table"`
  outside this file — an omission of completeness, not an error.

Why an FDE would plausibly act: two independent authoritative pages give the same
explicit "don't do X, do Y" instruction for exactly this page shape (single
full-page resource table), and the fix is a variant swap with zero semantic
change — this is squarely actionable.

### Baseline Finding 3 — Per-row Modal for activity drill-in vs. Split view

**Grade: B**

- Q1: Supported — verified `Identities.tsx` lines 267–274/281–287 and
  `PrincipalActivityModal.tsx`'s `Modal size="large"` wrapping an unbounded
  `ActivityTable`.
- Q2: The Modal quote used ("prevents interaction... keeps it visible...") is
  accurate but is the component's one-line intro blurb, not deeper usage guidance
  — a real quote from the real page, but the weakest evidence available on that
  page (the skill's version instead cites "avoid scrolling content," which is
  stronger and more specific to this content-heavy modal). Split View quote
  ("opens automatically on resource selection") confirmed exact.
- Q3/Q6: Applicability is inferential rather than an explicit rule ("don't use a
  modal for X") — no cited page forbids this outright. Real gap, but weaker than
  Finding 2.
- Q7: Clean — container/pattern choice, not implementation mechanics.

Why an FDE would plausibly act: plausible for a "check several principals in
turn" workflow, but nothing forces the change, and the evidence chain is more
inferential than Finding 2's.

### Baseline Finding 4 — No pagination on the table

**Grade: C**

- Q1/Q2: Both confirmed accurate (no `pagination` prop/key; Table View pattern's
  Pagination building block text confirmed verbatim, including "even if the
  resources set fits in one page").
- Q3/Q6: The pattern marks this building block optional and states no row-count
  threshold; the Table usage guidelines gate it on "more than five items," and
  the fixture gives no evidence of actual identity volume (the "wildcard admin,
  multi-account" comments support the filter finding but don't establish a large
  row count for pagination specifically). The finding itself flags this as its
  weakest, most hedged item.
- This is the textbook "correctly identified but low materiality, should be
  suppressed" case: the skill review, given the same evidence, explicitly
  suppressed the equivalent finding for exactly this reason. Baseline surfaces it
  as a full finding instead of exercising that discipline — not wrong, just
  routine.

Why an FDE would (not) act: without volume evidence this reads as a nice-to-have,
not something that reorders a backlog.

---

## Skill findings

### Skill Finding 1 — ContentLayout wrapping the table instead of `Table variant="full-page"`

**Grade: A** — same underlying claim as Baseline Finding 2, independently verified
the same way (Q1–Q7 above all apply and check out), plus additional rigor: full
four-point applicability writeup, the real `awsui-h1-sticky` enum value confirmed
on the live Table docs, and an explicit, honest flag that the `AppLayout
contentType="table"` half of the fix lives outside the bounded surface rather than
being silently assumed.

**This is the decisive scoping question for the case, so it gets its own
analysis.** The sibling `cloudscape-implementation-audit` eval's iteration-2 run
made functionally the same recommendation on this exact file and was
independently graded **D (overreach)** by that eval's verifier — not because the
underlying Cloudscape citation was wrong, but because (a) component/pattern
selection is explicitly outside `cloudscape-implementation-audit`'s declared
scope, so recommending it at all was already leaking into a different skill's
job; (b) it was asserted as a `violation` at REQUIRED strength off a pattern-page
citation that skill's own retrieval-priority scheme treats as a weaker, priority-4
source meant only to "establish a concrete rule already in play," not license a
page-composition mandate; and (c) half the fix (`AppLayout`) was left outside the
audited files without being named as a caveat.

Checking this run against those same three failure vectors:
- **(a) Domain fit:** `cloudscape-native-expression-review`'s job *is* component
  and pattern selection — this is not an implementation-audit skill borrowing
  someone else's authority. The finding's own `Boundary check` field states this
  explicitly: *"This is about which page-structure/table-variant concept
  Cloudscape composes for a full-page resource table, not whether `ContentLayout`
  or `Table` are each implemented correctly (both are used validly per their own
  APIs)."* That is exactly the line the sibling skill's finding blurred, drawn
  correctly here.
- **(b) Strength vs. evidence:** The finding is typed `combined component +
  pattern` (not `violation`), and its REQUIRED authority strength is earned by an
  explicit, fully-written four-point applicability argument (task match, current
  implementation solves the same problem, alternative preserves semantics, both
  cited pages state this as an explicit prohibition for this precise scenario) —
  not "the docs contain another example" dressed up, and not a bare citation.
- **(c) Incomplete fix named honestly:** The `AppLayout` dependency is called out
  by name as "a real dependency rather than assumed away," in the finding's own
  text — the opposite of the sibling's silent omission.

**Verdict on the single most important question: this run avoided the sibling
skill's exact overreach failure mode rather than repeating it in a new guise.**
The underlying Cloudscape claim is the same and equally well-supported in both
cases; what differs — correctly — is that here it is in-scope, honestly qualified,
and framed as pattern composition rather than an implementation violation.

### Skill Finding 2 — Modal for activity drill-in vs. SplitPanel

**Grade: B** — same substance as Baseline Finding 3, independently checked the
same way, with a materially stronger Modal citation ("avoid scrolling content,"
confirmed verbatim and directly on point for an unbounded, scrolling activity
log) than baseline used. The skill correctly self-labels this weaker than Finding
1 (medium/medium vs. high/high), which matches this verifier's independent read:
no page forbids modals outright here, and the case rests on converging rather
than singular authority. Boundary check is clean (container choice, not Modal/
ActivityTable implementation correctness).

### Skill's suppressed items (not separately graded — correctly withheld)

- **No pagination:** suppressed for the same reason this verifier downgraded
  Baseline Finding 4 to C — no documented threshold, no volume evidence in the
  fixture. This is the correct call and mirrors the rubric's own guidance that
  C-grade findings are "expected to be suppressed by the skill's own materiality
  discipline, not a verifier failure."
- **Badge severity-color choice:** correctly identified as a token/semantic
  question inside an already-correct component choice, i.e.
  `cloudscape-implementation-audit`'s domain, not this skill's. Good boundary
  discipline — the same discipline the sibling skill's flagship finding lacked.

---

## Case-level verdict

**Baseline:** Four real, evidence-grounded findings, no factually wrong claims,
all citations checked out verbatim against the live rendered docs. Three of four
land B or better; the fourth (pagination) is a real-but-low-value finding that a
more disciplined process would have suppressed rather than surfaced at equal
weight with the others. Baseline's ContentLayout/full-page finding independently
lands at A on its own merits and, notably, never drifts into implementation-audit
territory or unsupported confidence — but it is thinner than the skill's version
(one-sentence applicability argument, no mention of the `AppLayout` dependency, a
weaker Modal quote for Finding 3), so overall this is a solid, calibration-neutral
review that would benefit from an explicit materiality/suppression discipline.

**Skill:** Two findings (A, B), two explicitly and correctly suppressed
candidates, and explicit `Type`/`Boundary check`/`Authority strength` metadata
that made independent verification straightforward. On the question this case
exists to test — whether the ContentLayout/full-page finding is now correctly
scoped as pattern composition rather than repeating the sibling
implementation-audit skill's exact D-graded overreach — **the answer is yes**:
this run's Finding 1 is in-scope for what this skill actually does, backed by a
genuine four-point applicability argument rather than "a pattern page exists,"
explicitly separated from implementation correctness in its own boundary check,
and honest about the part of the fix that falls outside the audited files. This
is the clean, positive result the sibling eval's iteration-2 run failed to
produce on the same fixture.
