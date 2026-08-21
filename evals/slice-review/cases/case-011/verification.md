# Verification evidence

```
$ pytest notifications/test_dedup.py -v
notifications/test_dedup.py::test_record_event_stores_timestamp_per_user_and_key PASSED
notifications/test_dedup.py::test_first_notification_is_allowed PASSED
notifications/test_dedup.py::test_duplicate_within_window_is_suppressed PASSED
notifications/test_dedup.py::test_notification_allowed_again_after_window PASSED
notifications/test_dedup.py::test_mark_sent_records_timestamp PASSED

5 passed in 0.01s
```
