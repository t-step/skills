# Repo instructions (excerpt, billing/)

- All public functions in `billing/` must have type hints on parameters and
  return value.
- Invalid input must raise `ValueError` with a message describing what was
  invalid — never use a bare `assert` for input validation (asserts are
  stripped under `python -O`).
- New behavior needs a test in the matching `test_*.py` file.
