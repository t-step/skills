# AGENTS

- Run `pytest` before committing.
- Application code lives under `src/`; tests live under `tests/` and mirror
  the module they cover.
- New scheduled jobs belong in `src/jobs.py` and must be registered in
  `src/app.py`'s `run()` function to actually execute.
