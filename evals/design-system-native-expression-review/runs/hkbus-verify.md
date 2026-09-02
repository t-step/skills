# Adversarial Verification: hkbus-skill.md (Material UI native-expression review)

**Fixture:** hkbus/hk-independent-bus-eta @ `cb5b1fcbed5f9f7cb14635ee29507084b9de2578` (git HEAD independently confirmed to match).
**Review graded:** `evals/design-system-native-expression-review/runs/hkbus-skill.md`
**Rubric applied:** `evals/cloudscape-native-expression-review/rubric.md`, substituting Material UI for Cloudscape. No pre-written grading key exists for this fixture (real, unmodified OSS app) — graded against the rubric's general discipline.

Method: read the skill (`skills/design-system-native-expression-review/SKILL.md`), read all 9 bounded-surface files plus `App.tsx`, `components/layout/Root.tsx`, `components/layout/Header.tsx`, `components/layout/DbRenewReminder.tsx`, `components/layout/NoticeCard.tsx` for calibration, and independently WebFetched every cited `mui.com/material-ui/*` page (never MUI X/Joy/Base/M3) to check VERBATIM quotes character-for-character.

---

## Independent fact-check: does a persistent global app-shell header exist?

**Yes — confirmed independently, and it is materially relevant to Finding 1.**

- `src/App.tsx` routes every page (`/:lang`) through `<Route path="/:lang" element={<Root />}>`.
- `src/components/layout/Root.tsx` renders `<Header />` unconditionally, above `<Suspense><Outlet/></Suspense>`, on literally every route — i.e., `Header` is persistent global app-shell chrome.
- `src/components/layout/Header.tsx` root JSX is `<Toolbar sx={rootSx}>...</Toolbar>` (imported from `@mui/material`), containing: logo/home link (branding), a route search input, weather icons, geolocation/language/theme/settings actions. This is a bare `Toolbar`, **not** wrapped in `AppBar`.

So: no `AppBar` exists anywhere in the app (true, as both the review and my grep confirm), but a persistent global **bare-`Toolbar`** header does exist, and it is invisible from the 9 bounded-surface files alone — exactly as flagged. This is the established, repeated app idiom for "branding + screen content + actions" chrome (`AppBar`'s own documented job, verbatim below), and it sits immediately above `RouteHeader` in the render tree on `RouteEtaPage`.

---

## Finding 1 — RouteHeader → AppBar/Toolbar

**Type:** combined selection + composition. **Materiality:** high. **Confidence:** high. Reported unhedged.

1. **User task supported by evidence?** Yes — `RouteHeader.tsx:25-43` matches the description exactly (Paper flex row, ReverseButton, centered RouteNo+RouteStarButton+caption, vertical Divider, TimetableButton). Verified by direct read.
2. **Does cited AppBar guidance say what's claimed?** Yes, verified live. `https://mui.com/material-ui/react-app-bar.md` opens with "The App Bar displays information and actions relating to the current screen." (this is the page's lead/meta line, distinct from but consistent with the body paragraph "The top App bar provides content and actions related to the current screen. It's used for branding, screen titles, navigation, and actions.") — both sentences are genuinely on the page. "It can transform into a contextual action bar or be used as a navbar." is also verbatim, confirmed via a second fetch forcing character-for-character reproduction. No fabrication.
3. **Actually applicable — four-point test?** This is where the finding weakens materially. Applicability point 4 states: *"I checked whether a persistent global `AppBar`/`Toolbar` already exists elsewhere in the app (`src/App.tsx`, `src/components/layout/Root.tsx`) — it does not; the app has no app-shell `AppBar` at all... there is no competing/duplicate AppBar already claiming that role elsewhere in the app that this recommendation would collide with."* This is true of `AppBar`-the-component but is a materially incomplete answer to the question the review itself posed (it explicitly frames the check as "AppBar/Toolbar," then only reports on AppBar). `Root.tsx` — one of the exact two files the review says it checked — directly imports and renders `<Header />` as the very first thing in the tree; one hop into that sibling file (`Header.tsx`, same directory) shows a persistent, app-wide, unwrapped `Toolbar` performing precisely the "branding, screen titles ... actions" job AppBar's own docs describe. The review's own applicability argument therefore rests on an investigation that stopped one file short of a finding it was specifically checking for.
4. **Preserves task semantics?** Yes, if adopted, semantics are unchanged.
5. **Could current impl (Paper) already be equally valid, for a documented/supported reason?** Newly-material: the app's own established, repeated idiom for "bar-shaped chrome with actions" is a **bare `Toolbar`**, never `AppBar`. Given that, an experienced MUI-fluent implementer working in *this specific codebase* is at least as likely to reach for the codebase's own established bare-`Toolbar` convention for a second-level, route-scoped header as for the textbook `AppBar`+`Toolbar` pairing the review recommends — and stacking a second `AppBar`-wrapped bar directly beneath the already-existing bare-`Toolbar` global header is a different, non-trivial design decision the review never engages with because it didn't know the global header existed.
6. **Materiality — would an FDE actually restructure?** Weakened from "high/high" as reported. This is a real, genuine finding at the component level (the docs quote is accurate, the shape match is real), but the specific "no competing header, no collision" sub-claim that anchors the applicability argument and the confident unhedged tone is checkably wrong.
7. **Leaks into implementation correctness / generic UX?** No — stays component/composition level. Not the failure mode here.
8. **Duplicated across levels?** No — correctly unified as one `combined` finding; not a violation.
9. **Intent-dependent handling.** This is the crux. Given the discovered global `Toolbar`-based header, there are now genuinely two plausible readings the review never named: (a) `RouteHeader` should adopt `AppBar`/`Toolbar` per MUI's documented per-screen "contextual action bar" composition, independent of the global header, or (b) `RouteHeader` should match the app's own already-established bare-`Toolbar` idiom (consistency with the one convention this codebase has actually chosen), and introducing `AppBar` — a component that appears nowhere else in the app — for a single sub-component is itself a new one-off pattern, the exact anti-pattern the skill's "why it matters" language warns against ("forgoes shared vocabulary ... for a bespoke one-off"). The review had the evidence in hand (it explicitly went looking) and reached a confident, unhedged, high-materiality verdict on a question that — once the missed fact is included — should at minimum have been down-weighted, and arguably reclassified `intent-dependent` per the skill's own "Missing intent" section (name both readings, don't guess).

**Verdict: RouteHeader→AppBar/Toolbar was reported unhedged when it should not have been.** Not because AppBar is the wrong component in the abstract (the citations are accurate and the shape match is real), but because the review's own applicability argument makes a specific, checkable claim about the absence of a competing header pattern that is false in the way that matters most, and the correct response to that fact — once known — is either to fold it into an `intent-dependent` classification or to substantially downgrade confidence/materiality, not report it as-is.

**Grade: D** — overreach in the applicability argument (Q3/Q5), and a confident answer where the (self-uncovered, then missed) evidence should have produced either intent-dependent classification or a materially weaker claim (Q9). The underlying component-selection observation and its citations are sound; the grade is driven by the false "no competing chrome" sub-claim, not by citation integrity.

**Citation integrity: clean.** Both VERBATIM quotes are genuine, character-for-character verifiable against `mui.com/material-ui/react-app-bar`.

---

## Finding 2 — RouteUpdateNotice → Alert's `action` slot

**Type:** component selection. **Materiality:** medium. **Confidence:** high.

1. **Evidence supported?** Yes — `RouteUpdateNotice.tsx:29-49` confirmed exactly as described: a `Box` with `onClick={renewDb}` wrapping a `Typography` with an emoji, no `Alert` import.
2. **Cited guidance accurate?** Yes, verified live against `react-alert.md`: "Alerts display brief messages for the user without interrupting their use of the app." is confirmed as the page's lead line (distinct body text elsewhere reads "Alerts give users brief and potentially time-sensitive information in an unobtrusive manner." — both genuinely present, review cites the correct one verbatim). The `action` prop quote — "Add an action to your Alert with the `action` prop. This lets you insert any element—an HTML tag, an SVG icon, or a React component such as a Material UI Button—after the Alert's message, justified to the right." — is exact, word for word.
3. **Applicable?** Yes, cleanly passes all four points: the task (brief, non-blocking message + a follow-up action) is precisely Alert's stated purpose, not a superficial shape match; current impl solves the identical problem; an `Alert action={<Button onClick={renewDb}>}` preserves the exact same behavior; the difference (bespoke bordered `Box`+emoji vs. the one component in this corpus whose stated purpose is exactly this job) is the kind of thing an MUI-fluent implementer would plausibly fix.
4. **Preserves semantics?** Yes.
5. **Could current impl be equally valid for a documented reason?** No — and additional calibration I ran independently strengthens rather than weakens this: `src/components/layout/DbRenewReminder.tsx` is a near-duplicate of `RouteUpdateNotice.tsx` (same `Box`+`onClick`+bordered-`sx`+`Typography` shape, same `db-renew-text` copy), and `NoticeCard.tsx` is a third hand-rolled notice using `Paper`+`IconButton` rather than `Alert`. This is a repeated app-wide pattern of not reaching for `Alert`, which raises rather than lowers the case that this is a genuine, systemic missed opportunity — it does not read as an intentional, documented design choice (no MUI authority supports the custom-border approach), just repeated ad hoc styling. The review didn't need this to make its case, but it holds up under the same scrutiny that hurt Finding 1.
6. **Materiality?** Correctly scoped as `medium`, not oversold to `high`; correctly hedges that Alert's `severity` isn't established by the corpus.
7. **Scope leak?** None — stays cleanly at component-selection level; boundary check is accurate.
8. **Duplication?** N/A, single clean finding.
9. **Intent-dependent?** N/A — not applicable, correctly not forced into that category.

**Grade: A** — material and strongly validated. Clean citations, precise applicability, preserves the same task, correctly hedged on severity, and cross-file calibration (DbRenewReminder/NoticeCard) independently corroborates rather than undercuts it. This is the strongest finding in the review.

**Citation integrity: clean.**

---

## Finding 3 — StopDialog full-height styling / fullScreen (intent-dependent)

**Type:** intent-dependent. **Materiality:** medium. **Confidence:** medium.

1. **Evidence supported?** Yes — `StopDialog.tsx:67-99` and `rootSx` (103-112) confirmed exactly: `Dialog` with no `fullScreen` prop, `DialogTitle` built from a plain `Box` of five `IconButton`s, and `marginTop: "90px"` / `height: "calc(100vh - 100px)"` CSS overrides forcing near-full-height.
2. **Cited guidance accurate?** Yes, verified live against `react-dialog.md`: "Dialogs are purposefully interruptive, so they should be used sparingly." and "Dialogs inform users about a task and can contain critical information, require decisions, or involve multiple tasks." are both exact. I additionally fetched the actual "Full-screen dialogs" demo source and confirmed it genuinely pairs `<Dialog fullScreen>` with `<AppBar sx={{position:'relative'}}><Toolbar>` containing a close `IconButton`, a `flex:1` `Typography` title, and a trailing `Button` — so the SYNTHESIS's factual premise (a documented example pairs `fullScreen` with an `AppBar`/`Toolbar` title bar) is real, not invented, and the review correctly labels it as a demo/example, not a stated rule.
3. **Applicable — and correctly scoped?** Partially, and this is the finding's real weakness. Two things are bundled together as one "reading": (a) a genuine composition-level question — should the bare-`Box`-of-`IconButton`s title row become an `AppBar`/`Toolbar` title row, mirroring MUI's documented full-screen composition (this is legitimately component/composition-level, since it's a component substitution); and (b) whether the `marginTop`/`height` CSS hack should instead be the `fullScreen` boolean prop. (b) is a prop-vs-hardcoded-CSS question on an already-correctly-chosen component (`Dialog` — confirmed by the review's own Orientation notes as correctly selected independent of this finding) — which is squarely the skill's own out-of-scope category ("hard-coded style/token values," "unsupported component composition mechanics"). The skill's contract allows citing such a detail "minimally as supporting evidence, not as its own finding," but this review elevates it beyond that: the "Two plausible readings" section names "the `fullScreen` boolean prop" as a first-class part of the recommended alternative, and "Why it matters" is framed explicitly around "hand-tuned pixel values instead of the dedicated `fullScreen` prop" — i.e., the finding's own stated rationale is substantially about the prop-vs-CSS mechanics, not only the title-row component swap.
4. **Preserves task semantics?** N/A / correctly not asserted, per the hedge.
5. **Equally valid current usage?** Plausible under reading 2 (deliberately partial-height sheet), which the review names — correct discipline here.
6. **Materiality?** Self-capped at medium, appropriately — the finding is honest that it's unresolvable from the bounded surface.
7. **Scope leak — the decisive question for this finding.** Yes, partial: the composition-level kernel (title-row component swap) is legitimate; the prop-vs-hardcoded-CSS framing riding alongside it as part of the same recommendation is implementation mechanics dressed as composition reasoning. This is exactly the failure mode the task asked to scrutinize ("should this modal use the fullScreen prop" when Dialog is already the right component) — and it is present here, though not as the entire finding, only as a component folded into it.
8. **Duplication across levels?** No.
9. **Intent-dependent handling — executed correctly.** The two readings are genuinely named, "what would resolve it" is concrete and specific ("whether this dialog is intended to read... as a full-screen 'stop detail' destination... or as a deliberately bounded quick-look overlay"), and the review explicitly declines to pick a side, correctly downgrading Evidence mode to SYNTHESIS and Authority strength to INFERRED rather than borrowing REQUIRED/RECOMMENDED strength from the underlying pages. This part of the finding contract is followed exactly as the skill specifies.

**Verdict on the fullScreen scope-fence question:** the finding was **not cleanly handled** — it does contain a genuine, in-scope component-selection kernel (title-row: bare `Box` vs. `AppBar`/`Toolbar`), but it is bundled with, and its stated "why it matters" leans on, a prop-vs-hardcoded-CSS implementation-mechanics observation that the skill's own scope boundary excludes as anything beyond passing supporting evidence. The intent-dependent *procedure* (naming both readings, refusing to guess) is executed correctly and should be credited on Q9; the grade is capped by the Q7 scope leak, not a Q9 failure.

**Grade: D** — drifts into implementation correctness (prop vs. hardcoded style values) dressed as composition reasoning, per the rubric's own D definition, even though the intent-dependent discipline itself (Q9) is a genuine strength and the composition-level half of the argument is real.

**Citation integrity: clean.** No fabricated or misattributed quotes; the "Full-screen dialogs" demo composition was independently confirmed to actually pair `AppBar`/`Toolbar` as claimed.

---

## Suppressed section — spot-checked

- **StopAccordionList — Stepper vs. accordion list.** Correct suppression. `Stepper` is documented for linear process flows; the observed task (non-linear expand/jump/map-click navigation across an ordered-but-freely-addressable list of stops, confirmed in `StopAccordionList.tsx`) is not that. Correctly reasoned as the anti-fundamentalism rule's "superficial shape match," and correctly notes the actual `Accordion` usage lives outside the bounded surface (`StopAccordion.tsx`), so no component judgment is made about it. No issues.
- **StopDialog — Box vs. Stack for the icon row.** Correct suppression — genuinely an undifferentiated, equally-valid MUI layout choice; no authority favors one over the other for a plain icon row.
- **BookmarkedStopPage — Paper(elevation=0) vs. Box.** Correct suppression, confirmed against the actual file (`BookmarkedStopPage.tsx:73-97`): `Paper` at `elevation={0}` with a background image is a documented, valid surface usage; no rule against it.
- **StopEtaListPage — Typography+Divider header.** Correct suppression, confirmed against the file: unremarkable, no composition authority applies.

All four suppressions are well-reasoned and consistent with the skill's materiality discipline. No under- or over-suppression found.

## Orientation notes — spot-checked

- **Snackbar for copy-confirmation** (`StopAccordionList.tsx:65-73`, confirmed exact match including `autoHideDuration={1500}`). Quote "brief notifications of processes that have been or will be performed" verified verbatim against `react-snackbar.md`. Correct.
- **Dialog as the chosen component for StopDialog** — reasonable, and consistent with treating Finding 3 as intent-dependent only on the full-screen-vs-partial sub-question, not on Dialog's selection itself.
- **Bookmark icon toggle idiom** — plausible, unremarkable, no issue.
- **Vertical Divider with flexItem** (`RouteHeader.tsx:39`) — confirmed present in the file; quote "a thin, unobtrusive line for grouping elements to reinforce visual hierarchy" verified verbatim against `react-divider.md`. Correct.
- **AppContext/DbContext render no UI** — independently confirmed via grep: neither file imports `@mui/material` or `@mui/icons-material`.
- **`@mui/x-date-pickers` absent from all 9 bounded-surface files** — independently confirmed via grep across all 9 files: zero `@mui/x-` matches. Accurate, and the version-resolution claim (`@mui/material`/`@mui/icons-material` locked to `5.15.11`) was independently confirmed against `package.json`/`yarn.lock`.

No issues in Orientation notes.

---

## Citation integrity summary (independent, live re-fetch of every cited mui.com/material-ui page)

| Citation | Mode | Verified? |
|---|---|---|
| App Bar: "The App Bar displays information and actions relating to the current screen." | VERBATIM | Confirmed exact |
| App Bar: "It can transform into a contextual action bar or be used as a navbar." | VERBATIM (quoted) | Confirmed exact |
| Alert: "Alerts display brief messages for the user without interrupting their use of the app." | VERBATIM | Confirmed exact |
| Alert `action` prop paragraph | VERBATIM | Confirmed exact, word for word |
| Dialog: "Dialogs are purposefully interruptive, so they should be used sparingly." | VERBATIM | Confirmed exact |
| Dialog: "...critical information, require decisions, or involve multiple tasks." | VERBATIM | Confirmed exact |
| Dialog "Full-screen dialogs" example pairs `fullScreen` with `AppBar`/`Toolbar` | SYNTHESIS (factual premise) | Confirmed — actual demo source fetched and matches |
| Divider: "a thin, unobtrusive line for grouping elements to reinforce visual hierarchy." | VERBATIM (orientation note) | Confirmed exact |
| Snackbar: "brief notifications of processes that have been or will be performed." | VERBATIM (orientation note) | Confirmed exact |

**No fabricated, conflated, or misattributed quotes found anywhere in this review.** This is a clean result on the exact failure mode (citation fabrication under MUI's flatter corpus) the skill's lineage notes were designed to catch — none of the PARAPHRASE/INFERRED/SYNTHESIS labels were found dressed up in quotation marks either; the review is disciplined about reserving quote marks for VERBATIM claims throughout.

---

## Summary table

| Finding | Type | Grade | Primary driver |
|---|---|---|---|
| 1. RouteHeader → AppBar/Toolbar | combined | **D** | Q3/Q5/Q9 — applicability argument's "no competing header" claim is checkably incomplete once `Header.tsx`'s persistent global `Toolbar` is found; should have been down-weighted or reclassified intent-dependent, not reported unhedged at high/high |
| 2. RouteUpdateNotice → Alert | component selection | **A** | Clean on all nine questions; independently corroborated by sibling notice components (`DbRenewReminder`, `NoticeCard`) showing the same gap repeated app-wide |
| 3. StopDialog fullScreen | intent-dependent | **D** | Q7 — genuine composition kernel (title-row swap) bundled with an implementation-mechanics observation (prop vs. hardcoded CSS) that exceeds the "supporting evidence only" allowance; Q9 (intent-dependent procedure itself) executed correctly and should be credited separately |
| Suppressed (4 items) | — | correctly suppressed | spot-checked against source, no issues |
| Orientation notes (6 items) | — | correctly confirmed | spot-checked against source and live docs, no issues |

Citation integrity: **clean across the entire review** — no fabrications found in this adversarial pass.
