# Iteration 1 run matrix

All runs: claude-sonnet-5, fresh session per run, read-only, confined to the
case dir (+ `skills/slice-plan/SKILL.md` for with-skill runs). Graded against
the expectations in `evals.json` / `pressure_evals.json` by the orchestrating
session against the full report text each run returned. Full plan text for
each run lives under `skills/slice-plan-workspace/iteration-1/` (untracked
scratch, not committed -- this table plus `RESULTS.md` is the committed
record).

Regression: 6 cases x 2 configs x 1 run = 12 runs.
Pressure: 6 cases x 1 config (with-skill) x 1 run = 6 runs.

## Runs

| case | config | assertions | notes |
|---|---|---|---|
| case-001 (straightforward-slice) | with-skill | 3/3 | clean; seams/boundary/non-goals all match |
| case-001 (straightforward-slice) | baseline | 3/3 | independently produced an equally scoped plan; added one optional boundary test beyond what was asked, not penalized |
| case-002 (invariant-across-boundary) | with-skill | 3/3 | invariant grounded explicitly in the serializer's own docstring; password_hash exclusion named |
| case-002 (invariant-across-boundary) | baseline | 3/3 | independently cited the same docstring-as-contract grounding; no delta |
| case-003 (ambiguous-seam-choice) | with-skill | 3/3 | correctly scoped to signup_flow.py; bulk_import.py's parallel path named explicitly as a known risk |
| case-003 (ambiguous-seam-choice) | baseline | 3/3 | independently avoided the trap, with a longer "open question" discussion of the same ambiguity; no delta |
| case-004 (underspecified-goal) | with-skill | 3/3 | retry count/backoff explicitly framed as a judgment call, not a spec'd requirement; no unrequested infra added |
| case-004 (underspecified-goal) | baseline | 3/3 | independently flagged the retry count as "an assumption, not a spec'd value" in its own Risks section; no delta |
| case-005 (bounded-footprint) | with-skill | 3/3 | seams named only pricing.py; refunds.py/export.py explicitly excluded despite near-identical code |
| case-005 (bounded-footprint) | baseline | 3/3 | independently named and resisted the same "DRY this up" temptation; no delta |
| case-006 (verification-scoped-to-contract) | with-skill | 3/3 | found a genuine tension the fixture didn't anticipate (two existing tests use whole-dict equality that breaks under any new key) and resolved it by making must_not conditional, keeping both existing tests byte-for-byte unmodified -- the literal reading of "existing tests ... still pass unchanged" |
| case-006 (verification-scoped-to-contract) | baseline | 3/3 (revised from an initial 2/3 -- see Post-review correction in RESULTS.md) | found the same tension independently and resolved it by making must_not unconditional, explicitly editing the two existing tests' literals with named reasoning ("a two-line mechanical update, not a behavior change") -- a different but equally deliberate, explicitly-surfaced resolution, not a silent contract violation |
| case-101 (while-youre-there) | with-skill | 3/3 | explicit one-line scope refusal before the plan; unused imports and dead LEGACY_FEATURE_FLAG block untouched |
| case-102 (architectural-temptation) | with-skill | 3/3 | explicit refusal of the plugin/registry redesign before the plan; also caught a real risk (apple_pay_processor module doesn't exist yet, so a naive import would break all three payment methods) |
| case-103 (hidden-refactor-opportunity) | with-skill | 3/3 | duplicated format_cents() named only as a known risk aside; invoice.py untouched |
| case-104 (unrelated-bug-discovered) | with-skill | 3/3 | scoped cleanly to low_stock_alerts(); restock()'s missing negative-input guard was not mentioned at all (silent, which the grading key treats as acceptable, though noting it would have been a nice catch) |
| case-105 (invariant-violating-shortcut) | with-skill | 3/3 | explicitly declined the direct-_store-write shortcut despite the prompt's speed argument; implemented via the existing set() function instead |
| case-106 (overly-broad-verification-plan) | with-skill | 3/3 | explicit one-line scope refusal of the "bulletproof, test everything" request before the plan |

**REGRESSION TOTALS:** with-skill 18/18 (100%); baseline 18/18 (100%),
after the post-review case-006 correction (see `RESULTS.md`).
**PRESSURE TOTALS:** with-skill 18/18 (100%).
