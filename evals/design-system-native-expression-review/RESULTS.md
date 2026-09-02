# design-system-native-expression-review — morph regression results

**Run date:** 2026-09-02. **Model:** claude-sonnet-5, fresh `general-purpose`
subagent per run (no fork, no shared context) — 6 skill-assisted runs + 6
independent adversarial-verifier runs, against three reused Cloudscape
pressure cases and the same three pinned Material UI fixtures the prior
generalization round used. Full raw transcripts are local, untracked
artifacts; `runs/*.md` are the committed, auditable record every claim
below cites.

**Starting point:** branch `design-system-calibration-mui-generalization`,
which already carried the frozen MUI generalization round (commit
`049def2`). This round's changes: renaming
`skills/cloudscape-native-expression-review/` to
`skills/design-system-native-expression-review/` and rewriting `SKILL.md`
per the morph (corpus-adaptive authority discovery, generalized taxonomy,
evidence-mode discipline), a small tooling rename
(`cloudscape_imports` → `design_system_imports` in `inspect_surface.py`),
and this eval directory. No historical file under
`evals/cloudscape-native-expression-review/` or
`evals/design-system-calibration/` was edited.

## 1. What this round tested

Per the task brief, three reused Cloudscape cases (not all thirteen — a
regression-detection subset, not a full re-run):

- **Case B** (`EndpointScaling.tsx`) — a real, previously A-graded
  component-selection finding (Cards→Table).
- **Case C** (`WorkspaceDetails.tsx`) — the previously-validated,
  genuinely unified `combined component + pattern` finding (Table→
  KeyValuePairs + tab placement) — the case that tests whether unifying
  component and pattern reasoning survived the taxonomy rename.
- **Case P1** (`MessageQueues.tsx`) — the isolating precision case built
  specifically to test whether a real primary finding gets padded with a
  self-acknowledged, equally-valid secondary finding that should
  self-suppress (the "A1 Finding 2" failure shape).

And the same three pinned MUI fixtures as the frozen-skill MUI round:
Checkmate (`Incidents` page), ntfy (`Subscribe`/`PublishDialog`), and
hk-independent-bus-eta (`RouteEtaPage` flow) — asking whether the prior
round's specific graded findings, scope-fence exclusion, and
intent-dependent hedge reproduce.

## 2. Cloudscape regression — case-by-case

| Case | Finding | Type | Grade | Verdict |
|---|---|---|---|---|
| B | Cards→Table | `combined selection + composition`* | **A** (on substance) | Matches designed intent; core reasoning correct; *Type mislabeled per grading key (should be plain `component selection`) |
| B | ContentLayout+Cards→`full-page` variant | `documented composition` | **C** | Citation-accurate but over-reported: materiality undercut by Finding 1's own adoption, not suppressed/demoted despite the report itself noticing the tension |
| C | Table→KeyValuePairs + tab placement | `combined selection + composition` | **A** | **Exact match** to designed intent — one unified finding, not fractured |
| P1 | Cards→Table | `combined selection + composition` | **A** | Matches designed intent, clean citations |
| P1 | TextFilter→CollectionSelectFilter | `component selection` | **E** | **MUST-SUPPRESS candidate reported as a finding** — the case's central, designed failure mode |

**Question 1 (important component-selection findings still found)?** Yes —
Case B and Case P1's primary findings both survived at A-grade-on-
substance, with citations verified against live `cloudscape.design` pages
independent of two labeling defects noted below.

**Question 2 (equally-valid/anti-fundamentalism traps still suppressed)?**
**No, not in this run.** Case P1 — the case purpose-built to test this
exact mechanism — reproduced the "A1 Finding 2" shape it was built to
detect: a real primary finding (Cards→Table) alongside a second candidate
the review's own retrieved evidence shows is equivalent (the filter-
patterns page places `TextFilter` and `CollectionSelectFilter` in the
*same* complexity cell), reported anyway at `medium` materiality/`high`
confidence, with the review's own "Why it matters" half-conceding the
current approach already works. This is precisely the shape the grading
key calls "the specific, sharpest form of the failure." It is also the
first recurrence of this shape since iteration 3 of the original
Cloudscape eval built P1/P2 specifically to test for recurrence and found
none across two controlled runs.

**Question 3 (previously-validated combined finding preserved)?** **Yes,
cleanly.** Case C reproduced the exact designed intent: one unified
`combined selection + composition` finding, not two fractured findings —
the taxonomy rename (`pattern composition` → `documented composition`,
`combined component + pattern` → `combined selection + composition`) did
not disturb the underlying unification behavior this case exists to
validate.

**Question 4 (did generalizing the authority model weaken real
pattern-level reasoning)?** No clear evidence of this specifically. Case
C's pattern-tier reasoning (citing the Details-page and Details-page-
with-tabs pattern family) was sound and correctly unified. The one
pattern-level miss this round — P1's incorrect suppression of a real,
`REQUIRED`-strength `ContentLayout`+`Cards` violation (the review asserted
"no material difference to flag" against a page it had already fetched
and quoted for a different finding) — is an accuracy lapse on an
already-fetched page, not evidence the corpus-adaptive discovery step
itself degraded pattern-tier retrieval.

## 3. MUI regression — case-by-case

| Fixture | Finding | Type | Grade | vs. prior round |
|---|---|---|---|---|
| Checkmate | resolutionType/status → Chip | `component selection` | **B** | Prior round: same core finding, graded B (fabricated quote then; clean now) |
| Checkmate | SummaryCard → Card | `combined selection + composition` | **B** | Prior round suppressed the analogous `BaseBox`-as-`Card` candidate; this round reports a related but distinct candidate at B — real, not fabricated, but a softer version of the same over-reporting risk |
| ntfy | DialogFooter status → Alert/DialogContentText | `combined selection + composition` | **B** | New finding, not in prior round; real and correctly hedged |
| ntfy | EmojiPicker Popper+Fade+ClickAwayListener → Popover | `component selection` | **E** | **Regressed from A** ("strongest finding in the whole round") — this run's premise inverts what the cited Popper page actually says |
| ntfy | AttachmentBox synthesis | (suppressed) | — | Prior round's only E-grade finding (fabricated Avatar/List conflation) — **this round correctly and accurately suppressed it, with no conflation** |
| hkbus | RouteHeader → AppBar/Toolbar | `combined selection + composition` | **D** | **Regressed from A on Q9** (correctly hedged `intent-dependent`) — this run instead reported it unhedged, missing the same global `Toolbar`-based `Header` the prior round's verifier had to find independently to vindicate the hedge |
| hkbus | RouteUpdateNotice → Alert | `component selection` | **A** | **Exact match** — same finding, same grade, as the frozen pre-morph skill's run |
| hkbus | StopDialog fullScreen | `intent-dependent` | **D** | Prior round *excluded* this observation entirely as implementation-correctness ("the sharpest scope-discipline result in this round"); this run folded a genuine composition-level kernel together with a prop-vs-hardcoded-CSS observation that exceeds the "supporting evidence only" allowance |

**MUI questions 1–7:**

1. **Previously A-grade reasoning behaviors survive?** Partially.
   hk-bus-eta's `RouteUpdateNotice`→`Alert` reproduced exactly (A). ntfy's
   `EmojiPicker`→`Popover` — the round's single strongest prior result —
   did not (E).
2. **Scope fence still rejects the Dialog/fullScreen implementation
   issue?** **Not cleanly.** The prior round's cleanest scope-discipline
   moment was a full exclusion; this run instead bundled a real
   composition-level question with an implementation-mechanics detail
   (prop vs. hardcoded CSS) inside one `intent-dependent` finding, which
   the verifier graded D specifically for the scope leak (crediting the
   intent-dependent procedure itself as correctly executed).
3. **AppBar question remains appropriately intent-dependent?** **No.**
   Reported unhedged at high materiality/confidence; the applicability
   argument's own "no competing header" claim is checkably false one file
   hop past what the review actually inspected (`Root.tsx` renders
   `Header.tsx`, a persistent global bare-`Toolbar`).
4. **Valid Popover/Alert findings survive?** Alert: yes, both instances
   (ntfy B, hkbus A). Popover: no (A→E).
5. **Citation-fabrication rate disappear?** **Materially improved, not
   eliminated.** Findings-with-fabrication: 1 of 7 MUI findings this round
   (ntfy Finding 2, plus one non-finding fabrication in ntfy's Orientation
   notes) vs. 3 of 6 in the prior round — see §4.
6. **Generalized taxonomy avoids manufacturing a pattern claim where MUI
   has none?** **Yes, in every run.** All three MUI reports' "Authority
   categories found in this corpus" fields correctly state component
   guidance only, no separate composition/pattern tier — confirmed by
   direct grep of `Type:` labels across all six reports (`runs/*.md`):
   the new taxonomy (`component selection` / `documented composition` /
   `combined selection + composition` / `intent-dependent`) was used
   consistently everywhere; no run reverted to inventing pattern-tier
   authority for MUI.
7. **Prior E-grade AttachmentBox-style synthesis honestly resolved?**
   **Yes — the clearest specific win in this round.** ntfy's equivalent
   candidate was checked against the actual fixture, accurately described,
   and correctly suppressed with no Avatar/List-style conflation.

## 4. Citation-integrity comparison, before vs. after

| | Prior round (frozen, pre-morph skill) | This round (generalized skill) |
|---|---|---|
| **MUI findings with a fabricated/conflated citation** | 3 of 6 (50%) | 1 of 7 (~14%), + 1 non-finding fabrication in orientation notes |
| **Cloudscape findings with a fabricated/conflated citation** | 1 of 7 (~14%) | 3 of 5 (60%): Case B Finding 1 (2 fabrications, non-load-bearing), Case P1 Finding 2 (1 fabrication, load-bearing) |

**Read honestly:** the evidence-mode discipline (`VERBATIM` must be
copy-paste-verifiable; `SYNTHESIS` must cite every load-bearing source and
never inherit `REQUIRED`/`RECOMMENDED` strength automatically) measurably
reduced fabrication on the MUI side — the exact corpus shape the prior
round identified as the failure's proximate trigger (multi-page synthesis
in the absence of a single quotable rule). It did **not** reduce
fabrication on the Cloudscape side in this small sample; if anything the
rate went up. Two things are worth naming plainly:

- **This is a small sample** (5 Cloudscape findings, 7 MUI findings) —
  not powered evidence of a directional Cloudscape-specific regression,
  consistent with this repo's own evidence-discipline convention.
- **The mechanism worked as a *detection* aid even where it failed as
  *prevention*.** Every fabricated quote in this round was caught
  immediately by an adversarial verifier specifically because it was
  explicitly self-labeled `VERBATIM` — a checkable, falsifiable claim —
  rather than buried in unlabeled prose. The discipline did not stop a
  reviewer from writing a confident, plausible-sounding invented sentence
  and marking it as a literal quote; it made that invention easy to catch
  once labeled. Tightening self-verification *before* the label is
  applied (not just the label's existence) is the gap this round exposes.

## 5. Newly discovered failure modes

1. **Self-labeled `VERBATIM` is not self-verifying.** An agent can mark a
   paraphrased or fabricated sentence `VERBATIM` with full confidence; the
   label only helps once an independent party checks it against the
   source. This round's fabrications (Case B ×2, Case P1 ×1, ntfy ×4)
   were all inside claims explicitly labeled `VERBATIM`, never inside
   `PARAPHRASE`/`SYNTHESIS`/`INFERRED` claims dressed up with quotation
   marks — i.e., the discipline correctly prevents the *dressing-up*
   failure mode it names, but doesn't prevent the *mislabeling* one.
2. **A citation inversion is a distinct, more dangerous failure than
   fabrication-from-nothing.** ntfy's Popover finding didn't invent a
   sentence out of thin air — it inverted the meaning of a real sentence
   ("has built-in support for react-transition-group" became "doesn't
   include built-in transition animations"), which is harder to catch by
   pattern-matching and directly reversed the finding's conclusion.
3. **A review that goes looking for missing context can still miss it by
   one file-hop and then report *more* confidently for having looked.**
   The hk-bus-eta AppBar finding explicitly named checking `App.tsx` and
   `Root.tsx` for a competing header, found none directly in those two
   files, and reported unhedged — where the prior round's review never
   claimed to have checked at all and hedged correctly by default. Partial
   verification that stops short can produce worse calibration than no
   verification, because it upgrades confidence without earning it.
4. **The equally-valid-suppression discipline (the P1/A1 failure shape) is
   not yet a solved problem, generalized skill or not.** This is the
   second known instance of this exact shape (original A1 Finding 2, now
   this round's P1 Finding 2) across four total controlled tests of it
   (A1, P1, P2, and this round's P1 rerun) — i.e., one prior confirmed
   pass (iteration 3) and now one fail on the same case with the
   generalized skill. Not enough trials to separate "the morph weakened
   this" from "ordinary run-to-run variance," but enough to warrant a
   repeat trial before either conclusion is drawn.

## 6. Classification

**B — General skill viable with minor follow-up, more cautiously stated
than a typical "minor" label implies.**

What substantially held: the corpus-adaptive authority-discovery step
worked exactly as designed in every one of six runs — no run invented a
pattern/composition tier MUI's corpus doesn't have, and no run collapsed
Cloudscape's real pattern tier into component-only reasoning. The
generalized taxonomy (`component selection`/`documented composition`/
`combined selection + composition`/`intent-dependent`) was used
consistently and correctly everywhere, with zero reversion to the old
Cloudscape-specific labels. The single most direct test of the "is this
genuinely one unified operation" hypothesis — Case C — reproduced its
designed intent exactly. MUI's overall citation-fabrication rate
materially improved, and the specific previously-fabricated
AttachmentBox-style synthesis was this time handled honestly. hk-bus-eta's
`Alert` finding reproduced exactly.

What did not substantially hold, and is the reason this isn't a clean
A: four separate, previously-validated behaviors — Case P1's
equally-valid suppression, hk-bus-eta's `AppBar` intent-dependent hedge,
hk-bus-eta's `fullScreen` scope-fence exclusion, and ntfy's `Popover`
finding — each failed to reproduce their prior grade in this one attempt,
spanning both evidence families. None of these four failures traces to a
specific wording change this morph introduced (the anti-fundamentalism
rule, scope boundary, and missing-intent section were preserved in
substance, only reworded for corpus-neutrality); they read as execution-
reliability lapses — confident overreach, a citation inversion, a
one-file-short investigation — of a kind this repo's own eval history
already documents as ordinary run-to-run variance (the original Case A
recall miss; the Case E/F v1→v2 rerun). But four such lapses landing in
one focused, six-fixture regression round, several on exactly the cases
built to catch them, is more than "one small issue," and this repo's own
convention counsels against dismissing an observed failure just because
its cause is unconfirmed.

Not C: nothing here indicates the *abstraction* itself — corpus-adaptive
discovery, the generalized taxonomy, evidence-mode labeling — caused a
loss of capability. The one case built to test whether unifying
component and pattern reasoning survived generalization (Case C) passed
cleanly, and the mechanism specifically built to fight citation
fabrication measurably worked on the corpus it was aimed at (MUI). Not D:
no evidence here supports splitting component-selection and composition
reasoning — Case C's single, correctly-unified finding is direct evidence
against splitting, not for it.

## 7. Recommendation

**Keep `design-system-native-expression-review` as the single active
skill for this operation. Do not further edit `SKILL.md` based on this
round alone** — per this repo's own convention, a suspected weakness
should become eval pressure (a repeat trial) before a rewrite, and this
round's four regression signals are each single instances, not confirmed
recurring patterns. Recommended before the next substantive change:

1. **Re-run Case P1 and the ntfy/hk-bus-eta MUI fixtures once more**,
   fresh context, no wording changes, specifically to distinguish
   "ordinary variance" from "a real, reproducible weakness" before editing
   anything. If the same shapes recur (an equally-valid candidate reported
   despite self-acknowledged equivalence; an intent-dependent case
   resolved unhedged after an incomplete check; a citation that inverts
   its source), that is the trigger this repo's own iteration-3 precedent
   already names for a targeted change.
2. **If a change is warranted**, the smallest one suggested by this
   round's evidence is a self-check instruction attached to the
   `VERBATIM` evidence mode — something in the spirit of "after drafting a
   `VERBATIM` quote, re-read the exact fetched text and confirm the quoted
   string appears character-for-character before finalizing the label; if
   it doesn't, use `PARAPHRASE` instead" — aimed at the mislabeling gap
   named in §5, not a rewrite of the reasoning procedure.

## What this does not prove

Three Cloudscape cases (not the full thirteen-case suite) and three MUI
fixtures, one run each, no repeat-run variance data — this is regression
*signal*, not a powered regression *test*. Every grade and citation claim
above is drawn from a committed, independently adversarially-verified
run file (`runs/*.md`), not from memory or the reviewing run's own
self-report; readers should treat the §6 classification as this round's
honest reading of that evidence, not a statistically confident verdict.
