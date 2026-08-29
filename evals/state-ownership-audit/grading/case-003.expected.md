# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** partitioned-authority-not-single-source

**Why:** Each FC's `available_units` lives in that FC's own regional
database and is written only by code touching that FC's own data --
authority is legitimately partitioned by FC, not global, and deliberately
so (to preserve local sell-through during a network partition).
`GlobalCatalog` is a read-only, periodically-polled aggregate with no
write authority and a documented degradation mode (skip an unreachable
FC). The trap is the architect's proposal, which sounds like a
simplification ("one number, one owner") but would actually invert a
deliberate availability tradeoff -- collapsing to a single
`GlobalCatalog`-backed authority removes the very property (each FC can
keep selling independently) the partitioning exists to provide. A correct
audit names the partitioned shape explicitly and pushes back on the
proposal with the concrete consequence, rather than agreeing that "one
source of truth" is obviously the tidier design.
