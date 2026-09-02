# Adversarial verification — Case C: WorkspaceDetails.tsx

Verifier method: read rubric.md and the case's grading key, read both run
transcripts and the fixture source, then independently re-fetched every
cited Cloudscape URL (via a real browser session clicking through to the
"Usage" tab, cross-checked against the site's embedded JSON payload via
curl, since the static WebFetch/defuddle renders only return the
above-the-fold landing text for these client-routed pages) to confirm each
quoted string actually appears on the cited page, rather than trusting
either review's quotation marks.

Fixture ground truth (confirmed by reading
`cases/case-c-workspace-details/fixture/src/pages/WorkspaceDetails.tsx`):
lines 30–33 carry an explicit comment stating the general-configuration
facts are "relevant no matter which tab a user is currently looking at";
lines 73–89 render those facts as a `Table` with a single synthetic row
(`items={[{}]}`, `trackBy={() => 'workspace-overview-row'}`) inside the
"Overview" tab of a `Tabs` component; Members (lines 92–108) and Activity
(lines 109–118) are the other two tabs, each showing per-item data proper
to a real multi-row `Table`/`List`.

---

## Baseline review

### Baseline Finding 1 — Single-row `Table` should be `KeyValuePairs`

- **Grade: B**
- Q1 (repo evidence): accurate — lines 73–89, synthetic `trackBy`, one-row
  `items` array, `StatusIndicator` in a cell, all verified against the
  fixture.
- Q2 (citation accuracy): fully verified. Independently confirmed on the
  live key-value-pairs usage page: "Key-value pairs are lists of
  properties (labels) followed by their corresponding values" and,
  verbatim, "Status indicator: For example, to show the status of a task,
  failed or successful." On the live Table usage page, confirmed verbatim:
  "Only use filtering, pagination, and sorting if there are more than five
  items in the table" and "Only use selection if the user can take action
  on the items in the collection." Every quote checks out exactly.
- Q3/Q4/Q5: applicability argument is sound (single resource, six scalar
  facts, Table's selection/sort/pagination contract is meaningless here);
  native alternative preserves the same data and task.
- Q6: materially real — a hard-coded single-row table with a fabricated
  `trackBy` is something an experienced Cloudscape implementer would flag.
- Q7: clean — this is a component-choice question, not implementation
  mechanics or generic UX.
- **Q8 (the deciding factor): this is the component half of a case
  explicitly designed as one unified `combined component + pattern`
  finding.** Reported as a standalone finding, separate from Finding 2's
  placement argument, it is exactly the "duplicated one issue across
  abstraction levels" failure the grading key calls out as wrong ("Two
  separate findings... this is exactly the failure mode SKILL.md's
  `combined component + pattern` type and rubric question 8 exist to
  catch"). The individual claim is correct and well-cited, which is why
  this isn't a D/E — but it is not the complete, correctly-scoped
  recommendation on its own, so it doesn't earn an A.
- Why an FDE would act on it: yes, in isolation this is a real, concrete,
  well-evidenced defect (a table faked into a one-row property grid) that
  is easy to act on — but per Q8, the report as delivered asks the FDE to
  treat this as one ticket and the tab-placement issue (Finding 2) as a
  separate one, when they are the same restructuring.

### Baseline Finding 2 — General config belongs in the summary container, not a tab

- **Grade: B**
- Q1: accurate — all three tabs modeled via `Tabs`, and the fixture's own
  comment (lines 30–33) is correctly quoted as distinguishing
  page-level/always-relevant content from tab-appropriate content.
- Q2: fully verified. Confirmed verbatim on the live details-page pattern:
  "Place the most relevant information about the resource in this
  container. To organize content, use key-value pairs," and the title-text
  options "General configuration" / "[Resource type] settings" both appear
  on the page. Confirmed verbatim on the live details-page-with-tabs
  pattern: "Don't introduce tabs if you can group your content into
  meaningful sections on a Details page. The number of sections is not an
  indicator of whether to use tabs."
- Q3/Q4/Q5: applicability is correct — the pattern names a persistent
  summary container as the documented home for exactly this content; the
  proposed move (Container/`KeyValuePairs`, `Tabs` reserved for
  Members/Activity) preserves the same task.
- Q6: materially real per the grading key's own framing (moving to
  `KeyValuePairs` while leaving it inside a tab would not fix the "hidden
  on other tabs" problem — this finding is the piece that actually fixes
  that).
- Q7: clean — grounded in the named pattern's structural rule, not generic
  "it's confusing to lose context" UX intuition.
- **Q8: same driver as Finding 1.** This is the pattern half of the one
  designed-to-be-unified finding, delivered as a second, separate item.
  Per the grading key, this exact split ("one for the Table→KeyValuePairs
  swap, one for the tabs-persistence structure") is the named wrong
  answer.
- Why an FDE would act on it: yes — this is the more consequential half
  (it's the one that actually restores cross-tab visibility), but
  delivered separately from Finding 1 it invites fixing the component
  without necessarily also fixing the placement, or vice versa, since the
  report doesn't present them as one restructuring.

### Baseline Finding 3 — Activity entries should follow the timestamps pattern

- **Grade: D**
- Q1: accurate — lines 24–28/112–117, each `ACTIVITY` entry is one
  pre-formatted string rendered via `List`'s `renderItem`.
- Q2: citations are, unusually, all fully accurate. Independently
  confirmed on the live timestamps pattern page: the label format
  "[label] [timestamp] by [name]," the "[Noun] [verb]" label shape with
  the "Template edited 6 hours ago by plrs" example, and the accessibility
  requirement to "Wrap the relative timestamp in a `<time>` element and
  set the `datetime` attribute..." plus the `title`-attribute guidance —
  every quoted fragment is verbatim on the page.
- **Q6/case design: this is a finding on the Activity tab.** The grading
  key is explicit and unqualified: "A finding on the Members or Activity
  tabs: false positive — these are correctly-scoped, ordinary tab content
  and should not be flagged." Regardless of citation accuracy, this
  finding sits squarely in the case's designed false-positive zone. The
  underlying data is three hard-coded demo strings in a fixture, not
  evidence of a real feed a user depends on for precise timestamp
  navigation — materiality here is genuinely weak, and the "why it
  matters" section leans on the accessibility hover/`title`-attribute
  mechanics of `<time>`, which is `cloudscape-implementation-audit`'s
  domain (Q7), not component/pattern alignment.
- This is the one place baseline fell into a designed trap that the skill
  run correctly avoided (see skill's Orientation notes below, which
  explicitly checked List/Activity and declined to find an issue).
- Why an FDE would (not) act on it: an FDE would likely treat this as a
  copywriting/nice-to-have normalization at best, not something worth
  restructuring a demo activity feed for — it doesn't meet the bar the
  case was built to test.

### Baseline "Not flagged" section (header buttons, List-for-Activity component choice, breadcrumb depth)

Not graded individually (these are explicit non-findings), but all three
judgments are reasonable and consistent with what's actually documented —
worth noting because they show baseline's suppression discipline was
generally sound; the miss was specifically Finding 3's activity-*content*
framing, not the List-vs-something-else component choice.

---

## Skill-guided review

### Skill Finding 1 — Overview general config as fabricated Table inside a tab, instead of persistent `KeyValuePairs`

- **Grade: B**
- Q1: accurate and thorough — lines 34–91, the synthetic single row, the
  `cell` functions that ignore their row argument, and the code's own
  comment are all correctly cited.
- Q2 (citation accuracy — mixed, and this is the deciding factor):
  - Confirmed **verbatim** on the live details-page-with-tabs pattern:
    "important information that applies to tasks in all the tabs" and
    "always visible when users switch between the tabs."
  - Confirmed **verbatim** on the live key-value-pairs page: "lists of
    properties (labels) followed by their corresponding values."
  - Confirmed **verbatim** on the live Table page: the borderless variant
    exists "to place a table inside a container with other content, such
    as key-value pairs."
  - **Not found, anywhere on the cited key-value-pairs page**: the quoted
    fragment "displaying read-only property information... resource
    identifiers and metadata." I fetched and full-text-searched the raw
    page content (including the embedded rich-text JSON payload) for
    "read-only propert", "resource identifier", and "metadata" — none of
    these phrases exist on that page. This is presented in quotation marks
    as if directly quoting the same source as the (accurate) adjacent
    quote, and it does not check out. This is a fabricated citation.
  - **Not found as quoted** on the cited details-page pattern: "Details
    summary container (primary information using key-value pairs)." The
    actual page text under that heading reads "Place the most relevant
    information about the resource in this container. To organize
    content, use key-value pairs" — no "primary information" phrasing
    appears anywhere on the page. This is a misquote presented as a direct
    citation.
  - Minor: "more than five items in the collection" is presented in
    quotes; the actual Table page text says "more than five items **in
    the table**." A small word-substitution, not a fabrication, but still
    not the verbatim quote it's punctuated as.
  - Net: of roughly six quoted fragments in this finding, four check out
    exactly and two are unsupported by the cited page (one fabricated
    outright, one a misquote), plus one minor word substitution.
- Q3: the four-point applicability test is worked through explicitly and
  correctly (single resource, same task, same data, material mismatch) —
  this is the strongest part of the finding.
- Q4/Q5: native alternative preserves task semantics; boundary check
  correctly argues the current Table/Tabs usage is "mechanically valid"
  but not the documented fit.
- Q6: materiality argument is well made and specific (facts the code's own
  comment says should be cross-tab-visible are hidden the moment a user
  leaves the first tab).
- Q7: explicit, correct boundary check distinguishing this from
  implementation mechanics and generic UX.
- **Q8: this is exactly the case's designed intent — one finding, typed
  `combined component + pattern`, unifying the Table→KeyValuePairs swap
  and the tabs-placement issue.** Structurally this matches "what a
  correct response looks like" in the grading key almost point for point
  (single finding, high materiality, cites both the component fit and the
  pattern's persistent-summary language, explicit applicability argument,
  explicit boundary check). This is the clearest pass on Q8 of anything in
  either review.
- Net grade: the structural/substantive achievement (Q1, Q3–Q8) is A-level
  and matches the case's designed intent almost exactly — but Q2 is
  genuinely violated by a fabricated quote and a misquote sitting directly
  alongside accurate ones in the same evidence paragraph. Because the
  claim remains fully supported by the *other*, independently-verified
  quotes in the same finding (the KeyValuePairs core-purpose quote, the
  Table borderless-variant quote, and both details-page-with-tabs quotes
  are sufficient on their own to carry the argument), this doesn't fall to
  D/E — but it cannot be called "strongly validated" without
  qualification, so it lands at B rather than A.
- Why an FDE would plausibly act on it: yes — even discounting the two bad
  quotes, the remaining accurate citations and the applicability/boundary
  reasoning are more than sufficient to justify the restructuring; an FDE
  would restructure this exactly as recommended (KeyValuePairs, in a
  persistent summary container, outside the Tabs).

### Skill "Suppressed" note — Members `Table<Member>` below the five-item guideline

Not a positive finding; graded as a suppression judgment. Correct per the
grading key (Members should not be flagged) and correctly reasoned — three
comparable-attribute rows across multiple distinct entities is exactly
Table's documented shape, unlike the Overview tab's single-entity property
grid. Minor: characterizing the five-item guideline as "advisory
('consider')" slightly mischaracterizes its actual wording ("Only use
filtering, pagination, and sorting if there are more than five items in
the table" — an "only use X if Y" construction, not one using the word
"consider"), but the substantive suppression call is right.

### Skill "Orientation notes" (page shell, Tabs for Members/Activity, Members Table, Activity List)

Not graded individually — these are explicit no-issue notes. All are
consistent with the case's designed intent (Members/Activity should not be
flagged) and, notably, the Activity/List note explicitly states a check
was made and no mandating pattern was found — correctly avoiding the exact
trap baseline's Finding 3 fell into.

---

## Case-level verdict

**Designed intent**: one unified finding, `Type: combined component +
pattern`, high materiality — pulling the general-configuration facts out
of the Overview tab entirely into a persistent `KeyValuePairs` summary
container outside the `Tabs`, with Members/Activity correctly left alone
as ordinary, unremarkable tab content.

- **Skill review: matches the designed intent.** It produced exactly one
  finding, explicitly typed `combined component + pattern`, that unifies
  both halves (Table→KeyValuePairs and tabs-placement) into the single
  recommended restructuring, and it correctly left Members/Activity
  unflagged with reasoning that shows the "no pattern found" search was
  actually performed. The one real defect is a citation-integrity problem
  in Finding 1 (a fabricated quote and a misquote, detailed above) —
  material enough to keep the finding out of "strongly validated" A
  territory, but not enough to overturn a correct, well-structured,
  intent-matching result.
- **Baseline review: does not match the designed intent.** It found the
  same two underlying facts (component mismatch, and pattern-placement
  mismatch) — each individually well-evidenced with fully accurate
  citations, better citation hygiene than the skill review, in fact — but
  reported them as two separate findings rather than one unified
  `combined component + pattern` finding. This is precisely the failure
  mode rubric question 8 and the grading key's "what would be wrong"
  section describe. Baseline additionally produced one designed-false-
  positive finding (Finding 3, on the Activity tab), which the skill
  review correctly avoided.

**Summary trade-off**: baseline has better per-quote citation discipline
but the wrong finding-granularity structure (fails Q8) plus one
false-positive; skill has the exactly-right finding structure (passes Q8,
matches intent) but weaker citation discipline within that one finding
(two bad quotes out of roughly six). On the dimension this case exists to
test — Q8, unification of combined component+pattern issues — the skill
review is the one that got it right.
