# Verification evidence

```
$ pytest inventory/test_restock.py -v
inventory/test_restock.py::test_needs_restock_at_threshold PASSED
inventory/test_restock.py::test_days_until_stockout_basic PASSED
inventory/test_restock.py::test_expedite_when_stockout_before_lead_time PASSED
inventory/test_restock.py::test_no_expedite_when_stockout_after_lead_time PASSED
inventory/test_restock.py::test_no_expedite_when_usage_rate_zero PASSED

5 passed in 0.02s
```
