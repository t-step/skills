# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-invariant-separately-owned

**Why:** Auction and Bid are genuinely separate lifecycles (separate
databases, separate teams, separate transition functions) linked by
exactly one shared invariant (no bid accepted while its auction isn't
open) and one cross-boundary transition-triggering side effect
(`close_auction` -> `reject_all_open_bids`). The subtlety this case is
built around: the invariant is actually enforced on Bid's own side, via
`accept()`'s live check of auction status -- the bulk-reject on close is
cleanup/tidiness (moving stale `submitted` bids to `rejected`), not the
thing actually preventing an invalid accept. The incident confirms this:
when the reject RPC failed for six hours, the invariant still held,
because `accept()` independently re-checked. A shallow reading could
overclaim in either direction -- concluding the invariant was violated
(it wasn't) or concluding the missing retry doesn't matter at all (the
stale status for six hours is still a real, worth-naming gap, even
though it wasn't a correctness violation). A correct audit keeps these
separate: name the shared invariant, correctly attribute where it's
actually enforced, name the retry gap as a real mechanical finding, and
leave "should this be fixed" as the retro's own explicitly open
question rather than resolving it either way.

**Second, independent thing this case guards:** the accept()-reads-
Auction-status relationship is a mechanism/consistency trap in its own
right. `accept()` only ever reads `Auction.status` -- Auction never
reads or reacts to Bid -- so the mechanism is unambiguously One-way
observation. But that same one-way read is what carries the entire
shared invariant: nothing about Bid's or Auction's *persisted* state
ever needs to agree for the check to be correct, because it's resolved
live at the moment of the transition. A response that classifies this
channel as "One-way observation" and then defaults its consistency
answer to "no joint constraint" -- reasoning that one-way reads don't
carry joint constraints -- has derived the consistency axis from the
mechanism axis instead of evaluating them independently, even if its
surrounding prose correctly describes the invariant. The correct
consistency answer for this specific channel is a shared invariant
(with tolerable disagreement on the *status field* itself, since
`Bid.status` can lag by hours without breaking anything, per the
incident). This is graded as its own required point, separate from
whether the report gets the overall "does the missing retry break
anything" question right.
