# design-system-native-expression-review — post-fix refinement round

**Run date:** 2026-09-02. **Branch:** `design-system-calibration-mui-generalization`.
**Skill edited:** `skills/design-system-native-expression-review/SKILL.md`.

**Purpose:** the repeatability round (`RESULTS-REPEAT.md`) confirmed two
recurring weaknesses and explicitly ruled a third (AppBar/Toolbar
missing-intent investigation) out of scope for this round. This round
implements the smallest justified wording refinement for the two
in-scope weaknesses, then re-evaluates: the confirmed
equally-valid-candidate-suppression failure on Cloudscape Case P1, and
the smaller recurring VERBATIM self-verification weakness. It does not
touch AppBar/Toolbar, does not add framework-specific rules, and does
not restructure the skill's taxonomy or scope boundary.

## 1. Pre-change diagnosis

### 1a. The exact reasoning failure

Both repeatability-round P1 failures reported Finding "TextFilter vs.
CollectionSelectFilter" as a standalone, unhedged, `high`/`high` finding.
In both cases the review's own retrieval already contained the
disqualifying evidence: `patterns/general/filter-patterns/index.html.md`'s
criteria table places `TextFilter` and `CollectionSelectFilter` in the
*identical* cell ("Simple resource, small set of properties") for
"Complexity of the resource" — a directionless tie, not a preference —
while differentiating them only by an unresolved "User goals" row this
single-file fixture cannot evidence either way.

The governing rule already existed: SKILL.md's "Anti-fundamentalism
rule" point 4 ("the difference between current and proposed is material
enough that an experienced practitioner... would plausibly restructure
the code because of it") is the correct test, and "Apply a high
materiality bar" already named "an equally valid alternative" as
something that must not be reported. Neither propagated into practice:
point 4 is phrased as an abstract judgment call, with no instruction to
re-examine the *same* retrieved table for a tie before finalizing a
directional claim, and nothing forced the reviewer to reconcile a
same-tier classification it had already fetched with the confident
"this is material" conclusion it went on to write.

### 1b. The smaller weakness

Both the morph regression and its repeat found VERBATIM-labeled claims
containing fabricated or materially altered citation content (`RESULTS.md`
§5, `RESULTS-REPEAT.md` §3b) — the VERBATIM label was never itself checked
against the source it claimed to quote before being emitted.

## 2. Exact SKILL.md change, and why it is minimal

Two edits, both extending existing sections rather than adding new ones,
both framework-agnostic:

**A. "Anti-fundamentalism rule" — a new paragraph after the existing
four-point test**, naming a concrete, mechanical trigger for point 4's
existing "material enough to restructure" judgment: if the finding's own
retrieved authority is a decision table, fit-tier classification, or
unranked "use X or use Y" pairing that ties the current and proposed
approaches, point 4 fails — regardless of whether the finding's prose
quotes that tie or only a differentiating row nearby. A same-tier
differentiation by unresolved user intent ("if users tend to...") does
not license a direction; the reviewer must check whether *the bounded
surface itself* (not the authority page) resolves which intent applies,
and treat it as `intent-dependent` or suppress it if not. This does not
add a new rule — it makes explicit, mechanical, and self-checking the
same point-4 test that already existed, and preserves the anti-
fundamentalism rule's escape hatch (a genuine, task-specific advantage
still earns a finding).

**B. Finding contract's "Authority evidence" field** — when the cited
authority is a decision/criteria table, the finding must reproduce the
*whole* table, not only the row(s) supporting the finding's direction.
This is a formatting requirement on an existing field, not a new
reasoning rule, and it directly targets the demonstrated failure
mechanism (a technically-accurate but selectively-quoted citation).

**C. Finding contract's VERBATIM bullet** — a one-sentence
self-verification instruction: before emitting a VERBATIM claim, re-check
it character-for-character against the actual fetched text and confirm
correct page attribution; if it doesn't match, fix the quote or relabel
PARAPHRASE. This is the exact minimal candidate `RESULTS.md` §7 proposed
and `RESULTS-REPEAT.md` §8/§9 confirmed should be bundled into this round.

No Cloudscape- or MUI-specific language was added anywhere; no finding
type, authority category, or report section was changed; the
anti-fundamentalism rule, missing-intent escape hatch, and scope
boundary are otherwise untouched.

## 3. P1 before/after — four post-fix trials

Per this round's own evidence, the wording in (A)/(B) above was tightened
twice more, each time in direct response to a new, specific failure
mechanism observed in the immediately preceding fresh trial — not blind
re-layering. All four trials are fresh `general-purpose` reviewers, no
shared context, independently adversarially verified against the frozen
grading key at `evals/cloudscape-native-expression-review/grading/
case-p1-message-queues.expected.md` (full transcripts:
`runs-postfix/case-p1{,-v2,-v3,-v4}-skill.md` and matching `-verify.md`,
except v4 which was verified by direct fixture/table inspection in this
session rather than a separate verifier agent, given budget and the
unambiguous nature of the evidence).

| Trial | SKILL.md state | Finding 3/2 outcome | Failure mechanism |
|---|---|---|---|
| v1 | First edit (A alone, general phrasing) | Reported, `high`/`high` | **Selective quotation.** Cited the differentiating "User goals" row and one fabricated, non-existent VERBATIM sentence ("if a select filter has two properties, the operator is always and"); never quoted or engaged the tied "Complexity of the resource" row. |
| v2 | Tightened (A: "whether or not you end up quoting it," explicit re-examination instruction) | Reported, `high`/`high` | **False denial.** Applicability point 4 stated outright "there's no equalizing language in the filtering-patterns table" — verified false by live fetch; the tied row exists and was not quoted. |
| v3 | + (B): full-table transcription required in Authority evidence | Reported, `high`/`high` | **Acknowledged-but-argued-past.** The full table (including the tie) was reproduced verbatim this time, and the tie was explicitly named — but the finding then argued the table's *other* rows (a "user goals" differentiation) were "evidence within the same retrieved corpus" sufficient to license a direction anyway. |
| v4 | + closed the "different row of the same table" loophole explicitly; required resolution from the bounded surface itself | Reported, `high`/`medium` | **Fixture-comment argument.** Full table reproduced, tie named, the "different row" loophole not reused. Instead, the review cited the fixture's own code comment ("Operators can search by queue name, or narrow the list down to a specific status or region while triaging") as surface-level evidence resolving which "user goal" applies to which field — exactly the escape hatch this round's own wording (correctly) still allows. |

**Candidate 1 (Cards → Table) was correctly reported at Grade A in all
four trials**, with clean, verified citations — no regression on the
skill's ability to find and report a genuine, well-evidenced finding.

**Important, verified complication:** the grading key's Candidate 2
section states "the fixture shows no code, comment, or header language
establishing which lookup mode operators actually use." This is
factually incorrect against the actual, unmodified fixture (frozen in
the same commit, `647ff0e`, as the grading key itself) — the file's own
header comment (lines 29–33) does state operators "can search by queue
name, or narrow the list down to a specific status or region while
triaging." Both this session's direct fixture read and an independent
adversarial verifier (`case-p1-v3-verify.md`) confirm this. The v4
review's argument — that this comment resolves which intent applies to
which field — is not obviously wrong; it is a legitimate, if contestable,
reading of real fixture text, not a fabrication or a rationalization
built from nothing. The grading key's independent materiality argument
(24 items, one already-sufficient filter mechanism, no stated pain point
distinct from ordinary page-description copy) still supports the
MUST-SUPPRESS verdict, and per the grading key's own stated bar ("any
response that reports this candidate — regardless of hedged confidence —
reproduces the exact failure"), all four trials are scored FAIL. But this
complication means the isolating case itself is not as clean as its own
charter assumes, and that should inform how much weight the 4-for-4
result carries as a verdict on the wording fix specifically, versus on
the model's tendency to construct a plausible-sounding resolution once it
has already decided a candidate is worth reporting.

**Bottom line: P1's central adjudication target was not fixed.** Four
independent, diagnosis-driven iterations narrowed the specific mechanism
of failure (from outright selective citation and a false claim, to a
transparent but ultimately unpersuasive argument grounded in genuinely
ambiguous fixture text) without ever reaching the case's required
outcome (suppression or `intent-dependent`).

## 4. VERBATIM before/after

| Fixture | Before (repeat round) | After (this round) |
|---|---|---|
| P1 (Candidate 2 specifically) | 1 fabricated VERBATIM quote, load-bearing (repeat round's Finding 3) | v1: 1 fabricated VERBATIM quote (different sentence). v2/v3/v4: **zero** fabricated quotations found by adversarial verification — the failure moved from misquoting the source to misdescribing or over-extending what an accurately-quoted source supports. |
| ntfy | 1 fabricated + 1 drifted quote (repeat round), both non-load-bearing | **Zero** fabrications or drifts found across all three findings in this round's fresh run (`ntfy-verify.md`) — all three findings graded A. |
| Checkmate | 1 fabricated quote in the prior morph-regression round | **Zero** fabrications this round; one cosmetic punctuation splice (period silently became a comma to graft a continuation clause) — a citation-fidelity nit, not a fabrication. |
| Case B / Case C | Citation fabrications present in the original morph-regression round (Case B: 2, Case P1: 1) | Case B: all citations verified verbatim, zero fabrications. Case C: zero fabrications, one minor drifted quote in a non-load-bearing spot. |
| hk-bus-eta | Not previously graded for VERBATIM specifically | Zero fabrications, inversions, or misattributions across all 9 checked citations this round. |

**The VERBATIM self-check measurably worked.** Across five fresh, fully
independent post-fix runs (11 total findings, dozens of individually
checked quotations), adversarial verification found no fabricated or
semantically-inverted VERBATIM quotations anywhere except P1's own v1
trial (fixed by v2's edit). The remaining defects are cosmetic
(punctuation, structural merging of adjacent bullets) or — in P1's later
trials — analytical overreach about what an accurately-quoted table
supports, which is a different, deeper failure than fabrication and is
what §3's gate targets.

## 5. Regression results

| Fixture | Finding(s) | Grade | vs. baseline (repeat/round-1) |
|---|---|---|---|
| Case B | Cards→Table | A | Matches baseline exactly (A) |
| Case B | ContentLayout/full-page variant | C (over-produced, not itself scored per grading key) | Matches baseline exactly (C, same over-production defect, pre-existing and out of this round's scope) |
| Case C | Table→KeyValuePairs + tab placement | A | Matches baseline exactly (A) — unified `combined selection + composition` finding preserved |
| Checkmate | Hand-rolled status pill → Chip | A | Consistent with/exceeds baseline (B in round 1) |
| Checkmate | Select vs. ToggleButtonGroup inconsistency | B | New but real, correctly self-hedged |
| ntfy | 3 findings (InputAdornment, Autocomplete tags, Checkbox→Switch) | A, A, A | Improved citation cleanliness vs. baseline; no candidate this round resembled the repeat round's Popper/Popover inversion (not evidence the fix helped that axis — it simply didn't recur, consistent with the repeat round's own "likely run variance" classification) |
| hk-bus-eta | StopDialog DialogTitle/DialogActions | B (directionally reasonable, overstates page-survey completeness) | New finding shape |
| hk-bus-eta | RouteUpdateNotice → Alert | A | Matches the one previously-exact-reproducing finding (A in both round-1 and repeat) |
| hk-bus-eta | RouteHeader → AppBar/Toolbar | Suppressed, correctly | Per this round's own charter, **not used as evidence for or against this refinement** — the AppBar axis is explicitly out of scope. Noted only because the suppression's *outcome* was independently confirmed correct (a persistent global `Header`/`Toolbar` does exist, verified directly) and its *reasoning* was sound intent-discipline, not because this round's edit is credited with it. |

**No legitimate finding was accidentally suppressed anywhere in this
round.** Every verifier was explicitly tasked with checking for
over-suppression and for cases where two documented alternatives are
genuinely *not* equivalent (a material, task-specific advantage
established by authority). The one clean instance found — Checkmate's
`Stack` (1-D) vs. `Grid` (2-D) question for `CardDetails`' repeated
rows — was correctly resolved in the existing code's favor (`Grid` is
the documented right answer for two-dimensional layout), and no
suppressed candidate anywhere hid a real, task-specific documented
advantage that should have been a finding instead.

## 6. Framework-agnosticism

Both edits are stated entirely in terms of the skill's own generic
vocabulary — "decision table," "fit-tier classification," "unranked 'use
X or use Y' pairing," "the bounded surface's own code, comments, or
copy" — with no Cloudscape- or MUI-specific term, page name, or example
anywhere in either addition. The mechanism was exercised successfully in
its mechanical part (full-table reproduction) on a Cloudscape corpus
(P1) and the VERBATIM self-check was exercised and measured across both
evidence families (Cloudscape: Case B, Case C, P1; MUI: Checkmate, ntfy,
hk-bus-eta) with consistent improvement in both. No run in this round
invented a pattern/composition tier for MUI or reverted the corpus-
adaptive taxonomy.

## 7. Remaining unresolved weaknesses

- **Equally-valid-candidate suppression (P1 axis): still unresolved**,
  4-for-4 post-refinement fails on the case's own MUST-SUPPRESS bar,
  though the failure mechanism narrowed each iteration and the final
  trial's specific argument turns on a genuinely ambiguous piece of
  fixture text the grading key itself mischaracterizes (§3). This
  axis needs either a cleaner isolating case (one without the
  fixture-comment confound) or a fundamentally different lever than
  wording-level instruction-following, and should not be considered
  fixed by this round's edits.
- **AppBar/Toolbar missing-intent investigation: explicitly untouched**,
  per this task's own instruction. This round's hk-bus-eta run happened
  to suppress the RouteHeader/AppBar candidate correctly, but per the
  task's own instruction this is not evidence the refinement helped or
  hurt that axis — it wasn't the target of either edit, and the
  repeatability round already established this failure changes shape
  unpredictably between runs. It remains a candidate for a dedicated
  isolating case in a future round, not addressed here.
- **ntfy/hk-bus Popper/Popover, Dialog/fullScreen scope leak**: neither
  targeted, neither recurred, consistent with the repeatability round's
  own "likely run variance" classification — no new evidence either way
  from this round.
- **New, smaller observation**: hk-bus-eta's Finding 1 this round
  (DialogTitle/DialogActions) overstated its own evidentiary coverage
  ("every other demo agrees") in a way a fuller page survey contradicts,
  and the same run under-covered two of its three declared "main
  surfaces" (missed two near-duplicate instances of its own Finding 2
  pattern in `BookmarkedStopPage.tsx`). Neither is caused by this
  round's edits and neither was previously tested; noted for a future
  round, not acted on here.

## 8. Final recommendation

**Keep the refinement.** Across five fresh, independently-verified
regression runs plus four P1 trials, the change caused zero regressions
(no legitimate finding lost, no over-suppression, both previously-
validated combined findings — Case B, Case C — reproduced exactly) and
produced a measurable, verified reduction in citation fabrication (the
VERBATIM self-check's specific target) across every fixture tested,
Cloudscape and MUI alike. The equally-valid-candidate-suppression gate
did not achieve its primary goal on the P1 isolating case in any of four
attempts, but it did not make anything worse, and it visibly shifted the
failure from outright evidence-suppression/fabrication toward transparent
(if ultimately unpersuasive, or in v4's case genuinely arguable)
reasoning that a reader can audit and disagree with — which is a real, if
partial, improvement in reviewability even where it isn't yet a fix.

**This is not "the P1 axis is fixed."** A future round should not treat
this refinement as having resolved equally-valid-candidate suppression.
Recommended before claiming otherwise: (1) build a second P1-shaped
isolating case without the header-comment confound identified in §3, to
re-test the gate on a cleaner instrument; (2) if it still fails there,
treat this as evidence the failure is not reachable by wording-level
instruction-following at all, and consider whether the fix belongs in a
different layer (e.g., a mandatory adversarial self-check pass before
finalizing high-materiality findings, structurally separate from the
generation pass) rather than a further SKILL.md paragraph.

## Artifacts

- `runs-postfix/case-p1{,-v2,-v3,-v4}-skill.md`, `case-p1{,-v2,-v3}-verify.md`
  — four fresh P1 trials and three adversarial verifications (v4 checked
  directly in-session against live fixture/authority text, per §3).
- `runs-postfix/case-b-skill.md` / `case-b-verify.md`,
  `case-c-skill.md` / `case-c-verify.md` — Cloudscape regression set.
- `runs-postfix/checkmate-skill.md` / `checkmate-verify.md`,
  `ntfy-skill.md` / `ntfy-verify.md`, `hkbus-skill.md` / `hkbus-verify.md`
  — MUI regression set.
