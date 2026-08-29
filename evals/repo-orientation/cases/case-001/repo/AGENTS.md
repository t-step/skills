# AGENTS

- Run `pytest` and `ruff check .` before committing. Both must pass.
- New routes go in `app/routes.py`; new persisted models go in
  `app/models.py`. Don't put query logic directly in route handlers —
  put it in `app/services.py`.
- Use type hints on all public functions.
