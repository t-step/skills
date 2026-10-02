# Repository state

- SAI is developed on a long-lived feature branch, not directly against
  trunk. Individual tickets are reviewed and merged to that branch one at
  a time; the branch itself is periodically rebased against trunk as
  trunk moves forward.

- Already merged to the feature branch (not part of the remaining task
  list): the index-group interface (CASSANDRA-16092), the in-memory index
  and its query path built on a trie-based memtable index
  (CASSANDRA-16108 / CASSANDRA-18058), the on-disk string/literal index
  and its on-disk query path (CASSANDRA-18062), and removal of the
  `ALLOW FILTERING` requirement for CQL queries using multiple index
  expressions (CASSANDRA-18217).

- Trunk was bumped to version 5.0 as of a separate, already-completed
  release-process ticket (CASSANDRA-17973, closed March 2023) -- SAI is
  explicitly stated (in review discussion on the already-merged on-disk
  string index work) as not landing in any 4.x release.

- **The feature branch's periodic rebases have already surfaced real
  coupling to unrelated, non-SAI trunk work.** During a March 2023
  rebase, changes elsewhere in the codebase to the SSTable format API
  (a separate, already-completed CEP unrelated to SAI) required removing
  some capabilities from `SSTableFlushObserver` in SAI's own code to keep
  the branch rebasing cleanly. This is a concrete, already-observed
  instance of the kind of external coupling named in
  `dependencies.md` for CASSANDRA-18345 (which touches the same
  streaming/SSTable-component area) -- not a one-off, hypothetical
  concern.

- As of the most recent rebase-related update, the branch's Python
  distributed-test (dtest) pipeline was not yet fully wired up for this
  branch, though its unit and in-JVM distributed test suites were
  running as part of normal review.
