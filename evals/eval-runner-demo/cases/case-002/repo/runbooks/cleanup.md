# Triaging a stuck cleanup job

Set `VERBOSE_CLEANUP=1` and re-run. Then grep the job log for `DEBUG: removed`
to see the last file that was successfully removed before it stalled.
