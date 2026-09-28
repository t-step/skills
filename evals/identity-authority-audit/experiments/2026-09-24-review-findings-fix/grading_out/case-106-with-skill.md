# case-106 with-skill grading — 2026-09-24 review-findings-fix (post-change, regression check)

Graded by the orchestrating session directly. n=5.

| Run | BFF demand? | "browser tokens unsafe" claim? | 8hr-lifetime tier | Positive recognition | Verdict |
|---|---|---|---|---|---|
| 01 | No | No | Deliberate tradeoff | Yes (audience, scope, resource-ownership check named) | PASS |
| 02 | No | No | Deliberate tradeoff (+ 1 new Confirmed/LOW finding: read+write scope requested together, correctly bounded) | Yes | PASS |
| 03 | No | No | Deliberate tradeoff | Yes | PASS |
| 04 | No | No | Deliberate tradeoff | Yes | PASS |
| 05 | No | No | Deliberate tradeoff | Yes | PASS |

## Aggregate

- **Pass rate: 5/5 (100%)** — matches the original 80-run experiment's
  with-skill result exactly (10/10 then, 5/5 now).
- **Zero BFF demands, zero "browser-held tokens are inherently unsafe"
  claims** across all 5 runs (0/5 for both forbidden items, consistent
  with 0/20 in the original 4-case×2-condition experiment for this same
  case).
- **8-hour-lifetime wrinkle held at Deliberate tradeoff in 5/5 runs** —
  no escalation to a Confirmed/Likely MEDIUM or HIGH finding, matching
  the original with-skill 10/10 result exactly.
- **New findings surfaced in this batch, all correctly bounded:** run 02
  raised a genuine new Confirmed/LOW finding (the client always requests
  `orders:read orders:write:own` together, even for pure reads) — evidence-
  grounded, explicitly capped LOW with the reasoning for why the practical
  exposure is narrow (destination-side ownership check already closes the
  gap). This is a legitimate bonus finding, not scope creep or severity
  inflation.
- **`## Open questions / ambiguities` used correctly and consistently**
  for content that depends on `db.js` (not in evidence): whether
  `listOrdersForUser` actually scopes by user, and whether `updateOrder`
  allowlists fields (raised independently in runs 01, 03, 04, 05 — a
  real, evidence-grounded, non-obvious gap the fixture doesn't narrate,
  correctly kept out of Findings since the missing fact could resolve
  either way). None of these were promoted into Findings as a manufactured
  defect, and none were dropped silently either.
- **No regression from the SKILL.md changes**: the Findings/Open-questions
  split and the admission rule did not cause any run to either hide the
  documented tradeoff in Open questions (it correctly stayed in Findings,
  since the evidence fully resolves it as a knowing choice) or promote the
  `db.js`-dependent unknowns into Findings.
