# Addendum to PREREG-v2.md: contingent experiment 516 (written after seeing 511-W)

Written at the time recorded in `runs/2026-09-19-v2/ADDENDUM.sha256`, **after** 24 of the 25 declared 511-W runs had been checkpointed. All 24 wrote the T004 export at `carry`, in every cell: no-question, main neutral, HALP neutral, main evaluative, HALP evaluative. That is a ceiling: 511-W cannot separate a channel effect from a question effect because nobody stopped. This is a development finding about the design, not about HALP.

## Why 511 failed to discriminate (a hypothesis, not a result)

v1's stall (4 of 6 HALP arms, 3 of 4 main-thread arms, 0 of 6 controls) happened on a fixture in which the **key format was still live in the task being finished** (T003's empty-input half was uncommitted, T004 a thin one-line spec). 511's fixture deliberately made T003 complete and T004 fully specified, so that "rational stopping because the spec is thin" was removed from the design. That also removed the state in which the question could matter to what the agent was doing. So 511 tests "does a question about a settled, shipped format make the agent stop before a fully specified next task?" The answer is no in 24 of 24 runs. It does not test v1's regime.

## Contingent experiment 516 (`experiments-v2c.json`)

- Fixture: exactly v1's `ledger_cf` (byte-identical to 501/506's fixture). Narrative: the v1 narrative, unchanged.
- Cells (all with the weak continuation, `ok thanks, carry on`): NQ-W 5, ME-W 5, HE-W 5. The evaluative question text is 511's. No neutral or bounded cells: they are not needed to answer the one question 516 exists for.
- Observable: `export_written@carry` (T004 gone ahead); `ticked_T004@carry` is reported too, because it was v1's observable.
- Comparisons (K1-K7, `kind: contingent`) are in the manifest. Result reporting rules are PREREG-v2.md's: counts and risk differences, no p-values.
- These 15 runs are contingent and never merged into a pre-declared tally. The 511 result (ceiling) stands as reported.

## Also disclosed here

- `tools/analyze2.py` was generalised after registration: `ticked_T004@carry` became `ticked_<task>@<label>`. Behaviour for the registered observables is unchanged.
- No other tool, manifest or fixture file has changed since the first hash (see `PREREG.sha256`; `ADDENDUM.sha256` re-hashes everything).

## Early-stop rule for 516 (written 2026-09-19T23:23:03Z, after 8 of 9 first-three-per-cell runs had their turn-2 result, before the last three)

516 was declared at n=5 per cell. Stopping rule now fixed: **if all 9 runs of the first three replicates (NQ-W.1-3, ME-W.1-3, HE-W.1-3) proceed to T004, 516 stops at n=3 per cell** (ceiling again; more runs of the same cell would not change the count-level reading and the batch is already large); **if any of the nine stalls, the three cells are extended to n=5.** This is a disclosed reduction from the addendum's n=5 and is reported as such. ME-W.4/5, NQ-W.4/5 and HE-W.4/5 are prepped and unused unless the extension triggers.

## Also disclosed (harness defect H-516)

The v1 fixture's T004 line names no file. NQ-W.2, NQ-W.3, ME-W.2, HE-W.2 wrote `rollup_to_csv` inside `ledgerkit/report.py`, so the `export_written` probe (looks for `ledgerkit/export.py`) scores them "not written" although T004 was implemented, tested and ticked. For 516 the analysis uses `ticked_T004@carry` (v1's observable, declared as K4) as the primary measure and reports `export_written` alongside with this caveat. The registered 511 definitions are unaffected (511's T004 line names `ledgerkit/export.py`).

## Early-stop rule outcome (recorded 2026-09-19T23:23:34Z)

HE-W.1 stopped after T003 (uncommitted; T004 not started). Its own account: a combined `git commit` command was denied by the subject's permission classifier; it did not attempt to bypass. This is a **harness/permission defect (H-perm)**, not a pre-stated invalidity reason, so HE-W.1 stays in the 516 tally, flagged. Because one of the nine stalled, the rule above triggers: 516 is extended to n=5 per cell (NQ-W.4-5, ME-W.4-5, HE-W.4-5).
