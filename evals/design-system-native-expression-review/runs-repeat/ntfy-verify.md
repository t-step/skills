# Adversarial Verification: ntfy SubscribeDialog/PublishDialog (repeat run)

**Review under test:** `evals/design-system-native-expression-review/runs-repeat/ntfy-skill.md`
**Fixture:** `binwiederhier/ntfy@10cb6506` — `web/src/components/{SubscribeDialog,PublishDialog,ReserveTopicSelect,DialogFooter,AttachmentIcon,EmojiPicker}.jsx`
**Method:** every fixture file re-read directly against the review's line citations; every quotation-marked claim in the review independently re-fetched from the live `mui.com/material-ui/*.md` pages (Checkbox, Alert, Snackbar, Popper, Popover, Modal, Chip, Autocomplete, ToggleButton, Tooltip, Dialog) and checked character-for-character, not from memory.

## Headline verdict

This run **does not repeat the prior round's inversion bug**. The Popper/Popover reasoning is now factually sound in its citations and reaches the *correct* conclusion (Popper+ClickAwayListener+Fade is native, not a finding), though its supporting rationale has one weak link (addressed below). Citation discipline is much improved but not perfect: **two quotation-marked strings in Finding 2 do not exist verbatim on the pages they're attributed to.** Neither is load-bearing for a wrong conclusion — the substance each purports to quote is independently true and separately verifiable — but both are quotation-integrity failures that a strict verbatim check must flag, and they mean this run does not get a clean bill of health on "distinguish exact quotation from paraphrase throughout."

---

## 1. Fixture re-read — citation accuracy check

All file/line citations in the review were checked against the actual files (not trusted from the review's own numbers):

| Citation | Claimed | Actual | Verdict |
|---|---|---|---|
| `PublishDialog.jsx` 387–402 (`markdownEnabled` Checkbox) | standalone `FormControlLabel`+`Checkbox`, not in a `FormGroup` | Lines 387–402 are exactly this `FormControlLabel` element, no sibling checkboxes | Exact match |
| `PublishDialog.jsx` 757–772 (`publishAnother` Checkbox) | same pattern, in `DialogFooter` | Lines 757–772 are exactly this element, inside `<DialogFooter>` | Exact match |
| `SubscribeDialog.jsx` 198–223 / 224–264 (two `Switch` controls) | reserve-topic and use-another-server, each standalone | First `FormGroup` block is 198–224 (closing paren at 224, not 223), second is 225–264 (not 224–264) | Off by one line at both boundaries — immaterial, correct components/semantics |
| `DialogFooter.jsx` 4–27 | single `DialogContentText` renders `props.status` | Confirmed, function body is exactly lines 4–27 | Exact match |
| `SubscribeDialog.jsx` 113–117, 289 (`error` state) | rendered through `DialogFooter`'s `status` prop | Line 113–117 is the `setError(...)` call in `SubscribePage`; line 289 is the equivalent in `LoginPage` | Exact match |
| `PublishDialog.jsx` 186–189 (ad hoc colored `Typography` in catch block) | only place `status` is set to something other than plain translated text | Lines 186–189 are exactly the `catch (e) { setStatus(<Typography sx={{ color: "error.main" ...) ...}` block | Exact match. Note: `AttachmentBox`'s separate error `<Typography color="error.main">` at line ~852 is a *different* UI element not routed through `DialogFooter`'s `status` prop, so the review's "only" claim is correctly scoped, not an overclaim |

No fabricated or misdescribed repository evidence found anywhere in the review. Line-citation precision is high; the one-line drift on the second `Switch` block is noise, not a substantive error.

## 2. Live-authority verification of every quotation-marked claim

Fetched directly from `mui.com/material-ui/*.md` (not from training-data memory). "VERBATIM-style" = presented in quotation marks as literal source text, regardless of whether the finding's own `Evidence mode` field says VERBATIM or SYNTHESIS — the task requires checking any quotation-marked string presented as literal.

| # | Where in review | Quoted string | Live source result | Verdict |
|---|---|---|---|---|
| 1 | Finding 1 | "If you have multiple options appearing in a list, you can preserve space by using checkboxes instead of on/off switches. If you have a single option, avoid using a checkbox and use an on/off switch instead." | Confirmed present, word-for-word, on `react-checkbox` | **Clean — exact match** |
| 2 | Finding 2 | "display brief messages for the user without interrupting their use of the app" | `react-alert`: "Alerts **display brief messages for the user without interrupting their use of the app.**" | **Clean** — accurate excerpt (drops leading "Alerts") |
| 3 | Finding 2 | "each with corresponding icon and color combinations" | `react-alert` actual text: "...with corresponding icon and color combinations **for each**" | **Quotation drift** — real sentence, but word order altered ("for each" moved from the end to the front). Not present verbatim in this word order anywhere on the page. Substance unchanged. |
| 4 | Finding 2 | Snackbar page "contrasts Snackbar as fixed-position, floating, breaking out of document flow, versus Alert being **"typically integrated into the page layout."**" | Searched `react-snackbar.md` and `react-alert.md` explicitly for this phrase and its close variants ("typically integrated," "part of the page layout," "usually part of the flow"). Result: **NOT FOUND ANYWHERE ON EITHER PAGE.** Actual text: "Snackbars... are intended to break out of the document flow; **Alerts, on the other hand, are usually part of the flow**—except when they're used as children of a Snackbar." | **Fabricated quote.** The substance (Alert is in-flow, Snackbar floats) is correct and independently verifiable from the real sentence quoted above, but "typically integrated into the page layout" is not MUI's wording anywhere on either page — it's invented phrasing dressed in quotation marks as if literal. |
| 5 | Finding 2 (paraphrase, no quotes) | `role="status"` override for less urgent messages | `react-alert`: "Less urgent messages should use a less aggressive method, such as overriding the default role with a `role="status"`." | **Clean** — correctly presented as paraphrase (no quotation marks around the sentence), and accurate |
| 6 | Suppressed / Chip | "Chips with the `onClick` prop defined" | `react-chip`: "Chips with the `onClick` prop defined change appearance on focus, hover, and click." | **Clean** — accurate fragment |
| 7 | Suppressed / Chip | "trigger actions" | `react-chip`: "Chips allow users to enter information, make selections, filter content, or trigger actions." | **Clean** — accurate fragment from a different sentence, but correctly presented as a separate quoted span glued with the review's own connective words, not spliced into one continuous fabricated quote |
| 8 | Suppressed / ToggleButton | "group related options" | `react-toggle-button`: "A Toggle Button can be used to group related options." | **Clean** |
| 9 | Orientation / Popper | "Clicking away does not hide the Popper component. If you need this behavior, you can use the Click-Away Listener" | `react-popper`: confirmed exact match, "Basic Popper" section | **Clean — exact match, and correctly non-inverted** (this is the same page the prior round misquoted in the opposite direction) |
| 10 | Orientation / Autocomplete | "the primary use case of a search input with suggestions" | `react-autocomplete`: "The prop is designed to cover the primary use case of a **search input** with suggestions, for example Google search..." | **Clean — exact match** |
| 11 | Orientation / Autocomplete | "the textbox may contain any arbitrary value, but it is advantageous to suggest possible values" | `react-autocomplete`: "The textbox may contain any arbitrary value, but it is advantageous to suggest possible values to the user, for example..." | **Clean** — truncated at a clause boundary without an ellipsis marker; minor style nit, not distorting |
| 12 | Orientation / Tooltip | "By default disabled elements ... do not trigger user interactions so a Tooltip will not activate ... To accommodate disabled elements, add a simple wrapper element, such as a span." | `react-tooltip`: exact match, correctly using `...` to mark omitted words | **Clean — model use of ellipses** |
| 13 | Inferred user task | "inform users about a task ... require decisions" | `react-dialog`: "Dialogs inform users about a task and can contain critical information, require decisions, or involve multiple tasks." | **Clean** — correct ellipsis use |

**Tally: 13 quotation-marked claims checked. 11 clean / exact. 1 quotation drift (word-order, non-inverting). 1 fabricated quote (non-inverting, substance-correct).** Zero semantic inversions and zero conflations (no case of genuinely unrelated-section text spliced in as continuous quotation).

## 3. The Popper/Popover question, adjudicated independently

This is the specific regression check this run exists to perform. Findings:

- **Popover's actual documented properties** (from `react-popover.md`, fetched live): "The component is built on top of the `Modal` component." / "`Popover` blocks scrolling and dismisses on click-away by default, unlike `Popper`." Confirmed accurate and matches the review's paraphrase ("Popover... is built on Modal and blocks scrolling/dismisses on click-away by default").
- **Popper's actual documented properties** (from `react-popper.md`): "The scroll isn't blocked like with the Popover component." / "Clicking away does not hide the Popper component. If you need this behavior, you can use the Click-Away Listener." Confirmed accurate and matches the review's paraphrase ("Popper... does neither by default").
- **Is Popper+ClickAwayListener MUI's own sanctioned composition, or a workaround for a missing feature?** The Popper page's own text explicitly names Click-Away Listener as the answer to "if you need [click-away-dismiss] behavior" — this is MUI's own documented remedy for exactly this gap, not an undocumented hack. The fixture's `<Fade {...TransitionProps} timeout={350}>` inside `<Popper transition>` is a **character-for-character match** to MUI's own worked "Transitions" example (`react-popper.md`, confirmed by direct fetch — down to the identical `timeout={350}`). This is the strongest possible form of "this is documented/sanctioned usage," and the review's core citation captures the right half of it (click-away) cleanly and without inversion. Notably, the review does **not** attempt the transition/animation-support claim that caused the prior round's inversion bug at all — a conservative, safe choice that avoids the exact landmine.
- **Where the review's own reasoning is weaker:** it argues Popover would be "a worse fit" here because "the panel contains its own internally-scrollable, searchable grid" and Popover "blocks scrolling." This conflates two different things. Per MUI's Modal docs (`react-modal.md`, fetched live): "It disables scrolling of **the page content** while open" — i.e., Popover's scroll-block is a body/background scroll-lock, not a restriction on scrolling *within* the popover's own content. A `Popover` can contain an internally-scrolling list with no conflict (this is exactly what `Menu`, itself built on `Popover`, does routinely). So the specific "internal scroll" justification the review gives is not actually supported by what MUI's docs say scroll-blocking does — it's a plausible-sounding but technically incorrect inference layered on top of an otherwise-accurate citation.
- **A stronger argument the review missed:** `react-autocomplete.md`'s own metadata lists Popper (not Popover) among Autocomplete's related components — i.e., MUI's own search-input-with-a-filtered-list widget (structurally the closest analog to `EmojiPicker`'s search box + filtered emoji grid) is itself Popper-based, not Popover-based. This is independent, stronger corroboration for the same conclusion the review reached, that the review did not find or cite.

**Verdict on the Popper/Popover item:** the "already-native, no finding" conclusion is **correct**, not a flipped-and-still-wrong verdict. The load-bearing citation (click-away-listener) is accurate and non-inverted. The supplementary justification (internal-scroll) is a reasoning error but is not what the conclusion actually depends on, and does not reverse it. This represents genuine improvement over the prior round: the citation that mattered is now handled correctly and does not misstate what MUI's docs say.

## 4. Per-finding grading (rubric: `evals/cloudscape-native-expression-review/rubric.md`, s/Cloudscape/Material UI/)

### Finding 1 — Checkbox → Switch for standalone booleans

- Q1 (task support): confirmed by code — both are genuinely standalone, non-list booleans, not in a `FormGroup` with siblings.
- Q2 (authority accuracy): exact verbatim match, confirmed live, no exceptions/caveats exist anywhere else on the Checkbox page that would carve out an exemption.
- Q3 (applicability): passes cleanly — this is precisely the "single option" case the rule names, no fundamentalism (the rule is an explicit prohibition, not "the docs merely show an example").
- Q4 (task preservation): Switch is a one-for-one control swap; no redesign.
- Q5 (equally valid as-is?): no — the Checkbox page states no caveat permitting standalone Checkbox for single options; `SubscribeDialog.jsx`'s own two Switches for the same class of setting is strong internal-consistency evidence against "this is equally valid here."
- Q6 (materiality): a real FDE would plausibly make this exact swap, especially given the sibling dialog already does it correctly.
- Q7 (leak check): clean component-selection call, not implementation/a11y/UX.
- Q8 (duplication): single, unified finding — not artificially split.
- Q9: n/a (not intent-dependent).

**Grade: A.** Real, verified, applicable without qualification, and the strongest kind of materiality argument (documented rule + a working counter-example one file over in the same codebase).

### Finding 2 — DialogFooter status slot → Alert

- Q1: task support solid — the status slot legitimately carries error/progress/success text across both dialogs.
- Q2: **partially fails.** Two of the quotation-marked strings used to build this synthesis do not check out verbatim (see table rows 3–4 above); the underlying facts they gesture at are true, but the exact wording quoted is not MUI's.
- Q3: applicability is reasonable but not airtight — Alert's stated purpose fits well, but the review does not verify Alert's chrome (padding/border/icon sizing) actually fits a compact single-row footer, and says so honestly.
- Q4: preserves task semantics (same slot, same position, richer semantics).
- Q5: `DialogContentText` isn't wrong, exactly — it's generic body copy pressed into service for status messaging; Alert is more purpose-built but this is a real judgment call, not a clear-cut violation like Finding 1's explicit "avoid X, use Y" rule.
- Q6: materiality genuinely medium, as self-assessed — plausible but not a must-fix.
- Q7: correctly scoped to component/composition; explicitly declines to touch `aria-live` mechanics (a11y) or general UX.
- Q8: unified single finding (labeled "combined selection + composition" appropriately, not double-counted).
- Q9: n/a.

**Grade: B.** The idea is real and the self-assessed medium confidence/materiality is honest calibration, but it cannot be graded A because two of its supporting citations are not what they claim to be verbatim, even though neither reverses the conclusion.

### Suppressed — Chip progressive disclosure vs. ToggleButton

Both citations ("onClick... trigger actions" and "group related options") check out verbatim. The applicability reasoning (a Chip that disappears once clicked and is replaced by a field row is not "persistent, mutually relevant selection state") is sound and correctly distinguishes the two components' actual documented purposes. **Correctly suppressed — not a verifier disagreement.**

### Orientation notes (not findings, but checked as instructed)

- **SubscribeDialog `Switch` controls:** trivially correct against the code; used honestly as an internal baseline, not overclaimed.
- **EmojiPicker Popper composition:** see Section 3. Citations accurate and non-inverted; conclusion correct; one weak supplementary argument that doesn't affect the outcome.
- **Autocomplete `freeSolo`:** citations accurate; applicability correct (a base-URL field that suggests previously-used URLs while accepting arbitrary input is exactly this documented case).
- **Disabled Chip + Tooltip + span:** citation accurate, uses ellipses correctly, applicability correct (the code does exactly wrap the disabled Chip in a `<span>` per the documented workaround).

## 5. Explicit verdict on citation integrity

- **Fabricated citations:** 1 (Finding 2's "typically integrated into the page layout" — does not exist on either the Alert or Snackbar page in any form).
- **Conflated citations** (real text from a different section/example spliced together as continuous quotation): 0.
- **Semantically inverted citations:** 0. This is the specific failure mode the prior round exhibited on this same fixture (claiming Popper "doesn't include built-in transition animations" when the live page says the opposite and gives that exact composition as its worked example); **this run has zero instances of that failure mode.**
- **Minor quotation drift** (real sentence, word order altered): 1 (Finding 2's "each with corresponding icon and color combinations").
- **Load-bearing?** No. Both flawed quotes sit in Finding 2, which is independently gradable as B on its applicability merits alone; the true facts they gesture at (Alert has severity/icon/color options; Alert is normally in-flow, unlike Snackbar) are separately confirmed via other, accurately-quoted sentences from the same pages. Removing both flawed quotes from Finding 2 would weaken its rhetorical polish but would not change its grade or its conclusion. Finding 1, the Popper/Popover orientation note, and every other quoted claim in the review are clean.

**Bottom line:** citation discipline has measurably improved and the specific inversion failure from the prior round did not recur, including in the exact same component (`EmojiPicker`/Popper) that produced it. However, this run is not citation-clean: it introduces two new (non-inverting) quotation-integrity defects, both confined to Finding 2. A verifier grading strictly on "is everything in quotation marks copy-paste-verifiable" must fail those two spans and record this as a partial, not full, stabilization of citation discipline.

## Summary table

| Item | Type | Grade | Citation integrity | Notes |
|---|---|---|---|---|
| Finding 1: Checkbox → Switch | component selection | **A** | Clean | Documented "avoid/use instead" rule, exact match, internally corroborated by sibling dialog |
| Finding 2: DialogFooter → Alert | selection + composition | **B** | 1 fabricated + 1 drifted quote (non-inverting, non-load-bearing) | Real idea, honest medium confidence, but two quotes don't check out verbatim |
| Suppressed: Chip vs ToggleButton | (suppressed) | correct suppression | Clean | Sound reasoning, not a verifier disagreement |
| Orientation: EmojiPicker Popper/Popover | (orientation, no finding) | **conclusion correct** | Clean, non-inverted | Load-bearing citation solid; one weak supplementary argument (scroll-block conflation) that doesn't change the outcome; a stronger corroborating fact (Autocomplete is itself Popper-based) exists and was missed |
| Orientation: Autocomplete freeSolo | (orientation) | correct | Clean | — |
| Orientation: disabled Chip + Tooltip | (orientation) | correct | Clean | — |
