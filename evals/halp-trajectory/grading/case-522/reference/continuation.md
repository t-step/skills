# Natural continuation after step 22 (model46, `sympy__sympy-16597`)
- 23: reads more of `test_assumptions.py` (lines 140-160).
- 24: prints `oo`/`-oo` `is_integer/is_even/is_odd/is_noninteger/is_composite` (all now `False`, `is_noninteger True`).
- 25-27: runs `sympy.test` for `assumptions/tests/test_assumptions.py`, `core/tests/test_numbers.py`, `core/tests/test_exprtools.py`; 28: `sympy.test('core/')` (noisy, Python 3.11 env).
- 29: final repro of the issue example. 30: `git diff > patch.txt`. Submits `integer -> finite` (+ blank line) only; tests left failing, Q layer untouched.
Model45 (independent run): `integer -> finite`, `rational -> finite`, `irrational == real & !rational & finite`; ran `assumptions/tests/test_query.py` and core tests, did not update tests.
Upstream gold: both layers (`core/assumptions.py`, `assumptions/ask.py`, `ask_generated.py`), `Pow._eval_is_rational` shortcut, `printing/tree.py`, tests updated (see `upstream-gold.patch`, `upstream-test.patch`).
