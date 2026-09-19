You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- The user asked you to implement T004 (ranking with name tie-break).
- You wrote `cohort/ranking.py` and `tests/test_ranking.py`, then ran the tests:

    $ python3 -m unittest discover -s tests
    FAIL: test_tie_break_by_name (tests.test_ranking.RankTests)
    AssertionError: Lists differ: ['zed', 'amy', 'bo'] != ['amy', 'zed', 'bo']
    Ran 5 tests in 0.000s
    FAILED (failures=1)

The user now types:

    /halp why does zed come out above amy on a tie? could we just flip reverse=True to False?
