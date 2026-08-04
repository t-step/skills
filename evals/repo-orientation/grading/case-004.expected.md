# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** README claims Postgres and a real `npm test` suite;
`package.json`/`src/db.js` show `better-sqlite3` and a no-op `test` script
(`echo "no tests yet" && exit 0`).

**Why:** Directly tests the "deterministic facts over prose" rule. The
correct database is SQLite, grounded in the dependency list and `db.js`,
not Postgres. The correct statement about tests is that no real test suite
exists — the `test` script is a stub — not that `npm test` runs a passing
suite. Both conflicts should be named explicitly, not silently resolved in
either direction.
