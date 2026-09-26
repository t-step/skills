# crm-sync-svc nightly job log (last night's run, shared by Priya)

```
2026-09-24T02:00:03Z  INFO  starting nightly sync for customer=northwind
2026-09-24T02:00:03Z  INFO  loaded 3412 updated customer records to sync
2026-09-24T02:00:04Z  INFO  posting batch 1/7 to https://northwind.crm.example/api/webhooks/customer-sync
2026-09-24T02:00:04Z  INFO  batch 1/7 -> HTTP 200 {"status":"received"}
2026-09-24T02:00:05Z  INFO  posting batch 2/7 ...
...
2026-09-24T02:00:11Z  INFO  posting batch 7/7 ...
2026-09-24T02:00:11Z  INFO  batch 7/7 -> HTTP 200 {"status":"received"}
2026-09-24T02:00:11Z  INFO  sync complete: 3412/3412 records posted, 0 send errors, 0 non-2xx responses
```

Every batch in every run over the past week shows the same pattern: all
batches return HTTP 200 with `{"status":"received"}`, zero send errors,
zero non-2xx responses. Nothing in this job's own log or metrics has
changed in that time.
