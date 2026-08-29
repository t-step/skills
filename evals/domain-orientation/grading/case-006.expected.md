# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** canonical-vs-derived-and-lifecycle-flagging

**Why:** This fixture tests the canonical-vs-derived distinction on a
concept with no lifecycle at all (a price), directly beside a sibling
concept in the same file that does carry a lifecycle (`Product.status`).
A correct orientation must apply two different, correct treatments within
the same short report: `DisplayPrice` gets the full "other representation"
treatment (derived, one-directional, can be stale) without being handed
its own lifecycle entry it doesn't have anything to fill in for, while
`Product.status` gets flagged as a lifecycle-audit candidate and nothing
more -- no inline transition table.

The trap for a shallow pass is treating `DisplayPrice` as either a peer
"price" concept (since it's its own persisted table with its own fields)
or, in the other direction, forcing lifecycle language onto it because
the fixture sits next to `catalog/lifecycle.py`. Neither is right:
`fx_refresh.py` shows the data flows only `Product.price_cents_usd ->
DisplayPrice`, never the reverse, and `DisplayPrice` has no transition
guard or illegal-value rule of its own.
