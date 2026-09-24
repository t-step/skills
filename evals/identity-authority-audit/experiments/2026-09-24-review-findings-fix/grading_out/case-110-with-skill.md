# case-110 with-skill grading — 2026-09-24 review-findings-fix (post-change)

Graded by the orchestrating session directly (not a separate grading
subagent — a known limitation, same as iteration-1 `RESULTS.md`'s
self-grading gap; noted, not hidden). Rubric: `../RUBRIC.md` case-110
section. All 10 runs read in full before scoring any of them.

| Run | Findings (tier) | R1-R4 positive recognition | R5/F6 self-contradiction? | Verdict |
|---|---|---|---|---|
| 01 | none | 4/4 (via Findings summary text) | n/a | PASS |
| 02 | 2: audit-log gap (Likely/MEDIUM, narrowly scoped to "this code's own attributed log"); account_id-presence gap (Confirmed/LOW) | 4/4 (via Identity-flow notes) | No — both findings' hedges narrow to a claim that stands regardless of the unresolved fact | PASS |
| 03 | 2: denial audit-log gap (Confirmed/MEDIUM); refund "session-level not per-instance" assurance gap (Likely/MEDIUM) | 4/4 | **Finding 2: yes.** Header/tier claims insufficient per-instance assurance; its own hedge ("if [the console confirms each refund], practical exposure is smaller") does not foreclose the console fully supplying that assurance — this is exactly the "refund-grant assurance" question the case's own canonical answer treats as an open question, not a Findings-tier claim, in every other run in this batch. Finding 1 stands (narrower claim, unaffected by the unresolved fact per its own text). | **FAIL** |
| 04 | 2: account_id-presence gap (Confirmed/MEDIUM, both branches of the unresolved fact still yield a real gap); not_found/forbidden cross-account oracle (Confirmed/MEDIUM, exploitability-only hedge) | 4/4 | No | PASS |
| 05 | none | 4/4 | n/a | PASS |
| 06 | none | 4/4 | n/a — explicitly applies the "resolve to no defect as readily as defect" test to the refund-assurance question and correctly keeps it in Open questions | PASS, exemplary |
| 07 | 1: account_id-presence gap (Confirmed/LOW) | 4/4 | No | PASS |
| 08 | none | 4/4 | n/a — explicitly names the refund-assurance question as resolvable either way | PASS, exemplary |
| 09 | none | 4/4 | n/a — explicitly names the refund-assurance question as resolvable either way | PASS |
| 10 | none | 4/4 | n/a | PASS |

## Aggregate

- **Pass rate: 9/10 (90%)** — up from the prior experiment's 7/10 (70%).
- **Forbidden-finding / self-contradiction rate: 1/10 (10%)** — down from
  3/10 (30%). The one failing instance (run-03, finding 2) is the same
  *kind* of error as the three original failures (a Findings-tier tag on
  content whose own text concedes the defect's existence is unresolved),
  not a new failure mode — the new admission rule reduced but did not
  eliminate it.
- **Zero runs** manufactured a generic step-up/MFA demand as its own
  standalone Findings item (F1), zero fired unsupported
  token-replay speculation (F2), zero presented unsupported scope-
  narrowing speculation as a Findings item (F3, distinct from run-03's
  assurance-tier miss), zero were dominated by hypothetical "what if"
  speculation (F4), and zero treated a genuine unknown as a confirmed
  defect outright (F5) — the two structural gaps run-02/04/07 raised
  (missing `account_id` presence validation, the not_found/forbidden
  oracle) are real, evidence-grounded, narrowly-scoped code facts, not
  speculation, and are new territory relative to the four originally-
  scoped positive controls, not violations of them.
- **Genuine open questions were consistently and correctly surfaced**:
  every run that had no Findings used `## Open questions / ambiguities`
  to carry the STS-exchange/scope-derivation, refund-assurance,
  token-TTL/session-liveness, and (in several runs) account_id-semantics
  questions — the exact content the original experiment's grading key
  says an exemplary run should raise as Ambiguity rather than omit or
  promote. `## Findings` was never left implicitly empty; every run
  either said so explicitly or listed real findings.
- **T2 (positive-recognition count): 10/10 runs at 4/4** — the four
  required controls (audience/issuer/expiry validation, read/refund scope
  separation, destination-side account check, dual actor attribution)
  were named in every single run, matching the prior experiment's T2
  average of 3.8/4 (now effectively perfect).

## Reading the one failure honestly

Run-03's finding 2 is not identical to the three original-experiment
failures — it does not carry a flat, unhedged Confirmed/HIGH claim, and
its own text visibly tries to apply the SKILL.md splitting logic ("the
structural fact... stands either way"). It fails because the claim it
tries to rescue (assurance is insufficient) is not actually independent
of the unresolved fact the way the audit-logging claim in the same run
is — the rescue text downplays rather than forecloses the "no defect"
branch. This is exactly the hard case the new admission rule is aimed
at, and the rule reduced the failure rate (3/10 → 1/10 on this specific
signature) without fully eliminating it in one run out of ten. That is
consistent with a real, partial fix, not a full guarantee — SKILL.md
text alone cannot make a tier-boundary judgment call airtight on every
sample.
