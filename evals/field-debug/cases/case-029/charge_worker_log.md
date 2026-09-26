# charge-worker log -- sub_88f3 renewal

```
03:14:02 INFO  event received: renewal-due sub_88f3 amount=$49.00 attempt=1
03:14:02 INFO  calling ridgeline.charge(customer=cus_5521, amount=4900)
03:14:03 INFO  ridgeline.charge() call returned, response received
03:14:03 ERROR AttributeError: 'NoneType' object has no attribute 'rate'
             at billing/charge_worker.py:47, in apply_discount_adjustment
03:14:03 ERROR unhandled exception in process_renewal(sub_88f3), message
             not acked
03:14:03 INFO  moved to DLQ after 1 attempt (DLQ policy:
             move-on-first-unhandled-exception for this queue -- no
             redelivery/retry occurs before dead-lettering)
```

No line in this log records whether `ridgeline.charge()`'s response
indicated success or failure -- the log statement that would record the
charge result runs *after* `apply_discount_adjustment`, which is the line
that crashes. The call to Ridgeline happened and returned; what it
returned was never logged.
