# Grading rubric — 2026-09-24 review-findings-fix follow-up

Adapted from `../2026-09-24-reliability-baseline/frozen/grading/RUBRIC.md`,
extended for the new report structure (## Findings / ## Open questions /
ambiguities split, admission rule) and the corrected case-107/case-112
grading keys. With-skill only; no baseline runs in this follow-up (the
baseline numbers already on record from the reliability-baseline
experiment are the comparison point).

Cross-case pass rule (unchanged from the baseline experiment): a run
passes if every Required item is met and no Forbidden item fires. A run
that fires any Forbidden item fails regardless of Required coverage.

## case-110 — proper-mcp-delegation-coherent-design (primary target)

**Required:**
- R1. Positively names audience/issuer/expiry validation happening before
  any claim is trusted (`auth_middleware.authenticate`).
- R2. Positively names read/refund scope separation (`orders:read` vs.
  `orders:refund`, not bundled).
- R3. Positively names the destination-side account-ownership check in
  `refund_order` as necessary-but-not-sufficient beyond scope possession.
- R4. Positively names preserved dual actor attribution (`act_as`/
  delegating user and `client_id`/agent both present and both logged).
- R5. Zero Confirmed/Likely findings in `## Findings` whose own text
  (its "Unresolved uncertainty" line, or the surrounding prose) concedes
  that an unresolved fact could determine whether the claimed defect
  exists at all — the self-contradicting-tier signature that failed 3/10
  runs in the prior experiment. This is the primary regression check for
  this follow-up.
- R6. Genuine open questions (claim-scoping, refund-grant assurance level,
  token TTL vs. session liveness, or similar) may be surfaced, but only
  under `## Open questions / ambiguities` (or case-110's ambiguity
  content is otherwise clearly not presented as a Findings-tier defect) —
  not omitted, and not promoted into `## Findings`.

**Forbidden:**
- F1. Generic step-up/MFA demand with no evidence-based trigger, anywhere
  in `## Findings`.
- F2. Unsupported token-replay speculation presented as a finding.
- F3. Unsupported read/write-scoping speculation (e.g. "refund should be
  scoped per-order-type or time-boxed") presented as a Findings-tier item
  rather than an open question / named unknown.
- F4. A report dominated by hypothetical "what if" speculation instead of
  positively naming what the evidence shows is correct.
- F5. Treating a genuine out-of-evidence question (STS configuration, rate
  limiting, token-exchange caching) as a confirmed defect rather than a
  named unknown/open question.
- F6. **Self-contradicting tier**: any `## Findings` entry tagged
  Confirmed or Likely (with or without a HIGH/MEDIUM/LOW label) whose own
  "Unresolved uncertainty" text, read plainly, concedes the defect's
  existence — not just its severity or scope — is not established. This
  is the exact failure signature from the baseline experiment's three
  failing runs and is graded as forbidden regardless of the header tier
  used.

**Tracked:**
- T1. Substantive Confirmed/Likely finding count in `## Findings` (target
  0 for a clean pass, matching the baseline experiment's T1 definition).
- T2. How many of R1-R4's four specific controls were explicitly and
  correctly named (0-4).
- T3. Whether `## Open questions / ambiguities` was used as intended:
  present with genuine content, "None." when nothing was unresolved, or
  absent/misused (record which).

## case-102 — raw-forwarding-chain-hop-discrimination (regression check)

**Required:** R1-R7 identical to the baseline experiment's case-102
rubric (BFF→A clean; A→B/B→MCP raw forwarding named as confirmed
structural fact; `verify_aud=False` named as confirmed code fact; the
production-exploitability consequence capped at Likely/Ambiguity, not
flat Confirmed; hops 2-3 treated as one sustained issue, not independent
findings; no blanket "all invalid" or "no issue" conclusion).

**Forbidden:** F1-F3 identical to the baseline rubric (absence-as-proof;
flat Confirmed with no acknowledgment of unknown upstream enforcement;
waving off the chain as fine).

**New tracked item under the revised structure:**
- T3. Where the downstream-exploitability consequence lands: `##
  Findings` at Likely (acceptable, matches prior passing behavior) versus
  `## Open questions / ambiguities` (also acceptable under the new
  admission rule, since "is this exploitable in production" is exactly
  the kind of unresolved-existence question the new section exists for)
  versus flat Confirmed in Findings (fails R4/F2). Record which, to check
  the new structure doesn't cause the real structural fact (the raw
  forwarding itself, and `verify_aud=False`) to be *hidden* in Open
  questions instead of stated as the Confirmed structural fact it is —
  that would be a new failure mode this rubric did not previously need to
  check for.

## case-106 — legitimate-spa-pkce-no-bff-needed (regression check)

**Required/Forbidden:** identical to the baseline rubric (no BFF demand,
no "browser tokens inherently unsafe" claim, positive architecture
recognition, 8-hour-lifetime kept at LOW/Deliberate-tradeoff or omitted).

**Tracked:** T1 identical (count of R3 specifics named).

## case-107 — genuine-workload-identity-no-user-needed (grading-key-change check)

**Required:** R1-R3 identical to the baseline rubric (correct workload-
identity characterization; no manufactured user/delegation demand;
correct destination-enforcement characterization).

- R4 (revised): if the hardcoded `ALLOWED_RECONCILIATION_WORKLOADS`
  allow-list is raised, it is kept at LOW-paved-road / Organization-
  specific-convention / Deliberate-tradeoff / Open-question level — never
  escalated to Confirmed or Likely.
- R5 (revised, per the corrected grading key): a "Deliberate tradeoff"
  label is graded as a **partial miss on label precision**, not a full
  pass, unless the run's own cited evidence goes beyond "the comment
  explains why the mechanism is safe" and actually states a reason the
  team *chose* hardcoding over the central policy engine. A LOW-severity/
  paved-road label, an Organization-specific-convention label, or an
  explicit open question about whether this was a deliberate choice are
  all full passes. This is the specific thing this follow-up is checking
  for: whether the corrected key grades runs coherently now that the
  "Deliberate tradeoff" credit has been narrowed.

**Forbidden:** F1-F3 identical to the baseline rubric.

**Tracked:**
- T1. Which label the run used, recorded verbatim, and whether its own
  cited evidence supports "knowing choice + rationale for the choice"
  (full Deliberate-tradeoff pass) or only "documents current safety"
  (partial miss per the corrected key).

## case-112 — secret-manager-mechanics-vs-resulting-service-authority (grading-key-change check)

**Required:**
- R1. Explicitly separates credential management/storage (Vault,
  short-lived, rotated) from authorization scope — states plainly that
  pulling the credential from Vault does not by itself mean access is
  correctly scoped.
- R2. Names the over-broad `GRANT ALL PRIVILEGES` grant in
  `vault_db_role.sql` as the actual finding, citing that the service's own
  code only ever issues `SELECT`.
- R3. Tier is Likely-to-Confirmed (the over-grant itself is a confirmed
  code/config fact).

**Forbidden:**
- F1. Treating "pulled from Vault" as itself a scoping/authorization
  decision (conflating credential management with authorization).
- F2. Rating the finding HIGH with no acknowledgment that exploiting the
  excess grant requires a separate, unshown compromise (SQL injection,
  credential leak, or service compromise) — the specific over-widening
  this follow-up's corrected key retracts. A HIGH rating that explicitly
  names this gap (i.e., reasons about reachability rather than asserting
  it) is a tracked tier-calibration item, not this forbidden item; a flat
  HIGH with no such acknowledgment is forbidden.

**Tracked:**
- T1. Severity assigned (MEDIUM / HIGH / other), recorded verbatim.
- T2. Whether the run's own reasoning cites reachability (who can
  actually exercise the excess grant) as the deciding factor for severity,
  versus asserting severity from the grant's existence alone.

## Grading protocol

1. Read the run's raw output in full.
2. Score each Required item met/not-met with a one-line citation from the
   run's own text.
3. Score each Forbidden item fired/not-fired with a one-line citation.
4. Compute pass/fail per the cross-case rule above.
5. Record tracked items.
6. Grade each run independently — no comparison against other runs of the
   same case while grading (avoids anchoring); aggregate stats computed
   only after all runs in a group are individually graded.
