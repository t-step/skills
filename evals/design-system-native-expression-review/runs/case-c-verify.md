# Adversarial verification — Case C: WorkspaceDetails.tsx

Reviewed against `evals/cloudscape-native-expression-review/rubric.md`,
the case's grading key
(`evals/cloudscape-native-expression-review/grading/case-c-workspace-details.expected.md`),
the fixture
(`evals/cloudscape-native-expression-review/cases/case-c-workspace-details/fixture/src/pages/WorkspaceDetails.tsx`),
`skills/design-system-native-expression-review/SKILL.md`, and the run
under test
(`evals/design-system-native-expression-review/runs/case-c-skill.md`).

All cited Cloudscape pages were independently fetched live
(cloudscape.design) on 2026-09-02, both via WebFetch and via raw `curl`
of the `index.html.md` markdown sources, to get exact copy-paste text
rather than a summarized paraphrase.

---

## Finding #1 — "Overview tab's workspace properties: Table (one synthetic
row) inside a tab → Key-value pairs in an always-visible summary
container"

**Type as reported:** `combined selection + composition` · Materiality:
high · Confidence: high

### Nine-question pass

1. **Task supported by repo evidence?** Yes, strongly. Lines 34–91 match
   the review's description exactly: `Table` given `items={[{}]}`,
   `trackBy={() => 'workspace-overview-row'}`, six `columnDefinitions`
   whose `cell` callbacks ignore their row argument, `ariaLabels.tableLabel`
   literally `"Workspace general configuration"`, and the file's own
   comment (lines 30–33) stating the data is "relevant no matter which tab
   a user is currently looking at." Nothing here is invented.

2. **Does the cited guidance say what's claimed?** Yes, verified live
   against both pattern pages' raw markdown:
   - "Details page" pattern, building block D: raw source reads *"Place
     the most relevant information about the resource in this container.
     To organize content, use [key-value pairs](...)."* — matches the
     review's quote exactly once the markdown link is stripped.
   - "Details page with tabs" pattern, building block D: raw source reads
     *"For a **details page with tabs**, this section serves as a summary
     that is always visible when users switch between the tabs."* and, as
     a separate bullet, *"Use it to display important information that
     applies to tasks in all the tabs."* — matches.
   - Building block E ("Tabs"): raw source reads *"Examples of content
     that can be grouped into sections in a single tab: logs, charts, and
     data visualization for monitoring, key-value pairs, and
     descriptions."* — matches exactly.
   - The claimed cross-reference ("the tabs-variant page explicitly
     delegates to the base 'Details page' page for this exact building
     block") is real: block D literally opens "Follow the guidelines for
     [details page]" before adding the tabs-specific persistence rule.

3. **Applicability test (4-point) genuinely passed?** Yes. This is a
   single resource, the six properties are simple, stable, read-mostly
   scalars, and the file's own comment independently states the
   always-relevant-regardless-of-tab semantics the pattern names — this
   is not "the docs have an adjacent example," it's the same named
   building block for the same page type holding the same kind of
   content.

4. **Preserves task semantics?** Yes. Same information, same actions
   (Edit/Delete unchanged), Members/Activity remain tabs exactly as
   before; only placement and componentization change.

5. **Could current usage be equally valid, documented Cloudscape
   practice?** No credible counter-reading. A one-row `Table` with a
   synthetic `trackBy` for six always-true facts, hidden by tab
   switching, has no supporting "Don't" it satisfies and directly
   collides with the pattern's explicit "always visible... when users
   switch between the tabs" instruction. The current design's own code
   comment concedes the intended semantics are being defeated.

6. **Materially actionable?** Yes — an experienced Cloudscape implementer
   would restructure this on sight; it isn't a matter of taste.

7. **Genuinely component/pattern-level, not implementation or generic
   UX?** Yes. The boundary check is specific and correct: the finding
   never touches API/prop mechanics, and "Why it matters" is grounded in
   the pattern's explicit persistence rule rather than a bare "it's
   confusing to lose context" framing — exactly the trap the grading key
   warns against.

8. **Split across levels when it should be unified? (the case's central
   test)** No — and this is the important result. The review reports
   **one** finding, `Type: combined selection + composition`, that
   explicitly covers both the componentization (`Table` → `KeyValuePairs`)
   and the placement (`Overview` tab → persistent summary container
   outside `Tabs`) as one recommendation, with a single "Native
   expression" that does both moves together and even independently
   arrives at "drop the Overview tab" — a detail the grading key calls
   out as part of a fully correct answer. This is exactly the unification
   question 8 and the case were designed to test, and it passes cleanly.

9. **`intent-dependent` handling?** N/A — this finding correctly isn't
   classified `intent-dependent`; there's no genuine ambiguity here to
   mishandle.

**Grade: A — material and strongly validated.** All four applicability
points check out under independent re-fetch, task semantics are
preserved, the finding stays inside the component/pattern boundary, and
— critically — it is the single unified finding the case was designed to
require rather than a split into a Table-swap finding and a
tab-placement finding. An FDE would plausibly act on this immediately:
the file's own comment states an intent the implementation actively
violates, and the fix is small, concrete, and fully supported by the
pattern's own text.

### Citation-integrity notes (do not change the grade, but are real)

- **Authority evidence, "Details page" writing guidance quote** — the
  review renders this as one quoted sentence: *"For the details summary
  container, use this text: General configuration / [Resource type]
  settings."* The raw source is actually a heading plus a two-item
  bulleted list:
  ```
  - For the details summary container, use this text:
    - *General configuration*
    - *[Resource type] settings*
  ```
  The review collapsed the two list items into one string joined by
  `" / "` — a separator that does not appear on the page at all. The
  substance is accurate (both label options are real and correctly
  paired), but as rendered in quotation marks the string is not literally
  copy-paste-verifiable against the source; it's a reformatted paraphrase
  presented as a direct quote. **Minor conflation, flagged.**
- **Evidence-mode rationale (line with "(VERBATIM from ...)" labels)** —
  in justifying the `SYNTHESIS` classification, the review writes: *"use
  key-value pairs to organize this container's content" (VERBATIM from
  "Details page")* and *"this container is always visible across tabs,
  distinct from tab content" (VERBATIM from "Details page with tabs")*.
  Neither quoted string is the source's actual wording — both are the
  reviewer's own paraphrase (word order changed in the first; "distinct
  from tab content" is an inferential gloss not present at all in the
  second), yet both are put in quotation marks and explicitly labeled
  `VERBATIM`. Per `SKILL.md`, quotation marks are reserved for `VERBATIM`
  mode specifically because it must be copy-paste-verifiable — these two
  short phrases fail that test even though the *primary* Authority
  evidence quotes above them (question 2, above) are independently
  verified accurate. **Minor self-labeling inconsistency, flagged** — it
  does not misrepresent what the sources say, but it does violate the
  skill's own quotation-mark discipline in secondary/explanatory text.
- The `PARAPHRASE`-level claims in "Why it matters" about `Table`'s and
  `KeyValuePairs`' documented purposes are not put in quotation marks and
  were independently checked against the live component pages
  (`Table`: "collections of items" / comparison-oriented tabular display;
  `KeyValuePairs`: "lists of properties (labels) followed by their
  corresponding values") — both fairly represent the source without
  overclaiming. No issue.
- No `SYNTHESIS` source was fabricated or non-load-bearing: both cited
  pattern pages are real, both are directly on point, and the bridge
  between them (the tabs-page's own "follow the guidelines for details
  page" cross-reference) is real, not invented.

---

## Suppressed items — spot check

1. **Delete button has no wired behavior.** Correctly suppressed under
   "Missing intent": there is no delete flow to compare against a
   documented pattern at all, so naming a specific alternative would be
   guessing. Correct call.
2. **Activity tab's `List` of hardcoded strings.** The review quotes the
   `List` component's own "Don't" guidance verbatim: *"Don't use a list
   to display multiple columns of sortable data that users need to
   compare. Use a table instead."* Independently re-fetched and confirmed
   word-for-word accurate. The suppression reasoning (single-line
   chronological entries don't hit this "don't," and no named
   activity/audit-log pattern exists in this corpus) holds up, and
   matches the grading key's explicit statement that Activity is
   correctly-scoped false-positive material. Correct call, and this
   citation is clean.
3. **Breadcrumb depth (2 levels vs. the pattern's 3-level example).**
   Correctly suppressed as unresolvable from this bounded file alone
   (can't tell if a "service" tier exists elsewhere in the app) and low
   materiality either way. Reasonable call.

## Orientation notes — spot check

- **Members tab (`Table<Member>`).** Genuine multi-row resource
  collection with `trackBy`, `isRowHeader`, `empty` state — correctly
  left as no finding; matches the grading key's explicit statement that
  Members is deliberately unremarkable, correctly-scoped tab content.
  Correct call.
- **Outer page shell** (`ContentLayout`/`Header`/`BreadcrumbGroup`/`Tabs`)
  and **header actions** (`SpaceBetween` + Edit/Delete `Button`s) — both
  plausible as standard compositions; nothing in the fixture or fetched
  pages contradicts this. No independent citation was offered for these
  (they're asserted as "standard, documented composition" without a URL),
  which is a mild evidentiary thinness, but since no finding rides on
  them and they're correctly filed as "no finding," this doesn't warrant
  a downgrade.
- **`StatusIndicator` inside a table cell.** Reasonable, low-stakes
  observation that the same component works identically inside
  `KeyValuePairs` values — consistent with the finding's proposed fix and
  not contradicted by anything fetched.

---

## Case-level verdict: MATCH

The case was designed to test whether a reviewer would correctly produce
**one** `combined selection + composition` finding unifying the
Table→KeyValuePairs component swap with the Overview-tab→persistent-
summary-container placement issue, rather than fracturing it into two
findings at two abstraction levels (the specific failure mode rubric
question 8 exists to catch), and would correctly leave Members/Activity
unflagged.

The run does exactly this:

- **One** finding, correctly typed `combined selection + composition`,
  not two.
- The single "Native expression" addresses **both** halves together
  (componentization AND placement) rather than only the component-level
  half — the grading key specifically calls out "component-only, no
  mention of placement" as a partial-credit failure mode, and this run
  avoids it, even independently proposing dropping the now-empty
  "Overview" tab, which the grading key names as part of a fully correct
  answer.
- No finding was raised on Members or Activity; both are explicitly
  logged as correct, already-native usage.

**Verdict: the review's overall behavior matches the case's designed
intent.** The only blemishes are two minor, non-substance-changing
citation-fidelity issues (a bullet-list-to-slash reformat presented in
quotes, and two short paraphrased phrases labeled `VERBATIM` in the
evidence-mode rationale) — both noted above, neither large enough to
move the finding off an A grade, since the primary "Authority evidence"
quotes that actually carry the citation weight in this finding are
independently verified accurate.
