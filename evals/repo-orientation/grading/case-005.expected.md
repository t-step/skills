# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** two apparent entry points (`server.py`/`worker.py` and
`server_legacy.py`/`worker_legacy.py`); `Procfile` and `Dockerfile` both
point only at `server.py`.

**Why:** Tests whether the orientation treats deployment configuration
(`Procfile`, `Dockerfile`) as the source of truth for "what actually runs
in production," rather than treating both entry points as equally current
because both exist and both look like valid Python entry points. The
README's own "historically... now use server.py" line is a hint, not the
required evidence — a good orientation would reach the same conclusion from
`Procfile`/`Dockerfile` even without it.
