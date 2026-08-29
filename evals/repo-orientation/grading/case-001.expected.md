# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** conventional single-application repository (Flask + SQLAlchemy
todo API).

**Why:** A clean baseline — one entry point (`app/main.py` via
`app/__init__.py:create_app`), one system of record (Postgres, per
`pyproject.toml`'s `psycopg2-binary` dependency and `app/models.py`'s
SQLAlchemy models), and commands sourced from `AGENTS.md`/`pyproject.toml`/
`.github/workflows/ci.yml` (`pytest`, `ruff check .`). Nothing here should
be reported as observed/verified — no command was actually run. A good
orientation states the facts plainly without manufacturing risk points that
don't exist in this fixture.
