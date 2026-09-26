# Source notes: Hudi Metadata Table — synchronous redesign and default-on push

**Where this came from:** the Apache Hudi Jira project (issues.apache.org/jira,
project HUDI). All 19 tasks are real, currently-filed tickets, most of them
linked as children of the HUDI-1292 "[Umbrella] RFC-15: Metadata Table for
File Listing and other table metadata" epic (or directly related to it);
HUDI-2276 is also cross-linked under a separate, broader "make performant
out-of-box configs" epic (HUDI-2151), since defaulting metadata table on is
one instance of a wider effort to ship better out-of-the-box defaults, not
solely a metadata-table-specific initiative. This is the current backlog
as filed — nothing has been reworded to sound cleaner or more decomposed
than it actually is. HUDI-2475 is filed with only a title and no body yet
(see its entry in `tasks.md`); HUDI-2458 is filed as a problem statement
with no proposed mechanism yet (also see `tasks.md`) — both are genuinely
that thin in the tracker right now, not summarized down from something
richer.

**Stated priority:** present on every ticket, but not very discriminating
here — 11 of the 19 tasks are marked Priority: Blocker (see the bottom of
`tasks.md`). Treat "Blocker" as "the team considers this a hard requirement
for shipping this effort," not as a ranking among the 11 tasks that share
the label.

**Current repository state (as of this task list):**
- `hoodie.metadata.enable` defaults to `false` on both the write path and
  the read path. Users opt in explicitly. This has been true since the
  feature's introduction in 0.7.0/0.8.0.
- The metadata table is an internal Merge-on-Read table stored under
  `.hoodie/metadata`, currently holding only a "files" partition (partition
  and file listing). It does not yet contain any secondary index (no
  record-level index, no column-range/column-stats index) — that's future
  work this redesign is meant to unblock, not something already built.
  Don't assume tasks below are about indexing beyond file listing; none of
  them are.
- Hudi 0.9.0 just released this week without the default-on flip that had
  originally been the plan for this release — it's still pending, which is
  most of why this backlog exists.
- Multi-writer support (an external lock provider) already exists for the
  *data* table independent of the metadata table; the metadata table's own
  synchronous design (HUDI-2285) is what introduces locking/contention
  considerations specific to metadata table writes.
