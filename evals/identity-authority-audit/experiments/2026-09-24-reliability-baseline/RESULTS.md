# identity-authority-audit — reliability/baseline experiment (2026-09-24)

**Status:** complete — 80/80 runs generated, graded, aggregated.
**Separate experiment artifact.** This does not overwrite or supersede
`evals/identity-authority-audit/RESULTS.md` (the iteration-1 pressure-suite
results) or the independent adversarial review referenced in this
session's prior context. Both remain the authoritative record for what
they cover; this file covers only the reliability/baseline slice defined
below.

## What this experiment is

Four cases (102, 106, 107, 110) from `evals/identity-authority-audit/`,
each run 10 times with-skill and 10 times baseline (no skill), all
independent, isolated, fresh-subagent runs — 80 total. Every run was
graded after the fact against a frozen rubric. Model: claude-sonnet-5
throughout (both conditions, all runs, same session).

## Methodology

**Frozen before any run** (checksummed, verified unchanged before
dispatch and again after all 80 runs + grading completed —
`frozen/CHECKSUMS.sha256` and `FREEZE-MANIFEST.sha256`, both re-verified
clean at the end):

- `skills/identity-authority-audit/SKILL.md` and both references
  (`framework-signals.md`, `organization-profile-template.md`), copied
  verbatim.
- The four cases' fixture files and `context.md`, copied verbatim.
- The four cases' existing `grading/case-1XX.expected.md` narrative keys,
  copied verbatim.
- A derived `frozen/grading/RUBRIC.md`: an operational Required/Forbidden/
  Tracked checklist per case, built from the existing narrative keys plus
  the tracked signals specified for this experiment (case-102: absence-
  as-proof discipline, unresolved-external-enforcement handling, tier
  assigned to downstream-authorization claims; case-106: BFF-demand /
  browser-token-unsafe / architecture-recognition / 8-hour-lifetime
  severity; case-107: workload-identity understanding, unnecessary auth
  findings, tradeoff-vs-convention labeling and evidentiary support;
  case-110: substantive finding count, generic MFA/step-up findings,
  unsupported replay/scoping speculation, positive-recognition,
  ambiguity-escalation).
- Eight prompt template files (one per case×condition), assembled by
  script from the frozen sources so every run in a group received
  byte-identical task material.

Nothing in `frozen/` was touched after this point. No SKILL.md, fixture,
prompt, or grading-key edit occurred during generation or grading.

**With-skill runs:** fresh `general-purpose` subagent, given `SKILL.md`
and both references verbatim plus the case's evidence, instructed to
follow the skill's exact mode selection and report template, restricted
to a single `Write` call for output (no Read/Grep/Glob/Bash/Web tools
beyond the one prompt-file read), no sibling-run or grading-key access.

**Baseline runs:** fresh `general-purpose` subagent, given only the same
case evidence and a one-line task framing (no skill, no imposed
template/vocabulary), same tool restriction, same isolation.

**Grading:** eight fresh grading subagents (one per case×condition),
each given the frozen RUBRIC section, the original narrative key, and
its group's 10 raw run files. Each run was scored independently on its
own text before any cross-run comparison, per the protocol in
`frozen/grading/RUBRIC.md`. Baseline runs' unstructured prose was mapped
to the nearest Required/Forbidden item and nearest
Confirmed/Likely/Ambiguity + HIGH/MEDIUM/LOW equivalent, marked
"(mapped)" throughout the per-case grading reports in `grading_out/`.

**Raw artifacts:** all 80 raw run files are in `runs/<case>/<condition>/
run-NN.md`; the 8 full grading reports (per-run tables plus citation-
backed justification for every non-obvious call) are in `grading_out/
case-1XX-<condition>.md`. This file is the aggregated summary; the
grading reports are the underlying evidence for every number below.

## Grading-key defects found

None. No grading agent flagged a rubric item as unusable or a case's
Required/Forbidden list as internally inconsistent. One minor
interpretation ambiguity is worth recording for future revision, not
correction now (per instructions, nothing in `frozen/` was edited during
the experiment): case-110's rubric text for tracked item T1 ("substantive
Confirmed/Likely finding count, target 0") is unambiguous for the
with-skill condition, where every finding uses the skill's own tier
vocabulary. For baseline prose, the two grading agents independently
adopted a workable but not pre-specified convention — count a finding
toward T1 whenever the run states something with confident,
non-speculative certainty (whether or not it touches identity/authority
at all), since R5 only requires groundedness, not absence of findings.
This produced case-110 baseline's T1 average of 3.1 (driven almost
entirely by a real, code-grounded, but out-of-scope-for-this-skill bug —
see "What the results show" below), which is not comparable at face
value to case-110 with-skill's T1 average of 0.5. This is noted, not
corrected, and is accounted for in the analysis below.

## Numeric summary — raw counts and percentages

### Pass rate

| Case | With-skill | Baseline |
|---|---|---|
| 102 | 8/10 (80%) | 6/10 (60%) |
| 106 | 10/10 (100%) | 4/10 (40%) |
| 107 | 10/10 (100%) | 10/10 (100%) |
| 110 | 7/10 (70%) | 9/10 (90%) |
| **Total (n=40 each)** | **35/40 (87.5%)** | **29/40 (72.5%)** |

### Forbidden-finding rate (share of runs firing ≥1 forbidden item)

| Case | With-skill | Baseline |
|---|---|---|
| 102 | 1/10 (10%) | 4/10 (40%) |
| 106 | 0/10 (0%) | 6/10 (60%) |
| 107 | 0/10 (0%) | 0/10 (0%) |
| 110 | 3/10 (30%) | 1/10 (10%) |
| **Total** | **4/40 (10%)** | **11/40 (27.5%)** |

### Unsupported-finding rate (share of runs with ≥1 unsupported claim)

| Case | With-skill | Baseline |
|---|---|---|
| 102 | 2/10 (20%) | 4/10 (40%) |
| 106 | 1/10 (10%) | 2/10 (20%) |
| 107 | 0/10 (0%) | 1/10 (10%) |
| 110 | 3/10 (30%) | 1/10 (10%) |
| **Total** | **6/40 (15%)** | **8/40 (20%)** |

### Confidence-tier violation rate

| Case | With-skill | Baseline |
|---|---|---|
| 102 | 1/10 (10%) | 4/10 (40%) |
| 106 | 1/10 (10%) | 6/10 (60%) |
| 107 | 0/10 (0%) | 0/10 (0%) |
| 110 | 3/10 (30%) | 1/10 (10%) |
| **Total** | **5/40 (12.5%)** | **11/40 (27.5%)** |

### Mode-drift rate

| Case | With-skill | Baseline |
|---|---|---|
| 102 | 0/10 (0%) | 0/10 (0%) |
| 106 | 1/10 (10%) | 1/10 (10%) |
| 107 | 0/10 (0%) | 0/10 (0%) |
| 110 | 1/10 (10%) | 0/10 (0%) |
| **Total** | **2/40 (5%)** | **1/40 (2.5%)** |

### Severity distribution (of the tier/severity assigned to each case's
central, case-defining claim — not every bonus finding; see each grading
report for the full per-finding tally)

- **case-102** (downstream-authorization consequence, the case's core
  discrimination test): with-skill — 9/10 correctly capped at
  Likely/Ambiguity or an explicit fact/consequence split, 1/10 (run-07)
  flat Confirmed/HIGH with zero hedge; baseline — 6/10 correctly capped,
  4/10 flat Confirmed/HIGH with zero hedge.
- **case-106** (8-hour-lifetime wrinkle, the case's secondary trap):
  with-skill — 10/10 correctly held at Deliberate-tradeoff/LOW, 0
  escalated; baseline — 4/10 held at LOW (mapped), 6/10 escalated to
  MEDIUM (mapped), 0 to HIGH.
- **case-107** (allow-list wrinkle): with-skill — 10/10 Deliberate
  tradeoff or equivalent, 0 escalated; baseline — 9/10 Deliberate
  tradeoff/convention (mapped), 1/10 not raised at all, 0 escalated.
- **case-110** (main/highest finding on the coherent-design system):
  with-skill — 6/10 Ambiguity (no tier), 1/10 Confirmed/LOW, 1/10
  Likely/MEDIUM, 2/10 Likely/HIGH; baseline — 4/10 Confirmed/HIGH, 4/10
  Confirmed/MEDIUM, 2/10 Likely/MEDIUM (all ten runs' "main finding" here
  is the out-of-scope refund-idempotency bug, not an identity/authority
  defect — see below).

## Per-case tracked-signal detail

**case-102** — absent-gateway-evidence discipline is the case's whole
test. With-skill: 9/10 runs explicitly distinguished "the audience gap
is a confirmed code fact" from "whether it's exploitable in production is
unresolved without gateway evidence," naming the external-enforcement gap
as unresolved (T1) rather than dropping it; 1/10 (run-07) explicitly
declared "no unseen enforcement layer to point to here" and rated the
full consequence Confirmed/HIGH — a clean instance of treating absence of
repo-local evidence as proof of absence. Baseline: 6/10 did the same
discrimination correctly (four of them explicitly separating "a fact
about this repository's call graph" from "an enforced security
boundary"); 4/10 stated the downstream consequence as flat fact with no
gateway caveat at all.

**case-106** — no run in either condition demanded a BFF or claimed
browser-held tokens are inherently unsafe (0/20 total for both forbidden
items); all 20 runs positively named the architecture's coherent
properties. The entire measured gap between conditions is the secondary
trap: with-skill kept the 8-hour-lifetime detail at Deliberate-
tradeoff/LOW in 10/10 runs; baseline elevated it to an asserted,
actionable MEDIUM-level finding ("the real gap," "the real finding," "a
real blast-radius amplifier") in 6/10 runs, in several cases naming it as
the review's headline conclusion and recommending concrete remediation
with no cited XSS finding, observed leak, or compliance requirement.

**case-107** — both conditions correctly understood workload identity and
never manufactured a user-delegation demand (0/20 total for that
forbidden item) or an unnecessary auth finding against the hardcoded
policy (0/20). Tier/label choice for the allow-list wrinkle: with-skill
used a formal "Deliberate tradeoff" heading in 8/10 and an implicit-but-
still-correctly-capped version in 2/10 (both credited, per the earlier
case-107 grading-key note that either label is acceptable when evidence-
supported); baseline used "Deliberate tradeoff" language in 8/10, "LOW
paved-road/Organization-specific convention" in 1/10, and simply didn't
raise the wrinkle in 1/10 (which trivially satisfies "don't escalate it").
Every label in both conditions was judged evidence-supported.

**case-110** — this is the one case where with-skill (70%) underperformed
baseline (90%), and it is worth stating plainly rather than smoothing
over. Substantive-finding count (T1, target 0 for the identity/authority
core): with-skill averaged 0.5, baseline averaged 3.1 — but that
baseline number is driven almost entirely by a real, code-grounded
`refund_order` double-refund/idempotency bug (no status check before a
repeat `UPDATE`) that all 10 baseline runs independently found and that
is explicitly outside this skill's declared scope (a business-logic/
state-integrity bug, not an identity/authority fact) — SKILL.md's own
"what this skill refuses to do" section does not cover it, and no
with-skill run raised it. Generic MFA/step-up findings: with-skill fired
this pattern (F1) in 1/10 runs (run-05, "no differentiated assurance…
beyond scope membership," Likely/MEDIUM); baseline fired the matching
pattern in 1/10 runs (run-04, a step-up "confirmation step" with no
evidence-based trigger). Unsupported replay/scoping speculation (F3):
with-skill fired in 2/10 runs (run-07 and run-10, both proposing narrower
per-order-type/time-boxed refund scoping as a finding rather than a named
unknown); baseline fired the same pattern in the same run-04. Positive
recognition of the four coherent controls (T2, 0–4): with-skill averaged
3.8/4, baseline averaged 4.0/4 — baseline named all four controls
explicitly in every single run. Ambiguity being incorrectly escalated:
the three with-skill failures (run-05, run-07, run-10) share one exact
signature — each finding's own "Unresolved uncertainty" text concedes
the true support level is only Ambiguity, while the finding's own header
tier claims Confirmed or Likely. This is a self-contradiction internal to
the run's own text, not an inferred judgment call, and it is the clearest
single failure pattern in the entire 80-run set.

## With-skill vs. baseline

With-skill outperformed baseline on pass rate (87.5% vs. 72.5%),
forbidden-finding rate (10% vs. 27.5%), and confidence-tier violation
rate (12.5% vs. 27.5%) in aggregate. That aggregate advantage is not
uniform across cases — it is concentrated in 102 and especially 106 (where
baseline's forbidden rate, 60%, is the single worst cell in the whole
table), roughly a wash on 107 (both conditions clean), and reversed on
110, where with-skill's forbidden rate (30%) is three times baseline's
(10%) and its pass rate is 20 points lower. Unsupported-finding rate is
close between conditions overall (15% vs. 20%) and, unusually, favors
baseline. Mode-drift rate is low and roughly comparable in both
conditions (5% vs. 2.5%), and on the one case where it appeared in both
(106), the with-skill and baseline drift instances are structurally the
same shape (an out-of-scope XSS/reliability tangent, self-labeled as
adjacent in both cases) — evidence that mode drift here is a shared
tendency of the underlying model on ambiguous review prompts, not
something either condition specifically induces or specifically guards
against.

The case-110 reversal is the most important single finding in this
experiment and should not be summarized away by the aggregate. Reading
the grading reports' per-run citations (not just the tallies), the
failure mode in the three failing with-skill runs is not "the skill's
guidance was wrong" — SKILL.md's own evidence-discipline and tier-
splitting language (quoted verbatim in the RUBRIC and cited by the
grading agent) directly forbids exactly what these three runs did. The
failure is that having a formal Confirmed/Likely/Ambiguity vocabulary
available did not stop three of ten runs from reaching for a HIGH/MEDIUM-
sounding tier label for a speculative concern and then hedging it away in
the same finding's own "Unresolved uncertainty" line — the vocabulary
was used inconsistently within a single finding rather than misapplied
outright. Baseline, writing unstructured prose with no tier labels to
reach for, produced the equivalent judgment error in only one run (run-04
on case-110), and that run's error is the same content (a generic step-up
demand, unsupported velocity/scoping speculation) without the added
self-contradiction of a formal tier claim next to a hedge that undercuts
it. This suggests the skill's tiering vocabulary is a genuine asset when
applied consistently (case 102, 106, 107 all show this) but is not a
self-enforcing guardrail — a run can hold a correct definition of
"Ambiguity" in one paragraph and assign "Likely, HIGH" to a materially
identical claim two paragraphs later, and the vocabulary alone does not
catch that internal inconsistency the way baseline's absence of a formal
severity system incidentally avoided it here.

## Does fixture-comment narration explain baseline's performance?

Partially, and unevenly across the four cases — this is a real effect,
not absent, but it does not fully explain baseline's results, and it
explains different things on different cases.

**Where narration plausibly does most of the work:** case-107's fixture
comments are the most direct of the four — `ledger_service_reconcile_
handler.py`'s allow-list comment states its own rationale in full
sentences, and `nightly_reconciliation_job.py`'s and the handler's
docstrings both state outright that there is no per-user resource and no
human ever in the loop. Both conditions hit 10/10 pass with 0% forbidden
rate, and the baseline grading report explicitly notes that "the task
framing itself named both decoy alternatives explicitly in the prompt,"
making this case's trap unusually visible without any skill scaffolding.
This is the strongest single piece of evidence that a well-commented
fixture plus an unambiguous task framing narrows the gap between
conditions to near zero, and it means case-107's clean 10/10-vs-10/10
result is weaker evidence for the skill's necessity than it might first
appear — it may be evidence that this particular fixture doesn't need a
skill to get right, not that the skill adds nothing in general.

**Where narration correlates with correct positive recognition but not
with correct severity calibration:** case-106's fixture also narrates its
own tradeoff directly (the 8-hour-lifetime comment states the exchange
being made, "one fewer moving part" for "a token that... stays valid for
up to 8 hours"), and both conditions credited the architecture's positive
properties 10/10. But baseline still escalated the severity of that same,
narrated tradeoff to an asserted MEDIUM finding in 6/10 runs despite the
comment handing it the exact framing needed to cap it at LOW. Narration
of "here is the tradeoff and why it was made" did not, on its own,
prevent baseline from treating it as a defect worth pushing on — the
skill's explicit rule (elevating this specific detail past LOW "without
cited evidence of actual exposure" is manufacturing severity) is doing
real, measurable work here that fixture narration alone does not
replicate. Case-110 shows the same pattern in the other direction: its
fixture is arguably the most heavily narrated of the four (explicit
inline comments on every one of the four required controls), and both
conditions named all four almost perfectly (T2 3.8 vs. 4.0) — narration
appears to fully explain the strong positive-recognition numbers in both
conditions — but narration did nothing to prevent either condition's
failure mode (baseline's one generic step-up reflex, with-skill's three
self-contradicting tier escalations), because the fixture's comments
describe what is correct, not what would be incorrect to add.

**Where the fixture does not narrate the answer at all:** case-102's
`api_b.py` docstring states plainly that no infrastructure/gateway
configuration exists "anywhere in this repository" — evidence-absence
language that could be misread either way, and is exactly the kind of
statement the skill's evidence-discipline section is written to guard
against misreading. This is the case with the largest between-condition
gap on the forbidden-finding rate (10% vs. 40%) and the only case where
the skill's specific evidence-discipline framing (not general positive-
property narration) is doing the visible work: with-skill runs
consistently distinguish "a fact about this repository" from "an
enforced boundary" in language that tracks the skill's own "not visible
in the inspected path; verify" phrasing near-verbatim in several runs,
while 4 of 10 baseline runs collapse the two.

**Overall:** the fixtures narrate positive architectural properties
strongly in all four cases (T2/R3-style controls are named correctly at
90%+ in both conditions across the board), and this does measurably
narrow the with-skill/baseline gap on cases 106, 107, and 110's positive-
recognition axis specifically. It does not narrate severity discipline or
evidence-absence handling nearly as strongly, and those two axes are
where the largest and most consistent with-skill advantages appear (case
102's forbidden-rate gap, case 106's confidence-tier-violation gap). The
one case where baseline outperformed with-skill (110) is not explained by
narration doing baseline's work for it — both conditions were equally
well informed by the same comments — it is explained by with-skill's
formal tier vocabulary being available for three runs to misapply in a
way baseline's unstructured prose could not replicate.

## What this proves / what this does not prove

**Suggestive of:** across 80 independent runs (40 with-skill, 40
baseline) on four designed scenarios, the skill measurably reduces
forbidden-pattern and confidence-tier-violation rates in aggregate
(27.5%→10% and 27.5%→12.5% respectively) and improves pass rate in
aggregate (72.5%→87.5%), concentrated specifically in evidence-absence
discipline (case 102) and severity-escalation discipline (case 106).
Fixture-comment narration measurably explains a meaningful share of
baseline's competence at positive-property recognition on all four cases
and appears to explain most of case 107's near-identical performance
between conditions specifically. The skill's tier vocabulary is not a
self-enforcing guardrail against internal inconsistency within a single
finding — case 110 shows a fresh-subagent run can state a correct
Ambiguity-level hedge and an incorrect Confirmed/Likely-level tier label
in the same finding, and the vocabulary's availability did not prevent
that in 3 of 10 runs.

**Does not prove:** this is four cases, ten runs each, one model, one
session, one grading pass (self-graded by the orchestrating session, not
by an independently recruited second reviewer against the frozen
rubric — the same methodological gap the iteration-1 `RESULTS.md` names
for its own suite). It does not establish that the with-skill/baseline
gap generalizes to the other nine cases in the existing suite, to cases
built after this rubric was written, or to a different task framing on
these same four cases (case-107's near-zero gap is explicitly tied to a
task framing that named both decoy alternatives in the prompt itself; an
un-cued framing was not tested). It does not establish causal mechanism
beyond what the grading reports' citations directly support — the
case-110 reversal is described above from the actual finding-level
evidence, not inferred from the aggregate numbers alone, but a stronger
causal claim (e.g., "the tier vocabulary causes overconfidence") would
need a targeted follow-up, not just this observational contrast. It does
not test Explain or Design mode, organization-profile resolution, or any
case outside 102/106/107/110. The N=10 per cell is enough to see the
case-106 and case-110 effects clearly (they are large — 60-point and
20-point pass-rate gaps) but is not enough to bound the true rate on
cases 102's narrower gaps (80% vs. 60%, on n=10 each) with tight
confidence; a 2-3 unit swing in either direction on a re-run would not be
surprising.

## Recommended next step (not acted on in this experiment)

The case-110 finding — three with-skill runs stating a correct Ambiguity-
level hedge and an incorrect Confirmed/Likely tier label in the same
finding — is a real, observed, in-contract failure mode with a specific,
citable signature (check whether a finding's own "Unresolved uncertainty"
text concedes less confidence than the finding's own header tier
claims). Per this repository's "an observed failure justifies a direct
skill edit" convention, this is exactly the kind of finding that would
justify a targeted `SKILL.md` clarification (the same pattern the
iteration-1 suite's case-108 finding produced) — but per this
experiment's explicit instructions, no such edit was made in this
session; SKILL.md was frozen and never touched after the freeze
checkpoint above, verified by the final checksum re-run at the top of
this document.
