# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** policy-not-persisted-row

**Why:** This fixture's whole point is that the load-bearing domain
concept -- "what makes a deployment eligible to promote" -- has no
dedicated table, no status field, and no persisted row. It's a function
composed from `POLICY`, computed fresh every call. A shallow pass that
only inventories `Deployment` and `Approval` as "the domain model" (both
of which do have persisted fields) has missed the actual point of the
fixture: the gate/policy abstraction in `gates/` and `promotion.py` is
itself a first-class domain concept, expressed as code and rules rather
than as a row. `Approval` should be characterized as an input a gate
reads (a vote), not as the entity that owns the eligibility decision --
that authority sits with the gate/policy, evaluated fresh each time.
