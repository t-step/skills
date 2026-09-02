# MUI generalization round — experiment results

**Run date:** 2026-09-02. **Model:** claude-sonnet-5, fresh `general-purpose`
subagent per run (no fork, no shared context) — 3 baseline + 3 skill-assisted
+ 3 adversarial-verifier runs across three real, independently-selected,
pinned-commit Material UI open-source fixtures. Full raw transcripts are
local, untracked artifacts; `mui-runs/*.md` (`{fixture}-baseline.md` /
`{fixture}-skill.md` / `{fixture}-verify.md`) are the committed, auditable
record every claim below cites.

**Question under test:** does `cloudscape-native-expression-review`'s
reasoning *operation* — combined component-selection + pattern-composition
judgment, an anti-fundamentalism rule against existence-as-mandate
reasoning, an explicit implementation-correctness/general-UX scope fence,
and a "missing intent → don't guess" escape hatch — remain useful and
well-calibrated when pointed at Material UI, whose authoritative corpus has
no Cloudscape-style task/pattern layer? Per the task brief, a lower finding
rate is a valid, even expected, correct result; the target of this
evaluation is calibration and reasoning-shape, not finding count parity
with the Cloudscape round.

## 1. Frozen skill revision and fixture SHAs

- **Skill:** `skills/cloudscape-native-expression-review/SKILL.md`, content
  unchanged since commit `2745d97` (confirmed: `git diff ed03faf HEAD --
  SKILL.md` is empty). Not edited at any point in this round, before or
  after seeing any run's output, per this repo's freeze discipline.
- **Repo HEAD for this round:** `98cdffc` (the infrastructure-only
  correction below; no other repo changes were made before or during
  evaluation).
- **Fixtures** (all reconfirmed via `git rev-parse HEAD` against the local
  clones before this round's runs):

  | Fixture | Repo | SHA | Selected surface |
  |---|---|---|---|
  | Checkmate | `bluewave-labs/Checkmate` | `d347e29a286873541397fdcc4c79fa24cf0ee248` | `client/src/Pages/Incidents/` (index + 6 components + utils) |
  | ntfy | `binwiederhier/ntfy` | `10cb6506f836dbb00bb77e3b52669f6ace37f555` | `web/src/components/{Subscribe,Publish}Dialog.jsx` + 4 composed files |
  | hk-independent-bus-eta | `hkbus/hk-independent-bus-eta` | `cb5b1fcbed5f9f7cb14635ee29507084b9de2578` | `src/pages/RouteEtaPage.tsx` + 2 sibling pages + 4 `route-eta/` components |

- **Authority:** `evals/design-system-calibration/authority/mui-material-llms.txt`
  (fetched 2026-09-02, ETag `"d1e6e8e4e3010e2efcaa56ecceddeb20-ssl"`),
  strictly a discovery index — every citation below was independently
  re-fetched from its live `https://mui.com/material-ui/*.md` page by a
  separate verifier agent, not trusted from the reviewing agent's quotation.
- **MUI X boundary independently reconfirmed:** grepped all three selected
  surfaces for `@mui/x-*` / `@mui/lab` imports before launching any review.
  Zero hits in any of the three — all imports are `@mui/material` and
  `@mui/icons-material` only, even though Checkmate declares `@mui/lab`/
  `@mui/x-charts`/`@mui/x-date-pickers` and hk-independent-bus-eta declares
  `@mui/x-date-pickers` elsewhere in their respective repos. Both
  skill-assisted runs independently re-confirmed this for their own
  fixture rather than trusting the setup task's prior claim.

## 2. Infrastructure-only correction made before the freeze

`skills/cloudscape-native-expression-review/scripts/resolve_versions.py`
previously read only npm's `package-lock.json` and failed safe
(`"resolved": false`) on yarn-lockfile projects — a real gap exercised for
the first time by hk-independent-bus-eta (yarn, no `package-lock.json`
anywhere in the tree). Fixed with the smallest change that closes it: the
script now also looks for `yarn.lock` and, when found, matches the exact
declared `name@range` key against yarn v1 lockfile blocks to read the
resolved `version` — no semver reasoning, same "facts only, fail safe"
discipline as the npm path.

- Commit: `98cdffc` — `fix(resolve_versions): add yarn.lock support, closing MUI-round confound`.
- Verified: `hk-independent-bus-eta` now resolves `@mui/material` declared
  `^5.15.11` → locked `5.15.11`, `"resolved": true` (previously
  `null`/`false`), matching the value only obtainable before via manual
  `yarn.lock` inspection.
- Regression-tested unchanged against both npm MUI fixtures (Checkmate,
  ntfy) and both original Cloudscape npm/no-lockfile fixtures — identical
  output to before the change in every case.
- `bash scripts/check.sh` passes (strict skill-frontmatter lint,
  eval-isolation check, cross-skill dependency validation).
- No skill wording, retrieval priority, or evaluation semantics changed.
  `SKILL.md` itself was not touched by this commit.

## 3–4. Per-fixture baseline and skill-assisted results

### Checkmate — Incidents collection/management page

**Baseline** (5 findings, unguided, same question framing, no skill):
Grid-as-key/value-table in `CardDetails.tsx` (→ `Table`/`List`); colored
`Typography` for `resolutionType` where the adjacent `status` column
already uses a chip-like element (→ `Chip`); hand-rolled icon+color+message
severity indicator for the active-incidents count (→ `Alert`); hand-built
icon+label+value summary rows (→ `List`, self-hedged as weak); `Select` for
a fixed 3-value filter (→ `ToggleButtonGroup`, self-hedged as unproven).
One fabricated quote (a `react-list.md` sentence that doesn't exist), not
load-bearing to the finding it sits in.

**Skill-assisted** (1 reported finding): Chip vs. hand-rolled `ValueLabel`/
colored-`Typography` for the status/resolutionType attribute display,
typed `component selection`, self-rated high/high. Three candidates
explicitly considered and suppressed (Select-vs-Autocomplete for the
monitor filter, `BaseBox`-as-`Card`, Grid-vs-List key/value layout) with
stated reasoning for each. Independently reconfirmed `@mui/icons-material`
unused (icons come from `lucide-react`) and `@mui/lab` absent from the
bounded surface — correctly named as out of this round's authority
boundary rather than cited or silently ignored.

### ntfy — Subscribe/Publish dialog workflow surface

**Baseline** (5 findings): upload-progress rendered as text where the code
already computes the exact percentage `LinearProgress` needs; `EmojiPicker`
hand-assembling `Popper`+`ClickAwayListener`+`Fade` instead of `Popover`;
`ClosableRow`/`DialogIconButton` reimplementing `InputAdornment` at five
call sites, while `EmojiPicker.jsx` in the same codebase already uses
`InputAdornment` correctly; `Select` for two small icon-labeled option sets
(→ `ToggleButtonGroup`, self-hedged as unproven); a hand-built full-viewport
drag-overlay (→ `Backdrop`). Zero fabricated citations across seven
independently re-fetched URLs.

**Skill-assisted** (3 reported findings): `EmojiPicker`'s
`Popper`+`ClickAwayListener`+`Fade` vs. `Popover` (matches baseline
independently); upload progress text-only vs. `LinearProgress`; and
`AttachmentBox`'s hand-composed file-row vs. `Avatar`/`ListItemAvatar`/
`ListItemText`/`secondaryAction` (typed `combined component + pattern`,
built from two component pages' worked examples in the explicit absence of
a pattern-tier page — see §9). Three candidates correctly suppressed
(Chip-as-trigger, an auto-width text field with no MUI analog, a
login-page swap wrongly resembling `Stepper`).

### hk-independent-bus-eta — route → stop-ETA → stop-detail flow

**Baseline** (3 findings): `RouteUpdateNotice.tsx`'s clickable `Box` vs.
`Alert`; `StopDialog.tsx`'s manual `sx`/`MuiPaper-root` override vs.
`Dialog`'s documented `fullScreen` prop; `RouteHeader.tsx`'s `Paper`+flex
composition vs. `AppBar`/`Toolbar`, asserted unhedged. Zero fabricated
citations across six independently re-fetched URLs. Missed that
`BookmarkedStopPage.tsx` (in its own reviewed set) renders
`DbRenewReminder.tsx`, a near-verbatim duplicate of the exact `Box`
anti-pattern its own Finding 1 names, and mischaracterized that page as
"plain scaffolding."

**Skill-assisted** (2 reported findings, both eventually A-graded — see
§5): the identical `RouteUpdateNotice.tsx` → `Alert` finding, typed
`component selection`; and the `RouteHeader.tsx` → `AppBar` question,
correctly typed `intent-dependent` rather than asserted, naming the
missing resolving fact ("does a global `AppBar` already exist elsewhere in
the app shell") instead of guessing. The `Dialog`/`fullScreen` observation
was explicitly named and then deliberately excluded as
implementation-correctness ("Dialog is already the right component here")
— the sharpest scope-discipline result in this round; see §5.

## 5. Every retained finding, authority, and grade

Grades are from an independent adversarial verifier per fixture — a fresh
subagent, not the reviewer, that re-fetched every cited MUI page directly
and re-read the actual fixture code, following
`evals/cloudscape-native-expression-review/rubric.md`'s nine verification
questions with "Material UI" substituted for "Cloudscape." No case-specific
grading key exists for any of these three (all real, unmodified fixtures);
grading is against the rubric's general discipline, the same basis the
original Cloudscape round used for its own real fixture.

| # | Fixture | Finding | Type | Authority (RECOMMENDED unless noted) | Grade | Why |
|---|---|---|---|---|---|---|
| 1 | Checkmate | Chip vs. hand-rolled `ValueLabel`/colored-`Typography` | component selection | `react-chip.md` purpose statement (genuine) + a fabricated supporting quote on the `color` prop | **B** | Real core observation, passes the four-point applicability test, but overstates confidence: misses a third inconsistent treatment baseline caught in the same bounded files, never reconciles with its own sibling suppression logic (an app-wide shared-component argument it used to suppress `BaseBox`→`Card` but not against itself), and rests partly on a fabricated quote |
| 2 | ntfy | `EmojiPicker` Popper+ClickAwayListener+Fade vs. `Popover` | component selection | `react-popper.md` + `react-popover.md`, both fully verified verbatim | **A** | Strongest finding in the whole round: exact task match, current code literally reassembles what Popover bundles, self-hedges the one genuine counter-consideration (scroll-blocking) rather than overclaiming, independently corroborated by baseline's parallel finding |
| 3 | ntfy | Upload progress text-only vs. `LinearProgress` | component selection | `react-progress.md`, core citation genuine, one supporting clause fabricated | **D** | Real underlying idea (the exact percentage is already computed and discarded into a string) undermined by an invented supporting quote; baseline's citation-clean version of the identical finding is more trustworthy |
| 4 | ntfy | `AttachmentBox` vs. `Avatar`/`ListItemAvatar`/`ListItemText`/`secondaryAction` | combined component + pattern | `react-avatar.md` + `react-list.md`, cited as "worked examples" in the explicit absence of a pattern page | **E** | The central supporting citation is fabricated/conflated — merges two real but separate Avatar-page examples into one that doesn't exist; the proposed replacement also asks an undemonstrated mechanism (an editable field inside `ListItemText`) to do something no cited doc shows working |
| 5 | hk-bus-eta | `RouteUpdateNotice.tsx`'s clickable `Box` vs. `Alert` | component selection | `react-alert.md` + `react-snackbar.md` (contrast), fully verified verbatim | **A** | Repository evidence, citation, and applicability all hold; independently corroborated by a second, unused-by-either-review instance of the identical anti-pattern in `DbRenewReminder.tsx` outside the bounded surface |
| 6 | hk-bus-eta | `RouteHeader.tsx` vs. `AppBar`/`Toolbar` | intent-dependent | `react-app-bar.md`, fully verified verbatim | **A** (on rubric Q9: was declining to guess the right call) | Named both plausible readings and the exact resolving fact; independent investigation beyond the bounded surface confirmed the app *does* have a persistent global `Header`/`Toolbar` (invisible from the 8 reviewed files, not reachable by import), substantively vindicating the hedge rather than merely excusing it procedurally |

**Grade tally (6 skill-assisted findings across 3 fixtures):** A × 3
(including the intent-dependent Q9-correct call), B × 1, D × 1, E × 1.
Every A-grade finding was independently corroborated by evidence outside
what either review itself surfaced (a same-app duplicate anti-pattern, an
out-of-surface global-chrome check). Both sub-A findings (D, E) trace to
the identical root cause: a fabricated or conflated supporting quote, not
a wrong underlying judgment.

Baseline findings were **not** exhaustively A–E graded in this round (13
baseline findings across three fixtures vs. this round's narrower 6-finding
skill-assisted total); verifiers graded baseline findings only where
directly load-bearing to an adjudication (hk-bus-eta's two baseline
findings, both scored "would be D under this rubric" — see §6) or as a
citation-accuracy cross-check. This is a real scope reduction from the
original Cloudscape round (which graded all 26 baseline findings) made for
cost reasons; treat any claim about baseline's overall grade distribution
as unverified in this round, unlike the skill run's.

## 6. Deliberately suppressed candidates, and why

All nine suppressions/clearances across the three skill runs were
independently re-verified as correct or defensible — no case of a
verifier reinstating a wrongly-suppressed finding:

- **Checkmate:** `Select`-vs-`Autocomplete` for the monitor filter (no
  documented option-count threshold, no evidence the list is large —
  correctly suppressed); `BaseBox`-as-`Card` (no documented "don't use
  Box, use Card" pairing, and `BaseBox` is an established, app-wide
  convention — correctly suppressed, though the verifier notes this same
  reasoning should also have tempered Finding 1's confidence and didn't);
  `CardDetails.tsx`'s Grid key/value layout vs. `List` (outcome correct —
  neither `Table` nor `List` cleanly covers a single-record description
  list in MUI's vocabulary — though the stated reasoning was thinner than
  the candidate deserved).
- **ntfy:** Chip-triggered field reveal (Chip's own documented purpose
  explicitly includes "trigger actions" — no gap to report, verified A);
  `ExpandingTextField`, a bespoke auto-width editor (no MUI analog found in
  the retrieved corpus — a harder negative to prove with certainty, graded
  B); `SubscribeDialog`'s conditional page-swap vs. `Stepper` (Stepper
  documents numbered/wizard sequences, this is a conditional two-screen
  auth branch — same shape, different problem, correctly rejected, verified
  A).
- **hk-bus-eta:** fare text as `Chip` (Chip's purpose statement is generic
  enough here that citing it would be availability, not applicability —
  correctly suppressed); `Accordion` vs. `List`/`ListItemButton` (the
  existing controlled single-open pattern matches MUI's own documented
  controlled-Accordion example exactly — genuine "checked and cleared");
  a 5-`IconButton` cluster vs. `ButtonGroup`/`SpeedDial` (independent,
  non-exclusive actions, not a grouped/exclusive set or a FAB's sub-actions
  — sound, if lightly cited).

## 7. Evidence of Cloudscape-specific overfitting

**No case invented a hidden MUI "pattern layer."** All three skill runs
were explicit and honest, in their own text, that no pattern-tier page
exists in this corpus, and every citation across all six reported findings
resolves to a component-tier page (`react-*.md` under Components), never a
fabricated "product pattern" page. This is the literal failure mode the
task brief asked to watch for most directly, and it did not occur.

The nearest thing to a Cloudscape-shaped artifact is narrower and more
specific than an invented pattern layer: the skill's `combined component +
pattern` finding **type** — a taxonomy built around Cloudscape's real
two-tier corpus — was used exactly once in this round (ntfy's
`AttachmentBox` finding), and that is the one finding built from
synthesizing *across two separate component pages'* worked examples rather
than quoting a single page's stated rule, in the explicit absence of a
pattern-tier anchor to lean on instead. It is also the round's only
E-grade finding, disqualified specifically because that synthesis fabricated
one of the two source examples. The type label itself stayed honest (the
finding's own text explicitly flags "no separate Patterns section... this
finding's compositional evidence comes from two component pages' own
worked examples, not from a task/pattern-level page" — it never claims
pattern-tier authority strength it doesn't have) — so this is not
overfitting in the sense of the skill misrepresenting its evidence tier.
But it is a real, load-bearing signal that the *reasoning move* Cloudscape's
explicit pattern layer used to make unnecessary — synthesizing a
recommendation from multiple authoritative pages at once rather than one —
is exactly where citation reliability broke down under MUI. See §9 for how
this bears on the missing-pattern-layer question directly.

## 8. Evidence the core reasoning operation generalized successfully

- **Anti-fundamentalism rule (existence ≠ mandate):** 9 of 9 suppressed/
  cleared candidates across all three fixtures independently confirmed
  correct or defensible (§6) — the same discipline the Cloudscape round
  validated, reproduced with a structurally different corpus.
- **Scope fence (implementation-correctness exclusion):** hk-bus-eta's
  skill run explicitly named the `Dialog`/`fullScreen` observation and then
  deliberately excluded it — "this is a props/hard-coded-style-value
  question, not a component-selection question (`Dialog` is already the
  right component here)" — while baseline, unbound by any scope rule,
  reported the identical observation as if it were a native-expression
  finding. An independent verifier confirmed the skill's exclusion is
  correct per `SKILL.md`'s own boundary language and that baseline's
  inclusion is a genuine scope violation that would grade D under this
  rubric. This is the single cleanest, most concrete demonstration in the
  round that the scope fence is a general mechanism, not a Cloudscape
  artifact — it fired correctly against a document it had never seen
  before (Material UI's `Dialog` page), on a corpus with no equivalent to
  Cloudscape's own explicit implementation-vs-pattern split to lean on.
- **"Missing intent" / `intent-dependent` mechanism:** hk-bus-eta's skill
  run classified the `AppBar` question as `intent-dependent`, naming the
  exact fact that would resolve it (does a global `AppBar` already exist
  in the app shell) rather than guessing, while baseline asserted a
  confident, unhedged recommendation from the same file in isolation. An
  independent verifier went outside the bounded surface, read the app's
  router-layout files, and found the app *does* have a persistent global
  `Header`/`Toolbar` invisible from the reviewed files — substantively
  vindicating the hedge, not merely excusing it procedurally. Baseline's
  confident call, had it been implemented, risked the exact landmark
  collision the skill's hedge was built to guard against.
- **Component-vs-pattern tier shift:** all three runs explicitly narrated
  adapting to the evidence actually available — reasoning almost entirely
  at component tier, dropping straight to `INFERRED`/`intent-dependent`
  rather than treating a component page's "Features"/"Usage" prose as if
  it were pattern-level guidance. This is the literal behavior the special
  hypothesis asked to look for, and all three runs exhibited it without
  being told to.
- **Deterministic tooling:** both `inspect_surface.py` and (post-fix)
  `resolve_versions.py` ran unmodified across all three fixtures;
  verifiers independently spot-checked version-resolution and import-
  inventory claims in every run and found no factual errors.

## 9. Did MUI's missing pattern layer prevent a fair test of any portion of the operation?

**Yes, materially.** `SKILL.md`'s retrieval priority names four tiers —
component docs, pattern docs, foundations, inference — and its central
architectural claim is that unifying component-selection and
pattern-composition judgment as one operation is more powerful than
splitting them (this is the whole reason the skill exists as one skill
rather than two, per its own opening section). Across all three fixtures
and all six reported findings, **zero citations resolved to a pattern-tier
page**, because none exists in this corpus. Tier 2 of the retrieval
priority was never exercised even once. That means this round tested
whether the skill *degrades gracefully* when the pattern tier is absent
(it does — see §8) but could not test the tier-2 half of its own central
unification claim at all: no finding in this round could have been "one
combined recommendation that would have split into two weaker findings at
different levels," the exact scenario Cloudscape's Case C was built to
validate, because there was never a real pattern-tier source available to
combine with a component-tier one. The one time the skill reached for the
`combined component + pattern` type regardless (ntfy's `AttachmentBox`
finding, §7), it did so by synthesizing across two component pages as an
ersatz substitute — and that finding is this round's sole E grade. This
round is therefore evidence about the skill's tier-1/tier-4 behavior
(component-level reasoning, and honest retreat to inference/intent-
dependent when tier 1 doesn't settle it) and about its scope fence and
anti-fundamentalism rule — not evidence, one way or the other, about
whether its combined component+pattern unification claim holds on a
corpus that actually has two tiers to unify.

## 10. Classification

**C — Mixed / operation partly Cloudscape-dependent**, leaning positive.

Not A ("strong generalization"): a real, adversarially-confirmed
citation-integrity regression showed up specifically in this round.
Fabricated or conflated supporting quotes appeared in 3 of the 6
skill-assisted findings (Checkmate's Chip color-prop claim, ntfy's
LinearProgress supporting clause, ntfy's Avatar/List conflation) — a much
higher rate than the original Cloudscape round's one fabricated quote in
seven cases. All three instances share a shape: the reviewing agent needed
to state a fact it believed to be true (a real prop value, a real example's
gist) as a natural-language sentence, and where no single page supplied
that sentence verbatim, it wrote one and presented it in quotation marks.
This is not random noise — it concentrates exactly where §9 identifies the
skill working without Cloudscape's crisp, quotable "Don't...Instead"
pattern-page sentences to lean on, and it is the direct cause of this
round's only D and E grades.

Not D ("does not generalize"): the reasoning architecture itself —
four-point applicability test, anti-fundamentalism rule, scope fence,
missing-intent handling, honest tier-shift to component-level reasoning —
transferred cleanly and, on the round's two most rigorously adjudicated
questions (hk-bus-eta's `fullScreen` scope call and `AppBar` intent-
dependent call), **outperformed** an unguided baseline that had no
equivalent discipline, with both calls independently confirmed correct by
evidence gathered outside the bounded surface.

Not a clean B ("narrower evidence envelope" only): a narrower evidence
envelope alone would predict fewer, more conservative findings — which is
exactly what happened and is not a defect. But it would not predict a
citation-fabrication rate roughly triple the Cloudscape round's, and that
defect is orthogonal to "envelope narrowing" — it is about the reliability
of the citation mechanism itself under a specific condition (multi-page
synthesis in place of a single quotable rule) that this round newly
exposed and the Cloudscape round's corpus structure had been quietly
protecting against.

## 11. Recommendation

**Make a small, design-system-neutral refinement — do not abandon
generalization, do not split a capability, and do not touch the reasoning
procedure itself.**

The reasoning operation (scope fence, anti-fundamentalism rule,
missing-intent handling, tier-shift behavior) does not need Cloudscape-
specific content and should not be forked or narrowed to Cloudscape only —
§8's evidence is too direct to ignore, especially the two independently-
ground-truthed hk-bus-eta adjudications. What needs attention is narrower
and citation-mechanical, not conceptual: the Finding contract's "Cloudscape
evidence" field already requires "the exact authoritative source... and the
specific guidance it establishes," but nothing in `SKILL.md` currently
distinguishes *quoting* a source from *paraphrasing a fact the source
supports* — and this round's evidence says that distinction collapses
specifically under multi-page/no-explicit-rule synthesis, regardless of
design system. A targeted addition — something in the spirit of "a quoted
citation must be copy-paste-verifiable against the fetched page; if you are
stating a fact the source supports without a literal matching sentence, say
so explicitly rather than presenting it in quotation marks" — is a small,
general fix aimed at the actual observed defect, not a Cloudscape-specific
patch and not a rewrite of anything that performed well this round.

Per the task brief, this is recorded as a **proposed follow-up only** and
was not implemented as part of this evaluation; `SKILL.md` was not edited.
The frozen skill, fixtures, authority snapshot, and this round's six run
files plus three verification files stand as the evidence base for that
future, separate decision.

## What this does not prove

Three fixtures, six skill-assisted findings, one model, one run each (no
repeat-run variance data the way the Cloudscape round's Case E/F v1→v2
correction produced) — this is suggestive, not powered, evidence,
consistent with this repo's own evidence-discipline convention. The
citation-fabrication rate comparison to the Cloudscape round (3-in-6 vs.
1-in-7) is a real, directly-observed difference, not an estimate, but it
is one data point about one model on one day, not a controlled trial
isolating "MUI vs. Cloudscape" from other differences between the two
rounds (different fixtures, different total citation counts, a different
number of findings). Baseline findings were not exhaustively graded in
this round (see §5), so no full baseline-vs-skill grade-distribution table
comparable to the original round's Grade table can be honestly produced
here — the comparisons in §§5–10 are anchored to specific, individually
verified findings, not an aggregate percentage.
