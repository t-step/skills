# Context

Slack message from a platform engineer reviewing the nightly batch jobs
ahead of an internal audit:

> I was going through `nightly_reconciliation_job.py` for the ledger
> reconciliation and noticed there's no user token or session anywhere in
> the flow -- it just runs on a schedule, pulls a file from cloud storage,
> and calls ledger-service directly. Is that a gap? Should this be running
> under someone's delegated credentials, or attributed to whichever
> engineer last touched the reconciliation config, instead of however
> it's authenticating now?

Files in this directory (`nightly_reconciliation_job.py`,
`workload_identity.py`, `ledger_service_reconcile_handler.py`) are the
complete evidence available about this system for this review -- there is
nothing else to consult.
