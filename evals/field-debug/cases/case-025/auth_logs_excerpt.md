# billing-api -> ledger-svc auth log (excerpt, 09:00-11:45 UTC)

Sampled 30 request IDs from the failing set (from
`billing_api_app_errors.md`) and cross-referenced against
`ledger-svc`'s own auth-validation log:

None of the 30 sampled failing request IDs appear in `ledger-svc`'s auth
log at all -- consistent with `billing_api_app_errors.md`, which shows
these requests never leave the process (pool-exhausted before a
connection is attempted, so `ledger-svc` never sees them to authenticate
them).

For the ~60% of calls in the same window that *did* reach `ledger-svc`:
100% show a valid, successfully-validated service token
(`svc=billing-api`, `scope=ledger:write`), same token type and scope as
before 09:00 UTC. Zero `401`/`403` responses anywhere in the window.
Token expiry for the current service credential is 2026-11-30 -- not
expiring soon.
