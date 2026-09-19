You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- The user asked you to implement T004 (ranking) after T003 was committed.
- You wrote `cohort/ranking.py` (sort by readiness) and `tests/test_ranking.py`.
- You ran the tests:

    $ python3 -m unittest discover -s tests
    ERROR: test_tie_break_by_name (tests.test_ranking.RankTests)
    NotImplementedError: tie-break by name (FR-3)
    Ran 5 tests in 0.000s
    FAILED (errors=1)

The user now types:

    /halp
