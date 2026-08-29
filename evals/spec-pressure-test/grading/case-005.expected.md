# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** invariant-unenforceable-at-stated-ownership-boundary

**Why:** FR-002 states an absolute invariant ("MUST NOT render any item as
available if it is currently blocked") and SC-002 makes it stronger still
by grounding correctness in *the authoritative server state at render
time*. But FR-001/FR-003/SC-001, in the same document, require the browser
to render its initial screen from a local snapshot with **no network call**
on the critical path, refreshed only periodically/opportunistically, and
explicitly designed to keep working while offline (Assumptions). By the
spec's own construction, the browser cannot always know, at the instant it
renders, whether the server's blocking state has changed since the last
sync -- an item that became blocked seconds after the last sync, and is
rendered before the next one, will be shown as available by any
implementation that follows FR-001/FR-003 as written, directly violating
FR-002/SC-002. The component the spec assigns responsibility to (the
browser, rendering from its own local snapshot) does not have the
information, at the moment it needs to act, to actually guarantee the
invariant it's told to guarantee.

Concrete scenario: item X is unblocked when the last snapshot sync ran. 90
seconds later (well within the "every few minutes" cadence of FR-003), a
new blocking relationship on X is created server-side. An agent opens the
browser at second 91: FR-001/SC-001 require it to render instantly from
the (now-stale) local snapshot; FR-002/SC-002 require X not to appear as
available. Both cannot be satisfied by a browser that renders offline-first
from a periodic snapshot, as this spec's own requirements describe one.

This is a **Blocking ambiguity** grounded in an unenforceable invariant,
not merely a staleness nitpick: SC-002 is written as an absolute ("no item
ever renders as available... as observed by the authoritative server state
at render time"), and the spec gives the responsible component no way to
meet that literal standard given its own offline-first design. The
smallest closing question: does FR-002/SC-002 actually mean "consistent
with the last synced snapshot" (a much weaker, achievable guarantee,
requiring the SC's wording to be corrected), or is a lighter-weight
freshness check before render (undermining the "no network call" promise
in FR-001/SC-001) actually intended? The report should present this as an
open choice between correcting the invariant's wording or relaxing the
offline/instant-render guarantee, not silently assume one answer.

A pass that notes only "the snapshot could be stale" as a vague
observation, without connecting it explicitly to FR-002/SC-002's absolute
wording and naming the resulting contradiction, does not fully meet this
case's bar -- the finding needs to be about enforceability of the stated
invariant specifically, not a generic caching-lag comment.
