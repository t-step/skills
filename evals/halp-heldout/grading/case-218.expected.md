# Expected outcome (for grading, not shown to the agent under test)

Symptom: ValueError parsing an offset timestamp. Cause: A3 (all timestamps are UTC 'Z') is contradicted by fixtures/sample.csv, which uses -05:00 offsets. Invalidated: the Z-only parse in parse.py (and A3). Reusable with change: rollup.py's hourly bucketing, once parsing yields timezone-aware UTC values. Unaffected: validate.py, write.py, cli.py.

## Assertions

- REQUIRED: separates the symptom (ValueError on an offset timestamp) from the cause (A3, all timestamps UTC 'Z', is contradicted by fixtures/sample.csv, which uses -05:00 offsets)
- REQUIRED: names what is invalidated: the Z-only parsing in parse.py (and A3 in the plan)
- REQUIRED: names work that is reusable with change: rollup.py's bucketing logic still stands once parsing yields timezone-aware/UTC values (it needs adapting, not rewriting)
- REQUIRED: names work that is unaffected (at least two of validate.py, write.py, cli.py) and does not list them as needing rework
- REQUIRED: sorts the work explicitly into invalidated / reusable-with-change / unaffected groups, by file or function rather than only by task number
- Next options are grounded and advisory (e.g. confirm the source's timestamp format, update A3, then adapt parse.py); nothing is edited
