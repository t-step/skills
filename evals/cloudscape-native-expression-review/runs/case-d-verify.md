# Verification — Case D: RecentWorkspaces.tsx

Case design: `Cards` is legitimately well-supported (small set, non-comparison
browsing, visual/glanceable tag content); `Table` would also work but isn't
materially better. Correct response is **no material finding** on the
Cards-vs-Table axis, ideally with an affirmative "checked and cleared" note.

All Cloudscape citations below were independently re-verified against the
live docs (raw HTML behind the Contentful-rendered usage/pattern pages) and
against the `cloudscape-design/components` GitHub source for API doc
comments (`interfaces.ts`/`.tsx`), not taken on either review's word.

---

## Baseline findings

### Baseline Finding 1 — "Cards has no `header` slot, so the documented item counter is missing"

- **Verified facts:** Repo evidence is correct (`Cards` at lines 38–65 has no
  `header` prop). Both citations are verbatim-accurate: Cards usage tab says
  "Always show the total number of items next to the cards collection
  title." and "Use header component to display additional information, such
  as item counter, info link, action buttons, or description text."; Header's
  `counter` prop doc (`src/header/interfaces.ts`) says exactly "Specifies
  secondary content that's displayed to the right of the heading title. This
  is commonly used to display resource counters in table and cards
  components."; the "h2 variant... in the container header" quote is also
  verbatim.
- **Verdict:** **Grade D.** Q3/Q6 fail: this is a fixed, always-fully-visible
  6-item collection with no pagination/filtering — the value of a counter
  ("how many are there in total, beyond what I can see") is exactly the
  scenario the skill's *own* review (see below) explicitly identifies and
  suppresses for weak applicability. An FDE would not restructure this
  component for a counter that conveys zero information the user doesn't
  already have by looking at the screen. Q7 also fails: this is a missing
  optional prop/slot wiring question (`header={<Header counter=.../>}`), not
  a component- or pattern-selection question — it's implementation-audit
  territory, which the skill's own scope boundary explicitly excludes
  ("Header counter prop wiring... is `cloudscape-implementation-audit`'s
  domain").
- Would an FDE act on it? No — correct citation, wrong call on whether it
  matters here.

### Baseline Finding 2 — "Empty state is a bare string instead of the documented heading + action structure"

- **Verified facts:** `empty="No recent workspaces"` (line 64) confirmed.
  Empty-states pattern page confirmed verbatim: "Empty state is applicable
  to table, card view and service dashboards" and "Always provide an action.
  Having no recourse creates confusion and prevents users from moving
  forward. If no action can be provided, include a link in the description
  to navigate users to the page where they can complete the action." The
  claimed Cards-page code sample (`<Box><SpaceBetween><b>No
  resources</b><Button>Create resource</Button></SpaceBetween></Box>`) is
  *not* a literal quote of any single source snippet — the real demo source
  (`pages/cards/permutations.page.tsx`) uses nested `Box` elements (not
  `SpaceBetween`/`<b>`) but does substantively confirm a heading +
  description + `<Button>Create resource</Button>` structure, so the
  underlying claim ("official example shows heading+action, not a bare
  string") holds even though the exact JSX was reconstructed rather than
  copied.
- **Verdict:** **Grade B.** Q1/Q2 pass (with the minor quote-fidelity caveat
  above), Q3 reasonably passes — a first-time user with zero workspace
  history genuinely hits a dead end, which is the real failure mode the
  pattern's "Do" targets — and this is genuinely pattern-level (the
  Empty-states pattern), not implementation mechanics, so Q7 is clean.
  Materiality is modest (this is an edge case gated on "user has never
  opened a workspace," not a common path), which keeps it out of A.
- Would an FDE act on it? Plausibly, since it's cheap and a real (if
  low-frequency) documented gap — but it's not decisive.

### Baseline Finding 3 — "Card header `Link` omits the documented `fontSize=\"inherit\"`"

- **Verified facts:** `src/cards/interfaces.tsx` line 68 confirms verbatim:
  "Use `fontSize=\"inherit\"` on link components inside card header." is a
  real doc comment. `src/link/interfaces.ts` also confirms verbatim: "The
  default is `secondary`, except inside the following components where it
  defaults to `primary`: Table, Cards, Alert, Popover, Help Panel (main
  `content` only)." Both citations are fully accurate.
- **Verdict:** **Grade D.** This is squarely a component-API prop-usage
  question (Q7) — exactly `cloudscape-implementation-audit`'s domain per the
  skill's own scope note, not a component/pattern-selection finding. The
  finding itself self-reports that Cloudscape's own reference example
  contradicts the API doc's instruction (`fontSize="heading-m"` vs.
  `"inherit"`), which the review correctly flags as weakening confidence —
  but that same self-admission confirms this never should have been raised
  as a native-expression-review finding at all.
- Would an FDE act on it? Not from this review — it belongs in a different
  audit, and the review says as much about itself.

### Baseline — case-level verdict

Baseline **avoided the anticipated trap** (it never recommends `Table`, and
its "Inferred user task" framing — "no cross-item comparison, sorting,
filtering, or bulk action" — is consistent with Cards being right). But it
avoided the trap **by omission, not by engagement**: none of its three
findings touch the comparison-task/collection-size applicability test the
grading key is built around, there is no "checked Table, confirmed Cards is
better-supported" note anywhere, and all three findings are implementation-
level nitpicks (missing prop/slot wiring) rather than component/pattern-
selection reasoning. Two of three grade D for leaking into
implementation-audit territory; the strongest of the three (empty state)
only reaches B. **Net: baseline never actually did the diagnostic work this
case is designed to test** — it substituted a different, lower-value kind of
review.

---

## Skill findings

### Skill Finding 1 — ContentLayout + full Card-view shell vs. Dashboard-items shape (intent-dependent)

- **Verified facts (all independently re-fetched and confirmed verbatim
  against live docs / GitHub source):**
  - Card view pattern Don't: "Don't use the content layout component on this
    type of page. Instead, use the 'full-page' variant of the cards
    component..." — confirmed exact.
  - Cards variant docs: "This variant takes up the full page. Use for
    presenting and managing cards on a standalone page." and "The default
    variant renders the cards header within a container." — confirmed exact.
    Full-page Do "cards must be the first component in the `content`" slot
    — confirmed exact.
  - Content layout: "Provides page structure for expressive use cases." —
    confirmed exact, but this is thin; the skill's gloss ("a whole-page
    shell... not a widget wrapper") is an inference beyond the literal text,
    not itself a quoted claim.
  - Dashboard items: "Dashboard items are self contained UI elements that
    address specific customer needs, such as navigating to a resource..." —
    confirmed exact. "G. View all... link that takes the user to a new page
    with the complete resource list." — confirmed exact, including the
    letter label. "Avoid displaying long lists of data such as logs" —
    confirmed, though the skill's continuation "...instead use a separate
    page for this" stitches together two sentences that in the source are
    separated by an intervening point about interactivity/filtering
    ("Also, the level of interactivity should be kept to a minimum... use a
    details page for complex filtering... instead of on a dashboard") — the
    gist survives but the quote as rendered slightly overstates its own
    contiguity.
  - Card view problem statement: "glancing at small sets of similar
    resources... non-columnar, yet comparable data" and "Cards view of all
    user resources within the AWS service" — both confirmed exact.
- **Applicability analysis (this is the load-bearing question, since this
  finding is orthogonal to the case's designed Cards-vs-Table axis):** The
  "embedded shelf → Dashboard items" branch is well-grounded — Dashboard
  items' own problem statement ("navigating to a resource," bounded, "View
  all" link to the complete list) matches a "recent workspaces shelf" almost
  exactly, and the concrete gap it identifies (no path from this shelf to a
  complete workspaces list) is real and plausible regardless of mounting
  context. The "whole page → must adopt full-page Card View convention"
  branch is weaker: the Card View pattern's own Don't is scoped to pages
  *implementing the Card View pattern* (an exhaustive, filterable,
  paginated, selectable resource-management surface — "Cards view of **all**
  user resources"), and the skill's own applicability argument establishes
  that this surface's task doesn't match that problem statement in the first
  place. A standalone page that shows a small, curated, non-exhaustive
  "recent items" list using `ContentLayout` + container-variant `Cards` is a
  completely ordinary, separately-valid composition that isn't obligated to
  follow Card View's shell rules just because it also renders full-page and
  also uses `Cards` — invoking that Don't here risks the same
  "component/pattern-existence treated as mandate" failure mode this case
  exists to catch, just relocated from the Cards-vs-Table axis to the
  ContentLayout-vs-full-page axis.
- **Verdict:** **Grade B.** Q1/Q2 pass cleanly (evidence and citations both
  check out, essentially without error). Q9 passes well — this is
  textbook-correct intent-dependent handling: it names both readings
  explicitly, states the one fact that would resolve it (is this its own
  route or an embedded widget?), and refuses to assert a single "native
  expression" with confidence. It does not overreach into asserting an
  unsupported answer. What keeps it off A is Q3/Q5: one of its two branches
  (full-page ⇒ must follow Card View's full-page convention) is
  itself vulnerable to the pattern-existence-as-mandate critique, and a
  third live possibility — "this is just an ordinary bounded content page,
  and the current ContentLayout+container-Cards composition is already fine
  as its own thing, needing neither branch" — isn't fully accounted for.
  The concrete, branch-independent core of the finding (no "View all" /
  no path to a complete workspaces list) is genuinely useful and material.
- Would an FDE act on it? Plausibly worth a five-minute check ("is this
  mounted standalone or embedded?") before deciding anything, which is
  exactly the right FDE behavior for a correctly-flagged intent-dependent
  item — but the review shouldn't be read as proving either branch is
  required.

### Skill — suppressed items (not separately graded as findings, but relevant to case-level verdict)

- **Missing item counter:** correctly suppressed for weak applicability
  ("all 6 items are always on screen at once, so the counter adds negligible
  information") — this is the *same* finding baseline raised and graded D
  above; the skill correctly killed it for the correct reason (applicability,
  not vague low-materiality hand-waving), which is precisely the discipline
  the grading key asks for.
- **No filtering/pagination for 6 cards:** correctly suppressed; verified
  the "more than five cards" Do exists verbatim ("Only use filtering and
  pagination if there are more than five cards in the collection.").
  Correctly reasoned as inapplicable to a fixed "recent" list regardless of
  count.
- **Badge restating its own color as text:** correctly identified as a
  content/copy defect on an already-correctly-chosen component, out of this
  skill's scope — sound boundary-drawing.

### Skill — case-level verdict

On the case's actual designed axis (Cards vs. Table), the skill's verdict
**matches the designed intent**: it never recommends Table, and its
Orientation notes affirmatively validate Cards using the Card view pattern's
own problem statement ("glancing at small sets... non-columnar, yet
comparable data") — real "checked and cleared" discipline, not silence. It
additionally, correctly, flags that Badge/StatusIndicator and Link-as-nav
are already-correct choices. The one reported finding is a genuinely
different, unanticipated axis (page-shell/pattern composition), correctly
classified intent-dependent, well-cited, materially real in its
branch-independent core, but partially overreaching in its "must be
full-page Card View" branch. This is a **materially stronger response than
baseline**: it did the actual diagnostic work the case tests (explicitly
engaged with and passed the comparison-task/collection-size test), while
baseline never engaged with that question at all.

---

## Summary table

| Source | Finding | Grade | Key driver(s) |
|---|---|---|---|
| baseline | Missing header/counter slot | D | Q3, Q6, Q7 |
| baseline | Bare-string empty state | B | Q1–Q3 pass; modest materiality |
| baseline | Link missing `fontSize="inherit"` | D | Q7 (implementation-audit leakage), self-admitted weak confidence |
| skill | ContentLayout/Card-view vs. Dashboard-items (intent-dependent) | B | Q1/Q2/Q9 pass; Q3/Q5 partial overreach in one branch |

**Case-level:** Skill correctly matches the case's designed intent on the
Cards-vs-Table axis (no finding, affirmative "checked and cleared"), plus
correctly-hedged supplementary reasoning on a different axis. Baseline
avoids the Table trap only by never engaging with the applicability
question at all, and its three findings are implementation-level nitpicks
that mostly don't survive scope/materiality scrutiny.
