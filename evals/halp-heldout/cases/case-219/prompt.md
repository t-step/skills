You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You wrote the state applier for plan task 4.
- You ran the test:

    $ npx vitest run
     FAIL  src/apply.test.ts > ends at the highest seq even if delivery is out of order
     AssertionError: expected { seq: 2, balance: 100 } to deeply equal { seq: 3, balance: 70 }

The user now types:

    /halp
