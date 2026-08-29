# Tasks: Reporting Dashboard Fields

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add a `total_revenue` field to `ReportConfig` in
  `reports/schema.py`.
- T2: Add an `active_users` field to `ReportConfig` in
  `reports/schema.py`.
- T3: Add a `churn_rate` field to `ReportConfig` in `reports/schema.py`.
- T4: Update `render(cfg: ReportConfig)` in `reports/renderer.py` to
  read and display whichever of T1, T2, and T3's fields are present on
  the config it's given.
- T5: Add test `tests/test_report_fields.py` covering T1 through T4
  together: a config with all three fields renders all three, and a
  config missing one renders only the ones present.

No priority is stated between T1, T2, and T3.
