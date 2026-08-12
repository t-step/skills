# `make check` output (this session)

```
$ make check
ruff check .
All checks passed!

pytest -q
....F.....
=================================== FAILURES ===================================
___________________________ test_apply_late_fee_rejects_negative_days ___________________________

    def test_apply_late_fee_rejects_negative_days():
        with pytest.raises(ValueError):
>           apply_late_fee(balance=100.0, days_late=-3)
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/test_late_fees.py:22: Failed
--------------------------------- short test summary ---------------------------------
FAILED tests/test_late_fees.py::test_apply_late_fee_rejects_negative_days
1 failed, 9 passed in 0.41s
make: *** [Makefile:8: test] Error 1
```
