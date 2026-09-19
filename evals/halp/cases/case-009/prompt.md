You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You have been implementing T004 (ranking with name tie-break) for a while: writing `cohort/ranking.py`, adding tests, and staging the test file.
- Your last test run:

    $ python3 -m unittest discover -s tests
    ERROR: test_tie_break_by_name (tests.test_ranking.RankTests)
    NotImplementedError: tie-break by name (FR-3)
    Ran 5 tests in 0.000s
    FAILED (errors=1)

The user now types:

    /halp what is still uncommitted?
