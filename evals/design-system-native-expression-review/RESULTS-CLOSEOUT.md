# design-system-native-expression-review — closeout round

**Run date:** 2026-09-02. **Purpose:** resolve the one open item left by the
distillation round (`RESULTS-DISTILLATION.md` §8/§10/§11) — N2's mixed 1/2
result on the distilled skill vs. 2/2 on the original — before closing out
this branch. This round is verification only; it was scoped not to
tune, shorten, or otherwise edit `SKILL.md` unless the evidence showed a
reproducible, distillation-attributable regression.

## 1. N2 trial counts and outcomes

Fresh trials this round: 5 independent `general-purpose` subagents per skill
version, each starting from a clean scratch copy of the assigned `SKILL.md`
(+ unmodified `scripts/`) and the unmodified N2 fixture, with no shared
context between trials and no access to the grading key, prior run reports,
or any other file in this repository. All ten full reports are committed at
`runs-closeout/{distilled,original}-trial-{1..5}.md`.

| Skill version | Trial | Outcome | Notes |
|---|---|---|---|
| Distilled | 1 | **PASS** | Wizard finding, high/high, VERBATIM Length-table citation |
| Distilled | 2 | **FAIL** | Hedged `intent-dependent`; never surfaced the Length decision table |
| Distilled | 3 | **PASS** | Wizard finding, high/high, VERBATIM |
| Distilled | 4 | **PASS** | Wizard finding reported at high materiality (offered a second documented remedy alongside it, but did not suppress or hedge the core finding) |
| Distilled | 5 | **PASS** | Wizard finding, high/high, VERBATIM |
| **Distilled total (this round)** | | **4/5** | |
| Original | 1 | **PASS** | Wizard finding, high/high, VERBATIM |
| Original | 2 | **PASS** | Wizard finding, high/high, VERBATIM, explicit tie-check |
| Original | 3 | **PASS** | Wizard finding, high/high, SYNTHESIS across 3 pages, explicit tie-check |
| Original | 4 | **FAIL** | Correctly retrieved the Length table, then suppressed the Wizard candidate via a self-neutralizing argument (see below) |
| Original | 5 | **PASS** | Wizard finding, high/high, VERBATIM, explicit tie-check |
| **Original total (this round)** | | **4/5** | |

Combined with all prior recorded N2 evidence (`RESULTS-DISTILLATION.md` §8:
distilled 1/2 across 2 trials, both from the distillation round itself;
original 2/2 across 2 trials — 1 from the distillation round, 1 from the
earlier equivalence-isolation round, per `RESULTS-DISTILLATION.md`'s own
opening summary and §8 table): **distilled 5/7 across all recorded trials
(2 prior + 5 this round), original 6/7 (2 prior + 5 this round).** Both
versions show one failure in five fresh trials this round — comparable
variance, not a one-sided gap.

## 2. Failure-mechanism classification

**Distilled trial 2 — authority retrieval.** The trial correctly generated
the Wizard candidate as its own "Finding 2" (recall did not fail) and
correctly avoided fabricating a citation, but it fetched only the
"Single page create" and Wizard component pages, never surfacing the
"Create resource" pattern's Length/Complexity decision table that every
other trial (both skill versions) found and quoted verbatim. Reasoning from
the weaker "simple to medium-complex" / "complex flow" prose it did retrieve
(evidence mode: SYNTHESIS, not VERBATIM), it treated the single-page-vs-
multipage question as a genuinely unresolved "interrelatedness" judgment and
reported `intent-dependent` at medium materiality instead of the required
report. Mechanism: **(2) authority retrieval** — the decisive source was
never fetched, not a reconciliation or materiality failure on the material
it did have.

**Original trial 4 — materiality/reconciliation judgment.** This trial
retrieved the correct Length table and quoted it accurately (visible in its
own "Suppressed" section), so authority retrieval, reconciliation, and
applicability reasoning all worked correctly up to that point. It then
introduced a novel self-neutralizing argument: having independently
diagnosed a genuine, well-evidenced primary/additional-settings finding
(move already-defaulted fields into an `ExpandableSection`), it reasoned
that *after* that hypothetical restructuring the primary-section field
count would drop back under the single-page-create ceiling, and used that
projected future state — not the surface's actual, current field/group
count — to suppress the Wizard candidate as unnecessary. This is not the
"different row of the same table" or "interrelatedness" failure shapes the
same-tier-equivalence paragraph and the grading key's item 3 anticipate; it
is a new rationalization that treats two independently reportable,
non-conflicting findings as mutually exclusive. Mechanism: **(5) materiality
judgment** — the surface's own current, unmodified structure (20 fields, 6
groups, right now) is what the Length criterion measures, and the trial
substituted a hypothetical future structure for it.

Both failures are distinct from each other and from the distillation
round's own N2-trial-1 failure mechanism (surface-defaults-imply-"one-click-
to-create" intent argument, `RESULTS-DISTILLATION.md` §10). Across two
recorded distilled-skill failures and one original-skill failure, no two
share the same mechanism — this fixture appears to admit several different
plausible-sounding ways to talk past the Length criterion, on both skill
versions, rather than exposing one specific weakness the distillation
introduced or removed.

## 3. Reproducible distillation regression?

**No.** Applying this round's own decision rule: original and distilled
both showed one failure in five fresh trials (4/5 each), and the two
failures used unrelated mechanisms (authority retrieval on distilled vs.
materiality/reconciliation on original) rather than the same weakness
appearing more often on the distilled side. Per the decision rule, this is
run variance, not a confirmed distillation regression. No wording restoration
was attempted, and none of the two most-edited sections from the
distillation round (the same-tier-equivalence paragraph, the full-table
disclosure field) is implicated by either failure's mechanism.

## 4. Was SKILL.md changed?

**No.** `skills/design-system-native-expression-review/SKILL.md` is
unmodified from the distilled version this round evaluated (477 lines,
unchanged since the prior distillation-round commit). No new rule, hint, or
Wizard-specific instruction was added. Per this round's own scope, no
further trials beyond the N2 set above were run (no repeat of E1, N1, or the
Cloudscape/MUI positives), since the evidence did not surface a confirmed
regression requiring that follow-up.

## 5. Final validation

- `bash scripts/check.sh` — see command output for this commit; run from
  repo root before committing this round's artifacts.
- Working tree: this round added only new files under
  `evals/design-system-native-expression-review/runs-closeout/` and this
  file; no existing file in `evals/` or `skills/` was edited.
- `RESULTS.md`, `RESULTS-POSTFIX.md`, `RESULTS-EQUIVALENCE.md`, and
  `RESULTS-DISTILLATION.md` are untouched — no historical result was
  rewritten.
- `case-p1-message-queues` Candidate 2 remains marked retired/compromised
  for the equally-valid-suppression axis (`RESULTS-POSTFIX.md` §3,
  `RESULTS-EQUIVALENCE.md` §1); this round did not touch that retirement.
- E1, N1, and N2 remain the canonical regression family for the
  equally-valid-suppression/anti-fundamentalism axis; this round's evidence
  keeps N2 in that set (as an accepted-variance case, not an excluded one).
- `SKILL.md` remains framework-agnostic — this round did not add any
  Cloudscape- or MUI-specific rule.
- No marketplace/publishing/promotion action was taken or introduced.

## 6. Recommendation

**Keep the distilled skill; retain N2 as a known-variance case, not a
blocking one.** Both skill versions fail N2 at a similar rate (1-in-5 this
round) via different, fixture-specific rationalization paths rather than one
shared, distillation-introduced weakness. This is not evidence strong enough
to justify a wording change per this repo's own evidence bar (`AGENTS.md`:
"a suspected weakness should usually become eval pressure... before a skill
rewrite" — the pressure test has now run, twice, at 4-6 trials each, without
isolating a distillation-specific mechanism). No restoration was made; none
is recommended.

## Artifacts

- `runs-closeout/distilled-trial-{1..5}.md` — five fresh distilled-skill N2
  trials, this round.
- `runs-closeout/original-trial-{1..5}.md` — five fresh original
  (pre-distillation, commit `eedd66f`), unmodified-skill N2 trials, this
  round, for direct comparison under identical protocol.
- No changes to `SKILL.md`, `scripts/`, the N2 fixture, or the N2 grading
  key.
