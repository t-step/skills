# Tasks: SAI remaining work (open tickets under Feature/SAI, CASSANDRA-16052)

Real Jira issue IDs are used as task IDs. These are the currently open,
described tickets under the SAI component; already-merged phase 1/2 work
(the index-group interface, the in-memory index and query path, and the
on-disk string/literal index and its query path) is *not* included here --
see `repository-state.md` for what has already landed.

- **CASSANDRA-18067 -- On-disk numeric index.** Add an on-disk numeric
  index format and on-disk query path covering "all datatypes not
  supported by the on-disk literal index (CASSANDRA-18062)" -- i.e., the
  numeric-type counterpart to the already-merged on-disk string/literal
  index. Per the CEP-7 design, based on a modified one-dimensional block
  kd-tree adapted from Lucene. The largest remaining implementation item;
  in active development since November 2022.

- **CASSANDRA-18112 -- Add the feature of INDEX HINT for CQL.** Filed by
  an external contributor requesting a way to hint
  or force which secondary index CQL should use when a table has more
  than one index and a query could be satisfied by either. The filer's
  own description says a hint feature for CQL generally "may be a
  gigantic task with no clear goal," and that the specific grammatical
  form needs a mailing-list DISCUSS thread before implementation starts.

- **CASSANDRA-18165 -- Investigate removing PriorityQueue usage from
  KeyRangeConcatIterator.** During review of the (already-merged)
  in-memory index and query path work, it was identified that
  `KeyRangeConcatIterator`'s use of a `PriorityQueue` to maintain its
  active list of sorted `KeyRangeIterator`s could potentially be replaced
  with a simpler skip-based implementation. It was explicitly decided
  this change needed its own performance and correctness testing and
  would not be folded into the original ticket.

- **CASSANDRA-18166 -- Improve the code model around IndexContext.**
  `IndexContext` currently has to be constructed even for a non-indexed
  column, purely to carry information needed for post-filtering, which
  forces assertions throughout the code to guard against that case.
  Proposes splitting the column/index information needed for
  post-filtering out from the indexing/searching-specific information, to
  remove the need for those assertions.

- **CASSANDRA-18167 -- Bypass row-awareness for small partitions.** SAI's
  row-awareness (indexing both partition key and clustering key)
  significantly helps query performance for wide partitions with many
  rows, but may be unnecessary overhead for small partitions, where
  reading the whole partition and post-filtering (or batching rows for a
  single partition) could be cheaper. Notes SAI already tracks partition
  sizes during indexing and floats feeding those sizes into a histogram
  in index metadata to decide when to apply this optimization, but does
  not commit to a specific design ("However this is achieved...").
  Currently unassigned.

- **CASSANDRA-18216 -- Allow sharding of the SAI in-memory index.** The
  general Memtable implementation supports splitting into shards to
  reduce write contention; the SAI in-memory index (`MemtableIndex`,
  delivered by the already-merged in-memory index and query path work)
  does not, so all writes currently hit one synchronized write block.
  Proposes adding sharding to `MemtableIndex`, and using shard/key-range
  information to let in-memory searches search fewer indexes.

- **CASSANDRA-18280 -- Investigate initial size of
  GrowableByteArrayDataOutput in RAMIndexOutput.** `RAMIndexOutput`, used
  to build on-disk postings in SAI, initializes its backing
  `GrowableByteArrayDataOutput` at a fixed 128 bytes with no stated
  rationale, and grows only by allocating exactly enough for each write
  rather than in blocks -- likely producing many small reallocations and
  array copies once postings grow past that size. Proposes investigating
  a larger initial size and/or block-wise allocation.

- **CASSANDRA-18345 -- Enable streaming SAI components as part of
  repair.** SAI registers its on-disk components with the SSTable
  descriptor, expecting them to participate in the normal SSTable
  lifecycle, including streaming -- but the current SSTable format
  streams a fixed, hardcoded set of components
  (`Components.STREAMING_COMPONENTS`) rather than the actual set of
  components registered against a given SSTable. This needs to change so
  that streaming (and, by extension, repair -- which streams SSTables
  between replicas) carries SAI's index components along with the base
  SSTable data.

- **CASSANDRA-18479 -- Add basic text tokenisation and analysis.** The
  Index Group interface work (CASSANDRA-16092) removed text
  analysis/tokenisation support that existed previously. Adds it back via
  three analyzers: `normalize` (NFC text normalization), `case_sensitive`
  (case-sensitivity control), and `ascii` (ASCII folding).

- **CASSANDRA-18490 -- Add checksum validation to all index components on
  startup, full rebuild and streaming.** SAI does not currently
  checksum-validate per-column index data files at any point; it does
  checksum-validate per-SSTable components after a full rebuild, and
  checksum-validates per-column metadata on opening. Proposes
  checksum-validating all index components on startup, full rebuild, and
  streaming.

- **CASSANDRA-18494 -- Upgrade the vendored lucene-core dependency.**
  SAI's vendored `lucene-core` library is currently at version 7.5; this
  should be updated to whatever the current latest stable version of
  Lucene is.

- **CASSANDRA-18515 -- Optimize initial concurrency selection for the
  range read algorithm during SAI queries.** The distributed range-read
  path uses each index implementation's estimated-result-rows count to
  decide how many replicas to contact per round. SAI (like SASI before
  it) always returns an extreme value for that estimate to guarantee it's
  preferred over other index types on the same query -- which, as a side
  effect, floors the initial concurrency factor to 1, so a query is only
  ever sent to one replica per round even when many replicas could
  usefully be queried in parallel. Proposes letting an index bypass that
  initial concurrency-factor calculation so SAI queries can use more of
  the available round-robin parallelism.

- **CASSANDRA-18521 -- Unify CQLTester#waitForIndex and
  SAITester#waitForIndexQueryable.** A discussion on CASSANDRA-18217
  noted these two test-helper methods do the same thing and could be
  unified, and separately that it's easy to forget to call either of them
  after `CQLTester#createIndex`. Proposes renaming `createIndex` to
  `createIndexAsync` and adding a new method (e.g. `createIndexSync` or
  `createIndexAndWaitForQueryable`) that creates an index and waits for
  it to become queryable in one call.

No task above states an explicit relative priority against any other task
in this list; see `source-notes.md` for the one priority signal that does
exist (which phase of the overall SAI effort is currently active).
