# Grading report: case-102 stability rerun (N=10, with-skill only)

Graded by the orchestrating session directly (no independent second grader
— same methodological limitation named in both prior experiments). Rubric:
`../../2026-09-24-review-findings-fix/RUBRIC.md`'s case-102 section
(R1-R7 identical to the original baseline rubric; T3 is the new,
structure-specific tracked item). Grading key:
`../frozen/grading/case-102.expected.md` (frozen, unedited, verified
identical to the live repo key throughout — see `../CHECKSUMS.sha256`
and `../FREEZE-MANIFEST.md`).

Every run graded independently against the frozen key before any
cross-run comparison, then checked against the two prior grading passes
on this same case (`2026-09-24-reliability-baseline/grading_out/case-102-with-skill.md`,
pre-fix, n=10; `2026-09-24-review-findings-fix/grading_out/case-102-with-skill.md`,
post-fix, n=5) for precedent on borderline calls — in particular, whether
a two-block API-B/MCP presentation with explicit connecting language
("the same... credential," "same... pattern repeats") satisfies R5, per
the pre-fix baseline's own run-03/run-04 precedent (scored R5-met despite
two blocks, specifically because of that connecting language).

## 1. Per-run table

| Run | R1 (hop 1 clean) | R2 (raw fwd confirmed) | R3 (verify_aud=False confirmed) | R4 (consequence capped) | R5 (hops 2-3 one issue) | R6/R7 (no blanket verdict) | Required met/7 | Verdict | Failure signature(s) |
|---|---|---|---|---|---|---|---|---|---|
| 102-stability-01 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | A — absence-as-proof (explicit: "this would be downgraded to Likely" only "in an engagement with an incomplete repository," implying this one is treated as complete) |
| 102-stability-02 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | B — tier/severity collapse (Confirmed/HIGH; hedge explicitly says exploitability is unresolved, contradicting HIGH's own "reachable...without authorization" definition) |
| 102-stability-03 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | — (Confirmed/MEDIUM on the structural fact using "missing defense in depth" framing — matches MEDIUM's own definition; reachability question correctly routed to a dedicated Open Questions entry) |
| 102-stability-04 | ✓ | ✓ | ✓ | ✗ | ✓ borderline (title: "MCP tool dispatch accepts *the same* audience-mismatched credential" — connecting language, matches pre-fix-baseline run-04 precedent) | ✓ | 6/7 | **FAIL** | A — absence-as-proof, most explicit instance in the batch: "api_b.py's own handling is the complete picture of what happens to a request before this code runs" (stated as fact, no hedge) |
| 102-stability-05 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | B — tier/severity collapse (Confirmed/HIGH; "independent of anything else that may or may not exist around it" language keeps HIGH while conceding exploitability is exactly what's unresolved) |
| 102-stability-06 | ✓ | ✓ | ✓ | ✗ | ✗ — three non-adjacent findings (MCP, scope, API B, in that order), no connecting language between the MCP and API B blocks, hop order scrambled | ✓ | 5/7 | **FAIL** | E — chain-shape error (API B and MCP presented as unrelated findings, matching pre-fix-baseline run-08's fail pattern) + B (secondary; HIGH tier on both audience blocks despite a reachability-scoped hedge) |
| 102-stability-07 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | — (Likely/HIGH, explicit hedge, explicit citation of the skill's own tier-selection logic for why this is Likely not Confirmed) |
| 102-stability-08 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | B — tier/severity collapse, reasoned explicitly: "either way, the application layer's own explicit disabling... is directly observed... regardless of that fact" — used to justify keeping Confirmed/HIGH despite conceding severity could be lower |
| 102-stability-09 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | B — tier/severity collapse ("Why it matters" asserts "will be reachable," an unhedged reachability claim, immediately followed by an "Unresolved uncertainty" line conceding reachability is exactly what's unresolved) |
| 102-stability-10 | ✓ | ✓ | ✓ | ✗ | ✓ (title: "Same missing-audience pattern repeats at the MCP server" — near-identical connecting language to pre-fix-baseline run-04's passing title) | ✓ | 6/7 | **FAIL** | A — absence-as-proof, most blatant instance in the batch: hedge text explicitly names and dismisses "the usual 'maybe a gateway checks it' hedge" as foreclosed by the repo's stated completeness |

## 2. Aggregate

- **Raw pass count: 2/10 (20%)** — 102-stability-03, 102-stability-07.
- **R4 (consequence-tier discipline) failures: 8/10.** Every failing run
  failed specifically and only on R4 (the downstream-exploitability
  consequence not capped at Likely/Ambiguity) — no run failed on R1, R2,
  R3, R6, or R7.
- **R5 (chain-shape / hop continuity) failures: 1/10** (102-stability-06).
  Two other runs (04, 10) used a two-block API-B/MCP presentation but
  with explicit connecting language in the finding titles, which the
  pre-fix baseline's own grading precedent (run-03, run-04 there) scored
  as R5-met — applied consistently here rather than re-litigated with a
  stricter standard just because this batch's pass rate is already low.
- **Failure-signature category counts** (a run can carry more than one):
  - **A — Absence-as-proof:** 3 (runs 01, 04, 10)
  - **B — Structural/consequence collapse:** 5 (runs 02, 05, 06, 08, 09)
  - **C — Over-demotion (Confirmed fact pushed into Open Questions):** 0
  - **D — Finding/Open-question self-contradiction, as a distinguishable
    textual pattern within category B (own hedge concedes exactly what
    the tier asserts):** 5 of the 5 category-B runs show this explicitly
    (02, 05, 06, 08, 09) — folded into B above rather than double-counted,
    since in every instance it is the *mechanism* producing the B-type
    collapse, not a separate defect.
  - **E — Chain-shape error:** 1 (run 06)
  - **F — Other:** 0
- **Unsupported-finding count: 0/10.** Every finding in every run,
  passing or failing, is grounded in a specific cited file/function/line
  of the fixture; no run fabricated a fact not in evidence. All 8
  failures are calibration failures (wrong tier/severity or wrong
  finding boundary), not evidentiary fabrication.
- **Confidence-tier self-contradiction count (Finding's own uncertainty
  text vs. its Confirmed/Likely tier): 5/10** (runs 02, 05, 06, 08, 09).
  The other 3 failing runs (01, 04, 10) do not self-contradict — they
  resolve the uncertainty confidently and incorrectly (absence-as-proof)
  rather than stating the tension and then ignoring it.
- **Mode-drift count: 0/10.** Every run stayed in Review mode, used
  verification-oriented "Next verification step" language (never a
  remediation/mechanism recommendation), and did not drift into
  crypto/TLS, generic appsec, or unsolicited redesign — several runs
  raise the shared-signing-key observation but explicitly scope it as
  out of this skill's remit.
- **T3 (admission-rule / Open-Questions risk this structural fix was
  built to guard against): 0/10 fired.** In every run, the raw-forwarding
  and `verify_aud=False` facts were reported as Confirmed items inside
  `## Findings`, never demoted into `## Open questions / ambiguities`.
  The one mechanism the SKILL.md diff specifically targets did not
  misfire in this batch, in either direction.
