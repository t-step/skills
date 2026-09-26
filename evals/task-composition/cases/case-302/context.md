# Context: SAI (Storage Attached Indexes) -- remaining work under CASSANDRA-16052

Storage Attached Indexes (SAI) is a new secondary-index implementation for
Apache Cassandra, developed under the community-adopted CEP-7 proposal and
tracked as an umbrella epic, CASSANDRA-16052. Because it changes core
indexing behavior, it is being developed on a long-lived feature branch
rather than directly against trunk, with individual pieces reviewed and
merged to that branch one Jira ticket at a time.

The epic's own status update described the remaining work as five phases:

1. The index-group interface and memtable-adjacent (in-memory) indexing
   and query path.
2. On-disk SSTable indexing tooling, including the on-disk text/literal
   index and its query path.
3. An on-disk format for numeric indexing, with end-to-end numeric
   equality and range query support.
4. A dedicated fuzz/property-testing model ("Harry") for exercising SAI.
5. `LIKE`-operator prefix/suffix query support, plus related CQL
   statement-restriction cleanup.

Phases 1 and 2 have merged to the feature branch. Phase 3 -- the on-disk
numeric index -- is the actively worked, currently prioritized item.
Phases 4 and 5 have not yet been broken down into concrete engineering
tasks; a placeholder epic exists for phase 5's `LIKE` support, but its own
description says its indexing approach is "open to suggestions," so no
task from it is included below.

Alongside phase 3, a number of smaller improvements, cleanups, and
test-infrastructure tickets have accumulated -- surfaced during code
review and design discussion on the already-merged phase 1/2 work, plus a
couple of externally-filed feature requests. The task list below is every
currently open, described SAI-component ticket as of this snapshot; there
is no other backlog or roadmap to consult beyond what's written here and
in the accompanying dependencies/source-notes files.
