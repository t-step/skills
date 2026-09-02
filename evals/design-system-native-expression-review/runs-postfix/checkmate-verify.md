# Adversarial verification — Checkmate (Incidents page) design-system review

**Review graded:** `evals/design-system-native-expression-review/runs-postfix/checkmate-skill.md`
**Rubric:** `evals/cloudscape-native-expression-review/rubric.md` (Cloudscape → Material UI)
**Fixture:** `/Users/thomasestep/Developer/mui-eval-fixtures/Checkmate/client/` (real, previously-unscored repo — no expected-answer key; graded against the generic rubric only)

## Method actually followed

Re-read all seven composed fixture files independent of the review's claims
(`index.tsx`, `CardDetails.tsx`, `CardSummary.tsx`, `ControlsIncidentFilter.tsx`,
`DialogIncidentDetails.tsx`, `DialogResolution.tsx`, `IncidentTable.tsx`,
`utils.ts`), plus every repo file the review cites as supporting evidence
(`StatusLabel.tsx`, `StatusCodeLabel.tsx`, `BaseBox.tsx`, `MonitorUtils.ts`,
`HeaderTimeRange.tsx`, `Components/inputs/Select.tsx` + `inputs/index.tsx`,
`ActionsMenu`, `Table.tsx`, `Dialog.tsx`, `package.json`). Live-`curl`'d every
cited `mui.com/…md` page (raw markdown source, not WebFetch's summarizer) and
diffed each VERBATIM-tagged string character-for-character against the fetched
text.

## Citation-integrity table (VERBATIM / directly-quoted claims)

| # | Quoted string in review | Cited page | Live-fetch result |
|---|---|---|---|
| 1 | "Chips are compact elements that represent an input, attribute, or action." | `react-chip.md` | **Exact match**, verbatim, first line of page body. |
| 2 | Chip `color` union `'default' \| 'primary' \| 'secondary' \| 'error' \| 'info' \| 'success' \| 'warning' \| string`, default `'default'` | `react-chip.md` props table | **Exact match** to the live props table row (line 700 of fetched source). `variant: 'filled' \| 'outlined' \| string`, `icon`, `avatar` slots also confirmed present. |
| 3 | "A Toggle Button can be used to group related options." | `react-toggle-button.md` | **Exact match**, verbatim, page intro. |
| 4 | "With exclusive selection, selecting one option deselects any other." | `react-toggle-button.md` | **Exact match**, verbatim, "Exclusive selection" section. |
| 5 | "Select components are used for collecting user provided information from a list of options," | `react-select.md` | **Near-exact** — the source sentence ends with a **period**, not a comma: `"...list of options."` The review spliced its own continuation clause onto the quote using a comma, changing the terminal punctuation of the quoted material. Content and word order are otherwise identical. Minor citation-fidelity defect, not a fabrication or meaning inversion. |
| 6 | "Stack is ideal for one-dimensional layouts, while Grid is preferable when you need both vertical _and_ horizontal arrangement." | `react-stack.md` | **Exact match**, including the markdown italics markers around "and". |
| 7 | "Menus display a list of choices on temporary surfaces." | `react-menu.md` | **Exact match**, verbatim, page intro. |
| 8 | `ListItemText`'s "primary"/"secondary" renders a stacked two-line item, "Photos"/"Jan 9, 2014" demo | `react-list.md` | **Exact match** — the Folder List demo really does render `<ListItemText primary="Photos" secondary="Jan 9, 2014" />` as a stacked two-line item, confirming the review's structural claim (not a left/right two-column layout). |
| 9 | icons.md "explicitly documents `SvgIcon` for custom SVG icons and the `Icon` component wired to third-party icon fonts (its own worked example integrates Font Awesome)" | `icons.md` | **Confirmed** — `### Font Awesome` section exists (fetched lines 452–499) with a full worked `Icon` + Font Awesome CDN example, plus a dedicated `## SvgIcon` section for custom SVGs. |
| 10 | Card: "Cards contain content and actions about a single subject." | `react-card.md` | **Exact match**, verbatim, page intro (used in Suppressed section, not VERBATIM-tagged, but checked anyway). |

No fabricated quotes, no semantic inversions, no misattribution to the wrong page found. One punctuation-splice defect (item 5) — cosmetic, does not change what the cited page says or supports.

## Repository-evidence spot-check (line citations)

Every cited file:line in the review was checked against the actual fixture, not memory:

- `StatusLabel.tsx` — `ValueLabel` really spans lines 72–102 exactly as cited; `getStatusPalette`/`getValuePalette`/`getDockerStatePalette` in `MonitorUtils.ts` really span lines 23–56 exactly as cited, and really return literal `"success"|"error"|"warning"` — MUI theme palette keys, confirmed.
- `ValueLabel`/`StatusCodeLabel` call sites: `CardSummary.tsx:160`, `CardDetails.tsx:68` and `:128`, `IncidentTable.tsx:101` and `:156` — all five confirmed to be exactly what the review says at exactly those lines.
- `ControlsIncidentFilter.tsx`: `resolutionTypes` array at line 9 confirmed; `Select` + 3 `MenuItem`s at lines 57–72 confirmed exactly (opening tag line 57, closing tag line 72).
- `HeaderTimeRange.tsx`: `ToggleButtonGroup`/`ToggleButton` `exclusive` block at lines 39–59 confirmed exactly.
- `client/src/Components/inputs/Select.tsx` really wraps `@mui/material/Select` (confirmed via `inputs/index.tsx`: `export { SelectInput as Select } from "./Select"`, and `Select.tsx` imports `Select from '@mui/material/Select'`).
- `package.json`: `@mui/material: "7.3.7"` exact pin confirmed; `@mui/icons-material` absent from dependencies confirmed; `lucide-react` import confirmed as the actual icon source in `CardSummary.tsx`, `ActionsMenu`, `Table.tsx`.
- Orientation notes all verified against source: `ActionsMenu` really is `IconButton`+`Menu`+`MenuItem`; `Table.tsx`'s `Pagination` really wraps native `TablePagination` via its `ActionsComponent` slot (line 549); `DialogIncidentDetails`/`DialogResolution` really are thin compositions over a `Dialog`/`DialogTitle`/`DialogContent`/`DialogActions` wrapper (`Components/inputs/Dialog.tsx`); `CardSummary.tsx`'s `SummaryIncidentItem` really uses per-breakpoint `Grid` sizing (`size={{ xs: 12, lg: 5 }}` etc., lines 138, 157, 167).

One completeness gap found (does not falsify anything, but the review's own count is an undercount): `IncidentTable.tsx` lines 133–149 render `resolutionType` as a **third, uncataloged** hand-rolled color-coded pattern — a bare `Typography` with `color={theme.palette.warning.main | theme.palette.success.main}` and `textTransform="capitalize"`, doing exactly the "compact color-coded attribute" job Finding 1 is about, at a site the review's evidence list (which claims "five call sites... in this surface alone") never mentions. This doesn't invalidate the finding (the underlying claim — hand-rolled status coloring duplicates Chip's job — is if anything reinforced by a sixth instance), but it means the review slightly undercounts the extent of the problem it identified.

## Per-finding grade table

| # | Finding | Grade | Driving rubric question(s) | Why (A/B) or what failed (D/E) |
|---|---|---|---|---|
| 1 | Hand-rolled status pill (`StatusLabel`/`ValueLabel`/`ColoredLabel`) duplicates `Chip` | **A** | Q1 (repo evidence: exact, all line refs verified), Q2 (Chip page says exactly what's claimed, props table paraphrase exact), Q3 (four-point test passes cleanly: same task, same problem solved, alternative preserves task, materially duplicated 3x+5-6 sites), Q5 (correctly hedges to `INFERRED` not `RECOMMENDED` — no MUI page prohibits hand-rolled pills, honestly stated), Q6 (plausible FDE consolidation target), Q7 (correctly scoped to component selection; explicitly declines to also flag the dot-affordance as a violation) | An FDE maintaining three near-duplicate label components across 5–6 render sites, each re-deriving border/padding/color via `sx`, would plausibly consolidate onto `Chip`'s native `color`/`variant`/`size` API — especially since the repo's own palette functions already emit `Chip`-valid color keys with zero mapping work required. Minor: evidence undercounts one additional call site (`IncidentTable.tsx` resolutionType column) — doesn't change the verdict. |
| 2 | `Select` for `resolutionType` filter vs. sibling `ToggleButtonGroup` for `dateRange` | **B** | Q3 (four-point test passes, but review itself flags this as sitting right at the "same-tier equivalence" boundary), Q5 (explicitly interrogated: could `Select` be equally valid Cloudscape/MUI usage in the abstract? Yes — review says so directly and only escapes suppression via in-surface, not general-doc, evidence), Q6 (materiality self-rated medium, confidence self-rated medium — honest, not inflated) | Real and correctly reasoned SYNTHESIS finding: two structurally identical 3–4-value exclusive filters on the same page use two different native controls, and the repo has already demonstrated its own answer (`ToggleButtonGroup`) one control away. Worth keeping, not a must-fix — matches the review's own stated confidence, so B rather than A. |

Both findings pass all nine rubric questions with no D/E-level failures found. Neither finding leaks into implementation-correctness or generic UX (both explicitly bounded by their own "Boundary check" line, and both boundary claims hold up against the actual code). No cross-level duplication is possible/found — the review correctly notes this corpus has no separate pattern tier, so there is no combined component+pattern duplication to check.

## Suppressed section — soundness check

| Suppressed candidate | Verdict | Basis |
|---|---|---|
| `lucide-react` vs `@mui/icons-material` | **Correctly suppressed.** | Live-fetch of `icons.md` confirms MUI's own docs affirmatively support non-`@mui/icons-material` icon sources (`SvgIcon` for custom SVGs, `Icon` + a documented Font Awesome worked example for third-party fonts). Reporting this as a violation would have been the exact "existence doesn't imply a rule" failure the skill is designed to avoid. No genuine SVG-vs-font preference in the docs applies here either — lucide-react ships SVG components, not a font, so even the one real preference statement on that page ("SVG is preferred... renders faster and better", found at line 578 of the fetched source) doesn't argue against lucide-react. |
| Monitor `Select` → `Autocomplete` | **Correctly suppressed.** | No cardinality evidence (no pagination/count/virtualization on the monitor list) to establish the task premise; naming it without that evidence would be guessing. Reasonable to fully suppress rather than mark `intent-dependent`, since the missing evidence here is about scale, not about which of two designed alternatives is intended. |
| `SummaryCard` (custom `BaseBox`) vs `Card`/`CardContent` | **Correctly suppressed**, arguably could have been named as `intent-dependent`/low-confidence rather than fully dropped, but the low-materiality call is defensible. | `Card`'s doc line ("Cards contain content and actions about a single subject.") verified verbatim; MUI doesn't state a preference against a themed `Box` achieving the same bordered look, and `Card` itself is "little more than a themed `Paper`" — accurately characterized, no overreach. |
| `CardDetails.tsx` 29 `Grid` tags for label/value rows (possible `List`/`ListItemText`) | **Correctly suppressed, and well-reasoned.** | Verified against both cited pages: `Stack`-vs-`Grid` docs really do frame `Grid` as for layouts needing both-axis arrangement (verbatim-confirmed), and the label/value grid really is multi-row-by-2-column, i.e., two-dimensional — so `Grid` is not a mismatch. `List`/`ListItemText`'s `primary`/`secondary` demo really does render as a stacked two-line item, not a left-label/right-value row (verbatim-confirmed against the "Photos"/"Jan 9, 2014" demo) — so it doesn't structurally fit. This is the strongest suppression write-up in the review: it does the actual work of fetching and checking both alternatives rather than asserting equivalence. |

**Explicit check for wrongly-suppressed material findings (genuinely non-equivalent alternatives):** None found. The one place two alternatives are genuinely *not* same-tier equivalent per the docs — `Stack` (1-D) vs `Grid` (2-D) for `CardDetails`' repeated rows — is exactly the case correctly resolved in favor of the *existing* code (Grid is the documented right answer for a 2-D layout), so there was no material finding to report there, and the review didn't invent one. No suppressed item hides a real, task-specific, documented advantage that should have been surfaced as a finding instead.

## Overall verdict

This is a strong, well-earned review for a real (non-pressure-case) fixture. Both reported findings survive adversarial re-verification at grade A and B respectively: repository evidence is precise down to individual line numbers (all independently reconfirmed against the actual files, not trusted from the review's transcription), every VERBATIM-tagged authority quote matches the live `mui.com` page essentially character-for-character (one cosmetic punctuation splice in the Select quote, not a substantive misquote), the four-point applicability test is genuinely applied rather than gestured at, and the review actively resists overreach — hedging Finding 1 to `INFERRED`, self-rating Finding 2 as medium confidence/materiality, and doing real cross-page verification work before suppressing four other candidates rather than suppressing them on vibes. The Suppressed section in particular is unusually rigorous: it fetches and reasons through the alternative pages rather than asserting "no MUI rule forbids this" as a blanket excuse.

Weaknesses found, none rubric-fatal:
1. **Select quote punctuation splice** (period silently became a comma to graft the review's own clause onto it) — cosmetic citation-fidelity nit.
2. **Undercounted evidence for Finding 1** — a sixth hand-rolled color-coded instance (`IncidentTable.tsx:133–149`, resolution-type column) exists and wasn't catalogued, making "five call sites" an undercount. Doesn't change the finding's validity, but the "Why it matters" section's specific tally is not fully exhaustive.

Neither issue moves either finding's grade down a tier; both are noted for completeness per the rubric's evidence-preservation instruction.
