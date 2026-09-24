# Reliability/baseline experiment — grading rubric (frozen)

Authored and frozen before any run in this experiment was dispatched or
observed. Operationalizes each case's existing `grading/case-1XX.expected.md`
(copied unchanged into `frozen/grading/`) into a checkable Required/Forbidden
list, plus the case-specific tracked signals the experiment specified. This
file is graded against, never revised mid-experiment. If a defect is found
in it during grading, it is recorded in RESULTS.md's "Grading-key defects
found" section, not edited here.

## Cross-case metrics (recorded for every run, every case)

- **Required expectations met / total** — per the case's Required list below.
- **Pass/fail** — PASS iff every Required item is met AND no Forbidden item
  fires. Otherwise FAIL.
- **Forbidden findings** — which Forbidden items fired, verbatim quote/cite.
- **Unsupported findings** — any claim (required, forbidden, or bonus) stated
  with a certainty the cited evidence doesn't actually support, independent
  of the case-specific tiers below (e.g. a bonus finding asserted as fact
  with no code citation).
- **Confidence-tier violations** — for with-skill runs: misuse of the
  Confirmed/Likely/Ambiguity/Tradeoff/Convention vocabulary (asserting
  Confirmed where only Likely/Ambiguity is supportable, or the reverse —
  under-claiming a directly observed fact). For baseline runs (no imposed
  vocabulary): the nearest equivalent — stating something as flatly true or
  false when the evidence only supports a hedge, or hedging something the
  evidence directly establishes.
- **Severity** — the tier/severity assigned to the run's main finding(s), in
  whatever vocabulary the run used (skill runs: Confirmed/Likely/HIGH etc.;
  baseline: its own words, recorded verbatim and mapped to nearest
  Confirmed/Likely/Ambiguity + HIGH/MEDIUM/LOW for comparability, marked
  "(mapped)").
- **Mode drift** — unsolicited scope expansion: a remediation/redesign
  proposal asserted where only a review/analysis was asked for, a numeric
  maturity score, or drift into out-of-scope domains (crypto/TLS, password
  policy, general appsec/OWASP, pentesting) not raised by the actual
  evidence.
- **Useful bonus findings** — real, evidence-cited findings beyond the
  Required list that are correct and grounded (not speculative).

## case-102 — raw-forwarding-chain-hop-discrimination

**Required:**
- R1. Names the BFF->API A hop clean/audience-checked-and-matching; does not
  flag it as an issue.
- R2. Identifies the raw-forwarding pattern (identical token, unchanged) at
  API A->API B and API B->MCP as a directly observable, confirmed
  structural fact.
- R3. Treats API B's/MCP's `verify_aud=False` (audience not checked in this
  code) as a confirmed fact about the code itself.
- R4. Does not give full Confirmed certainty to "this token is therefore
  usable/exploitable at API B in production" — caps that consequence at
  Likely or Ambiguity-requiring-verification, because no gateway/
  infrastructure evidence exists in this repo for API B.
- R5. Treats hops 2 and 3 (API B, MCP) as the same sustained audience-
  persistence issue continuing one hop further, not as two independent new
  findings.
- R6. Does not conclude "all forwarding here is invalid" (blanket
  condemnation of the chain).
- R7. Does not conclude "no issue" for the chain as a whole (blanket
  clearance).

**Forbidden:**
- F1. Treating the absence of gateway/infrastructure evidence as proof that
  enforcement is absent (declaring "audience validation is missing" as a
  flat fact rather than "not visible in the inspected path").
- F2. Declaring the audience gap Confirmed at full severity with no
  acknowledgment that nothing in evidence establishes what happens to the
  request before it reaches this code.
- F3. Waving off the whole chain as fine solely because "forwarding is
  normal."

**Tracked (recorded, not pass/fail on their own):**
- T1. Whether external/upstream-gateway enforcement is explicitly named as
  unresolved/ambiguous (appropriate) versus silently dropped from the
  report.
- T2. The confidence tier actually assigned to the downstream-authorization
  consequence (Confirmed / Likely / Ambiguity / other) — record verbatim.

## case-106 — legitimate-spa-pkce-no-bff-needed

**Required:**
- R1. Does not recommend or demand introducing a BFF for this architecture.
- R2. Does not claim, as a blanket statement, that browser-held bearer
  tokens are inherently unsafe.
- R3. Positively recognizes the legitimate SPA+PKCE architecture as
  coherent — names at least some of: audience narrowing to one API, scope
  narrowing, in-memory-only token storage, destination-side resource-
  ownership check (`order.userId !== req.auth.payload.sub`).
- R4. Treats the 8-hour-token-lifetime/no-refresh-rotation detail at most as
  a LOW-consequence note, or omits it — not a Confirmed/Likely MEDIUM or
  HIGH finding.

**Forbidden:**
- F1. Explicit recommendation/demand for a BFF.
- F2. Blanket claim that browser-held tokens are inherently unsafe/wrong.
- F3. Elevating the 8-hour token lifetime to a Confirmed/Likely MEDIUM or
  HIGH finding with no cited evidence of actual exposure (no XSS finding,
  no observed leak path, no compliance requirement).

**Tracked:**
- T1. Specificity of the positive architecture recognition (which of the
  R3 specifics were actually named, by count).

## case-107 — genuine-workload-identity-no-user-needed

**Required:**
- R1. Correctly characterizes the workload-identity mechanism (short-lived,
  single-audience OIDC token via the metadata server / GCP Workload
  Identity, no static key) as the right mechanism for this job.
- R2. Does not manufacture a missing-user/missing-delegation finding —
  does not insist the job must run under an engineer's credentials or a
  borrowed/attributed user identity; states plainly that no user principal
  is expected here.
- R3. Characterizes destination-side enforcement correctly: signature/
  issuer/audience validation (`authenticate_workload`) followed by a
  workload-scoped allow-list authorization decision
  (`authorize_reconciliation_workload`), not a rubber stamp.
- R4. If the hardcoded `ALLOWED_RECONCILIATION_WORKLOADS` allow-list is
  raised, it is kept at LOW / Deliberate-tradeoff / Organization-specific-
  convention / paved-road-observation level — not escalated to Confirmed or
  Likely.
- R5. Whatever label is used for R4 is actually supported by evidence cited
  in the run (e.g., "Deliberate tradeoff" is credited only if the run cites
  the code comment explaining the rationale for the hardcoded list).

**Forbidden:**
- F1. Any finding demanding the job run under a named engineer's
  credentials or a delegated/borrowed user token, or flagging "no user
  context" as a missing-actor-attribution gap.
- F2. Escalating the hardcoded allow-list to a Confirmed/Likely authority
  hazard.
- F3. Generic auth findings against the hardcoded policy ungrounded in the
  fixture (e.g., asserting it as a defect requiring immediate fix rather
  than an optional paved-road note).

**Tracked:**
- T1. Which label the run used for the allow-list wrinkle (Deliberate
  tradeoff / Organization-specific convention / LOW paved-road observation
  / other), recorded verbatim, and whether the cited evidence actually
  supports that label per R5.

## case-110 — proper-mcp-delegation-coherent-design

**Required:**
- R1. Positively names audience/issuer/expiry validation happening before
  any claim is trusted (`auth_middleware.authenticate`).
- R2. Positively names read/refund scope separation (`orders:read` vs.
  `orders:refund`, not bundled).
- R3. Positively names the destination-side account-ownership check in
  `refund_order` (`order["account_id"] != ctx.claims["account_id"]`) as
  necessary-but-not-sufficient beyond scope possession.
- R4. Positively names preserved dual actor attribution (`act_as`/
  delegating user and `client_id`/agent both present and both logged).
- R5. Zero manufactured Confirmed/Likely findings not grounded in the three
  files.

**Forbidden:**
- F1. Generic step-up/MFA demands with no evidence-based trigger in this
  case.
- F2. Unsupported token-replay speculation.
- F3. Unsupported read/write-scoping speculation presented as a finding
  (e.g. "refund should be scoped per-order-type or time-boxed") rather than
  acknowledged as outside the evidence.
- F4. A report dominated by hypothetical "what if" speculation instead of
  positively naming what the evidence shows is correct — graded as falling
  into the trap even if every item is hedged.
- F5. Treating a genuine out-of-evidence question (STS configuration,
  rate limiting, token-exchange caching) as a confirmed defect rather than
  a named unknown.

**Tracked:**
- T1. Substantive Confirmed/Likely finding count (target: 0 for a clean
  pass).
- T2. How many of R1-R4's four specific controls were explicitly and
  correctly named (0-4).

## Grading protocol

1. Read the run's raw output in full.
2. Score each Required item met/not-met with a one-line citation from the
   run's own text.
3. Score each Forbidden item fired/not-fired with a one-line citation.
4. Compute pass/fail per the cross-case rule above.
5. Record the cross-case metrics.
6. Record case-specific Tracked items.
7. Do this independently per run — no comparison against other runs of the
   same case/condition while grading (avoids anchoring); aggregate stats
   are computed only after all runs in a group are individually graded.
