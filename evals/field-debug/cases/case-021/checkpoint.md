## field-debug checkpoint: nightly customer-export job silently dropping rows for large accounts

**Objective**: find why the nightly customer-record export job has been
dropping a small percentage of rows, for the last 3 nights running, for
some customers but not others.

**Current system model**: `export_job_excerpt.md` shows the job paginates
through each customer's records using `recordsdb-client` (a third-party
library, v4.2), fetching pages of 500 records at a time using the
library's own keyset cursor (`next_cursor`, derived from each page's last
row) rather than a plain numeric offset. No deploy or config change to
this job in at least 6 weeks.

**Observations**:
- Drops have occurred on all 3 of the last 3 nightly runs: 4.2%, 3.9%,
  and 4.1% of rows missing from the export, in that order (oldest to most
  recent).
- Every night, the affected customers are the same 12 accounts, and only
  those 12. All 12 have more than 10,000 records each (i.e., they always
  require multiple pages to export). No customer with under ~2,000
  records has ever shown a drop.
- Those same 12 accounts are also the only customers in our whole book
  with meaningful order/record-update activity happening *during* the
  export window (02:00-02:30 UTC) -- everyone else's data is essentially
  static at that hour.
- Small/inactive accounts, even ones that happen to be large in record
  count but inactive overnight, have never shown a drop in the export
  history I checked.

**Active hypotheses**:
- H1: `recordsdb-client`'s keyset-cursor pagination is not safe against
  concurrent writes to the boundary row between pages -- i.e., if the
  last row of a fetched page gets updated after being read but before the
  next page is requested using it as the cursor, some rows may be
  silently skipped. This would explain both correlations at once (large
  accounts need multiple pages; only accounts with concurrent activity at
  export time can hit the unsafe window) without needing two separate
  explanations.

**Ruled-out hypotheses**: a plain offset-based pagination bug (skipping
or double-counting a fixed offset) is ruled out -- the job uses the
library's keyset cursor, not manual offsets, and the drop rate isn't
consistent with any fixed page-boundary miscount I can construct.
Application-level filtering/validation dropping rows is ruled out -- the
missing rows aren't filtered by any business rule I can find; they're
present in the source query's row count but absent from the exported
file.

**Assumptions**: assuming the 12-account overlap across all 3 nights is
meaningful and not coincidence -- reasonable given it's the *same* 12
accounts each night, not a random subset, but not proven by anything
beyond the consistency of the pattern itself.

**Unknowns**: whether `recordsdb-client`'s keyset cursor actually has a
documented concurrent-write caveat -- I couldn't reach the library's docs
site from this sandbox to check. That's the one thing that would confirm
or eliminate H1 outright.

**Constraints**: no other hypothesis is currently live; if the docs don't
confirm a concurrent-write caveat, this needs a different explanation
than H1 and I don't have one queued up yet.

**Last known-good / first known-bad boundary**: not cleanly known -- this
could have been happening for longer than 3 nights; 3 nights is just as
far back as export logs are retained.

**Next discriminating move**: check `recordsdb-client`'s official
documentation (or CHANGELOG) for any known caveat about keyset-cursor
stability when the boundary row is concurrently updated. Couldn't reach
it from here -- whoever resumes this should check that specifically. If
it confirms the caveat, H1 is settled; if not, this needs fresh
hypotheses.

**Time-sensitive evidence that should be revalidated on resume**: the
exact drop percentages (4.2%/3.9%/4.1%) and the specific 12-account list
are current as of last night's run -- confirm the pattern is still
holding (same accounts, similar magnitude) before relying on it, though
the underlying job code and deploy version are not expected to have
changed on their own.
