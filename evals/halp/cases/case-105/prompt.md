You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You are implementing T004 (ranking with name tie-break): `cohort/ranking.py` and its tests exist and are uncommitted.
- Last test run:

    $ python3 -m unittest discover -s tests
    ERROR: test_tie_break_by_name (tests.test_ranking.RankTests)
    NotImplementedError: tie-break by name (FR-3)
    Ran 5 tests in 0.000s
    FAILED (errors=1)

- You had just told the user: "Next I'll implement the tie-break in ranking.py by sorting on name after score." You hadn't started yet when the user typed the command below.

The user now types:

    /halp what's the difference between normalize_score and normalize_selector?
