# case-107 (genuine-workload-identity-no-user-needed) — with-skill — grading report

Graded independently per run against `frozen/grading/RUBRIC.md`'s case-107 section
and `frozen/grading/case-107.expected.md`. Each run was scored on its own merits
before any cross-run comparison; aggregate stats below are computed only after
all ten are individually graded.

## 1. Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations | Severity of main finding(s) | Mode drift | Bonus findings | T1 tracked value |
|---|---|---|---|---|---|---|---|---|---|
| run-01 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 0 | "Deliberate tradeoff" — supported |
| run-02 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; 2 Ambiguity items; allow-list = Deliberate-tradeoff-equivalent | No | 2: (a) durable persistence of workload attribution in an audit trail unconfirmed (Ambiguity); (b) trigger-hop principal/enforcement not observable (Ambiguity) | "Deliberate tradeoff" (implicit — see paragraph) — supported |
| run-03 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: trigger-invocation authorization not visible in evidence (Ambiguity) | "Deliberate tradeoff" — supported |
| run-04 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: audit trail attributes to the workload, not a named human (Ambiguity) | "Deliberate tradeoff" — supported |
| run-05 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely (two Deliberate-tradeoff findings elaborating R2); allow-list treated in Paved-road section | No | 0 (extra depth is elaboration of R2, not a new finding) | "Deliberate tradeoff" (implicit — see paragraph) — supported |
| run-06 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: runtime attribution vs. config-change attribution distinguished as two different questions (Ambiguity) | "Deliberate tradeoff" — supported |
| run-07 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: Cloud Scheduler → Cloud Run invocation auth not in evidence (Ambiguity) | "Deliberate tradeoff" — supported |
| run-08 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: trigger authentication not in evidence (Ambiguity) | "Deliberate tradeoff" — supported |
| run-09 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely; allow-list = Deliberate tradeoff | No | 1: Cloud Storage read-scope enforcement not independently verifiable (Ambiguity) | "Deliberate tradeoff" — supported |
| run-10 | 5/5 | PASS | none | 0 | none | No Confirmed/Likely ("No confirmed or likely issues were identified in the primary authentication/authorization path"); allow-list = Deliberate tradeoff | No | 0 | "Deliberate tradeoff" — supported |

## 2. Per-run notes

**run-01.** Clean pass, nothing borderline. R1–R3 are satisfied directly in the
identity-flow table row 3 ("`authenticate_workload()` validates signature/
issuer/audience... `authorize_reconciliation_workload()` then checks the
authenticated identity against `ALLOWED_RECONCILIATION_WORKLOADS`"). R4/R5 are
met with a formal Finding heading, "Hardcoded workload allowlist instead of
central policy engine -- Deliberate tradeoff," citing the code comment
verbatim as evidence. No forbidden items fire; the two Slack questions are
answered directly and correctly without manufacturing a delegation gap.

**run-02.** Pass, but the T1 label is the one genuinely non-obvious call in
this batch. Unlike every other run, run-02 does not give the allow-list its
own "-- Deliberate tradeoff" Finding heading; it is discussed only under
"Paved-road opportunities": *"the reconciliation allowlist intentionally does
not use it for the workload-permission decision; the comment names this as a
deliberate choice rather than an oversight."* This still satisfies R4 (never
escalated past a paved-road-level observation) and R5 (the rationale is cited,
even if the sentence "but doesn't say why the policy engine itself wasn't
used" is a slightly more skeptical reading of the same comment other runs
treat as fully self-explanatory). I credit this as "Deliberate tradeoff"
(implicit) rather than mark it a violation, since RUBRIC R4's bar is "kept at
LOW / Deliberate-tradeoff / Organization-specific-convention /
paved-road-observation level," and a Paved-road-opportunities mention with no
escalation clears that bar by name. This run also carries two legitimate,
well-cited bonus Ambiguity findings not present in most other runs (durable
audit-trail persistence; trigger-hop principal).

**run-03.** Clean pass. R1 is satisfied in the Paved-road section ("mints
short-lived, audience-scoped identity tokens on demand with **no static key
checked in anywhere**"), closing the one gap that might otherwise have been
argued (the identity-flow table itself doesn't use the words "no static key").
R4/R5 use a formal "-- Deliberate tradeoff" heading with the comment quoted in
full. The trigger-invocation Ambiguity finding models the skill's evidence
discipline well: *"its absence from this evidence is not evidence it's absent
from the system."*

**run-04.** Clean pass. R2 is met emphatically — "No confirmed or likely
issues were found in this flow. The platform engineer's core question... is
answered directly by the evidence, not left ambiguous" — directly rebutting
the ticket's leading framing rather than hedging around it. R4/R5 met with a
formal Deliberate-tradeoff heading and full comment quote. The bonus
audit-trail-attribution finding is correctly hedged and explicitly avoids
treating the absence of a human name as a gap: *"before treating the absence
of a human name as a gap."*

**run-05.** Pass; same borderline T1 placement as run-02. The allow-list note
appears only in "Paved-road opportunities" ("Org's central policy engine for
workload-identity authorization -- referenced directly... The comment states
this is deliberate... it is not, on this evidence, an authority gap"), not as
a separate Finding with a "-- Deliberate tradeoff" heading. R4/R5 are still
satisfied (not escalated; rationale cited), so this is credited as pass, with
the same caveat as run-02 noted for the T1 tally. This run is otherwise the
most discursive of the ten, splitting R2 into two full Deliberate-tradeoff
Findings ("No user/session in the flow is the documented design, not a gap"
and "'Attribute to whichever engineer last touched the config' would replace
an accurate audit fact with an inaccurate one"), both well-cited — counted as
depth on R2 rather than new bonus findings.

**run-06.** Clean pass. R3 is stated unusually explicitly: *"Authorization is
a hardcoded allow-list, not a central policy engine, per the handler's own
comment explaining that choice"* appears alongside a separate note that
authentication and authorization are two distinct enforcement steps. R4/R5 met
with a formal heading and full comment quote. The bonus finding usefully
separates "who ran this" from "who last edited the config" as two different
audit questions — grounded, not speculative.

**run-07.** Clean pass. R2 met with an unusually direct line: *"A credential
that isn't there can't be delegated."* R3 explicit: *"Destination-side
enforcement is present for both authentication and authorization -- this is
not a UI-only or client-trusted check."* R4/R5 met with formal heading and
full quote. Bonus trigger-ambiguity finding well-hedged.

**run-08.** Clean pass. R1–R5 all satisfied with formal headings/citations,
including an explicit rejection of the engineer-attribution alternative as
*"a weaker attribution model than what's already in place."* Bonus
trigger-authentication-ambiguity finding is well-scoped and explicitly cites
the skill's evidence-discipline principle.

**run-09.** Clean pass. R3 explicitly separates authentication from
authorization in the table notes ("Authorization is destination-side, not
merely authentication; the allow-list is the actual authorization decision").
R4/R5 met with formal heading and full quote. The bonus Cloud-Storage
read-scope finding is a genuinely new angle not raised by most other runs, and
is explicitly bounded ("this is a read-only capability, so the consequence
class is bounded").

**run-10.** Clean pass, most concise of the ten. R2 is stated as a flat,
well-supported conclusion: *"there is nothing to delegate forward... Running
the job 'under someone's delegated credentials' would manufacture a
delegation where none exists in this flow."* R4/R5 met with formal heading and
full comment quote. No findings beyond the required allow-list item; the
report explicitly states "No confirmed or likely issues were identified in
the primary authentication/authorization path" as its closing summary of the
core flow.

## 3. Group aggregate (case-107, with-skill, n=10)

- **Pass rate:** 10/10 (100%)
- **Forbidden-finding rate:** 0/10 (0%) — no run fired F1 (manufactured
  user-delegation demand), F2 (escalated allow-list to Confirmed/Likely), or
  F3 (generic ungrounded auth finding against the hardcoded policy).
- **Unsupported-finding rate:** 0/10 (0%) — every required, forbidden-adjacent,
  and bonus claim across all ten runs carried a specific file/comment/docstring
  citation at a certainty level the citation actually supports.
- **Confidence-tier violation rate:** 0/10 (0%) — no run asserted Confirmed
  where only Likely/Ambiguity was supportable, escalated the allow-list past
  Deliberate-tradeoff, or under-hedged a directly-established fact (e.g. the
  scheduler-invocation-IAM ambiguity findings, present in 6/10 runs, were
  uniformly and correctly hedged as "absence of evidence ≠ evidence of
  absence" rather than asserted as a missing control).
- **Mode-drift rate:** 0/10 (0%) — no remediation/redesign demand asserted
  where only review was requested, no maturity score, no drift into
  crypto/TLS/password-policy/OWASP/pentesting territory in any run.
- **Severity distribution:**
  - Main flow (primary identity/authority conclusion): Confirmed = 0,
    Likely = 0, in all 10/10 runs — every run reached "no confirmed or likely
    issue" for the core workload-identity flow.
  - Required allow-list wrinkle (T1 item): Deliberate tradeoff (or
    Deliberate-tradeoff-equivalent) = 10/10, all supported per R5; Confirmed
    or Likely = 0/10.
  - Bonus Ambiguity findings beyond the required list: 8 total instances,
    spread across 7/10 runs (run-02 ×2; run-03, run-04, run-06, run-07,
    run-08, run-09 ×1 each; run-01, run-05, run-10 ×0). All 8 correctly
    tiered Ambiguity/requiring-verification, none escalated, none
    unsupported.
- **T1 label tally (allow-list wrinkle, n=10, all judged supported per R5):**
  - "Deliberate tradeoff" (formal Finding heading, exact phrase): 8/10
    (run-01, run-03, run-04, run-06, run-07, run-08, run-09, run-10)
  - "Deliberate tradeoff" (implicit — raised only under "Paved-road
    opportunities," described in prose as "deliberate"/"knowingly bypassed"/
    "intentional, evidenced bypass" rather than given its own Finding
    heading, but never escalated): 2/10 (run-02, run-05)
  - "Organization-specific convention": 0/10
  - "LOW paved-road observation" (standalone, no deliberate-tradeoff framing):
    0/10
  - "Other" / unsupported: 0/10

**What this shows / does not show:** across this batch, the with-skill
condition produced a perfectly uniform pass rate and zero forbidden triggers
or confidence-tier violations for case-107 — strong, consistent adherence to
the skill's "no user needed here" and "allow-list is a tradeoff, not a
defect" guidance. It does not show that the skill guarantees this outcome in
general; n=10 on one case is not evidence about other cases or about
adversarial/edge-case pressure on this same scenario, and the two borderline
T1-placement calls (run-02, run-05) indicate some real variance in how
strictly runs follow the report template's per-item tier-heading convention
even when the underlying judgment is correct.
