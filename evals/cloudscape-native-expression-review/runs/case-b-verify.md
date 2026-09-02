# Verification — Case B: EndpointScaling.tsx (fleet cards)

Verifier method: read rubric.md, grading/case-b-fleet-cards.expected.md, both
run transcripts, and the fixture source directly. Independently re-fetched
every cited Cloudscape URL (patterns/resource-management/view/card-view,
patterns/resource-management/view/table-view, components/table,
components/cards) via a rendered browser session (WebFetch alone returned
only nav shell for the two component pages, since they're client-rendered —
Playwright `document.body.innerText` was used to get full text) and diffed
every quoted string against the live page text.

## Citation-accuracy summary (both reviews)

All quotes checked by both baseline and skill were verified **verbatim
accurate** against the live pages:

- Card view: "effective for glancing at small sets of similar resources with
  text, numerical, and imagery data sets" — confirmed.
- Card view "Do": "Use cards to display non-columnar, yet comparable data."
  — confirmed.
- Card view "Don't": "Don't use the content layout component on this type
  of page. Instead, use the 'full-page' variant of the cards component to
  implement this pattern." — confirmed.
- Card view "Related patterns" (Table view): "effective for quickly
  identifying categories or comparing values in a large text and numerical
  data set." — confirmed (baseline correctly attributes this to the
  card-view page's *related-patterns* blurb about table view, not the
  table-view page itself).
- Card view Filter building block: "Text filter helps users with an
  extensive number of table rows to quickly find one or several resources
  with a matching query." — confirmed (this literal "table rows" wording
  appears verbatim on the *card*-view page too — a copy/paste artifact in
  Cloudscape's own docs, not an error introduced by either review).
- Card view Selection building block: "Cards can be selected individually
  or in bulk (multiple selection) by using the checkbox mechanism. Actions
  initiated after selection affect only the selected, visible cards." —
  confirmed.
- Table view: "Use table view pattern for static data with multiple
  attributes displayed in a tabular format." / "The best data type for a
  table view is data that is structured, easily comparable, and sortable."
  — confirmed. "Don't use the content layout component..." full-page
  variant rule — confirmed, worded identically for table.
- Table component usage guide, Cell: "Right-align quantitative numeric data
  within table cells to make them easier to compare and contrast... This
  consistency helps users to quickly scan lists and compare values." —
  confirmed exact.
- Table component usage guide, Multi-column sorting: "useful when users
  need to analyze multi-dimensional data. For example: Grouping by instance
  type, then rank by highest CPU within each type to find over-provisioned
  instances." — confirmed exact.
- Cards component usage guide: Features list is exactly Filtering,
  Pagination, Preferences — no Sorting feature exists for Cards anywhere on
  the page — confirmed (skill's "no sorting feature exists for Cards at
  all" claim holds).
- Cards component usage guide: "Only use filtering and pagination if there
  are more than five cards in the collection." — confirmed (matches skill's
  paraphrase "add filtering and pagination once a collection exceeds five
  items").
- Cards component usage guide: "Use icons in cards only to show status." —
  confirmed (skill's orientation note).

No fabricated or misrepresented citation was found in either review. Every
quote checked matches the source verbatim and in the context claimed.

---

## Baseline findings

### Baseline Finding 1 — Cards used for a columnar, sortable comparison task instead of Table
**Grade: A**

- Q1 (task evidence): Fully supported — quotes the file's own comment
  (lines 29–33) and header `description` (line 40) verbatim; not invented.
- Q2 (citation accuracy): Confirmed exact, see above.
- Q3 (applicability test): Passes all four prongs implicitly — engages
  data shape (columnar/numeric, no imagery), collection size (22, not
  "small"), and the explicit comparison-to-decide task from the page's own
  copy.
- Q4 (task-semantics preservation): Yes — proposes Table with the same
  data, same "Scale up" action, framed as enabling (not replacing) the
  stated comparison task via sort.
- Q5 (equally valid as-is?): No — grading key confirms Cards was
  mechanically correct but the wrong component choice; baseline reaches the
  same conclusion via the same reasoning path the grading key prescribes.
- Q6 (materiality): High — an FDE would plausibly restructure this; the
  finding names the concrete mechanism (sort) the task requires and Cards
  categorically lacks.
- Q7 (boundary): Genuinely component/pattern-level, not implementation or
  generic UX.
- Q8 (duplication): N/A, single finding.
- Q9 (intent-dependent): N/A, task is stated explicitly in the file, not
  inferred.

This is close to a word-for-word match of the grading key's "what a correct
response looks like": same applicability reasoning, same Table
recommendation with sort as the concrete mechanism, same boundary framing.
Minor, non-disqualifying gap: baseline doesn't use the skill's structured
`Type`/`Materiality`/`Confidence` finding-contract fields (expected, since
this is the unguided baseline) — content quality is what's graded and it is
excellent. An FDE reading this would very plausibly open a ticket to
re-platform the page onto Table.

### Baseline Finding 2 — ContentLayout used instead of the pattern's full-page variant
**Grade: D**

- Driven by Q3, Q5, Q9. The cited "Don't use ContentLayout, use full-page
  variant" rule is real and accurately quoted (confirmed above, present
  nearly verbatim on both the card-view and table-view pattern pages). But
  the grading key states explicitly: *"The page composition around it
  (ContentLayout + Header with a task-describing description) is ordinary
  and not itself a finding."* Baseline asserts this as a confident,
  named-anti-pattern finding ("This is an explicit, named anti-pattern for
  exactly this page archetype") without engaging the real ambiguity: a
  single-file fixture cannot establish whether `EndpointScaling` is meant
  to be the canonical standalone top-level "view resources" page (where the
  full-page building block would apply) or a page embedded within a larger
  app-shell/content area (where `ContentLayout` + a container-variant
  collection is ordinary, valid composition). The skill review encountered
  this identical fork and explicitly suppressed it for exactly this reason
  — the case design rewards that judgment call, and baseline's confident
  assertion is the failure mode Q9 targets (asserting an answer on missing
  intent instead of classifying it intent-dependent or declining).
- An FDE would not restructure the page's layout container on this
  evidence alone — the finding treats a documented building-block rule as
  a mandate without establishing that this specific fixture is a top-level
  page rather than an embedded view.

### Baseline Finding 3 — No text filter for an "extensive" resource set
**Grade: C**

- Driven by Q6. Citation is accurate and the "more than five cards →
  add filtering/pagination" Cards-specific threshold is real and confirmed,
  so this isn't wrong. But it isn't part of the case's designed finding
  space either — it's a routine collection-hygiene suggestion that doesn't
  bear on the core diagnostic (Cards vs. Table for a comparison task) and
  remains true regardless of which component wins that argument (a Table
  would want the same filter). Not the kind of thing that moves an FDE's
  actual decision; more a checklist nit that would get folded into
  whichever component is chosen, not a separate action item.

### Baseline Finding 4 — No selection/bulk-action mechanism despite plural "one(s)"
**Grade: D**

- Driven by Q1, Q6. The Selection building-block quote is accurate, but the
  inferred requirement — that the operator specifically needs to bulk-apply
  "Scale up" across multiple endpoints in one action — is built on thin
  evidence: a single grammatical hedge, "one(s)," in the header description.
  That reads at least as plausibly as ordinary singular/plural hedging in
  UI copy as it does a deliberate signal for a bulk-operation requirement.
  This is scope creep beyond the stated task (which is *comparison to
  decide*, not *bulk execution of the decision*) and isn't part of the
  case's designed finding. An FDE would likely read this as speculative
  rather than actionable.

---

## Skill findings

### Skill Finding 1 — Fleet comparison/scaling-decision task expressed as Cards instead of Table
**Grade: A**

- Q1: Fully supported — same file evidence as baseline, plus a concrete
  negative-evidence scan (no `sortingField`, no sort control, no filter,
  no pagination, no preferences slot anywhere in the file).
- Q2: All four distinct citations (card-view pattern, table-view pattern,
  table Cell right-align guidance, table multi-column-sort CPU example,
  Cards features list) confirmed verbatim accurate against the live pages
  — see citation-accuracy summary above. This is broader and more
  thoroughly sourced than baseline's version of the same finding.
- Q3: Explicitly runs the four-point applicability test as a labeled
  paragraph — data shape, task statement, current composition's structural
  gap (no sort mechanism at all), and a concrete same-semantics
  alternative. This is the clearest four-point-test execution of any
  finding in either review.
- Q4: Preserves task semantics exactly — same columns, same "Scale up"
  action, framed as an in-context row action rather than a workflow
  redesign.
- Q5: Explicitly and correctly reasons that Cards is not equally valid
  here because it has no comparable sort mechanism at all (confirmed:
  Cards' documented Features list is Filtering/Pagination/Preferences
  only, no Sorting).
- Q6: High materiality, well-argued — ties the recommendation to the
  specific documented multi-column-sort example ("rank by highest CPU...
  to find over-provisioned instances"), which is structurally identical to
  "rank by error rate to decide which to scale."
- Q7: Clean boundary check included as its own paragraph; correctly scoped
  to component/pattern alignment, explicitly declines to touch
  implementation correctness or generic UX (deferred to "What was not
  evaluated").
- Q8: Single unified finding, type `combined component + pattern` — this
  is the grading key's flagged labeling nuance (it suggests the cleaner
  label is `component selection` alone, calling a `pattern composition`
  mislabel a non-disqualifying issue). The skill didn't use `pattern
  composition`; `combined component + pattern` is defensible here since
  the finding genuinely draws on both component-level evidence (Cards'
  feature set lacks sorting) and pattern-level evidence (card-view vs.
  table-view fit) for one coupled issue, and it is *not* a case of splitting
  one issue into two separate findings — it's correctly unified. Not
  penalized.
- Q9: N/A — task stated explicitly, not inferred.

An FDE would very plausibly act on this: it's the single clearest,
best-evidenced finding across both reviews, with the applicability
reasoning made explicit and auditable rather than left implicit.

### Skill's suppressed item — ContentLayout vs. full-page variant
Not graded as a candidate finding (explicitly not asserted), but notable:
this is the same rule baseline turned into Finding 2, and the skill
correctly declined to assert it, naming the exact ambiguity (standalone
top-level page vs. embedded view) that the grading key's design also turns
on. This is precisely the Q9 behavior the rubric rewards, and it directly
tracks the grading key's statement that this composition is "ordinary and
not itself a finding."

---

## Case-level verdict

**Skill review: matches the case's designed intent.** One material,
correctly-scoped, thoroughly-sourced `component selection`-flavored finding
recommending Table over Cards for the comparison task, with an explicit and
well-reasoned four-point applicability argument, a semantics-preserving
native alternative (Table with sort, same columns, same action), a clean
boundary check, and correct suppression of the one plausible but genuinely
intent-dependent secondary issue (ContentLayout/full-page variant) rather
than asserting it. This is close to the best achievable outcome under the
rubric.

**Baseline review: partial match.** It found the same core, correctly-scoped
finding as the skill (Finding 1, grade A) via an independent and equally
sound applicability argument — the unguided baseline did not miss the
designed signal. But it then added three further findings not designed
into the case, one of which (Finding 2, ContentLayout) directly contradicts
the grading key's statement that this composition is "ordinary and not
itself a finding" — the baseline asserted it as a confident, named
anti-pattern rather than recognizing the same standalone-vs-embedded
ambiguity the skill correctly flagged and suppressed. The other two
(Finding 3: text filter; Finding 4: bulk selection) are real but routine/
thin-evidence additions that dilute the review's focus without being part
of the case's intended diagnostic. Net effect: the baseline's report would
hand an FDE the right primary conclusion buried alongside one questionable
overreach and two low-value asides — a materially noisier signal than the
skill's tightly-scoped single finding.

| Source | Finding | Grade |
|---|---|---|
| baseline | 1. Cards vs Table for comparison task | A |
| baseline | 2. ContentLayout vs full-page variant | D |
| baseline | 3. Missing text filter | C |
| baseline | 4. Missing bulk selection | D |
| skill | 1. Cards vs Table for comparison task (combined component+pattern) | A |
