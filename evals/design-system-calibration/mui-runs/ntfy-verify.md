# Adversarial Verification: ntfy MUI Component-Fit Review (baseline vs. skill-assisted)

Verifier method: read both reviews in full, read all six fixture files
directly (`SubscribeDialog.jsx`, `PublishDialog.jsx`,
`ReserveTopicSelect.jsx`, `DialogFooter.jsx`, `AttachmentIcon.jsx`,
`EmojiPicker.jsx`), re-fetched every MUI doc URL cited in either review via
its `.md` endpoint, and independently read the code for the two
baseline-only findings the skill run did not report. Grades follow
`evals/cloudscape-native-expression-review/rubric.md` with "Material UI"
substituted for "Cloudscape."

---

## Part 1 — Citation audit (every MUI URL cited in either review)

| URL | Cited by | Verdict |
|---|---|---|
| `react-progress.md` (determinate/value, "Uploading photos" caption) | baseline F1 | **Accurate.** Quotes match verbatim; caption confirmed. |
| `react-popover.md` (purpose, blocks-scroll/dismiss-on-click-away vs Popper, Grow default, elevation) | baseline F2, skill F2 | **Accurate**, both reviews. Minor imprecision in baseline ("the docs example uses elevation={8}" — this is actually the documented *default* prop value, not merely an example choice); trivial, doesn't affect the finding. |
| `react-text-field.md` (InputAdornment purpose, password-toggle worked example) | baseline F3 | **Accurate.** Quote and worked example both verified verbatim. |
| `react-toggle-button.md` (group related options, exclusive selection) | baseline F4 | **Accurate.** Confirmed no comparative Select-vs-ToggleButtonGroup guidance exists on the page — baseline explicitly and correctly says this itself. |
| `react-select.md` ("interchangeable with a native `<select>`") | baseline F4 | **Accurate.** |
| `react-backdrop.md` (narrows focus, dimmed layer, state-change use cases) | baseline F5 | **Accurate**, all three quotes verbatim. |
| `react-checkbox.md` (single-option → switch, not checkbox) | baseline orientation note | **Accurate.** |
| `react-avatar.md` (icon-avatar wrapping a file-type icon, captioned "Q4 budget spreadsheet, last edited by Remy Sharp") | **skill F1** | **FABRICATED / CONFLATED.** The page has two *separate* examples: (1) an "Icon avatars" section with `<Avatar><FolderIcon/></Avatar>` — a generic folder icon, no caption, no file-type variation; (2) a "With badge" section where `InsertDriveFileIcon` (captioned "Q4 budget spreadsheet, last edited by Remy Sharp") is used **standalone, explicitly not wrapped in Avatar** — the Avatar in that example is a small profile-picture badge overlay indicating *who* edited the file, not a container for the file icon. The finding's central sentence merges these two into an example that does not exist on the page. |
| `react-list.md` ("Avatar with text and icon" example; "separate target" quote) | skill F1 | **Partially accurate, partially misattributed.** The `ListItemAvatar`+`Avatar(icon)`+`ListItemText`+`secondaryAction` delete-`IconButton` example is real and accurately described. But the "separate target" quote is lifted from a *different* example (`CheckboxListSecondary`, describing a checkbox as the secondary action) and re-attached in the finding as if it characterizes the delete-icon example. The words are real; the attribution is not. |
| `react-popper.md` (purpose, click-away not built in, render-prop transition) | skill F2 | **Accurate**, all quotes verbatim. |
| `react-progress.md` ("the Linear variant's own examples are built around 'file uploads, buffered loading, and contextual progress display'") | **skill F3** | **FABRICATED.** Confirmed by direct re-fetch: this phrase does not appear anywhere on the page, in any section. The rest of skill F3's citation (determinate/value, "displayed alongside the progress bar") is accurate — only this one clause is invented. |
| `react-chip.md` (trigger actions) | skill, suppressed candidate | **Accurate.** "Chips allow users to enter information, make selections, filter content, or trigger actions" confirmed verbatim. |
| `react-stepper.md` (numbered/wizard progress) | skill, suppressed candidate | **Accurate.** "Steppers convey progress through numbered steps. It provides a wizard-like workflow" confirmed. |

**Headline finding:** baseline's citations are clean across all seven URLs — zero fabrications, one trivial imprecision. The skill-assisted review, despite a formal procedure with explicit "Authority strength" labeling meant to guard against exactly this, contains **two real citation defects**: a fabricated quote (F3) and a fabricated/conflated worked example that is the load-bearing evidence for its highest-materiality finding (F1). This is the opposite of what the skill's structure is supposed to buy.

Repository-evidence (code line citations) in both reviews checked out against the actual files with no discrepancies worth noting — both reviews are reliable on "what the code does," the divergence is entirely in "what the docs say."

---

## Part 2 — Per-finding grades (skill-assisted review)

### Finding 1 — AttachmentBox → Avatar/List — **Grade: E**

1. Task evidence: supported, accurate.
2. Cited authority says what's claimed: **no**, for the Avatar half — see citation audit above. The List half is accurate but only supports a narrower, less distinctive claim (a generic icon+text+delete-button list item shape, not specifically a "file item with caption" shape).
3. Four-point applicability test: weakened by (1); further weakened because the proposed native expression asks `ListItemText`'s `primary` slot to host an *editable* `TextField` (`ExpandingTextField`) — no cited example anywhere shows an editable control inside `ListItemText`. The finding asserts "no behavior change" but doesn't establish this compositional mechanism is actually supported.
4. Task-semantics preservation: asserted, not demonstrated by any citation.
5. Could current code be equally valid MUI usage: plausible — nothing in the accurately-cited material forbids a hand-built row.
6. Materiality: labeled "high" in the review, but that label leans on the fabricated evidence; without it the finding drops toward "medium" at best.
7. Boundary: correctly framed as component/pattern, not implementation — fine on this axis.
8. Combined type: appropriately used.

Because the fabricated Avatar example is explicitly invoked as the primary supporting citation for a "high materiality / medium-high confidence" finding, this fails Q2 in a way that's disqualifying under the rubric's E criterion ("the cited authority doesn't say what's claimed"). This is the review's most confidently-stated finding and its evidentiary base doesn't hold up on direct re-fetch.

### Finding 2 — EmojiPicker: Popper/ClickAwayListener/Fade → Popover — **Grade: A**

1. Task evidence: accurate, precise line citations.
2. Citations: both `react-popper.md` and `react-popover.md` quotes verified verbatim.
3. Four-point test: passes cleanly — task match is exact (anchored panel, dismiss-on-click-away, transition), current code literally reassembles the three things Popover bundles.
4. Preserves task semantics: yes.
5. Equally valid current usage: the review itself surfaces the one genuine counter-consideration (Popover's default scroll-blocking inside an already-modal `Dialog`) and appropriately keeps confidence at "medium" rather than "high" instead of glossing over it — this is exactly the calibration discipline the rubric rewards.
6. Materiality: real — duplicated logic (350ms `Fade` timeout, hand-wired `ClickAwayListener`) with drift risk, correctly labeled "medium."
7. Boundary check: correctly scoped to component selection, not implementation.

This is the strongest finding in either review: accurate, well-hedged, and an FDE would plausibly act on it (or at minimum flag the scroll-block tradeoff before deciding). Matches baseline's independently-produced Finding 2 almost exactly, which is itself corroborating evidence.

### Finding 3 — Upload progress text-only vs LinearProgress — **Grade: D**

1. Task evidence: accurate, correct line citations in both `PublishDialog.jsx` and `DialogFooter.jsx`.
2. Citations: the core citation (determinate/value prop, "displayed alongside the progress bar") is accurate; **one supporting clause is fabricated** ("file uploads, buffered loading, and contextual progress display" does not appear on the page in any form).
3. Four-point test: reasonably argued independent of the fabricated clause — the code already computes the exact `value` a determinate bar needs and discards it into a string.
4. Preserves task semantics: yes — proposed as additive (pair bar + existing text), not a replacement, which is a better-calibrated recommendation than simply asserting text is wrong.
5. Equally valid current usage: the review itself acknowledges text-only is valid and accessible, appropriately keeping materiality at "medium" rather than "high" — good discipline.
6. Materiality: reasonable as stated.

Downgraded from what would otherwise be a solid B because a supporting quote is invented. It's a smaller defect than Finding 1's (the finding survives without it), but it's still exactly the kind of thing this adversarial pass exists to catch, and it's disqualifying enough to keep this out of A/B territory. Notably, baseline's parallel finding on the identical issue (its Finding 1) uses only real, verified quotes (the "Uploading photos" caption) and would grade higher on citation grounds alone.

### Suppressed candidate — Chip-triggered field reveal — **Grade: A (correct suppression)**
`react-chip.md` genuinely lists "trigger actions" as a documented use case; suppression is accurate and well-reasoned, not merely asserted.

### Suppressed candidate — ExpandingTextField (no MUI analog) — **Grade: B (reasonable suppression)**
A negative claim ("no MUI component targets this") is harder to independently falsify with certainty, but nothing in the retrieved corpus contradicts it, and the anti-fundamentalism framing is applied correctly.

### Suppressed candidate — SubscribeDialog page-swap vs Stepper — **Grade: A (correct suppression)**
Confirmed via `react-stepper.md`: Stepper's documented purpose is "numbered steps"/"wizard-like workflow" for a known sequence, not a conditional two-screen auth branch. Correct, well-reasoned non-finding.

---

## Part 3 — The recall-gap question

### (a) `ClosableRow`/`DialogIconButton` reimplementing `InputAdornment` — **meaningful recall gap, not defensible non-coverage**

Read against the actual code: `ClosableRow` (PublishDialog.jsx:791–803) plus `DialogIconButton` (805–820, with hand-tuned `height: "45px"` / `marginTop: "17px"` to visually align an externally-flexed `IconButton` against a standard-variant `TextField`) is used at five call sites — the topic/server override row, Click URL, E-mail, Attach URL+filename, and Delay — plus an equivalent pattern in `SubscribeDialog.jsx`'s "generate topic name" button row. `EmojiPicker.jsx`, a file the skill run *directly cited* for its own Finding 2, contains the correct version of the identical UI need one function away (lines 79–88: `slotProps.input.endAdornment` → `InputAdornment position="end"` → `IconButton`).

Checked against the skill's own four-point applicability test: (1) task match is exact — "field + inline clear/dismiss action" is `InputAdornment`'s stated purpose verbatim; (2) the current code solves the identical problem; (3) the substitution preserves the task with zero semantic change; (4) materiality is about as strong as this kind of finding gets, because the evidence isn't "the docs show another way" (the anti-fundamentalism trap) — it's "the same codebase, one file away, already does it correctly," which is the single most compelling category of evidence this skill's materiality bar is built to reward. This finding would grade **A** by the same rubric applied above to Finding 2, and arguably has stronger evidence (a same-repo contradiction) than any finding the skill run actually reported.

The skill run had every input needed to find this — it reviewed `PublishDialog.jsx` closely enough to cite `progressFn` at exact line numbers, and reviewed `EmojiPicker.jsx` closely enough to quote its `InputAdornment` usage almost (lines 74–89) for a different purpose. It walked past the contrast without connecting the two. This reads as a genuine recall gap in the run, not a case where the skill's discipline correctly filtered out a weak candidate.

### (b) `ToggleButtonGroup` for the 5-option priority / 4-option reservation-access pickers — **defensible non-coverage, not a meaningful gap**

Baseline's own Finding 4 is unusually candid about the weakness of its own claim: "the MUI docs do not explicitly say 'prefer ToggleButtonGroup over Select for small sets' — that comparison isn't made on either page." Independent re-fetch confirms this: `react-toggle-button.md` documents what ToggleButtonGroup *is* (a container for exclusive, related options) but makes no statement comparing it to `Select`, and `react-select.md` states Select is "meant to be interchangeable with a native `<select>` element" with no stated size/count ceiling — the only escalation path the docs name is to `Autocomplete` for combobox/multiselect/async needs, not to `ToggleButtonGroup` for small counts. `ReserveTopicSelect.jsx`'s `Select`+`MenuItem`+`ListItemIcon`+`ListItemText` composition is, in fact, exactly the pattern the skill run separately confirmed as "standard MUI Select composition" in its own orientation notes for the very same file.

Run through the rubric's four-point test, this candidate fails point 1 in the same way the anti-fundamentalism rule is designed to catch: "MUI ships ToggleButtonGroup for related exclusive options, and this is a set of related exclusive options" is existence-as-mandate reasoning, not an established applicability gap — there's no documented tension the current `Select` usage collides with. This is a **C-grade candidate** ("technically plausible but routine/low-value... expected to be suppressed by the skill's own materiality discipline, not a verifier failure") were it run through the skill's own procedure. Its absence from the skill run's findings and suppressed list looks like correct triage, not a miss.

### Was skill Finding 1 (AttachmentBox) genuinely stronger than what baseline produced, or overreach?

**Overreach**, and by a clearer margin than its "high materiality / medium-high confidence" labels suggest. Baseline never attempted this finding at all, so there's no direct baseline counterpart to compare it to — but measured against baseline's other findings (all of which check out on re-fetch) and against the skill run's own Finding 2 (which is well-hedged and citation-accurate), Finding 1 is the outlier: it's the one place either review states a specific worked example exists on a specific page, and that example turns out not to exist as described. The underlying intuition — a hand-built icon+editable-text+metadata+remove-action row resembles a list-item shape — has some genuine merit from the real `react-list.md` example, but the review oversells it by (a) inventing corroborating evidence on the Avatar page and (b) never confronting that its proposed replacement asks an undemonstrated MUI mechanism (an editable field inside `ListItemText`) to do something none of the cited docs show it doing.

---

## Summary verdict

- Skill F2 (Popper→Popover): **A** — cleanly validated, matches baseline's independent finding of the same issue.
- Skill F3 (upload progress): **D** — real underlying finding, undermined by one fabricated supporting quote; baseline's citation-clean version of the same finding is more trustworthy.
- Skill F1 (AttachmentBox→Avatar/List): **E** — its central supporting citation is fabricated/conflated; the proposed replacement mechanism is never actually demonstrated in the docs it cites.
- Suppressed candidates (Chip, ExpandingTextField, Stepper): **A / B / A** — all three are correct, well-reasoned non-findings.
- Recall gap (a), InputAdornment: **meaningful miss** — the skill run had the contradicting evidence in hand and didn't connect it; would have graded A had it been reported.
- Recall gap (b), ToggleButtonGroup: **defensible non-coverage** — correctly filtered by the same materiality discipline the skill is designed to apply; baseline's own hedging concedes this.
