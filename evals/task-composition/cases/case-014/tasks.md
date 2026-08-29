# Tasks: Worker Crash Recovery

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `heartbeat_at` and `status` columns to the `jobs` table via
  `migrations/0031_add_job_heartbeat.py`.
- T2: Update `worker/runner.py`'s job-processing loop to update
  `heartbeat_at` on the current job every 5 seconds while it is being
  processed.
- T3: Add `reclaim_stale_jobs()` in `worker/reclaim.py` -- finds jobs
  with `status='running'` whose `heartbeat_at` is older than 30 seconds,
  and resets them to `status='pending'` so another worker can pick them
  up.
- T4: Wire `reclaim_stale_jobs()` (T3) to run once at the start of
  `worker/runner.py`'s main loop, before the worker starts pulling new
  jobs.
- T5: Add test `tests/test_job_reclaim.py` -- simulates a worker
  crashing mid-job (a job row left with `status='running'` and a stale
  `heartbeat_at`), starts a fresh worker process, and asserts the job is
  reset to `status='pending'` and then picked up and completed by the
  fresh worker.

No column, function, or table introduced here is used by any other
feature in this plan or the current codebase; `heartbeat_at`,
`reclaim_stale_jobs()`, and the `jobs.status` field exist solely to
support this crash-recovery behavior. No priority is stated between
these tasks, and no other backlog item depends on any of them.
