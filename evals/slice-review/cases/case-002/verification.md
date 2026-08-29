# Verification evidence

The author ran the pricing test file locally and pasted this terminal output:

```
$ pytest checkout/test_pricing.py -v
checkout/test_pricing.py::test_compute_total_no_discount PASSED
checkout/test_pricing.py::test_compute_total_matches_prior_behavior PASSED
checkout/test_pricing.py::test_apply_discount_20_percent PASSED

3 passed in 0.03s
```

This output is genuine — all three tests really do pass against the diff above.
