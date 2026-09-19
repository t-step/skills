# Case 402 (A, twin/control: 401)

Varies: mtime of logs/pytest.log: 17:00, AFTER the uncommitted report.py edit (15:00)

Should change: the passing log becomes applicable (as of its time) to the current code

Should stay invariant: current unit T003, committed-vs-uncommitted split, next step

## Properties

- MUST: Identifies T003 (monthly rollup) as the unit in progress [regex proxy]
- MUST: Separates committed work from the uncommitted empty-input change [regex proxy]
- MUST: Reports the passing result (as of the log's time) [regex proxy]
- MUST_NOT: Calls the log stale/older than the code [regex proxy]
- MUST_NOT: Treats the passing log as completion: calls T003 done [regex proxy]
