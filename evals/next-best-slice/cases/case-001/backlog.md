# Backlog / candidate next work

- **Protect `/api/account`** — this endpoint currently returns any caller's
  account details given a user id in the query string, with no auth check
  at all. Small: apply the new `require_auth` decorator and read the user
  id from the verified token instead of the query string.
- **Build a role-based permission system (RBAC)** — admin/staff/customer
  roles, per-endpoint permission checks, an admin UI to manage roles. Large,
  multi-week effort.
- **Refactor the API routing layer** — routes are currently a flat list of
  `(method, path, handler)` tuples; several people think a class-based
  router would be cleaner and easier to extend.
- **Add per-IP rate limiting** — no rate limiting exists anywhere in the API
  yet; unrelated to authentication.
