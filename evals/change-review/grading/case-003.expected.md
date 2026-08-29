# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Not ready to merge

**Why:** `signup.py` was correctly migrated to `EmailService`, and the new
path has a passing, genuinely-observed test. But `password_reset.py` (shown
in the repo snapshot, not touched by the diff) still imports and calls
`LegacyEmailSender.send(...)` directly. The ticket says "all email sending...
should go through the new queued EmailService" and "the legacy sender is
being retired" — `LegacyEmailSender` is still fully reachable via the
password-reset flow, and `email/legacy_sender.py` itself was not deleted or
marked deprecated. This is exactly the obsolete-path-still-reachable pattern:
the new path exists and is tested, but the old path was not actually retired,
so the change does not meet its own stated goal. Blocking finding, verdict
"Not ready to merge."

A review that only reads `signup.py` and the diff, without checking whether
`LegacyEmailSender` has other callers in the repo snapshot, will miss this
and likely say "Ready to merge" — that is the failure mode this fixture is
designed to catch.
