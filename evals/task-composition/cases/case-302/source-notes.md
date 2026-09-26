# Source notes

## Where this task set came from

Every task above is a currently open Apache Cassandra Jira issue in the
`Feature/SAI` component, under the umbrella epic CASSANDRA-16052 (CEP-7,
Storage Attached Indexes). This is the real, currently-filed backlog for
this area of the project as of this snapshot -- not a curated or
simplified example.

## Stated priority

The umbrella epic's own status update lays out the remaining SAI work as
five phases (quoted in `context.md`). Of those:

- Phases 1 and 2 have already merged to the feature branch (see
  `repository-state.md`).
- **Phase 3 -- the on-disk numeric index, CASSANDRA-18067 -- is the
  named, currently active priority.** It is the next phase in the
  epic's own stated sequence now that phases 1 and 2 have merged, and it
  is the largest and longest-running item still open -- work on it has
  been underway since November 2022, in parallel with phases 1 and 2
  being finished and merged.
- Phases 4 (a dedicated fuzz-testing model) and 5 (`LIKE` query support)
  are stated as future phases. Phase 5 has a placeholder epic filed, but
  its own description explicitly leaves the indexing approach "open to
  suggestions" with no committed design -- it has not been broken down
  into any concrete task, so nothing from it appears in `tasks.md`.

**No relative priority is stated among the twelve smaller tasks**
(18112, 18165, 18166, 18167, 18216, 18280, 18345, 18479, 18490, 18494,
18515, 18521). They surfaced independently -- some from code review on
already-merged work, one from an external contributor's feature request
-- and nothing in the record ranks them against each other. Do not invent
a priority ordering among them.

## Filing order vs. dependency order

The tasks in `tasks.md` are listed in filing (creation) order, which
spans roughly five months (November 2022 -- May 2023). Filing order is an
accounting detail here, not a dependency signal -- e.g. CASSANDRA-18490
(filed May 2023) depends on CASSANDRA-18345 (filed March 2023), which is
already the "expected" direction, but that shouldn't be assumed to hold
in general for this list; check the concrete dependencies described in
`dependencies.md` rather than relying on filing order or issue-number
order.
