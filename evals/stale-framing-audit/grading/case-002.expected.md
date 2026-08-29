# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** true-statement-implies-wrong-write-authority

**Why:** "Coordinator manages worker state and routes incoming tasks... based
on the current worker registry" is not false -- the Coordinator really does
route tasks using worker data. But coordinator.py never writes to the
`workers` table and has no database handle at all; worker_registry.py is
the sole writer, and Coordinator only holds an in-memory summary derived
from published events. This is the paradigm "true statement, wrong induced
ownership model" case the skill's Misleading-emphasis category exists for.
A correct audit does not call the README claim false, names the specific
phrase doing the misleading work ("manages worker state"), grounds the
correction in worker_registry.py's write path and coordinator.py's
lack of any write path, and directly tells the engineer the new write
belongs in worker_registry.py.
