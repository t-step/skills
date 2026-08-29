# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** terminology-map-same-and-different

**Why:** This fixture pairs two terminology traps that need opposite
resolutions, and a shallow pass is likely to get at least one backwards:

- `Customer` (billing) and `account` (the public API's field names) are
  the *same* underlying row under two names -- `get_account` calls
  billing's `get_customer` with the same id, and `account_response` is a
  pure field rename. Nothing in the fixture states this conclusion in
  prose; it has to be traced through the call.
- `Member` (loyalty) sits right next to `Customer`/`Account` -- another
  people/identity-shaped concept -- and is tempting to fold into the same
  bucket. It's genuinely different: `MemberCustomerLink` is many-to-many
  (a household `Member` can link to more than one billing `Customer`),
  and a `Customer` can have zero `Member` rows. Collapsing `Member` into
  `Customer`/`Account` because they're all "people" concepts is the
  specific mistake this case exists to catch.

A correct orientation states both conclusions explicitly, in a
terminology-map-shaped section, each grounded in the specific evidence
(the call chain for the first, the join table's cardinality for the
second) rather than either guessed from the names alone.
