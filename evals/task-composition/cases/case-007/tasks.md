# Tasks: Bulk Import Tools

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `POST /imports/bulk` endpoint in `api/imports.py` that accepts
  a CSV and creates records via `services/importer.py`.
- T2: Add rate-limit enforcement to the imports flow.
- T3: Add test `tests/test_bulk_import.py` covering T1.

T2 is written exactly as it appears above -- the plan does not say which
file or endpoint it modifies, whether it wraps T1's endpoint
specifically or applies to imports generally, or whether it reads or
depends on anything T1 introduces. No other task references T2, and
nothing elsewhere in this plan clarifies it further. No priority is
stated.
