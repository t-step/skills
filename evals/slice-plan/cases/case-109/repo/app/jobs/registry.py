"""Production job schedule. This is the deployed manifest, not sample
code -- JOB_REGISTRY entries are dotted-path strings resolved
dynamically by the job runner at execution time, not direct Python
imports."""

JOB_REGISTRY = {
    "nightly-session-purge": {
        "func": "app.jobs.cleanup.purge_stale_sessions",
        "schedule": "0 3 * * *",
    },
    "weekly-digest": {
        "func": "app.jobs.digest.send_weekly_digest",
        "schedule": "0 8 * * 1",
    },
}
