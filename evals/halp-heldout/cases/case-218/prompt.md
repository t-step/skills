You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You wrote timestamp parsing and the hourly rollup for plan task 4.
- You ran the test:

    $ pytest -q tests/test_rollup.py
    E   ValueError: time data '2026-09-01T09:15:00-05:00' does not match format '%Y-%m-%dT%H:%M:%SZ'
    1 failed

The user now types:

    /halp
