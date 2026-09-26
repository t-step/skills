# Context

Slack message from an engineer on the data-platform team:

> The nightly inventory-sync job has been quietly dropping about 3% of
> SKU updates for the last few weeks -- we only noticed because a
> downstream reconciliation report started flagging drift. `sync_job.py`
> looks fine to me: it retries on failure and logs a summary line when
> it's done. Can you figure out why some updates are getting lost, and
> whether it's something we need a bigger fix for (batching, retries,
> concurrency) or something narrower?

This directory is a slice of a larger internal-tools monorepo -- treat
its contents (`sync_job.py`, `README.md`, and anything they point you
toward within this directory) as what's actually available to inspect.
There is no live system to query and no one else to ask; this is a
Recon-then-Diagnose task from static evidence alone.
