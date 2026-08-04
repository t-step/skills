# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** ports-and-adapters layout (`domain/`, `boundary/`,
`adapters/`), explained and justified in `docs/architecture.md`.

**Why:** Tests whether an unusual-looking layout gets read against its own
documented rationale before being treated as a risk or confusion point. The
skill's own methodology warns against inventing intent from names alone —
this fixture is the positive case: the intent *is* documented, so the
orientation should find and cite it, not independently guess at (or worse,
flag as suspicious) a layout the repo already explains.
