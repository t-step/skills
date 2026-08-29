# Verification evidence

```
$ pytest billing/test_late_fees.py -v
billing/test_late_fees.py::test_discount_applies_after_five_days_early PASSED
billing/test_late_fees.py::test_one_week_late PASSED
billing/test_late_fees.py::test_two_weeks_late PASSED
billing/test_late_fees.py::test_zero_days_late_no_fee PASSED
billing/test_late_fees.py::test_cap_applies_for_far_overdue PASSED

5 passed in 0.02s
```
