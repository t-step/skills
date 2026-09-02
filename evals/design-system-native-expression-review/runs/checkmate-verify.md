# Adversarial Verification: Checkmate — Incidents page (Material UI)

Reviewed run: `evals/design-system-native-expression-review/runs/checkmate-skill.md`
Rubric: `evals/cloudscape-native-expression-review/rubric.md` (questions applied with "Material UI" substituted for "Cloudscape")
Fixture: `bluewave-labs/Checkmate` @ `d347e29a286873541397fdcc4c79fa24cf0ee248`, Incidents page

No pre-written grading key exists for this fixture — grading is against the rubric's general discipline, not a designed answer key.

## Method

- Read all 7 named fixture files plus the transitively-cited design-elements files (`BaseBox.tsx`, `StatusLabel.tsx`/`ValueLabel`, `StatusCodeLabel.tsx`, `Table.tsx`, `Dialog.tsx`, `Select.tsx`, `actions-menu/index.tsx`, `HeaderTimeRange.tsx`) to check every repository-evidence claim, including exact line numbers.
- Live-fetched every MUI page cited (`react-chip`, `react-card`, `react-select`, `react-tabs`, `react-list`, `react-table`, `react-divider`, `react-dialog`) from `https://mui.com/material-ui/*` and checked every quoted string against the fetched text.
- Confirmed `@mui/material` version (7.3.7, locked) and absence of `@mui/icons-material` directly against `package.json`/`package-lock.json`.

## Finding 1 — `resolutionType` plain text vs. `Chip`

1. **Task supported by evidence?** Yes. `IncidentTable.tsx` lines 95–111 (status/`ValueLabel`), 129–150 (`resolutionType`/`Typography`), 151–162 (`statusCode`/`StatusCodeLabel`) match exactly as cited, down to line numbers.
2. **Does the cited authority say what's claimed?** Yes, verbatim-verified: Chip page states "Chips are compact elements that represent an input, attribute, or action." and "You can use the `color` prop to define a color from theme palette." Both check out on the live page.
3. **Actually applicable (four-point test)?** Passes on shape/problem match (categorical attribute value, same job as neighboring cells) and on preserving current semantics. Weakens on point 4 (materiality of the specific fix) — see below.
4. **Preserves task semantics?** Yes — pure visual/component substitution, same data, same colors.
5. **Could current code be equally valid usage?** Partially, and the review under-explores this. **Repository check**: `ValueLabel` (used for the `status` column) and `StatusCodeLabel` are themselves hand-rolled `BaseBox`-based pills with a status dot (`StatusLabel.tsx` lines 72–101) — **not** MUI `Chip`. So the review's own "why it matters" framing ("two different visual patterns instead of one consistent, documented MUI primitive") somewhat overstates what the proposed fix achieves: swapping `resolutionType` to `Chip` would leave the row with *two* different pill languages (the existing `ValueLabel` dot-pill used twice, plus a new `Chip` used once) rather than one. A more directly-motivated, more material fix sitting in the same file — reuse `ValueLabel` for row-internal visual consistency — is not named or weighed against the `Chip` proposal, even though the review's own repository evidence surfaces it.
6. **Actually material?** Medium, as labeled, but the "why it matters" argument for *why Chip specifically* (vs. the app's own existing pattern) is weaker than presented.
7. **Component/pattern-level, not implementation/UX?** Yes, cleanly in scope — this is a component-choice judgment, not a props/a11y/hierarchy critique.
8. **Improperly split/duplicated?** No, single finding, correctly typed `component selection`.
9. **Intent-dependent handling?** N/A — not applicable here, correctly not over-claimed as `intent-dependent`.

**Grade: B.** The core observation (a categorical value rendered as ad hoc `theme.palette.*.main`-colored `Typography`, in a table that already renders two structurally identical categorical values via a pill component, where MUI ships a purpose-built primitive for exactly this) is real, correctly cited (`OPTIONAL` strength, not oversold), and cleanly scoped. It's not A because the "consistency" argument in "Why it matters" is overstated — it doesn't reconcile with the fact that the row's other two "consistent" cells aren't actually native `Chip` usage either, and the more locally obvious, more material fix (reuse the already-imported `ValueLabel`) is never named or weighed. An FDE reading this file would very plausibly reach for `ValueLabel` first, not fresh `Chip`, which the review doesn't address. Still correct and worth keeping, not a must-fix as framed.

## Finding 2 — Summary panels hand-roll Card's header/content split on `BaseBox`

1. **Task supported by evidence?** Yes. `CardSummary.tsx` line ranges for `SummaryCard` (52–79), `SummaryCardActiveIncidents` (85–124), `SummaryCardLatestIncidents` (183–200), `SummaryCardStats` (206–236) all check out exactly. `BaseBox.tsx` (4–18) confirmed as a plain styled `Box` (background/border/radius tokens), no Card semantics.
2. **Does the cited authority say what's claimed?** Yes, verbatim-verified against the live Card page: "Cards contain content and actions about a single subject.", Card = "a surface-level container for grouping related components.", CardHeader = "an optional wrapper for the Card header.", CardContent = "the wrapper for the Card content." All four check out exactly.
3. **Actually applicable?** Reasonably — each panel is a titled, single-topic, bounded surface, a real (not superficial) match to Card's stated purpose. The review is honest that point 4 (materiality) is the weak leg: it explicitly concedes `BaseBox` already visually approximates an outlined Card, so the visible cost today is low.
4. **Preserves task semantics?** Yes, pure component substitution — same three-panel layout, same content.
5. **Could current code be equally valid usage?** The review names a real, plausible counter-reason itself: `BaseBox` is a deliberately reused, generic bordered-surface primitive used elsewhere for non-Card-shaped jobs too (confirmed — it's also used in `CardDetails.tsx` for record-detail sections that don't have the same title/content split shape). This is a legitimate architectural reason the team might prefer one generic primitive over introducing `Card` in some but not all of its uses, and the review's `Authority strength: INFERRED` (rather than RECOMMENDED/REQUIRED) reflects that honestly.
6. **Actually material?** Medium as labeled, correctly hedged — the review does not oversell this as a must-fix; it explicitly frames the primary cost as theme-customization/maintenance (auto-inheriting `MuiCard`/`MuiCardHeader` overrides) rather than a visible defect.
7. **Component/pattern-level, not implementation/UX?** Yes — clean scope, explicitly not about the `eyebrow` typography variant, styling, or the responsive `Stack`.
8. **Improperly split?** No — correctly typed `combined selection + composition` since the recommendation is genuinely both "use Card" and "use CardHeader/CardContent inside it," which is one underlying recommendation, not two.
9. **Intent-dependent?** N/A, correctly not invoked.

**Grade: B.** Well-calibrated, honestly hedged (`INFERRED` strength, `medium` materiality, self-identified low visible cost), correctly scoped, and the applicability reasoning survives scrutiny — this is a legitimate "valid usage today, but the design system's own vocabulary more natively expresses this" finding, not a fundamentalism violation. It stays at B rather than A because the review's own admission that the visible cost is low and the win is mostly a latent theming/consistency argument makes this the textbook "non-decisive, worth keeping, not a must-fix" case the rubric describes for B.

## Suppressed candidates — spot-checked

- **Select vs. Autocomplete (monitor filter).** Correct suppression. WebFetch of the Select page confirms the routing language ("more advanced features, like combobox, multiselect, autocomplete, async or creatable support... head to the Autocomplete component") is real and verbatim, but the review is right that this bounded surface gives no evidence of monitor-count scale, so applicability can't be established — good discipline, not a missed finding.
- **Active/Resolved tables vs. `Tabs`.** Correct suppression. WebFetch confirms Tabs' documented purpose is for content "related and at the same level of hierarchy" — active vs. resolved incidents plausibly differ in operational priority, so collapsing them behind a tab click would be a product-redesign risk, correctly avoided per the scope boundary.
- **`CardDetails.tsx` label/value rows vs. `List`/`Table`.** Correct suppression. WebFetch confirms List's docs describe homogeneous item lists (mail folders, contact-style rows) and Table's stated purpose is "sets of data" (implying multiple records) — neither matches a single record's heterogeneous field/value panel. This is the anti-fundamentalism rule working correctly, not a missed opportunity — MUI has no purpose-built "detail panel" component to recommend instead.
- **Extending Finding 1's Chip fix to `ValueLabel`/`StatusCodeLabel` themselves.** Correct scope call — those wrappers are reused app-wide, outside this bounded surface.

## Orientation notes — spot-checked

All five affirmative claims were checked against source and hold up: `Table.tsx` genuinely composes MUI `Table`/`TableContainer`/`TableHead`/`TableBody`/`TableRow`/`TableCell` directly and extends `TablePagination` via its documented `ActionsComponent` prop (confirmed in `Table.tsx` lines 548–558); the 3-item resolution-type `Select` matches Select's own stated purpose (WebFetch-verified quote: "collecting user provided information from a list of options"); `Dialog`/`DialogTitle`/`DialogContent`/`DialogActions` composition and the Confirmation+Form dialog blend in `DialogResolution.tsx` is accurate and both quoted patterns check out verbatim on the live Dialog page; `ActionsMenu` (`actions-menu/index.tsx`) is a plain `IconButton` + anchored `Menu` + `MenuItem` list; `HeaderTimeRange.tsx` is a 4-option `ToggleButtonGroup` with `exclusive`; the `Divider` claim (index.tsx line 208, quote "a thin, unobtrusive line for grouping elements to reinforce visual hierarchy") is verbatim-verified.

## Citation integrity (independent of grade)

**No fabrications found.** Every `VERBATIM`-flagged or quotation-marked string in the report — across both findings, the Suppressed section, and Orientation notes — was independently fetched live from `https://mui.com/material-ui/*` (Chip, Card, Select, Tabs, List, Table, Divider, Dialog) and is copy-paste-verifiable against the current page text. No conflated, misattributed, or invented quotes were found — this run does not reproduce the prior round's Avatar/List-style fabrication.

Two minor, non-fabricating format notes:
- Neither finding uses `SYNTHESIS` mode at all — both stay at single-source `VERBATIM`/`PARAPHRASE`, which is the more conservative (and, per the skill's own lineage notes, historically safer) choice; there is nothing to scrutinize under the SKILL.md SYNTHESIS rule here.
- Both findings split the `Evidence mode` field into two components ("VERBATIM for X; PARAPHRASE for Y") rather than picking exactly one value as the Finding Contract specifies ("Evidence mode — exactly one of..."). This is a small contract-format deviation, but it errs toward more transparency, not less, and does not misrepresent anything — quoted text really is verbatim, and the applicability leap really is the reviewer's own reasoning. Not a citation-integrity failure, worth noting for skill-authoring feedback only.
- Finding 2 places quotation marks around three phrases ("a surface-level container for grouping related components", "an optional wrapper for the Card header", "the wrapper for the Card content") without an explicit per-phrase `VERBATIM` tag, under an overall `PARAPHRASE` evidence-mode label. All three are independently confirmed as literal page text, so this is not a fabrication, but it's a stricter-reading violation of "quotation marks may only be used for VERBATIM" that a tighter run would avoid by either tagging them VERBATIM individually or dropping the quotation marks.

## Summary table

| Finding | Type | Grade | Primary driver |
|---|---|---|---|
| 1: resolutionType text vs. Chip | component selection | B | Real, correctly cited, `OPTIONAL`-strength; "why it matters" consistency claim overstated since neighboring cells aren't native `Chip` either, and the more locally obvious fix (reuse `ValueLabel`) is unaddressed |
| 2: Summary panels vs. Card | combined selection + composition | B | Real, correctly cited, honestly hedged (`INFERRED` strength, medium materiality, admits low visible cost); non-decisive by its own framing |

Citation integrity: **clean** — no fabricated, conflated, or misattributed VERBATIM quotes across the whole report; no SYNTHESIS claims to scrutinize.
