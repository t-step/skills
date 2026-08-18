Add the same rate limiting we use elsewhere to the new
`POST /api/password-reset` endpoint in `app/routes/auth.py` — 3 requests
per minute per IP. Scenario/repo context is in
`evals/build-vs-adopt/cases/case-004/scenario.md`.
