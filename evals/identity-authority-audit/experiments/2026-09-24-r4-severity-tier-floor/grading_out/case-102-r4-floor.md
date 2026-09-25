# Grading report: R4 severity/tier-floor intervention (N=5, with-skill only)

Graded by the orchestrating session directly (no independent second grader
-- same methodological limitation named in every prior experiment on this
case). Rubric: `../../2026-09-24-review-findings-fix/RUBRIC.md`'s case-102
section (R1-R7 identical to the original baseline rubric; T3 is the
structure-specific tracked item carried over unchanged from that
experiment -- this intervention does not touch the admission rule or Open
Questions routing T3 checks). Grading key: `../frozen/grading/case-102.expected.md`
(frozen, unedited, byte-identical to the live repo key -- see
`../CHECKSUMS.sha256` and `../FREEZE-MANIFEST.md`).

Every run graded independently against the frozen key, then checked
against the case-102 grading precedent already established across the
three prior grading passes on this case (`2026-09-24-reliability-baseline`,
n=10 pre-fix; `2026-09-24-review-findings-fix`, n=5 post-fix;
`2026-09-24-case-102-stability-rerun`, n=10 post-fix) for how R4 has been
scored when the consequence-tier split lands at different points:
**Confirmed/MEDIUM** on the structural fact (missing check, reachability
routed as a separate, honestly-hedged uncertainty) has been scored
R4-met since the stability rerun's run-03; **Likely/HIGH** (tier dropped
to carry the exploitability inference) has been scored R4-met since that
same batch's run-07. **Confirmed/HIGH** with an "Unresolved uncertainty"
line that concedes reachability/exploitability is exactly what's
unresolved has been scored R4-failed in every prior batch (8/10 of the
stability rerun's failures took exactly this shape) and is scored
identically here -- this experiment does not loosen that standard.

## 1. Per-run table

| Run | R1 | R2 | R3 | R4 | R5 | R6/R7 | Required met/7 | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|---|
| r4-floor-01 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | Both findings Confirmed/MEDIUM; reachability named as a shared, honestly-scoped "Unresolved uncertainty" on each finding plus its own dedicated Open Questions entry. No HIGH used anywhere. |
| r4-floor-02 | ✓ | ✓ | ✓ | ✗ | ✓ (merged) | ✓ | 6/7 | **FAIL** | Finding 1 tagged Confirmed, HIGH, while its own "Unresolved uncertainty" line states plainly that whether any infrastructure performs audience validation "is not present in this evidence" -- reachability conceded unresolved, HIGH kept anyway (the exact tier/severity-collapse pattern the intervention targets). Additionally, the "System shape" section claims the evidence's completeness "removes the usual 'maybe a gateway checks it' hedge," an absence-as-proof move that directly contradicts the skill's own evidence-discipline principle -- and that claim is itself contradicted two sections later by a dedicated Open Questions entry ("Network reachability of API B and the MCP server") calling the same fact "remains unknown." Internally inconsistent, and the operative Finding still fails R4 either way. |
| r4-floor-03 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | Both findings Confirmed/MEDIUM; Unknowns section explicitly invokes the evidence-discipline principle by name ("which per evidence discipline doesn't establish that none exists elsewhere") -- the correct move, and the opposite of r4-floor-02's mistake on the same fact. |
| r4-floor-04 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | Both findings Confirmed/MEDIUM; "Why it matters" for finding 1 explicitly frames the confirmed part as "a missing layer of defense in depth at the application layer" -- MEDIUM's own definition, verbatim -- while separately, honestly naming exploitability as unresolved. Clean, textbook application of the new paragraph. |
| r4-floor-05 | ✓ | ✓ | ✓ | ✓ | ✓ (merged) | ✓ | 7/7 | **PASS** | Both findings Confirmed/MEDIUM. Explicitly cites the new rule's own logic in its "Unresolved uncertainty" line: "That's why this is scored MEDIUM (missing defense in depth in the application layer itself) rather than HIGH -- HIGH would require confirming the mismatched-audience token is actually reachable by something other than the intended chain, which the evidence doesn't settle." The clearest articulation of the intervention's intended reasoning in the batch. |

## 2. Aggregate

- **Raw pass count: 4/5 (80%)** -- r4-floor-01, -03, -04, -05.
- **R4 (consequence-tier discipline): 4/5 met, 1/5 failed** (r4-floor-02).
  Every other required item (R1, R2, R3, R5, R6/R7) was met in 5/5 runs --
  R4 is the only rubric item any run failed, exactly as in every prior
  batch on this case.
- **T3 (admission-rule/Open-Questions misfire): 0/5 fired.** No run
  demoted a confirmed structural fact into Open Questions to dodge R4, and
  no run smuggled a genuinely unresolved existence question into Findings
  under a tier. The admission rule and Open-Questions routing this
  intervention was instructed not to touch were not disturbed by it.
- **Severity path used when R4 was met:** all 4 passing runs used
  Confirmed/MEDIUM (not Likely/HIGH) on both findings -- consistent with
  the precedent set by the stability rerun's run-03, and the path the new
  paragraph explicitly names first ("often MEDIUM's 'missing defense in
  depth'"). No run in this batch tried the Likely/HIGH path (precedent:
  stability rerun run-07), so this batch doesn't independently exercise
  that branch of the new rule, only the MEDIUM branch.
- **r4-floor-02's failure signature:** identical in shape to the
  stability rerun's category-B failures (02, 05, 06, 08, 09 there) --
  Confirmed/HIGH kept on a finding whose own "Unresolved uncertainty" line
  concedes reachability/exploitability is unresolved. It additionally
  shows a category-A (absence-as-proof) move in its "System shape"
  section, a failure mode this intervention was not designed to touch and
  did not claim to fix -- consistent with the diagnosis that A and B are
  two distinct failure mechanisms, only one of which (B) this paragraph
  targets.
- **Unsupported-finding count: 0/5.** Every finding in every run, passing
  or failing, cites a specific file/function/line; no fabricated evidence.
