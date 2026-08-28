# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** cdc-index-lag-not-peer-sync

**Why:** `trust_and_safety.py` is the only writer of `User.status`; the
search pipeline README states plainly that the indexer only ever copies
what CDC delivers from the `users` WAL. That is a textbook projection
relationship, not two peers. The support ticket's 10-minute gap is
larger than the documented ~5s typical lag, which is worth flagging as a
possible DLQ/backlog symptom -- but it's still staleness of a derived
view, not evidence of two independently-authoritative lifecycles out of
sync. The trap is the ticket's proposed fix: "should the admin panel
also write directly to the search index?" -- which would create a
*second* writer of the projection, undermining the single-writer CDC
design rather than fixing anything. A correct audit names User.status as
sole authority, names the search document as derived/staleable, and
either rejects the direct-write proposal outright or at minimum flags
the second-writer risk it introduces; it redirects the real fix toward
CDC lag/DLQ monitoring, not a reconciliation mechanism between the DB
and the index.
