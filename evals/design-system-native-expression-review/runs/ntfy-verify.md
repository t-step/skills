# Adversarial verification: ntfy-skill.md (Material UI native-expression review)

Fixture: binwiederhier/ntfy @ 10cb6506f836dbb00bb77e3b52669f6ace37f555, files under
`/Users/thomasestep/Developer/mui-eval-fixtures/ntfy/web/src/components/`.
This is the real, unmodified fixture — no pre-written grading key. Graded against the
rubric's general discipline (`evals/cloudscape-native-expression-review/rubric.md`,
"Cloudscape" read as "Material UI").

All repository citations (file/line) in the review were independently re-read and
match the code exactly: `DialogFooter.jsx:1-29`, `PublishDialog.jsx:186-189, 404-409`,
`SubscribeDialog.jsx:266,334`, `EmojiPicker.jsx:3,47-113`, `PublishDialog.jsx:822-870`
(`AttachmentBox`), `ReserveTopicSelect.jsx`, `SubscribeDialog.jsx:198-263` (Switch /
Autocomplete). No fabricated or misdescribed repository evidence found anywhere in
the review.

---

## Finding 1 — DialogFooter status line vs. DialogContentText/Alert

**Grade: B**

1. Task supported — yes. `DialogFooter.status` is passed a plain string at
   `SubscribeDialog.jsx:266,334` and a hand-colored `Typography` at
   `PublishDialog.jsx:186-189`, all confirmed by direct read.
2. Authority accuracy — both VERBATIM quotes check out against live
   `mui.com/material-ui/react-dialog.md` and `react-alert.md`: "a wrapper for text
   inside of `<DialogContent />`" and "Alerts display brief messages for the user
   without interrupting their use of the app" / "corresponding icon and color
   combinations" are copy-paste-verifiable exactly as quoted.
3. Applicability (4-point test) — passes reasonably: task match (transient,
   non-interrupting message) is close, not superficial; the code already solves
   the same problem by hand in exactly one call site; the proposed swap preserves
   the same info/placement; materiality is honestly capped at `medium` because
   only the publish-failure branch actually needed severity.
4. Task semantics preserved — yes, same status slot, same location.
5. Equally-valid alternative? — partially. Nothing in the fetched Dialog page
   forbids `DialogContentText` outside `DialogContent`; the finding's own
   "documented-role deviation" framing is descriptive, not a stated constraint,
   and the review correctly avoids claiming `REQUIRED` strength for it.
6. Materiality / would an FDE act — plausible for the `Alert` half (an FDE
   reviewing the `sx={{ color: "error.main" }}` hack would likely reach for
   `Alert severity="error"` instead); less compelling for the container-nesting
   half.
7. Scope leak — this is the finding's real weak point. The skill's own
   out-of-scope list names "unsupported component composition mechanics" and
   "hard-coded style/token values" as implementation correctness, and the
   DialogContentText-outside-DialogContent observation sits close to that line.
   The review keeps this defensible by using it only as supporting evidence for
   a component-selection claim (Alert vs. hand-rolled severity), which the skill
   explicitly permits, but it is a real knock, not a non-issue.
8. No duplication across levels — this is legitimately one combined finding, not
   two split ones.
9. N/A (not intent-dependent).

Evidence mode, authority strength, and materiality are all self-consistently and
honestly labeled (SYNTHESIS correctly defaulted to `OPTIONAL` rather than
inheriting strength from its parts, per the skill's explicit rule). Real and
correct, but not decisive enough for A — worth keeping, not a must-fix. An FDE
would plausibly swap the one hand-styled error branch for `Alert`, but the
"every other caller lacks severity treatment" framing overstates urgency since
none of those callers currently need severity.

## Finding 2 — EmojiPicker's Popper+ClickAwayListener+Fade vs. Popover

**Grade: E — factually wrong premise, plus a citation-integrity failure.**

1. Task supported — yes, `EmojiPicker.jsx:3,47-113` confirmed exactly as
   described (Popper, ClickAwayListener, Fade, `timeout={350}`).
2. Authority accuracy — **fails**. The review presents, in quotation marks (i.e.
   claims verbatim), "Popper 'doesn't include built-in transition animations.'"
   Live-fetching `mui.com/material-ui/react-popper.md` shows this sentence does
   not exist on the page and inverts its actual framing: the page states Popper
   **"has built-in support for react-transition-group"** and its own code
   example is `<Popper ... transition>{({TransitionProps}) => (<Fade
   {...TransitionProps} timeout={350}>...` — i.e., the *exact* pattern
   `EmojiPicker.jsx` uses, down to the `timeout={350}` value. "Doesn't include
   built-in transition animations" is not a defensible paraphrase of "has
   built-in support for react-transition-group and ships a worked Fade example
   using this exact structure" — it inverts the point the docs are making.
3. Applicability test — **fails on point 1 (task match) and point 2 (same
   problem)**, because the premise that Popper "lacks" what the current code
   supplies is false for the transition half: the current code is not
   hand-rolling a missing feature, it is reproducing MUI's own canonical Popper
   example almost line-for-line.
4. Task semantics — the alternative itself (`Popover`) is plausible in the
   abstract, but the reasoning for why it's a *needed* substitute is broken.
5. **Equally-valid / documented-reason check — this is where the finding is
   overturned.** For click-away dismissal, the Popper page's own text — "If you
   need this behavior, you can use the Click-Away Listener" — is a direct,
   affirmative instruction to compose `ClickAwayListener` with `Popper`, not a
   deficiency being silently worked around. For the transition, the docs'
   own worked example *is* Popper + Fade via the `transition` render prop,
   matching `EmojiPicker.jsx` structurally. So both "hand-assembled" behaviors
   the finding treats as gaps are in fact the documented, sanctioned way to use
   Popper for exactly this need. That satisfies rubric Q5 squarely against the
   finding.
6. Materiality — moot given the broken premise.
7. Scope — not a leak issue; this is a legitimate component-selection question,
   it's just resolved incorrectly.
8. No duplication.
9. N/A.

The review's own hedge (Popover's scroll-lock makes Popper a defensible choice
inside an already-open Dialog) shows real applicability instinct, but it doesn't
rescue the finding — the core "duplicates behavior Popper explicitly lacks"
framing is false once the actual Popper page and its worked example are read
in full, not just the "clicking away does not hide" sentence in isolation.

---

## Citation-integrity audit (independent of letter grade)

Every VERBATIM-quoted fragment in the review (findings, suppressed list, and
orientation notes) was independently fetched live from `mui.com/material-ui/*`
and checked for copy-paste verifiability.

**Confirmed exact matches:**
- Dialog: "a wrapper for text inside of `<DialogContent />`" — exact.
- Dialog: "Form dialogs allow users to fill out form fields within a dialog." —
  exact (first Orientation-notes quote).
- Alert: "Alerts display brief messages for the user without interrupting their
  use of the app." — exact.
- Alert: "corresponding icon and color combinations" — exact substring.
- Popper: "Clicking away does not hide the Popper component" — exact.
- Popover: "Popover blocks scrolling and dismisses on click-away by default,
  unlike [Popper]" — exact (link text stripped, otherwise verbatim).
- Switch: "a single setting" — exact substring of "toggle the state of a
  single setting on or off," and the page does link an external (non-MUI)
  UX Planet article on Switch vs. Checkbox as claimed.
- Chip: "trigger actions" — exact substring of the documented purpose list.
- Accordion: "show and hide sections of related content" — exact.
- Autocomplete: "a normal text input enhanced by a panel of suggested
  options" — exact (second Orientation-notes quote).
- Select: "collecting user provided information from a list of options" —
  exact.

**Failures found (three fabricated/misquoted VERBATIM fragments, all in
Finding 2 or the Orientation notes):**

1. **Finding 2, Popper:** `"doesn't include built-in transition animations"`
   is not on the page and misrepresents it — see grading above. This is the
   most serious failure: it isn't just imprecise wording, it inverts the
   docs' actual claim and is load-bearing for the finding's central argument.
2. **Finding 2, Popover:** `"constructed on the Modal component"` — actual
   text is "The component is built on top of the Modal component." Close in
   meaning but not copy-paste-verifiable as quoted; should have been
   paraphrased without quotation marks.
3. **Finding 2, Popover:** `"uses the Grow transition by default"` — actual
   text is "Popover uses Grow by default." Again meaning-preserving but not a
   literal quote; presented with quotation marks it shouldn't have had.
4. **Orientation notes, Dialog:** `"TextField components within DialogContent
   and submit functionality via DialogActions buttons"` — this sentence does
   not appear on the Dialog page at all. It is the reviewer's own description
   of the Form-dialogs example's code structure, dressed as a direct quote.
   Not part of a graded finding, but it is a real violation of the skill's own
   rule that "Quotation marks may only be used for VERBATIM mode," and would
   mislead a reader checking the orientation claim against the source.

No SYNTHESIS finding fabricated a sentence outright — findings correctly named
each source's contribution and the inferential bridge — but Finding 2's
synthesis is undermined by fabricated verbatim material inside it (see above),
and its inferential bridge itself turns out to be factually backwards once the
full Popper page (not just the isolated click-away sentence) is read.

**AttachmentBox check (specifically requested):** the "Suppressed" list
item comparing `AttachmentBox`'s icon + editable filename + size + close row
to `Chip`'s avatar/label/delete composition was checked against
`PublishDialog.jsx:822-870` in full. It accurately describes `AttachmentIcon`
(icon), `ExpandingTextField` (editable filename), `formatBytes(file.size)`
(size), and the `DialogIconButton`/`Close` icon (close action) — no Avatar/List
conflation, no quotation marks used, and it is correctly suppressed rather than
reported (the hard blocker — Chip's label isn't documented to support inline
editing — is real and correctly identified as the applicability failure). This
does **not** reproduce the fabricated Avatar/List conflation seen in the prior
evaluation round on the pre-generalization skill.

---

## Suppressed list — spot check

All five suppressed items were checked for citation accuracy (repository
description and any quoted MUI text) and found accurate:

- Priority `Select` vs. `ToggleButtonGroup` — accurate; MUI's own
  "exclusive selection" ToggleButtonGroup example is indeed icon-only
  (alignment buttons), and Select's stated purpose is genuinely
  undifferentiated between the two. Correct suppression under the
  anti-fundamentalism rule (equally-valid alternative, no stated preference).
- `Switch` vs. `Checkbox` — accurate quote and external-link claim (verified
  above). Correctly suppressed for lack of an MUI-owned normative statement
  rather than inflated to an `INFERRED` finding.
- `EmojiDiv` vs. `IconButton` — accurate: IconButton's docs are about
  app-bar/toolbar and single-choice icon toggles, not a dense multi-item
  search grid; correctly routed to "out of scope, a11y implementation" rather
  than forced into a weak component-selection finding.
- Chip-triggered disclosure vs. `Accordion`/`Collapse` — accurate Accordion
  quote; the "targets larger content blocks, not six independently-revealed
  single fields" framing is the reviewer's own unquoted judgment, correctly
  not dressed as a citation.
- `AttachmentBox` vs. `Chip` — see AttachmentBox check above; accurate and
  correctly suppressed.

## Orientation notes — spot check

Three of four orientation claims check out (Dialog "Form dialogs" first
quote, Autocomplete purpose quote, media-query/`fullScreen` claim which is
purely a repository-code observation with no citation needed,
`ReserveTopicSelect`'s Select/MenuItem/ListItemIcon/ListItemText composition
which is an accurate, unremarkable description of `ReserveTopicSelect.jsx`).
The second Dialog "Form dialogs" quote is fabricated — see citation-integrity
failure #4 above.

---

## Summary

| Finding | Grade | Primary driver |
|---|---|---|
| 1. DialogFooter → Alert/DialogContentText | B | Real, correctly-hedged component-selection finding; weakened by a composition-mechanics observation that brushes the implementation-correctness boundary, and by only one of four call sites actually needing what's proposed. |
| 2. EmojiPicker Popper → Popover | **E** | Premise is factually wrong: the "hand-assembled" transition and click-away behavior are the docs' own recommended composition for Popper (worked example matches the code almost exactly), not gaps Popover uniquely fills. Also carries the review's most serious citation-integrity failure. |
| Suppressed items (5) | not formally graded | All accurate on spot-check; no fabrication; AttachmentBox item specifically does not reproduce the prior round's Avatar/List conflation. |
| Orientation notes (4) | not formally graded | One fabricated VERBATIM quote (Dialog "Form dialogs" second fragment); rest accurate. |

**Citation-integrity failures: 4**, all misquotes/fabrications inside
quotation marks (none are wholesale invented facts about the fixture code —
all repository evidence throughout the review is accurate). Three cluster in
Finding 2 and are load-bearing for its (wrong) conclusion; one is in the
Orientation notes and is not load-bearing for any reported finding.
