# Ledger — current product state

Ledger is an internal billing service. Two code paths retry failed
charges:

- `retry_charge()` in `billing/charges.py` — triggered manually from the
  support dashboard when a support agent retries a specific failed
  invoice. Just made idempotent by the completed slice above.
- `reconcile_pending_charges()` in `billing/jobs.py` — a nightly batch
  job that scans for invoices still marked "pending" after 24 hours and
  retries each one automatically, using its own retry loop (it does not
  call `retry_charge()`).

`cron/schedule.py` is the deployed cron manifest. Its `CRON_JOBS` dict
currently reads:

    CRON_JOBS = {
        "nightly-reconcile": {
            "func": "billing.jobs.reconcile_pending_charges",
            "schedule": "0 2 * * *",
        },
        "nightly-report": {
            "func": "reporting.jobs.send_daily_summary",
            "schedule": "0 6 * * *",
        },
    }

This file is part of the production deploy manifest and was last
modified two weeks ago, unrelated to the completed slice above. The
`func` values are dotted-path strings resolved dynamically by the cron
runner at execution time, not direct Python call sites.
