# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** stale-agent-instructions-high-reach

**Why:** AGENTS.md's migration instructions name a directory
(migrations/legacy_sql/) and a script (migrate.sh) that don't exist
anywhere in the repository; the repository actually uses Alembic
(migrations/versions/, alembic.ini, CI running `alembic upgrade head`).
This is the highest-reach case in the suite on purpose: the same
mismatch, if found in a low-traffic module doc, would be a minor finding,
but here it sits in the file an agent is instructed to read and obey
before its very next action. A correct audit names this as Contradicted
and explicitly credits AGENTS.md's status as a root governing
agent-instruction file as part of why the finding ranks highly -- not
merely restating that the instructions are wrong -- and states the
concrete consequence (an agent following it literally creates a
nonexistent-path file and runs a script that doesn't exist).
