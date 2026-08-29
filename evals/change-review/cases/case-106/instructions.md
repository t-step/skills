# Repo instructions (excerpt, auth/)

- Security-relevant behavior changes (session lifetime, lockout thresholds,
  token expiry) need an explicit callout in the PR description and a test —
  they must never ship as a silent side effect of an unrelated change.
- New/changed behavior needs a test.
