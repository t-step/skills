# state-ownership-audit — iteration 1 run-level record

Every run counted in `RESULTS.md`'s totals is listed here. One
general-purpose subagent per row, instructed not to read anything outside
the named case directory (plus `skills/state-ownership-audit/SKILL.md` for
with-skill runs). Raw transcripts are local, untracked artifacts (per this
repository's convention); this file plus the grading files under
`grading/` are the auditable record of what each run actually said.

## Regression suite, with skill

| Case | Config | Result | Notes |
|---|---|---|---|
| 001 | with-skill | 5/5 (revised key) | Correctly named Postgres/`update_price()` as sole authority and the Redis key as invalidate-then-repopulate. Additionally found a real, unintended repopulation race in the fixture (a concurrent cache-miss read can land its `r.set()` after `update_price()`'s `r.delete()`, re-caching a stale price for up to the 300s TTL) and reported it as a narrow, bounded, self-correcting finding without recommending a new mechanism -- a more sophisticated answer than the original grading key anticipated; the key was revised to credit this (see "Fixture and grading-key findings" below). |
| 002 | with-skill | 5/5 | Correctly re-anchored authority on the append-only `transactions` log rather than `ledger.balance_cents`, characterized both writers as deriving from that one source, and explicitly rejected "two writers = bug." Bonus finding: `reconcile_all_accounts()`'s own read-then-write is not atomic and races against `apply_transaction()` -- a real, narrower hazard distinct from the "two writers" framing the onboarding question raised. |
| 003 | with-skill | 4/4 | Named per-FC partitioned authority explicitly, characterized GlobalCatalog as a lossy periodic aggregate with no write authority, and pushed back on the architect's single-source-of-truth proposal by naming the specific availability guarantee it would remove. |
| 004 | with-skill | 4/4 | Named `order_events` as sole authority and the summary view as an async, DLQ-backed projection; concluded the ~1.5s lag is within the documented SLA and is not a bug, without recommending synchronous writes or a reconciliation job. |
| 005 | with-skill | 4/4 | Named the hazard as the centerpiece finding, grounded it precisely in the incident, and stopped without designing a fix -- the case this suite most needed to catch. |
| 006 | with-skill | 4/4 | Explicitly named the README-vs-code conflict, sided with the executable write paths (auth originates/validates; profiles only mirrors), and gave the new hire the correct, contradicting-the-README answer. |

## Pressure suite, with skill

| Case | Config | Result | Notes |
|---|---|---|---|
| 101 | with-skill | 4/4 | Reported current authority as unresolved; explicitly declined to treat the extraction design notes' "eventually notification-service will own this" as settling current ownership, naming it an unimplemented, unscheduled intention. Named the silent post-seed divergence as its own finding. |
| 102 | with-skill | 4/4 (revised key) | Correctly named the transferable, lifecycle-scoped authority and flagged Device as a lifecycle-audit candidate. Went further than the original key expected: rather than accepting the `status` check as an atomic guard, it read the actual SQL and found the check-then-act pattern (`SELECT status` then a status-blind `UPDATE`) leaves a real TOCTOU window where a stale ProvisioningService write can land after a device has gone active -- caught exactly the kind of gap the skill's "check for a fencing/validity guard" instruction exists to catch. Key revised to credit this as the intended, higher-quality answer (see below). |
| 103 | with-skill | 4/4 | Performed the ownership audit correctly (no hazard, invalidate-on-write cache) and explicitly declined the bundled ReconciliationCoordinator design request, naming it out of scope regardless of the Slack thread's claimed team consensus. |
| 104 | with-skill | 4/4 (revised key) | Named the circular dependency between Pricing.final_price and Promotions' price-matched discount explicitly, and correctly noticed the fixture's promo-validation logic is stubbed -- so it reported the cycle as a real hazard the code *permits* rather than a confirmed live occurrence, which is the more evidence-disciplined answer than the original key's flatter framing. Did not assign resolving authority to either side. Key revised to credit this precision (see below). |

## Regression suite, baseline (no skill)

All 6 regression cases were run, for direct comparison (a full sample, not
partial, given the suite's small size).

| Case | Config | Result (substantive) | Notes vs. with-skill |
|---|---|---|---|
| 001 | baseline | Correct | Independently found the same repopulation race and also the delete-failure gap; reached the same "decline the reconciliation job" conclusion. Structurally similar depth to the with-skill run; no imposed report template or explicit evidence-tier labels. |
| 002 | baseline | Correct | Reached the same "transactions is authority, two writers isn't the bug" conclusion and found the same reconcile-not-atomic race. Went further than the skill's contract allows: proposed two concrete fix designs (CAS update / row-lock) -- the skill explicitly refuses to design a fix. |
| 003 | baseline | Correct | Reached the same partitioned-authority conclusion and gave comparably strong, specific pushback on the proposal (four numbered reasons, closely tracking the with-skill run's reasoning). |
| 004 | baseline | Correct | Reached the same "documented SLA, not a bug" conclusion, citing the same p99<2s figure. |
| 005 | baseline | Correct | Correctly diagnosed the same two-writer, no-arbitration hazard and traced the same incident mechanics. Went further than the skill's contract allows: prescribed two named remediation designs ("Stripe-is-truth" vs. "override-can-supersede") -- the skill explicitly refuses to choose or design a resolution. |
| 006 | baseline | Correct | Reached the same conclusion (README inverted, auth is actual authority, validation belongs in auth) via a clear side-by-side claim-vs-code table. |
