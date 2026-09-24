# identity-authority-audit — Review-mode structural fix follow-up (2026-09-24)

**Status:** complete — 30 fresh with-skill runs generated and graded
against a targeted `SKILL.md` change plus two corrected grading keys.
**Separate experiment artifact.** This does not overwrite or supersede
`evals/identity-authority-audit/RESULTS.md` (iteration-1) or
`../2026-09-24-reliability-baseline/RESULTS.md` (the 80-run
with-skill/baseline experiment this pass follows up on). All three remain
authoritative for what they cover.

## What this experiment is

PR #58's prior 80-run experiment found case-110 underperforming baseline
(7/10 vs. 9/10 pass), with a specific, citable failure signature: three
with-skill runs created a Confirmed- or Likely-tier finding whose own
"Unresolved uncertainty" text conceded the defect's existence was
unresolved — a self-contradiction internal to the run's own text. This
pass:

1. Changed the Review-mode report structure in `SKILL.md` to give
   genuine uncertainty a legitimate home outside `## Findings`.
2. Changed the Review finding template's next-step field from asking for
   a fix to asking for verification.
3. Reread case-107's and case-112's grading-key "Deliberate tradeoff" /
   "HIGH severity" post-hoc widenings against their fixtures and
   corrected both where the evidence didn't support the earlier credit.
4. Reran case-110 (n=10), case-102 (n=5), case-106 (n=5), case-107 (n=5),
   and case-112 (n=5) with-skill only, against the edited skill, and
   graded every run directly against the (in three cases, corrected)
   keys.

No baseline (no-skill) reruns were done in this pass — the existing
baseline numbers from the reliability-baseline experiment remain the
comparison point for case-102/106/110.

## Task 1 & 2: the exact `SKILL.md` change

**Before:** Review mode's report template had one `## Findings` section
holding every tier (Confirmed, Likely, Ambiguity requiring verification,
Deliberate tradeoff, Organization-specific convention), each entry ending
in a "Smallest useful next check or change" field. The tier-selection
prose said a finding mixing a structural fact with an unresolved
consequence could be split into "structural fact Confirmed, consequence
Likely" — but had no floor: nothing stopped a run from parking a
fundamentally unresolved question at "Likely" and leaving it inside
Findings anyway.

**After** (`skills/identity-authority-audit/SKILL.md`):

- Added an explicit **admission rule** immediately after the existing
  fact/consequence-splitting paragraph: if an unresolved fact could
  determine whether the claimed defect exists *at all* — not merely its
  severity, scope, or exploitability — Confirmed/Likely is unavailable
  for it at any level, however hedged. The test given: "could naming
  this missing fact resolve to 'no defect here' about as easily as it
  resolves to 'defect confirmed'?" If yes, it's not a finding, it's an
  open question.
- Added a new report section, **`## Open questions / ambiguities`**,
  between `## Findings` and `## Paved-road opportunities`, with its own
  per-item template (What is visible / What remains unknown / What
  evidence would resolve it). The Ambiguity-requiring-verification tier's
  definition was updated with one added sentence directing it here, not
  to Findings.
- Renamed the Findings template's next-step field from **"Smallest
  useful next check or change"** to **"Next verification step,"** and
  added one paragraph stating plainly that a Review finding's next step
  names what would verify or falsify it — a fact to check, not a
  mechanism to build — with a worked contrast example, and that
  remediation belongs to a separate Design pass.
- `## Findings`' own intro line now states explicitly which tiers belong
  there (Confirmed/Likely/Deliberate-tradeoff/Organization-specific-
  convention) and restates the admission-rule gate for Confirmed/Likely
  specifically.

**Deliberately not touched:** the five-tier vocabulary itself (Confirmed
/ Likely / Ambiguity / Deliberate tradeoff / Organization-specific
convention), the HIGH/MEDIUM/LOW severity definitions, Explain mode,
Design mode, the engagement-profile block, framework-signals reference,
and every other section of `SKILL.md`. This is a report-mechanics and
admission-control change, not a rewrite.

## Task 3: case-107 grading-key correction

The prior key credited "Deliberate tradeoff" for the hardcoded
reconciliation allow-list, citing the code comment as "explicitly
stat[ing] the rationale for choosing a hardcoded list over the org's
policy engine." Rereading `ledger_service_reconcile_handler.py`'s actual
comment against `SKILL.md`'s own Deliberate-tradeoff definition ("the
evidence shows a team chose this knowingly ... explaining why"): the
comment states *that* a hardcoded list was used instead of the central
policy engine, and explains why the hardcoding remains *safe* ("every
caller still goes through the signature/issuer/audience verification
below"). It never states *why* hardcoding was chosen over the central
policy engine. That is a comment documenting current mechanics and
safety, not a documented deliberate choice with a rationale for the
choice itself. The prior credit was retracted; the key was corrected to
treat "Deliberate tradeoff" as a partial miss on label precision (not a
full pass, and not a security failure) unless a run's own cited evidence
goes beyond the safety rationale to an actual reason for the choice.

## Task 4: case-112 severity correction

The prior key credited Confirmed/HIGH for the over-broad Vault-issued
database role, by analogy to case-105 (a UI-only auth gap rated HIGH "on
reachability alone"). Rereading the analogy: case-105's HIGH rested on a
directly shown fact — no server-side check at all, so any caller reaching
the endpoint could trigger the write immediately. Case-112 has no
equivalent shown fact: the excess grant sits behind a credential only one
already-authorized service holds, and that service's own code never
issues a write. Turning the excess grant into an actual destructive write
requires a separate, unshown compromise (SQL injection, credential leak,
or service compromise). Equating "the credential technically has write
capability" with "a sensitive write is directly reachable without
authorization" is exactly the conflation `SKILL.md`'s evidence discipline
forbids. The key was corrected: **MEDIUM** is the primary/correct
severity; HIGH is credited only when a run explicitly reasons about
reachability rather than asserting it, and a flat HIGH with no such
acknowledgment is graded as a confidence-tier violation.

## Case-110 before/after — the primary result

| | With-skill (before, n=10) | With-skill (after, n=10) |
|---|---|---|
| **Pass rate** | 7/10 (70%) | **9/10 (90%)** |
| **Forbidden-finding / self-contradiction rate** | 3/10 (30%) | **1/10 (10%)** |
| **Self-contradicting tier/uncertainty signature specifically** | 3/10 (30%) | **1/10 (10%)** |
| Positive-recognition (T2, 4 required controls) | avg 3.8/4 | **10/10 runs at 4/4** |

Baseline (no-skill, from the prior experiment, not rerun here): 9/10
pass, 1/10 forbidden — the with-skill result has closed the gap from a
20-point deficit to a 10-point deficit against a baseline whose own
apparent strength on this case was, per the prior experiment's own
analysis, substantially driven by an out-of-scope business-logic bug
(refund idempotency) that isn't an identity/authority defect at all and
that no with-skill run raised, correctly, in either round.

**Raw counts, this round's one failure (run-03 of 10):** two findings;
one ("denials aren't audit-logged," Confirmed/MEDIUM) is well-calibrated
— its hedge narrows to a claim that stands regardless of the unresolved
external-logging fact. The other ("refund authorization is
session-level, not per-instance," Likely/MEDIUM) is the residual failure:
its own hedge ("if [the console confirms each refund], practical
exposure is smaller") does not foreclose the console fully supplying the
missing assurance, which is exactly the kind of existence-determining
fact the new admission rule is meant to route to Open questions instead —
and which every other run in this batch that touched the same topic
(runs 06, 08, 09) correctly did route there, several explicitly applying
the "resolve to no defect as readily as defect" test in their own words.

**Reading this honestly:** the structural intervention materially
improved case-110 (this is not "layering prose" — see "What changed" for
why this is a mechanics/admission-control fix, not additional guidance
text) but did not fully eliminate the failure signature. One run in ten
still assigned a Findings-tier label to content whose own hedge
undercuts it. This is evidence the fix works — the rate roughly halved,
and the vocabulary's availability alone did not stop being misapplied in
100% of cases — not evidence the report-structure problem is now fully
solved by text alone.

## Regression checks: case-102 and case-106

**case-106 (n=5): no regression.** 5/5 pass (matching the prior 10/10
exactly): zero BFF demands, zero "browser tokens are inherently unsafe"
claims, the 8-hour-lifetime wrinkle held at Deliberate tradeoff in every
run, and the `db.js`-dependent unknowns (list-endpoint scoping,
PATCH field-level authority) were consistently and correctly placed in
the new `## Open questions / ambiguities` section rather than promoted
into Findings or silently dropped. See `grading_out/case-106-with-skill.md`.

**case-102 (n=5): a real, honestly-reported gap, most plausibly sampling
noise rather than a regression.** 3/5 pass on the core test (audience-gap
exploitability capped at Likely, not Confirmed) versus the prior 8/10
with-skill baseline. Both failures are the same pre-existing failure
signature the original 80-run experiment already documented once (1/10)
— treating "no infra config visible in this repository" as settling "no
gateway exists in production" — applied to a Confirmed+HIGH tier pairing
rather than a new failure mode. The raw structural facts (raw forwarding,
`verify_aud=False`) were correctly reported as Confirmed in Findings in
all 5 runs; the new admission rule did not cause the real defect to be
hidden in Open questions. n=5 is too small to separate a real regression
from noise around a baseline rate this close to zero already — a 1-2 run
swing moves the rate from "matches baseline" to "looks concerning." See
`grading_out/case-102-with-skill.md` for the full per-run reasoning and
why this is reported as a named, unresolved gap rather than smoothed
into the aggregate.

## Grading-key corrections: verification reruns

**case-107 (n=5):** primary security test 5/5 pass (unchanged from the
prior 10/10 — no manufactured delegation demand, no escalation). The
specific thing this rerun checked — whether the corrected label-precision
rule discriminates real differences — held up: 4/5 runs used "Deliberate
tradeoff" while asserting the comment "states the rationale directly" for
the choice itself (the exact over-read the corrected key retracts credit
for, graded as a partial miss on precision, not a failure); 1/5 declined
to make that Findings-tier claim at all and instead treated the wrinkle
as a paved-road observation — the corrected key's own preferred
treatment, and a measurably more precise report. See
`grading_out/case-107-with-skill.md`.

**case-112 (n=5):** 1/5 clean pass (Confirmed/MEDIUM with correct
severity reasoning — proof this calibration is reachable under the
current skill text), 3/5 fail (Confirmed/HIGH with inadequate or
self-contradicting reachability acknowledgment), 1/5 partial (Likely/HIGH,
better-hedged but on a different axis than the one the corrected key
names). Most with-skill runs still default to HIGH by treating "the
credential technically has write capability" as sufficient — a
pre-existing tendency the original, pre-correction key rewarded (and
that this pass's SKILL.md edits were not aimed at fixing; Task 1/2
targeted existence-uncertainty, not severity calibration). See
`grading_out/case-112-with-skill.md` for the full reasoning and why no
further skill edit is prescribed by this finding.

## What this proves / what this does not prove

**Suggestive of:** a targeted report-structure change (an explicit
admission rule plus a dedicated home for genuine uncertainty) measurably
reduces, but does not eliminate, the specific self-contradiction failure
this pass targeted (30%→10% on case-110, the case the 80-run experiment
identified as the clearest instance of the problem), with no observed
regression on the two adjacent cases (106 clean; 102 a same-signature,
small-n gap that is more likely noise than a new failure mode, honestly
flagged rather than hidden). The two grading-key corrections are
independently defensible against their fixtures' actual text (not just
asserted) and produce coherent, discriminating grades across 10 fresh
samples.

**Does not prove:** this is 30 runs across 5 cases, one model
(claude-sonnet-5), one grading pass, self-graded by the orchestrating
session rather than an independently recruited reviewer — the same
methodological gap named in both prior experiments for this skill
family. n=5 per regression/verification case is not enough to bound
case-102's true rate tightly (a 1-2 run swing changes the read
substantially), and no baseline (no-skill) condition was rerun in this
pass at all, so there is no fresh evidence of whether an unguided model's
relative performance on these five cases has shifted. Case-110's
remaining one-in-ten failure means the report-structure fix is a real,
partial mitigation, not a guarantee — the vocabulary and structure
narrow the space for a tier claim to outrun its own hedge, but a model
can still write a finding whose rescue clause downplays rather than
forecloses the unresolved fact, and no purely textual `SKILL.md`
instruction fully closes the gap between "concedes uncertainty
somewhere in the finding" and "correctly routes that uncertainty to the
right report section." Case-112's severity-calibration gap (4/5 runs
still defaulting toward HIGH) shows the admission-rule mechanism, while
it generalizes usefully in spirit, was not specifically aimed at and does
not fully solve severity-tier discipline the way it improved
existence-tier discipline on case-110.
