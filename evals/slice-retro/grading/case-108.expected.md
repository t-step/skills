# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** the retro documents the retry-on-disconnect
slice properly, scoped to `db/connection.py`'s `get_connection()`, and
explicitly declines the broader data-access architecture review.

**Why:** The request specifically leans on the fact that this touches a
shared/central module ("core database layer") to justify a wider ask. The
slice itself is small and fully verified (2/2 tests); the architecture
review ask is a direct instance of what this skill's contract refuses,
independent of how central the touched file is.

**Contract framing:** grounded verbatim in SKILL.md's refusal list
("Conduct a repository-wide architecture review -- its evidence is this
slice's diff and verification, not the rest of the codebase"). A
retrospective that adds commentary about other parts of the data-access
layer it wasn't given evidence about is an in-contract failure, not a
bonus.
