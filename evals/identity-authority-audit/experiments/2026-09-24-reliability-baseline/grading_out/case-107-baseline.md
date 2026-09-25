# Grading report — case-107 (genuine-workload-identity-no-user-needed), baseline condition

Graded against `frozen/grading/RUBRIC.md` (case-107 section + Grading protocol +
Cross-case metrics) and `frozen/grading/case-107.expected.md`. Each run graded
independently on its own merits before any cross-run comparison. Baseline runs
carry no imposed vocabulary; Required/Forbidden/Tracked items are mapped to
their nearest substantive equivalent in the run's own prose, marked
"(mapped)" throughout per the task instructions.

All 10 runs answer the same implied Slack-thread framing: "is the missing
user token a gap, and should this run under delegated user credentials or be
attributed to whoever last touched the config?" — the case's two decoy
alternatives are explicit in every run's opening paragraph, indicating the
one-line task framing itself surfaced the trap; grading below still checks
each run's substance rather than assuming the framing did the work.

## Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations (mapped) | Severity of main finding (mapped) | Mode drift | Bonus findings | T1 tracked value (mapped) |
|---|---|---|---|---|---|---|---|---|---|
| run-01 | 5/5 | PASS | none | 1 (borderline) | none | No issue / Confirmed-clean | No | 1 — suggests framing the write-up as "confirm this pattern" for auditors | Not raised (allow-list mentioned only as part of the enforcement mechanism, never flagged as a wrinkle) — R4 vacuously met |
| run-02 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 1 — notes `claims["email"]` as strong audit-trail evidence | Deliberate tradeoff — supported (cites "the code comment calls this out as a deliberate choice") |
| run-03 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 3 — allow-list governance, `email_verified`-guarantee confirmation, bucket-scope confirmation | Deliberate tradeoff — supported (cites "the comment says this is deliberate") |
| run-04 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 2 — allow-list migration note, IAM-bindings/logging-outside-evidence note | Deliberate tradeoff — supported (cites "the code comment says this is deliberate") |
| run-05 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 1 — allow-list "paper trail" confirmation note | Deliberate tradeoff — supported (cites "the code comments that this is deliberate") |
| run-06 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 1 — recommends code-review/approval + log-retention practice | LOW paved-road / Organization-specific convention — supported (grounded in the hardcode-vs-centralized fact and the verification-ordering reasoning; does not explicitly quote the code comment's stated rationale) |
| run-07 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 3 — allow-list stewardship, service-account blast-radius confirmation, deploy-pipeline governance | Deliberate tradeoff — supported (cites "the comment... explicitly notes" the rationale) |
| run-08 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 1 — allow-list governance note | Deliberate tradeoff — supported (cites "the code comment... acknowledges this is deliberate") |
| run-09 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 2 — allow-list note + suggestion to centralize "if one exists and this pattern is used elsewhere" | Deliberate tradeoff — supported (cites "the handler's own comment... notes every caller still goes through full signature/issuer/audience verification first") |
| run-10 | 5/5 | PASS | none | 0 | none | No issue / Confirmed-clean | No | 1 — allow-list tradeoff confirmation note | Deliberate tradeoff — supported (cites "the comment says every caller still goes through full signature/issuer/audience verification regardless") |

Required items (mapped to baseline prose):
- R1 (mechanism correctly characterized: short-lived, single-audience OIDC token, metadata server / GCP Workload Identity, no static key) — met in all 10.
- R2 (no manufactured missing-user/delegation finding; states plainly no user principal is expected) — met explicitly and emphatically in all 10; every run opens with an explicit rejection of both decoy alternatives.
- R3 (destination-side enforcement characterized correctly: verify signature/issuer/audience, then a separate allow-list authorization decision, not a rubber stamp) — met in all 10, though none of the runs quote the exact function names `authenticate_workload` / `authorize_reconciliation_workload` verbatim as identifiers (they describe the two-step behavior in prose instead) — graded as met by substance per the task's mapping instruction for unstructured baseline prose.
- R4 (allow-list wrinkle, if raised, kept at LOW/tradeoff/convention level) — met in all 10 (9 raise it and keep it low-severity; 1 does not raise it, which trivially satisfies R4).
- R5 (label actually supported by cited evidence) — met in all 10 (9 explicitly cite the code comment's stated rationale or the hardcode-vs-centralized fact; 1 is N/A because the wrinkle was never raised).

Forbidden items — none fired in any run:
- F1 (demand for named-engineer credentials / delegated-user token, or "no user context" flagged as a missing-actor-attribution gap) — not fired in any run; all 10 explicitly argue against both decoys.
- F2 (escalating the allow-list to Confirmed/Likely authority hazard) — not fired in any run.
- F3 (generic ungrounded auth finding against the hardcoded policy, asserted as requiring immediate fix) — not fired in any run; every mention of the allow-list is framed as an optional note/confirmation, not a defect demanding a fix.

## Per-run notes (non-obvious calls only)

**run-01.** Clean pass. The only borderline item: it states "an authenticated-but-unlisted workload still gets a 403" as a flat fact — a specific HTTP-status detail none of the other 9 runs mention, and the run gives no direct quote/line citation for the status code itself (only for the allow-list check's existence). Not disqualifying (it doesn't touch a Required/Forbidden item and is a plausible consequence of the described allow-list check), but flagged as a minor unsupported specific claim since it's asserted with more precision than the run's own citations support. R4/R5 are graded met vacuously because the run never raises the hardcoded allow-list as a wrinkle at all — it only lists it in passing as part of describing the two-step enforcement (R3): *"it checks the verified caller identity against an explicit allow-list (`ALLOWED_RECONCILIATION_WORKLOADS`) before permitting the reconciliation operation."*

**run-02.** Clean pass, and the clearest example of R5 being satisfied: *"The code comment calls this out as a deliberate choice ('every caller still goes through the signature/issuer/audience verification below; this list only decides which already-authenticated workload identity is then permitted to proceed'), and I'd agree it's a reasonable tradeoff."* This directly quotes the rationale comment before applying the "reasonable tradeoff" label, which is exactly what R5 asks for.

**run-03.** Clean pass. Slightly more assertive than most on the allow-list follow-up — *"it does mean adding or removing an allowed workload requires a code change/deploy to this service, so make sure that change path itself is reviewed with the same rigor as any other access grant"* — but this is a process-review recommendation, not an assertion that a defect exists; it stays at the "worth confirming" register rather than escalating to Confirmed/Likely, so F2/F3 do not fire.

**run-04.** Clean pass. Notable for explicitly separating "what's wrong" from "what's unconfirmed": *"None of these are the 'missing user token' issue raised in the original question — that part of the design is sound as-is,"* immediately after listing its own follow-up questions as open items rather than findings — a clean confidence-tier calibration.

**run-05.** Clean pass. Frames the allow-list note carefully as documentation, not a defect: *"One thing I'd flag for the audit, not as a defect but as context worth documenting."* No escalation language anywhere in the run.

**run-06.** The only run whose T1 label doesn't explicitly quote the code comment's stated rationale — it reasons independently from the verification ordering instead: *"it's not a security gap as implemented: every caller still goes through full signature/issuer/audience verification before the allow-list is even consulted."* Because it never writes "the comment says..." or "deliberate," this is mapped to LOW paved-road / Organization-specific-convention rather than Deliberate tradeoff. R5 is still credited as met because the label is grounded in an accurately-described fact about the code (hardcoded vs. centralized, and the check ordering), not asserted without evidence.

**run-07.** Clean pass, most audit-question-heavy run (3 bonus follow-ups). Explicitly ties its tradeoff label to the code comment: *"The comment in `ledger_service_reconcile_handler.py` explicitly notes `ALLOWED_RECONCILIATION_WORKLOADS` is hardcoded rather than sourced from the org's central policy engine... That's a reasonable, deliberate design given the file's own explanation."*

**run-08.** Clean pass. Cleanly separates the required finding from the tracked wrinkle with a dedicated section header ("One thing worth a note in the audit, not a fix") and cites the comment directly: *"The comment in the code acknowledges this is deliberate and notes every caller still goes through full signature/issuer/audience verification first."*

**run-09.** Clean pass. The only run to add an explicit migration suggestion contingent on an unconfirmed premise — *"I'd still suggest sourcing it from the central policy engine if one exists and this pattern is used elsewhere"* — but immediately caps it: *"that's a maintainability improvement, not a security hole,"* keeping it at LOW/tradeoff level and avoiding F2/F3.

**run-10.** Clean pass. Directly quotes the comment's substance and explicitly labels it a tradeoff: *"The comment says every caller still goes through full signature/issuer/audience verification regardless, and the list only gates which already-authenticated identity may proceed -- that's a reasonable tradeoff for a single-entry, rarely-changed list."*

## Group aggregate — case-107, baseline condition

- **Pass rate:** 10/10 (100%)
- **Forbidden-finding rate:** 0/10 (0%) — no run fired F1, F2, or F3
- **Unsupported-finding rate:** 1/10 (10%) — only run-01's unattributed "403" status-code detail; no other run asserted a claim beyond what its own citations supported
- **Confidence-tier violation rate (mapped):** 0/10 (0%) — no run stated something as flatly true/false where the evidence only supported a hedge, and no run hedged something the evidence directly established
- **Mode-drift rate:** 0/10 (0%) — no run demanded a BFF/redesign, assigned a numeric maturity score, or drifted into crypto/TLS/password-policy/general-OWASP/pentesting territory; the extra follow-up questions raised (bucket scope, allow-list governance, service-account blast radius, deploy-pipeline access) all stayed inside the identity/authority scope of the actual evidence
- **Severity distribution (mapped), main finding:** 10/10 "No issue / Confirmed-clean" — no run assigned a Confirmed or Likely identity/authority defect to the overall flow
- **Severity distribution (mapped), allow-list wrinkle specifically:** 9/10 runs raised it, all 9 at LOW / tradeoff / convention level; 0/10 escalated it to MEDIUM/HIGH or Confirmed/Likely; 1/10 (run-01) did not raise it at all
- **T1 label tally (mapped, across 10 runs):**
  - Deliberate tradeoff (evidence-supported, cites the code comment's rationale): 8 — run-02, run-03, run-04, run-05, run-07, run-08, run-09, run-10
  - LOW paved-road / Organization-specific convention (evidence-supported, no direct comment quote): 1 — run-06
  - Not raised: 1 — run-01

## What this does and does not show

This shows that, for this specific case and this specific one-line task
framing, 10/10 baseline (no-skill) runs independently avoided the case's
central trap (manufacturing a user-delegation/attribution finding for a
genuinely workload-owned job) and independently kept the allow-list wrinkle
at low severity with cited rationale. It does not show that the skill is
unnecessary for this case in general: the task framing itself named both
decoy alternatives explicitly in the prompt, which may have made the trap
unusually visible without any skill scaffolding; a framing that only asked
"review this for identity/authority issues" without naming the decoys was
not tested here. It also does not establish baseline reliability on other
cases (102, 106, 110) or under different framings — this is a single
case/condition slice of the broader reliability-baseline experiment.
