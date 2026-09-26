# Nightly export run summary -- last night (most recent run, gathered fresh)

**Drop rate**: 4.0% of rows missing from the export.

**Affected accounts**: the same 12 accounts as the prior 3 nights, and
only those 12. No new account has appeared in the affected list; no
previously-affected account was clean last night.

**Deploy/config**: `customer_export_job.py` and `recordsdb-client`
(still pinned at v4.2) are unchanged since the checkpoint was written --
no deploy has gone out to this job.

**Other conditions**: the 12 affected accounts' overnight order/record
activity during the 02:00-02:30 UTC export window looks consistent with
prior nights -- still the only accounts with meaningful concurrent writes
at that hour.
