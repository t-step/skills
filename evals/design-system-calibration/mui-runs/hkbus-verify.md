# Adversarial Verification: hkbus-baseline.md vs hkbus-skill.md

Verifier note: I independently read all 8 bounded-surface fixture files, plus
(for adjudication purposes only, going beyond the bounded surface the same
way an adversarial verifier is entitled to) `src/components/layout/Header.tsx`,
`src/components/layout/Root.tsx`, and `src/components/layout/DbRenewReminder.tsx`,
and grepped the whole `src/` tree for `AppBar` and `Alert` usage (zero hits for
both, anywhere in the app). All six MUI documentation URLs cited across the two
reviews were independently re-fetched from their `.md` endpoints.

## Citation check (both reviews)

All citations in both `hkbus-baseline.md` and `hkbus-skill.md` were re-fetched
and checked against the live `.md` pages:

| URL | Claimed quote | Verified? |
|---|---|---|
| `react-alert.md` | "Alerts display brief messages for the user without interrupting their use of the app." | Exact match |
| `react-alert.md` | action prop: "insert any element — an HTML tag, an SVG icon, or a React component such as a Material UI Button — after the Alert's message, justified to the right" | Exact match (baseline's wording); skill's paraphrase ("any element ... positioned after the message") is a fair compression of the same sentence |
| `react-snackbar.md` | "Snackbars (also known as toasts) are used for brief notifications of processes that have been or will be performed" | Exact match |
| `react-snackbar.md` | "Snackbars are not intended to convey critical information or block the user from interacting with the rest of the app." | Exact match |
| `react-dialog.md` | fullScreen prop, default `false`, in API table | Confirmed present |
| `react-dialog.md` | "Responsive full-screen" example using `useMediaQuery(theme.breakpoints.down('md'))` → `<Dialog fullScreen={fullScreen}>` | Confirmed present |
| `react-dialog.md` | "Dialogs inform users about a task and can contain critical information..." | Exact match |
| `react-app-bar.md` | "The App Bar displays information and actions relating to the current screen." | Exact match |
| `react-app-bar.md` | "used for branding, screen titles, navigation, and actions" | Exact match |
| `react-app-bar.md` | leading IconButton(edge="start") / Typography title / trailing IconButton-Button composition | Confirmed — this is the page's recurring worked-example shape |
| `react-accordion.md` | "show and hide sections of related content on a page" | Exact match |
| `react-accordion.md` | "Use the `expanded` prop with React's `useState` hook to allow only one Accordion item to be expanded at a time." | Exact match |
| `react-chip.md` | "Chips are compact elements that represent an input, attribute, or action." | Exact match |

**No fabricated or misquoted citations found in either review.** Every quoted
sentence in both write-ups is real, verbatim (or a clearly-labeled fair
paraphrase), and represents the cited page's actual claim rather than a
stretched or cherry-picked fragment. This is a clean result for both runs on
citation discipline specifically — the difference between the two reviews
below is about scope discipline and applicability reasoning, not about
whether they're citing real material.

## Repository-evidence spot check

Read directly: `RouteEtaPage.tsx`, `StopEtaListPage.tsx`, `BookmarkedStopPage.tsx`,
`RouteHeader.tsx`, `StopAccordionList.tsx`, `StopAccordion.tsx`, `StopDialog.tsx`,
`RouteUpdateNotice.tsx`. All file/line citations in both reviews for the three
skill findings and the baseline's three findings check out structurally — the
described JSX shapes, prop names, and line ranges match the real code (baseline's
line ranges are occasionally a line or two loose, e.g. bundling `return (`/`);`
into the cited range, but never misdescribe what's there).

One completeness gap in **baseline**, not a graded finding but worth recording:
baseline's "Not flagged" note calls `BookmarkedStopPage.tsx` "plain
`Box`/`Typography`/`Divider` scaffolding" — the actual file is a `Paper`
wrapping five custom children (`StopTabbar`, `NoticeCard`, `BadWeatherCard`,
`DbRenewReminder`, `SwipeableStopList`), one of which (`DbRenewReminder.tsx`)
is a near-verbatim duplicate of the exact `Box`+`onClick`+`Typography`
anti-pattern baseline's own Finding 1 flags in `RouteUpdateNotice.tsx` (same
border/padding `sx`, same `onClick={renewDb}` on the whole box, same
`db-renew-text` copy). Baseline had this file in its reviewed set and missed
both the mischaracterization and a second instance of its own Finding 1.
Not a citation problem, but it undercuts baseline's "no finding" call on that
page — the skill review, to its credit, explicitly declined to read
`BookmarkedStopPage.tsx`'s unopened children (`StopTabbar`, `SwipeableStopList`)
rather than mischaracterize them, though it didn't catch `DbRenewReminder`
either (it wasn't named as an unopened import the way the other two were).

## Skill-assisted review: per-finding grading

### Finding 1 — Bespoke clickable notice box duplicates Alert's documented job

1. Task supported by evidence — yes, grounded in `RouteUpdateNotice.tsx`'s
   `show` gating and `RouteEtaPage.tsx:235` render site.
2. Cited authority says what's claimed — yes, verified above.
3. Four-point applicability test — passes: same problem (brief, non-blocking,
   actionable staleness notice), current code already solves that exact
   problem, `Alert`+`action` preserves the same task, and the gap (no
   severity/role semantics, whole-box ambiguous click target) is the kind of
   thing a fluent implementer would actually fix.
4. Preserves task semantics — yes, same message/same renew action.
5. Could current impl be equally valid MUI usage? No documented alternative
   pattern justifies a raw `Box` for this; independently confirmed there is
   no `Alert` usage anywhere else in the app to point to as a competing
   established convention, and no counter-evidence surfaced.
6. Materiality — real: no `role`, no severity-driven color/icon, entire
   region is an unlabeled click target. An FDE would plausibly act on this.
7. Component/pattern, not implementation or generic UX — correctly bounded;
   boundary check present and accurate.
8. Not a component/pattern duplicate-finding split.
9. N/A (not intent-dependent).

**Grade: A.** Repository evidence, citation, and applicability argument all
hold up; this is the strongest finding either review produced. Independent
check found no competing pattern in the app that would excuse the current
implementation, and the same anti-pattern recurs verbatim in
`DbRenewReminder.tsx` outside the bounded surface — further (unused-by-either-
review) evidence this is a real, repeated gap rather than a one-off.

### Finding 2 — App Bar / `RouteHeader.tsx` (`intent-dependent`)

Graded per rubric Q9 (did the run correctly decline to guess, naming both
plausible readings and the resolving evidence, rather than pick one?).

- Named both readings explicitly: (a) if no global `AppBar` exists,
  `RouteHeader` is effectively serving as the screen's app bar and the
  purpose-built component is being bypassed; (b) if a global `AppBar` already
  exists, the current `Paper` composition is likely the *more* correct choice
  because it avoids a second app-bar-semantic landmark colliding with the
  first.
- Named the specific resolving evidence: whether a global/root `AppBar`
  exists in the app shell, outside the 7-file bounded surface.
- Did not assert a confident recommendation despite having a plausible,
  well-cited candidate (`AppBar`/`Toolbar`) sitting right there — this is
  exactly the guess-suppression the skill's "Missing intent" section exists
  to enforce.

**Independent check of the missing evidence:** I read `Root.tsx` (the
route-outlet-level layout) and `Header.tsx`, and grepped all of `src/` for
`AppBar` — zero hits anywhere in the codebase. `Root.tsx` renders `Header`
(a bare `Toolbar`, not wrapped in `AppBar`) as the persistent top chrome for
every page, above the `<Outlet/>` that eventually renders `RouteEtaPage` →
`RouteHeader`. So a persistent, page-independent top bar genuinely does
already exist in the app shell — it's just not literally an `<AppBar>`
component. This resolves the skill's named uncertainty in favor of its
"global chrome already exists" branch: `RouteHeader` is a *secondary*,
route-scoped header sitting below an already-present primary header, which
is exactly the scenario the skill flagged as the reason a confident `AppBar`
recommendation could be wrong. Critically, none of `Header.tsx`/`Root.tsx`
is reachable from the 8 reviewed files by import — `RouteEtaPage.tsx` never
imports `Header` or `Root` (they're wired in via the router's layout route,
not a local import), so the skill run's characterization of this as
genuinely outside the bounded/one-hop surface is accurate, not an excuse.

**Grade: A.** The classification itself is the right call, executed to the
letter of the "Missing intent" procedure, and independent investigation
beyond the bounded surface shows the hedge wasn't just procedurally cautious
— it was substantively pointing at the right answer.

## Skill-assisted review: suppressed candidates

- **Fare-text-as-`Chip`** (`StopAccordion.tsx` `AccordionSummary` secondary
  line): correctly suppressed. `Chip`'s documented purpose ("compact
  elements that represent an input, attribute, or action") is generic enough
  that citing it for fare values is availability, not applicability — no
  normative signal that fare figures specifically should be chips.
  **Grade if scored: C** (technically citable, correctly identified as
  low-value and suppressed — this is the skill's materiality discipline
  working as intended, not a miss).
- **`Accordion` vs. `List`/`ListItemButton`**: correctly cleared. Verified
  against the real `react-accordion.md` quote above — the documented
  controlled single-open pattern is exactly what `StopAccordion`/
  `StopAccordionList` implement (`expanded={stopIdx === idx}`,
  parent-driven state). Genuine "checked and cleared."
- **5-`IconButton` cluster in `StopDialog.tsx` title vs. `ButtonGroup`/
  `SpeedDial`**: repository evidence confirmed accurate (bookmark, directions,
  map, open-full-page, close — 5 independent `IconButton`s in the
  `DialogTitle`). The suppression reasoning (independent, non-exclusive
  actions rather than a mutually-exclusive button set or a FAB's fanned
  sub-actions) is sound on its face; I did not independently re-fetch
  `react-button-group.md`/`react-speed-dial.md` since neither review cited
  them as authority for this suppressed candidate (correctly — nothing here
  claims documentation says otherwise, it's a straightforward "doesn't fit"
  call). **Grade if scored: B/C** — plausible and correctly suppressed,
  slightly less rigorously cited than the Accordion clearance but not wrong.

## Adjudication 1 — `StopDialog.tsx` `fullScreen`: is the skill's scope exclusion correct?

**Verdict: the skill run's exclusion is correct; baseline's inclusion is a
real scope violation under this skill's own rules, even though baseline was
never bound by them.**

Read `StopDialog.tsx` directly. The relevant code is exactly as both reviews
describe: `<Dialog open={open} onClose={onClose} sx={rootSx}>` with
`rootSx` targeting `& .MuiPaper-root` to hand-set `width: "100%"`,
`marginTop: "90px"`, `height: "calc(100vh - 100px)"` to approximate a
full-viewport sheet, instead of the documented `fullScreen` boolean prop.

The determinative fact: **both reviews agree `Dialog` is already the correct
component for this job.** Neither review argues for a different component.
The entire disagreement is over how the full-viewport *sizing* is achieved —
a hard-coded `sx` override targeting an internal MUI class name
(`.MuiPaper-root`) versus a documented boolean prop. SKILL.md's scope
boundary lists, verbatim, as out-of-scope: *"hard-coded style/token values,
unsupported component composition mechanics... on an already-correctly-chosen
component."* This is not an adjacent or arguable case — it is close to a
textbook instance of exactly that carve-out. Nothing about *which* MUI
concept was chosen is in question; the question is purely a props/API-usage
substitution on a component both reviews already agree is native. That is
implementation correctness, not component or pattern selection, by SKILL.md's
own explicit boundary language.

Baseline's Finding 2 header — *"`StopDialog.tsx` fights `Dialog`'s default
sizing with manual CSS instead of using the documented `fullScreen`
prop"* — makes this explicit: baseline never claims `Dialog` is the wrong
component either. It's the same underlying observation as the skill run's
"not evaluated" note, just reported as if it were a native-expression/
component-fit finding because baseline had no boundary discipline to draw
the line. Scored against this rubric's Q7 ("does it leak into implementation
correctness... wearing a citation?"), baseline's Finding 2 would land a
**D** — the citation (`fullScreen` prop, `useMediaQuery` pattern) is real
and accurately quoted, but the finding itself belongs to a different review
layer than the one baseline is nominally conducting (an unguided,
no-named-scope review, so "violation" is really "the thing a scope-less
review predictably does" — but exactly the failure mode this skill's own
scope boundary exists to prevent).

## Adjudication 2 — App Bar / global chrome: which call is more defensible?

**Verdict: the skill's `intent-dependent` classification is clearly the more
defensible call, and independent investigation shows it wasn't just
procedurally correct — it was substantively closer to right.**

Baseline's Finding 3 asserts, unhedged: *"Composing it from `Paper` + three
bespoke `sx` blocks forfeits the built-in `Toolbar` slot/spacing
conventions... in favor of reinventing the same layout by hand,"* treating
the `AppBar`/`Toolbar` swap as a clear win with no caveat about the rest of
the app's chrome. Baseline never opens or mentions `Header.tsx` or
`Root.tsx` — it reasons entirely from `RouteHeader.tsx` in isolation and
extrapolates a confident recommendation from a component-purpose match
alone, which is exactly the "existence + superficial shape match" failure
SKILL.md's anti-fundamentalism rule and "Missing intent" section are built
to catch (point 4 of the four-point test — would a fluent implementer
*actually* restructure this — is never actually interrogated against
the *rest of the app*, only against the isolated file).

As shown under Finding 2 above, the app does have a persistent top-level
`Header`/`Toolbar` mounted once at the router-layout level and shown above
every page, `RouteEtaPage` included — a fact invisible from the 8-file
bounded surface (no import chain connects `RouteEtaPage.tsx` to
`Header.tsx`/`Root.tsx`) but real. That means baseline's confident
recommendation, if actually implemented, risks creating precisely the
collision the skill named as a live possibility rather than a hypothetical
hedge: a second app-bar-semantic landmark nested inside page content below
an already-present persistent header. The skill's refusal to assert either
way, and its explicit naming of "does a global AppBar already exist
elsewhere" as the deciding fact, holds up under actual investigation of the
wider codebase. Baseline's confident, single-file-scoped assertion does not.

## Summary table

| Item | Type | Grade | Note |
|---|---|---|---|
| Skill Finding 1 (Alert) | component selection | **A** | Strongest finding in either review |
| Skill Finding 2 (App Bar) | intent-dependent | **A** (Q9: correct classification) | Verified substantively correct via out-of-surface check |
| Suppressed: fare `Chip` | — | C (if scored) | Correctly suppressed, low materiality |
| Suppressed: Accordion vs List | — | checked-and-cleared, verified | — |
| Suppressed: 5-icon cluster vs ButtonGroup/SpeedDial | — | B/C (if scored) | Correctly suppressed, sound but lightly cited |
| Baseline Finding 2 (`fullScreen`) | (baseline, not scored A–E per instructions) | would be **D** under this rubric | Scope violation: implementation-correctness wearing a component-fit label |
| Baseline Finding 3 (App Bar) | (baseline, not scored A–E per instructions) | would be **D** under this rubric | Confident assertion on genuinely missing intent; contradicted by out-of-surface evidence |

Citation discipline: **clean in both reviews** — no fabricated or
misrepresented MUI documentation found anywhere in either write-up.
