# Tasks: Password Reset Endpoint

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `POST /auth/password-reset` endpoint in `api/auth.py` that
  emails a one-time reset token and stores its hash in the
  `password_resets` table.
- T2: Add test `tests/test_password_reset.py` covering T1: requesting a
  reset creates a `password_resets` row, and a stale or already-used
  token is rejected.

No other tasks are planned. No priority is stated.
