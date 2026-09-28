# case-112 with-skill grading — 2026-09-24 review-findings-fix (grading-key-change check)

Graded by the orchestrating session directly against the corrected key
(`../../../grading/case-112.expected.md`). n=5. Purpose: verify severity
calibration behaves coherently after the HIGH-widening was retracted.

| Run | Tier/severity | Reachability acknowledgment | Verdict per corrected key |
|---|---|---|---|
| 01 | Confirmed, HIGH | "Some other layer... could theoretically add a further restriction, but nothing in evidence indicates one exists, and the Postgres role privilege is what actually governs..." — raises then closes the question, does not name the compromise-path precondition (SQLi/service compromise) at all | **FAIL** — F2: HIGH asserted with the reachability question closed rather than left open |
| 02 | Confirmed, HIGH | "if this service's own code path is ever exploited... the credential in hand can mutate or delete" — explicitly names the compromise precondition, but still tags the consequence **Confirmed** rather than capping it | **FAIL** — the finding's own text names an unresolved fact (whether the service is ever exploited) that determines whether the consequence materializes, while tagging Confirmed; this is the same self-contradiction pattern Task 1's admission rule targets, applied to severity rather than tier |
| 03 | **Confirmed, MEDIUM** | Explicitly separates the Confirmed structural fact (over-broad grant) from the unestablished practical exploitability, and does not inflate to HIGH absent a shown reachability path | **PASS, exemplary** — matches the corrected key's stated severity and reasoning almost exactly |
| 04 | Confirmed, HIGH | No acknowledgment of any compromise precondition or reachability gap at all — the hedge addresses only "was this deliberate," a different axis | **FAIL** — F2, flat HIGH |
| 05 | Likely, HIGH | Tier correctly downgraded to Likely (not Confirmed) with an explicit hedge, but the hedge addresses a *different* unresolved fact (a downstream compensating control) rather than the specific "requires a separate compromise" reachability question the corrected key names | **Partial / tracked** — better-calibrated than 01/02/04 (right instinct to hedge, right direction on tier), but doesn't fully land on the corrected key's specific reachability framing; graded as a tier-calibration miss rather than a forbidden-item violation, since HIGH here is explicitly qualified rather than asserted flatly |

## Aggregate

- **Pass rate against the corrected key: 1/5 clean pass (MEDIUM,
  exemplary), 3/5 fail (F2: HIGH with inadequate or self-contradicting
  reachability acknowledgment), 1/5 partial (Likely/HIGH, better-hedged
  but not on the precise axis).**
- **The corrected key is enforceable and produces a real, useful signal**:
  run 03 demonstrates a MEDIUM-with-correct-reasoning response is fully
  achievable under the current skill text, and the key's distinction
  between "the credential technically has write capability" and "a
  sensitive write is directly reachable without authorization" cleanly
  separates it from the other four runs.
- **Most with-skill runs (4/5) still default to HIGH.** This is
  consistent with — not a regression from — the pattern the original,
  pre-correction grading key rewarded (the original with-skill run in
  iteration-1's `RESULTS.md` also called this HIGH by default, which is
  exactly why the key needed correcting). The severity-inflation tendency
  observed here predates this pass's SKILL.md edits and is not something
  Task 1/2's admission-rule and Findings/Open-questions changes were aimed
  at (those changes target existence-uncertainty, not severity
  calibration specifically) — though run 02's failure shows the same
  underlying discipline (don't let a tier/severity label outrun what the
  finding's own hedge concedes) generalizes usefully to severity, not
  just to Confirmed/Likely/Ambiguity tier selection.
- **No SKILL.md change is prescribed by this finding**, per Task 4's
  scope (a grading-key correction, not a mandate to rewrite the HIGH/
  MEDIUM/LOW definitions). The existing HIGH definition ("a sensitive
  write reachable without appropriate authorization") already supports
  the corrected key's reasoning; the gap is in how consistently models
  apply "reachable" as a real constraint rather than reading "has write
  capability" as sufficient. This is named as a remaining open question
  in the final write-up, not treated as something this pass's scope
  covers fixing.
