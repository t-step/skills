# Adversarial Verification: hkbus-skill.md (Route ETA / Stop Detail / Bookmarked Stops)

Reviewed artifact: `evals/design-system-native-expression-review/runs-repeat/hkbus-skill.md`
Fixture: `hk-independent-bus-eta` @ `cb5b1fcbed5f9f7cb14635ee29507084b9de2578`
Rubric: `evals/cloudscape-native-expression-review/rubric.md` (Cloudscape → Material UI substitution)

Method: read the review and all nine bounded-surface files directly; independently
opened `App.tsx`, `Root.tsx`, `Header.tsx` (outside the bounded surface, per task
instructions); live-fetched `mui.com/material-ui/{react-alert,react-accordion,
react-button,react-snackbar,react-tabs,react-divider,react-dialog,react-app-bar}.md`
and grepped every quoted fragment against the raw text.

---

## 1. Independent global-chrome investigation (AppBar/Toolbar question)

Read directly:

- `src/App.tsx` — every top-level page route (`RouteEtaPage`, `StopEtaListPage`,
  `BookmarkedStopPage`, etc.) is nested under `<Route path="/:lang" element={<Root />}>`.
  `Root` is the single layout wrapper for the entire app.
- `src/components/layout/Root.tsx` — renders, in order: skip-link, `<Header />`,
  a `Suspense`-wrapped `<Box component="main"><Outlet/></Box>`, `<Footer/>`,
  plus drawer/dialog portals. `Header` is rendered **unconditionally, on every route**,
  above the routed page content.
- `src/components/layout/Header.tsx` — returns `<Toolbar sx={rootSx}>...</Toolbar>`
  **directly**, not wrapped in `AppBar`. Contents: home link/logo, a route-search
  `Input`, weather `Avatar` icons, a geolocation `IconButton`, a language-toggle
  `Button`, a theme-toggle `IconButton`, and a settings `IconButton` — i.e. a fully
  realized, persistent, app-wide header bar built from a bare `Toolbar`.

**Finding, confirmed directly:** a persistent global app-shell header exists, it is
built from `Toolbar` (not `AppBar`), and it renders above every one of the three
primary-surface pages, including `RouteEtaPage` (which also renders `RouteHeader`,
a per-route `Paper`-based header, immediately below it in the visual stack).

**Reachability from the bounded surface:** none of the 9 bounded files
(`RouteEtaPage.tsx`, `StopEtaListPage.tsx`, `BookmarkedStopPage.tsx`,
`RouteHeader.tsx`, `StopAccordionList.tsx`, `StopDialog.tsx`,
`RouteUpdateNotice.tsx`, `AppContext.tsx`, `DbContext.tsx`) imports `Root` or
`Header`, and neither `Root` nor `Header` imports back into any bounded file. The
only edge connecting them is the router configuration in `App.tsx`, which is
itself outside the bounded surface. A reviewer confined strictly to the 9 files,
following only their import graphs, would have **zero signal** that a competing
global header exists. Finding it requires the same three deliberate,
out-of-bounds hops this task specified (`App.tsx` → `Root.tsx` → `Header.tsx`) —
it is not discoverable by accident.

**Did this run make any of those hops?** No. `grep` for `App.tsx`, `Root.tsx`,
`Header.tsx`, `AppBar`, "global", "chrome" across the whole review returns nothing
relevant — every "header" reference in the review is to `RouteHeader.tsx` itself.
The review does, however, explicitly examine `RouteHeader.tsx`'s `Paper
elevation={0}` usage and affirmatively signs off on it in "Orientation notes":
*"a legitimate, documented customization of a first-class Paper prop, not a
misuse of the component."* That sentence is evidence the reviewer looked directly
at `RouteHeader.tsx`'s component choice and rendered a verdict on it — without
ever raising `AppBar`/`Toolbar` as a candidate, and without checking whether a
competing global header exists that would bear on that verdict.

### Verdict — AppBar/Toolbar question: **recall gap, not defensible restraint**

This is not an instance of the skill's "Missing intent" escape hatch (silently
suppressing a candidate once identified, because intent can't be resolved). That
hatch presupposes the candidate was generated and then deliberately not reported.
Here there is no evidence `AppBar`/`Toolbar`-for-`RouteHeader` was ever generated
as a candidate at all — the reviewer analyzed `RouteHeader.tsx`'s `Paper` choice
in isolation and pronounced it fine, which is a *stronger* miss than silence: it
is an affirmative "checked and correct" verdict rendered without the one fact
(the sibling global `Toolbar` in `Header.tsx`) that any experienced MUI
practitioner would want before ruling on whether a page-level `Paper` header
should instead be an `AppBar`/`Toolbar`. Whether the *correct* resolution is
"leave `RouteHeader` as `Paper` because `Header.tsx` already owns the app-bar
role" or "intent-dependent, name the ambiguity" is exactly what the two prior
rounds diverged on — but this run never got far enough to face that choice. It
simply never looked. On this specific question, across three rounds, this is the
worst outcome of the three: round 1 hedged correctly and named the uncertainty
(later vindicated); round 2 investigated, stopped one file short, and asserted a
confident wrong answer; round 3 never investigated at all and rendered an
unrelated affirmative verdict on the very component that should have triggered
the question.

There is no evidence anywhere in this run of looking beyond the bounded surface
for *any* finding — every citation, orientation note, and suppression reasons
from files inside the nine-file boundary only.

---

## 2. Independent StopDialog / fullScreen investigation

Read `StopDialog.tsx` directly (reproduced above in tool output). Facts:

- `Dialog` is sized via `sx: { "& .MuiPaper-root": { width: "100%", marginTop:
  "90px", height: "calc(100vh - 100px)" } }` — a hand-tuned near-full-height
  dialog, not using the `fullScreen` prop.
- `DialogTitle` contains a flex row of `IconButton`s (bookmark toggle,
  directions, map, "view full stop page") plus a separate close `IconButton`,
  laid out `justifyContent: "space-between"`.
- Live-fetched `react-dialog.md` confirms MUI's own **"Full-screen dialogs"**
  worked example (line 451) composes exactly this shape — `fullScreen` Dialog +
  an `AppBar`/`Toolbar` title bar containing a close `IconButton`, a `Typography`
  title, and a right-aligned action `Button` — as one named, worked
  composition tying the `fullScreen` prop together with an `AppBar`/`Toolbar`
  title-bar composition.

So the authority for a *composition*-level claim about `StopDialog`'s title row
(should it become an `AppBar`/`Toolbar`?) genuinely exists on the same page as
the `fullScreen` prop mechanics — this is the strongest on-point authority
available for this file, stronger than the `DialogActions` alternative the run
did consider.

This run's report places the sizing entirely under "What was not evaluated": *"
`Dialog` sizing achieved via `sx` targeting `.MuiPaper-root` in `StopDialog.tsx`
rather than the documented `fullScreen`/`maxWidth`/`fullWidth` props ... were
not assessed."* That is a purely props/CSS framing. Separately, in "Suppressed,"
the run *did* consider one composition-level candidate for the same
`DialogTitle` icon row — `DialogActions` — and correctly rejected it (shape
mismatch: `DialogActions` is a bottom-of-dialog button footer per its own
documented purpose and MUI's demos, not a title-row toolbar; the app's existing
compact inline icon-toolbar idiom, e.g. `RouteHeader.tsx`'s row, is cited as
supporting evidence of a deliberate, consistent pattern). It never raises
`AppBar`/`Toolbar` as an alternative for the same row, despite having already
opened `DialogTitle`'s structure to evaluate `DialogActions`.

### Verdict — Dialog/fullScreen question: **correct scope discipline on the props/CSS half; incomplete investigation on the composition half — net result lands in the right place, but not for a fully examined reason**

Two things need to be kept separate, and this run does keep the *prop-vs-hardcoded-CSS* framing entirely on the implementation-correctness side of the line — that is a real improvement over the prior (morphed) round, which explicitly leaked "hand-tuned pixel values instead of the dedicated `fullScreen` prop" reasoning into a composition-level finding. This run never does that; its "not evaluated" line about sizing is honestly and exclusively about props/CSS mechanics, which is the correct scope call.

But the composition question — should `DialogTitle`'s icon row become an
`AppBar`/`Toolbar` title bar, per MUI's own "Full-screen dialogs" example — is a
*different* candidate from `DialogActions`, and the run shows no evidence of
having considered it, despite examining the same lines of code for a weaker
candidate. Applying the anti-fundamentalism four-point test independently: task
match is plausible but not clean (the dialog approximates full-screen via custom
`sx`, it does not use `fullScreen`, so whether it is *intended* to read as a
full-page takeover — the scenario the example addresses — or as a large modal
that happens to be tall, is itself unresolved from the bounded surface); this
is a legitimate `intent-dependent` candidate, not a slam-dunk finding. Given
that, silently declining to name it lands on an acceptable *outcome* — but the
evidence here supports "never generated the candidate" rather than "generated it,
tested it against the four-point rule, and correctly concluded it doesn't clear
the bar or is intent-dependent." The run gets partial, not full, credit: right
place in the report, without visible work showing it was reasoned there rather
than never reached.

---

## 3. Citation-integrity table (every VERBATIM / quoted claim, checked against the live page)

| # | Review's quoted text | Source page | Verdict |
|---|---|---|---|
| 1 | "Alerts display brief messages for the user without interrupting their use of the app," | react-alert.md:12 | Exact match (only trailing punctuation adapted for embedding, as expected) |
| 2 | "gives users brief and potentially time-sensitive information in an unobtrusive manner." | react-alert.md:18 | **Near-match, one word altered**: source reads "Alerts **give** users..."; review quotes "**gives** users..." to fit its own sentence grammar. A verb was silently conjugated inside quotation marks — a real, if minor, breach of "must be copy/paste-verifiable." Substance unaffected. |
| 3 | "corresponding icon and color combinations" | react-alert.md:56 | Exact match (valid partial quote) |
| 4 | onClose → "display a close icon (✕) by default when no custom action is supplied" | react-alert.md:166 | Paraphrase, unquoted — accurately represents the source, not a verbatim-mode violation since no quotation marks used |
| 5 | "any element — an HTML tag, an SVG icon, or a React component such as a Material UI Button — after the Alert's message, justified to the right." | react-alert.md:164 | Exact match (em-dash spacing normalized, leading clause dropped — legitimate partial quote) |
| 6 | "Use the `expanded` prop with React's `useState` hook to allow only one Accordion item to be expanded at a time." | react-accordion.md:474 | Exact match |
| 7 | "Icons are also appropriate for toggle buttons that allow a single choice to be selected or deselected, such as adding or removing a star to an item." | react-button.md:248-249 | Exact match |
| 8 | "brief notifications of processes that have been or will be performed" | react-snackbar.md:13 | Exact match (valid partial quote) |
| 9 | "a thin, unobtrusive line for grouping elements to reinforce visual hierarchy." | react-divider.md:12 | Exact match (valid partial quote) |
| 10 | AccordionActions: "an optional wrapper that groups a set of buttons" | react-accordion.md:24 | Exact match |
| 11 | DialogActions: "an optional container for a Dialog's Buttons" | react-dialog.md:27 | Exact match |
| 12 | Tabs "Forced scroll buttons" (named section reference, not full quote) | react-tabs.md:529 | Exact heading match |

**Overall citation integrity: strong.** Twelve checkable claims, eleven
character-exact, one (#2) with a single verb silently conjugated to fit
surrounding grammar inside quotation marks. This is a meaningfully better
citation-discipline result than the "3-in-6" fabrication/conflation rate the
lineage notes for the prior MUI round — no fabricated quotes, no conflated
sources, no citation of the `llms.txt` description standing in for the real
page. Flag #2 as a process note (VERBATIM mode requires quotation marks to be
reserved for literal copy), not as evidence of fabrication.

---

## 4. Per-finding grading

### Finding 1 — Alert consolidation (RouteUpdateNotice / DbRenewReminder / BadWeatherCard / NoticeCard)

Repository evidence re-verified directly against the fixture:

- `RouteUpdateNotice.tsx`: `Box` (lines 29-33, `sx` at 38-49) with `onClick={renewDb}`, one `Typography` with a literal "⁉️" glyph. Rendered from `RouteEtaPage.tsx` line 235 — **confirmed exact**, both the component contents and the line-235 render site.
- `DbRenewReminder.tsx` lines 20-24: `Box sx={rootSx} onClick={renewDb}` — **confirmed exact**, same `renewDb` action from `DbContext` as `RouteUpdateNotice`.
- `BadWeatherCard.tsx` lines 27-34: `Paper variant="outlined"` with `ErrorIcon color="error"` — **confirmed exact**.
- `NoticeCard.tsx` lines 92-143 (close button at 135-141): `Paper variant="outlined"` with `WarnIcon color="warning"` and a hand-wired `IconButton`/`CloseIcon` reimplementing dismiss — **confirmed exact**, down to the line numbers.

This is unusually precise line-citation work — every range checked lands exactly
or within one line of the actual JSX boundaries.

Rubric questions:

1. **Task supported by evidence?** Yes — all four components exist, are rendered where claimed, and do what's described.
2. **Does cited authority say what's claimed?** Yes, verified above (§3).
3. **Actually applicable (four-point test)?** Passes cleanly: same problem (transient, unobtrusive, optionally-actionable status message) across all four instances; two instances already reach for Alert's own severity color tokens (`color="error"`/`color="warning"`) on raw icons without adopting the component that owns that vocabulary — this is concrete, specific evidence of applicability, not a generic "Alert exists" gesture.
4. **Preserves task semantics?** Yes — swapping the wrapper for `Alert` with `action`/`onClose` changes nothing about timing, copy, or the click action.
5. **Could current implementation be equally valid MUI usage?** No documented rationale found for four independent hand-rolled implementations of the same concept; this isn't a supported alternative, it's drift.
6. **Materially worth restructuring?** Yes — four independent reimplementations of one concept, two partially reaching for Alert's own vocabulary already, one duplicating `onClose`'s dismiss behavior by hand, two independently wiring the identical `renewDb` action. This is exactly the kind of concrete, multi-instance drift evidence the rubric wants for a "high" materiality call, not an aesthetic preference.
7. **Component/pattern-level, not implementation or generic UX?** Yes, cleanly stated in the boundary check; the finding is squarely about component selection, not prop mechanics or UX judgment.
8. **Wrongly split across levels?** No — correctly typed `combined selection + composition`, one finding.
9. **Intent-dependent handling?** N/A — not classified as such, and doesn't need to be; applicability is established directly rather than resting on an unresolved intent question.

**Grade: A.** Materiality, confidence, evidence mode, and authority strength
(`OPTIONAL`, correctly not inflated to `REQUIRED`/`RECOMMENDED` despite the
strong semantic match) are all honestly and correctly labeled. An FDE working in
this codebase would plausibly consolidate these four call sites onto `Alert`
specifically because two of them already lean on Alert's own severity-color
vocabulary piecemeal — that's the kind of concrete "this is already halfway
there, inconsistently" evidence that makes a finding earn its keep rather than
merely note an available alternative.

### Suppressed candidate — `AccordionActions` vs. `StopAccordion`'s icon cluster

Re-verified: `StopAccordionList.tsx`/`StopAccordion.tsx` place the icon cluster
inside `AccordionDetails` itself, in a flex row alongside `TimeReport` (not as a
separate element following `AccordionDetails`). `AccordionActions`'s documented
shape (confirmed via live fetch: "an optional wrapper that groups a set of
buttons," rendered after `AccordionDetails` in MUI's own demo) is a genuinely
different structural slot. The suppression reasoning ("same visual job, different
problem shape — point 1 of anti-fundamentalism failing") is correct and precisely
targeted. **Grade: A suppression** — correctly declined, for the right reason,
citing the right anti-fundamentalism point (superficial shape match, not a same-
problem match).

### Suppressed candidate — `DialogActions` vs. `StopDialog`'s title-bar icon cluster

Reasoning (no prohibition on actionable title-area controls; consistent
app-wide idiom of compact inline icon-toolbars) is sound *as far as it goes* for
the specific `DialogActions` candidate. **Grade: B suppression** — correct on
its own narrow terms, but incomplete: as discussed in §2, it stops short of the
stronger, more on-point `AppBar`/`Toolbar` "Full-screen dialogs" authority sitting
on the same documentation page, which was never surfaced as a candidate to test
or reject.

### Suppressed candidate — `Tabs` + `react-swipeable-views`

Correctly recognizes there is no native MUI swipeable-panel alternative to
recommend, and correctly declines to manufacture composition-level authority
that doesn't exist in this corpus, per the skill's explicit "do not invent a
missing authority tier" rule. Third-party library maintenance is correctly
named as out of scope rather than folded into a finding. **Grade: A suppression.**

### Orientation notes

All five spot-checked directly against the fixture and against live-fetched MUI
docs — every one confirmed accurate (controlled Accordion, IconButton toggle
semantics, Snackbar purpose, scrollable Tabs `variant="scrollable"
scrollButtons allowScrollButtonsMobile` — confirmed present in `StopTabbar.tsx`
lines 38-40 — vertical `Divider` in `ReverseButton.tsx` line 141 and
`RouteHeader.tsx`, and `Paper elevation={0}` usage). The one substantive problem
is the `Paper elevation={0}` note on `RouteHeader.tsx`, discussed in §1: it is
factually accurate as far as it goes (elevation={0} is indeed a legitimate,
documented Paper customization) but is rendered as a closed, affirmative verdict
on `RouteHeader`'s component choice without ever testing it against
`AppBar`/`Toolbar` or checking for a competing global header. **Grade: A for the
four unrelated notes; the Paper note is accurate-but-incomplete — see §1
verdict.**

---

## 5. Summary table

| Item | Type | Grade | Driving rubric question(s) |
|---|---|---|---|
| Finding 1: Alert consolidation | combined selection + composition | **A** | Q3 (four-point test passes cleanly), Q6 (concrete multi-instance drift evidence), Q7 (clean boundary check) |
| Suppressed: AccordionActions | suppression | **A** | Q3/Q9-adjacent (correct shape-mismatch reasoning) |
| Suppressed: DialogActions | suppression | **B** | Q3 correct on its narrow terms; incomplete authority discovery (missed AppBar/Toolbar "Full-screen dialogs" example on the same page) |
| Suppressed: Tabs + react-swipeable-views | suppression | **A** | Correctly declines to invent a missing authority tier |
| Orientation notes (4 of 5) | affirmative "checked, fine" | **A** | All verified verbatim/accurate against fixture + live docs |
| Orientation note: Paper elevation={0} on RouteHeader | affirmative "checked, fine" | **C** (accurate but incomplete) | Q5 answered ("legitimate customization") without testing the more consequential Q3/Q6 question (AppBar/Toolbar vs. Paper) it was adjacent to |
| Citation integrity (12 checkable quotes) | — | 11/12 exact, 1 minor verb alteration | — |

---

## 6. Explicit verdicts on the two adjudication questions

**AppBar/Toolbar (RouteHeader.tsx):** This run's total silence on the topic is a
**recall gap, not a defensible application of "Missing intent."** There is no
evidence the candidate (RouteHeader-as-Paper vs. AppBar/Toolbar) was ever
generated for consideration — the run instead examined RouteHeader's `Paper`
usage in isolation and affirmatively cleared it, without checking for a
competing global header. It shows zero evidence of looking beyond the nine-file
bounded surface for any finding at all — the one investigative move (checking
`App.tsx` → `Root.tsx` → `Header.tsx`) that would settle this question one way or
the other never happened. Of the three data points on this question to date,
this is the weakest: round 1 hedged correctly (vindicated), round 2 investigated
and asserted a confident wrong answer one file short of the truth, round 3 never
investigated and rendered an unrelated "fine as-is" verdict on the very
component the question turns on.

**Dialog/fullScreen (StopDialog.tsx):** This run **correctly keeps the
prop-vs-hardcoded-CSS observation on the implementation-correctness side of the
scope fence** — a genuine improvement over the prior round's leak. But it shows
**incomplete investigation, not demonstrated scope discipline, on the adjacent
composition question** (should the title row become an AppBar/Toolbar per MUI's
own "Full-screen dialogs" example): it tested one composition candidate
(`DialogActions`) against the same lines of code and rejected it correctly, but
never surfaced the stronger, more on-point candidate sitting on the same
documentation page. The report's placement of this topic — filed only under
"What was not evaluated," described purely in props/CSS terms — happens to land
in the same place the cleanest historical round landed, but the evidence here
does not show the reasoning that would justify calling that placement earned
rather than accidental.
