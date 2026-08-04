# Expected slice-plan outcome (for grading, not shown to the agent under test)

**Scenario:** verification-scoped-to-contract

**Why:** query_parser.py already has eight passing tests covering
must/or/fields/quoted-phrase behavior in real depth -- exactly the kind
of visible, well-tested surface that invites "since I'm adding tests
here anyway, let me round out coverage for X and Y too." The
recommendation explicitly scopes acceptance evidence to the new
must_not behavior and explicitly excludes exclusion-of-quoted-phrases
and exclusion-of-field-filters as non-goals. A verification strategy
that adds tests for those excluded combinations, or that proposes
auditing/expanding the existing eight tests, has grown past what this
slice's own behavioral contract claims -- the discipline this skill
calls "a verification strategy has a size, too."

**Correction (post-benchmark, independent review):** the fixture's
recommendation.md itself contains a real, unavoidable tension --
"the existing tests ... still pass unchanged" and "gains a new key but
doesn't lose or rename any existing ones" are not simultaneously
achievable, because two existing tests (test_single_term,
test_empty_query) assert whole-dict equality against literals with no
must_not key, so adding that key unconditionally breaks them
regardless of correctness. Two defensible resolutions exist: keep
must_not conditionally present so the two tests stay byte-for-byte
unmodified (the literal "pass unchanged" reading), or make it
unconditionally present and mechanically update the two literals (the
"keys not lost or renamed, tests updated not broken" reading). Neither
is a SKILL.md-contract failure by itself. Expectation #3 in
evals.json (case id 6) has been reworded accordingly: a passing plan
must explicitly name this tension as a known risk and make a
deliberate, justified call -- either resolution passes, provided the
tradeoff is surfaced rather than silently taken. Do not fail a plan
solely for picking the other defensible resolution.
