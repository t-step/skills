# case-003 — trivial-local-helper (regression)

**In-contract expectation:** the response just gives the one-line
`report_date.strftime("%Y-%m-%d")` (or equivalent) with no build-vs-adopt
apparatus at all. This is exactly the "local code is obviously smaller and
simpler, no dependency seriously in contention" not-material case.

**Pass requires:**
1. A direct, minimal answer (the format call), with no decision brief,
   no options table, no "let's survey the solution space" framing.
2. Does not raise or consider adopting a dependency for this.

**Fails if:** the response produces any kind of formal build-vs-adopt
survey, options table, or pause for this trivial a request.
