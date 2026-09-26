# ach_batch_export.py -- run log, 2026-09-26

```
02:00:00 INFO  batch_id=ACH-20260926-01 entries=247 total=$412,880.13
02:00:00 INFO  building NACHA file, validating entry hashes... OK
02:00:14 INFO  POST https://gateway.ferrousbank.example/v1/ach/batches
02:00:14 DEBUG streaming request body (chunked)
02:00:52 DEBUG upload complete: 247/247 records transmitted (100%)
02:00:52 DEBUG awaiting response...
02:00:59 ERROR ConnectionResetError: [Errno 104] Connection reset by peer
02:00:59 ERROR no HTTP status code received, no batch confirmation id
             returned
02:00:59 ERROR job ach_batch_export marked FAILED, batch_id=ACH-20260926-01
02:00:59 INFO  auto_retry: disabled for ach_batch_export (see job config,
             ach_export.yaml: `retry.enabled: false  # ACH is one-shot,
             do not auto-resubmit -- see incident RCA-1188`)
02:20:03 INFO  paged: on-call engineer acknowledged
```

No later log line records a status check, a webhook callback, or a
confirmation ID for `ACH-20260926-01`. The job has not been re-run since
this failure.
