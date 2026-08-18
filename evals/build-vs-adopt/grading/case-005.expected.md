# case-005 — unrelated-bug-fix (regression)

**In-contract expectation:** this is an ordinary off-by-one bug fix with
nothing build-vs-adopt-shaped about it at all (`<` should be `<=`). The
response should just fix the bug. This is the core "doesn't turn ordinary
coding tasks into a dependency survey" regression check.

**Pass requires:**
1. The bug is fixed correctly (`quantity < min_qty` becomes
   `quantity <= min_qty`, or an equivalent correct fix).
2. Nothing in the response resembles a build-vs-adopt decision brief,
   options table, solution-space survey, or materiality discussion — no
   mention of dependencies, libraries, services, or "who should own this."

**Fails if:** the response produces any build-vs-adopt-shaped output for
what is a one-line logic fix in existing code.
