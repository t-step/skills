# case-107 with-skill grading — 2026-09-24 review-findings-fix (grading-key-change check)

Graded by the orchestrating session directly against the corrected key
(`../../../grading/case-107.expected.md`). n=5. Purpose: verify the
corrected "Deliberate tradeoff" label-precision rule behaves coherently,
not to re-test workload-identity understanding (already 10/10 in the
prior 80-run experiment and unaffected by this pass).

| Run | Label used for allow-list wrinkle | Hedge quality (per corrected key) | Escalated to Confirmed/Likely? | Verdict |
|---|---|---|---|---|
| 01 | Deliberate tradeoff | "Unresolved uncertainty: none... the comment states the rationale directly" — asserts the comment establishes a knowing *choice*, the exact over-read the key retracts | No | Primary test (no security escalation): PASS. Label precision: partial miss, per corrected key. |
| 02 | Deliberate tradeoff | "none that changes the tier -- the comment states the rationale directly" — same over-read | No | Primary: PASS. Label precision: partial miss. |
| 03 | Deliberate tradeoff | "none bearing on whether this is a deliberate choice -- the comment states the rationale directly" — same over-read | No | Primary: PASS. Label precision: partial miss. |
| 04 | Deliberate tradeoff | Better-hedged: "whether the org's central policy engine treats this workload class as exempt by design, or whether a static in-code allow-list is an accepted exception... not established by this evidence" — names a real residual uncertainty rather than asserting closure | No | Primary: PASS. Label precision: closer to correct, still asserts "Deliberate tradeoff" as the header tier rather than treating the choice-vs-exception question as itself open. |
| 05 | **No Findings-tier label at all** — moved to Paved-road opportunities: "an intentional bypass with rationale given in evidence... verify separately whether the central policy engine would produce a different authorization outcome" | N/A — sidesteps the label-precision question by not claiming Findings-tier certainty about the choice at all | No | PASS, matches the original (pre-widening) key's own suggested treatment exactly. |

## Aggregate

- **Primary security test: 5/5 pass.** No run manufactured a
  user-delegation demand, no run escalated the allow-list wrinkle to
  Confirmed/Likely, and all 5 correctly characterized the workload-identity
  mechanism and destination-side enforcement. This confirms the corrected
  key's tightening does not disturb the case's main, already-passing
  behavior.
- **Label-precision test (the specific thing this rerun was checking):**
  4/5 runs used "Deliberate tradeoff" and, in doing so, asserted the code
  comment "states the rationale directly" for the *choice* itself — this
  is the exact over-read the corrected key identifies and retracts credit
  for (the comment documents why the mechanism stays *safe*, not why
  hardcoding was *chosen* over the policy engine). Per the corrected key,
  these 4 are graded as a **partial miss on label precision, not a full
  pass**: they don't fail the security test, but they overstate what the
  evidence supports about deliberateness.
- **1/5 runs (run 05) matched the corrected key's preferred treatment
  exactly** — declining to assert "Deliberate tradeoff" as a Findings-tier
  claim and instead treating it as a paved-road observation with an
  explicit note that the *rationale for the choice itself* is unverified.
- **This shows the corrected key is coherent and discriminates real
  differences between runs** — it isn't a distinction without a
  difference; run 05's report is measurably closer to the evidence than
  runs 01-03's. It also shows the label-precision issue is a real,
  common model tendency (4/5 in this batch), not a one-off — consistent
  with the original run this key was originally written around also
  making the same over-read, which is what motivated Task 3 of this pass.
- **No skill change is prescribed by this finding.** Task 3 scoped this
  to a grading-key correction; SKILL.md's Deliberate-tradeoff definition
  itself ("a comment, ADR, ticket, or design note explaining why") is
  unchanged and, read carefully, already requires exactly the distinction
  the corrected key now enforces at grading time. This is a grading-key
  fix, not a skill-behavior regression.
