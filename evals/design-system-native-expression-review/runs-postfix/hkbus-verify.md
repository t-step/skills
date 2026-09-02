# Adversarial Verification: hk-independent-bus-eta (Route ETA / Stop ETA / Bookmarked Stop)

**Review graded:** `evals/design-system-native-expression-review/runs-postfix/hkbus-skill.md`
**Rubric:** `evals/cloudscape-native-expression-review/rubric.md` (read "Cloudscape" → "Material UI")
**Fixture:** `/Users/thomasestep/Developer/mui-eval-fixtures/hk-independent-bus-eta/` (frontend root, real repo, no pre-written grading key)

Method actually followed: re-read every cited fixture file directly from disk (not trusting the review's
line numbers), live-`curl`'d each cited `mui.com/*.md` page and grepped the exact quoted strings against
the raw fetched text, and read three additional layout components (`Root.tsx`, `Header.tsx`) plus three
BookmarkedStopPage-composed notice components (`DbRenewReminder.tsx`, `NoticeCard.tsx`,
`BadWeatherCard.tsx`) that the review's own scope list did not name, specifically to test the suppression
reasoning and to check for missed duplicate instances of reported findings.

---

## Citation-integrity table

| # | Citation | Claimed as | Fetch result | Verdict |
|---|---|---|---|---|
| 1 | `react-dialog.md` — "Dialog Actions: an optional container for a Dialog's Buttons." | VERBATIM | Exact match, line 27 | **Pass** |
| 2 | `react-dialog.md` — "Dialog Title: a wrapper used for the title of a Dialog." | VERBATIM | Exact match, line 26 | **Pass** |
| 3 | `react-dialog.md` — "The dialog has a close button added to aid usability." | VERBATIM | Exact match, line 365, in the "Customization" section as claimed; the close `IconButton` is confirmed a sibling of `DialogTitle` (not nested inside it), and `DialogActions` still hosts "Save changes" in that same demo | **Pass** |
| 4 | `react-alert.md` — "Alerts display brief messages for the user without interrupting their use of the app." | VERBATIM | Exact match, line 12 (page tagline) | **Pass** |
| 5 | `react-alert.md` — "Add an action to your Alert with the `action` prop. This lets you insert any element—an HTML tag, an SVG icon, or a React component such as a Material UI Button—after the Alert's message, justified to the right." | VERBATIM | Exact match, lines 163–164 (two consecutive sentences, correctly concatenated, no word-order drift) | **Pass** |
| 6 | `react-alert.md` — "is no longer documented in the Material Design guidelines, but Material UI will continue to support it" | VERBATIM (paraphrase-flagged as note) | Matches line 37 near-verbatim (page reads "This component is no longer documented in the Material Design guidelines, but Material UI will continue to support it.") | **Pass** |
| 7 | `react-button.md` — "Icons are also appropriate for toggle buttons that allow a single choice to be selected or deselected, such as adding or removing a star to an item." | VERBATIM | Exact match, lines 248–249 | **Pass** |
| 8 | `react-accordion.md` — "lets users show and hide sections of related content on a page" | paraphrase, not flagged VERBATIM | Matches line 13 near-verbatim | **Pass** |
| 9 | Alert "Anatomy" section — icon/message/action as distinct regions | paraphrase | Confirmed: `MuiAlert-icon`, `MuiAlert-message`, `MuiAlert-action` are three sibling `<div>`s under one `Paper` root (lines 340–351) | **Pass** |

No fabrication, inversion, or misattribution found anywhere in the review's citations. Every VERBATIM tag is
earned. This is a clean, honest citation record — the review's biggest risk is not quotation accuracy but
**applicability reasoning built on an incomplete survey of the cited page** (see Finding 1 below).

---

## Per-finding grade table

| Finding | Grade | Driving question(s) | FDE-would-act rationale (if A/B) |
|---|---|---|---|
| **1** — Stop dialog stacks functional actions in `DialogTitle` instead of `DialogActions` | **B** | Q2 (partial), Q3, Q5 | The header-row overload (5 icon buttons + stop name jammed into one flex row) is a real, checkable problem and `DialogActions` is a legitimate, cheap destination for at least the bookmark/directions/map/navigate actions — an FDE skimming the file would plausibly reach for `DialogActions` on sight of the crowded title. |
| **2** — `RouteUpdateNotice` hand-rolls a notice band instead of `Alert` | **A** (finding itself) / flagged for a **scope-coverage gap**, see below | Q1–Q6 all pass cleanly | `Alert`'s `action` prop is a purpose-built, one-line substitution for exactly this "message + one action" shape; the current `Box`/`onClick` re-derives border, padding, and click semantics `Alert` ships for free, and preserves the identical `renewDb` behavior. |
| Suppressed — `RouteHeader` (`Paper`) vs. `AppBar` | **Correct suppression** | Q9 | Sound: the review named the two-branch ambiguity ("competing global AppBar exists" vs. "this is meant to be primary chrome") and declined to guess instead of asserting either. See detailed check below — the branch it left open resolves in the review's favor. |
| Orientation — `IconButton` toggle usage | **A (confirmed non-finding)** | Q1, Q2 | Correctly not reported; quote and code match exactly. |
| Orientation — controlled single-open `Accordion` | **A (confirmed non-finding)** | Q1, Q2 | Correctly not reported; `stopIdx` state lives in `RouteEtaPage.tsx` and drives `expanded` in `StopAccordion.tsx` exactly as described. |
| Orientation — `Snackbar` for copy confirmation | **A (confirmed non-finding)** | Q1, Q2 | Correctly not reported; matches code in `StopAccordionList.tsx` exactly (`isCopied` state, `autoHideDuration={1500}`, bottom-center anchor). |

### Finding 1 — detailed reasoning (why B, not A)

Repository evidence is accurate: `StopDialog.tsx`'s `DialogTitle` does contain five `IconButton`s (bookmark,
directions, map, navigate, close) plus the stop name, `DialogActions` is never imported, and the two
`DialogActions`/`DialogTitle` quotes are verbatim. The applicability argument is SYNTHESIS-labeled and rests
on a specific empirical claim: *"Every other worked example on the [Dialog] page that has functional buttons
... places them inside `<DialogActions>`, never inside `<DialogTitle>`."*

That claim is **incomplete**. The Dialog page has a "Full-screen dialogs" demo (a distinct section from the
"Responsive full-screen" one the review does cite) that the review never mentions. In that demo, the dialog's
top chrome is an `AppBar`+`Toolbar` holding a close `IconButton` on the left, the dialog's title as
`Typography` in the center, **and a functional "save" `Button` on the right — all three as siblings in one
top bar**, not split into a separate `DialogActions` region below scrollable content. This is precisely the
documented MUI pattern for a near-fullscreen dialog, and `StopDialog` is styled to be near-fullscreen
(`marginTop: "90px"`, `height: "calc(100vh - 100px)"`) even though it doesn't use the `fullScreen` prop or
`AppBar`/`Toolbar` literally. This is exactly a Q5 case ("could the current implementation be equally valid —
is there a documented, supported reason the code already does this?") that the review should have surfaced
and hedged against, and didn't.

This doesn't invalidate the finding — `StopDialog` crams *four* distinct functional actions plus a close icon
into the title row, which is denser than even the full-screen demo's single action button, so the
"overloaded header" observation still has force, and `DialogActions` remains a legitimate destination. But
the review's confident "every other demo agrees" framing overstates the evidence it actually surveyed, and a
more careful version would have named the full-screen `AppBar`/`Toolbar` pattern as the harder counter-case
and either distinguished it (e.g., "four actions is still too many for that pattern too") or hedged
materiality accordingly. That gap between claimed and actual page coverage is a synthesis-evidence weakness,
not a fabrication, so it lands at B rather than A or D.

### Finding 2 — detailed reasoning (why A, with one caveat)

All four points of the applicability test pass cleanly, the quotes are verbatim, and the "Why it matters"
argument checks out for the specific claim that the codebase re-derives what `Alert` provides for free.

One phrase deserves a caveat: *"a hand-rolled notice band next to genuine Alert usage elsewhere in a
Material UI app is a consistency/maintenance cost."* A `grep` for `Alert` imports across `src/` turns up
**zero** files that import `@mui/material`'s `Alert` component anywhere in this repository. If that clause is
read as a claim that this specific app already has "genuine Alert usage elsewhere," it is unsupported and
should be struck; read generically (a Material UI app, in the abstract, ships `Alert` for exactly this
purpose), it's defensible but ambiguously worded. This doesn't change the finding's core validity — the
`Alert` substitution stands on its own applicability argument without needing that sentence — but the phrase
is a small piece of unearned rhetorical support that an adversarial pass should flag.

---

## Suppressed section — detailed check

**`RouteHeader` (`Paper`) vs. `AppBar`.** The review declines to report this, citing insufficient evidence
because its bounded surface didn't include the app's root layout/navigation shell.

Per the task's instruction, I read `src/components/layout/Root.tsx` and `src/components/layout/Header.tsx`
directly. Finding: `Root.tsx` renders `<Header />` unconditionally above `<Outlet />` on every route, and
`Header.tsx` returns a bare `<Toolbar>` (search input, weather, geolocation, language, theme, settings) — a
persistent, page-independent global header. It is **not** wrapped in `<AppBar>` (no `position="fixed"` chrome,
no elevation) — a nuance the review's own hypothetical framing ("whether the app already has a global
`AppBar` elsewhere") gets slightly wrong in vocabulary, though the framing was explicitly speculative and
hedged, not asserted as fact, so this is not a citation or evidence error.

Substantively, this confirms the exact branch the review left open in its own favor: a persistent global
header **does** exist, so `RouteHeader`'s use of `Paper` as a secondary, route-scoped info+action strip
(route number, reverse/star/timetable) is correctly *not* competing with app-bar-level navigation chrome —
there is no missing finding here. The suppression's **outcome** is correct. Its **stated reasoning**
("insufficient evidence, bounded surface excludes root shell") is honest given what the review was actually
handed to review (the task's own file list separates "main surfaces"/"directly composed" from
`Root.tsx`/`Header.tsx`, which it only asked *me* to check) — so this is sound, disciplined intent-handling
per rubric Q9 (name the ambiguity, don't guess), not over-suppression.

---

## Coverage gap found: two missed duplicates of Finding 2's own pattern

This is not a graded "finding" in the review (nothing was written down, so there's no claim to score E on),
but it is material to the overall verdict on completeness. `BookmarkedStopPage.tsx` — one of the three
explicitly in-scope "main surfaces" — directly composes:

- **`DbRenewReminder.tsx`**: an almost byte-identical duplicate of `RouteUpdateNotice.tsx` — same
  `<Box sx={rootSx} onClick={renewDb}><Typography>{t("db-renew-text")}</Typography></Box>` shape, same
  hand-rolled bordered/padded/pointer-cursor styling, same missing `Alert` import. Finding 2's entire
  applicability argument applies to this file verbatim.
- **`BadWeatherCard.tsx`**: `<Paper variant="outlined" onClick={...}><ErrorIcon color="error" /><Typography>...</Typography></Paper>` — manually reconstructing `Alert`'s documented icon+message anatomy (including a severity-colored icon, `color="error"`) on a bare `Paper`, again with the whole surface as the click target.
- **`NoticeCard.tsx`**: a closable, dismiss-tracked warning banner (`WarnIcon` + message + close `IconButton`) that separately re-derives the exact "message + default close icon" shape the Alert page documents for the `onClose` prop, though its carousel/`Tabs` structure is more elaborate and a weaker one-line `Alert` fit.

The review's stated "directly composed" scope (`RouteHeader`, `StopAccordionList`, `StopDialog`,
`RouteUpdateNotice`, `AppContext`, `DbContext`) covers only `RouteEtaPage.tsx`'s subtree. Despite
`BookmarkedStopPage.tsx` being named as an in-scope main surface, none of its three composed
notice-band components were examined, and at least `DbRenewReminder.tsx` is materially indistinguishable
from the one instance the review did catch. This is a real completeness gap, not a wrong finding — the
review's single `Alert` finding is correct as far as it goes, but it under-covers its own declared scope.

---

## Overall verdict

- **Citation integrity: clean.** All 9 checked quotations verify character-for-character against the live
  `mui.com` pages; no fabrication, inversion, or misattribution anywhere.
- **Finding 2 (`Alert`) is well-evidenced (A)** but the review only caught one of at least two near-identical
  instances of the same anti-pattern inside its own declared bounded surface (`DbRenewReminder.tsx` in
  `BookmarkedStopPage.tsx` was missed entirely; `BadWeatherCard.tsx` is a softer but related miss).
- **Finding 1 (`DialogTitle`/`DialogActions`) is directionally reasonable but overstated (B)** — its central
  "every other demo agrees" premise is false once the Dialog page's "Full-screen dialogs" demo (a documented,
  on-point counter-pattern for near-fullscreen dialogs like this one) is factored in. The underlying
  crowded-header observation still has merit, but the confidence claimed exceeds what a full page survey
  supports.
- **The one suppression is correctly reasoned and its outcome is independently confirmed correct** by reading
  the root layout files the review didn't have in scope — good intent-discipline, not over-suppression.
- **All three orientation notes are accurate**, verified against both code and the cited MUI page text.
- **Net effect:** this review is trustworthy on what it says (no invented evidence, no misquotation) but
  incomplete on what it should have said — it under-covers two of its three named main surfaces
  (`StopEtaListPage.tsx` got no findings/notes at all beyond the shared inferred-task description, and
  `BookmarkedStopPage.tsx`'s composed notice components were skipped even though they duplicate a finding
  already made). A reader should treat this as a solid but partial pass over the bounded surface, not a
  complete one.
