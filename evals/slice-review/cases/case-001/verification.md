# Verification evidence

The author ran the billing test file locally and pasted this terminal output:

```
$ pytest billing/test_amounts.py -v
billing/test_amounts.py::test_parses_dollar_string PASSED
billing/test_amounts.py::test_rejects_negative_amount PASSED

2 passed in 0.02s
```
