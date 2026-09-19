You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You implemented T004 (ranking) and its tests, then added a test that ranks the upstream sample export in `data/sample_cohort.json`.
- You ran the suite:

    $ python3 -m unittest discover -s tests
    ERROR: test_ranks_upstream_sample (tests.test_sample_data.SampleDataTests)
      File "cohort/normalize.py", line 6, in normalize_score
        v = max(lo, min(hi, value))
    TypeError: '<' not supported between instances of 'NoneType' and 'int'
    Ran 6 tests in 0.001s
    FAILED (errors=1)

- You told the user: "I'll add a None guard to normalize_score and re-run." You haven't done it yet; the user typed the command below first.

The user now types:

    /halp
