# case-102 with-skill grading — 2026-09-24 review-findings-fix (post-change, regression check)

Graded by the orchestrating session directly. Rubric: `../RUBRIC.md`
case-102 section. n=5 (not a full re-run of the original n=10 baseline).

| Run | Core finding tier for downstream audience gap | R4 (caps exploitability at Likely/Ambiguity)? | R5 (hops 2-3 as one issue)? | R6/R7 (no blanket verdict)? | Verdict |
|---|---|---|---|---|---|
| 01 | API B: **Confirmed, HIGH**, "Unresolved uncertainty: none that changes whether the defect exists"; MCP: Likely, HIGH (correctly hedged) | **No for API B** — the hedge affirmatively closes the uncertainty rather than naming it, reading the fixture's "no infra config in this repository" as settling production reality | No — reported as two separate findings (API B / MCP) rather than one sustained issue, though internally consistent about why | Yes | **FAIL** (R4) |
| 02 | Single merged finding, **Likely, HIGH**, hedge explicitly separates repo-absence from production reality | Yes | Yes — merged into one finding spanning both hops | Yes | PASS, exemplary |
| 03 | Single merged finding, **Likely, HIGH**, hedge explicit ("absence in the repo isn't proof of its absence in the deployed system") | Yes | Yes | Yes | PASS, exemplary |
| 04 | Single merged finding, **Confirmed, HIGH** ("Audience validation stops after hop 1"), hedge names the external-gateway possibility but keeps the Confirmed/HIGH tier | **No** — SKILL.md's own HIGH definition requires "reachable... without appropriate authorization"; the finding's own hedge admits reachability is unresolved (network-level control "could independently limit... regardless of token audience"), so Confirmed+HIGH together assert what the hedge two lines later says isn't established | Yes (merged) | Yes | **FAIL** (R4, tier/severity pairing inconsistent with SKILL.md's own HIGH definition) |
| 05 | Single merged finding, **Likely, HIGH**, hedge explicit and correctly asymmetric between API B (repo-explicit) and MCP (repo-silent) | Yes | Yes | Yes | PASS, exemplary |

## Aggregate

- **Pass rate: 3/5 (60%)** on the core R4 tier-discipline test, versus the
  original 80-run experiment's with-skill baseline of 8/10 (80%).
- Both failures are **Confirmed+HIGH tier assignments where the finding's
  own text does not fully rule out an external gateway** — the same
  failure signature as the single with-skill failure in the original
  80-run experiment ("run-07," 1/10), not a new failure mode. Run 01 is
  the more severe instance (a hedge that explicitly closes off the
  uncertainty rather than naming it); run 04 is more borderline (the
  hedge is present and honest but the Confirmed/HIGH tier pairing is
  inconsistent with it under SKILL.md's own HIGH definition, which
  requires "reachable... without appropriate authorization").
- This is reported honestly as a lower pass rate than the prior baseline,
  not smoothed over. Two considerations bound how much weight to put on
  it: (1) n=5 is small — a 2-3 unit swing on a binomial rate this close
  to the baseline's own single-failure rate is well within plausible
  sampling noise; the prior experiment's own "what this does not prove"
  section already flagged case-102's ~80%-vs-60% with-skill/baseline gap
  as too narrow an n=10 margin to bound tightly. (2) The specific trap
  (treating "no infra config in this repository" as settling "no
  gateway exists in production") is not new, is not something Task 1/2's
  structural changes touch (the admission rule and the Findings/Open-
  questions split govern *which section* an item goes in and *whether*
  an unresolved existence-question may carry Confirmed/Likely at all —
  they don't relax the pre-existing Confirmed-vs-Likely tier-selection
  discipline this specific trap tests), and reproduces in this batch at
  a rate compatible with noise around the original 1/10. There is no
  causal mechanism in the SKILL.md diff that would predict this specific
  regression, and the three passing runs (02, 03, 05) show the correct
  behavior is still reliably reachable under the edited skill.
- **No run in this batch fired F1 (absence-as-proof) or F3 (waved off the
  whole chain as fine)** outright — even the two failing runs correctly
  named the structural forwarding/`verify_aud=False` facts and the
  scope-never-checked finding; the miss is specifically the tier pairing
  on the downstream-exploitability claim, not a wholesale failure to
  reason about the chain.
- **T3 (new, this experiment):** in all 5 runs, the raw-forwarding
  structural fact and `verify_aud=False` itself were reported as
  Confirmed **in Findings**, never demoted to Open questions — the new
  admission rule did not cause the real structural defect to be hidden
  in the ambiguity section. This is the specific new-structure risk this
  experiment's case-102 tracked item was watching for, and it did not
  occur in any of the 5 runs.
