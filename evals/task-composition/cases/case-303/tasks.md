# Tasks: Hudi Metadata Table — synchronous redesign and default-on push

This is the current Jira backlog for this effort, as filed, sorted by
issue ID. There is no other roadmap document beyond what's written here.

- **HUDI-2276** — Enable Metadata Table by default for both writers and
  readers. Metadata table has been available since 0.8.0 but ships
  disabled by default (opt-in via config) because it was released as an
  experimental feature. Turn it on by default for both the write path and
  the read path so users get the file-listing performance benefit out of
  the box without extra configuration.

- **HUDI-2285** — Metadata Table Synchronous Design. Metadata Table v1
  (0.7.0) only supports file-listing and syncs to the metadata table
  somewhat asynchronously relative to the reader. To add further metadata
  (a record-level index and column-range/column-stats indexes) at large
  scale (50B+ records), and to support a multi-writer model where table
  services like clustering, cleaning, and backfills run in separate
  pipelines, the metadata table needs a re-architected, synchronous
  design: every write-side operation on the data table synchronously
  updates the metadata table's delta-commit before the data-table commit
  itself completes, and readers rely on the completed data-table timeline
  rather than needing to sync/catch up on the read side. Because each
  operation writes to the same single file slice for a given partition
  (e.g. the file-listing partition), only one writer at a time may update
  the metadata table, enforced via the existing Transaction Manager lock.
  Upgrading from the current (v1) design requires re-bootstrapping the
  metadata table (schema differs, and reconciling in place isn't
  practical) rather than an in-place migration.

- **HUDI-2303** — Bug surfaced while enabling Metadata Table by default:
  MergeOnReadTable test fails after compaction. While enabling metadata
  table in tests (as part of the work to turn it on by default),
  `TestMergeIntoLogOnlyTable` fails: after a Merge command triggers inline
  compaction, the resulting parquet file is missing data from the latest
  log file written right before compaction. Likely cause: the metadata
  table is returning an incorrect file list for the compaction step,
  omitting the most recent log file.

- **HUDI-2395** — Make metadata table tests lean and consistent. Rewrite
  the metadata-table test suite to consistently use the shared
  `HoodieTestTable` test-table utility instead of ad hoc test setup, so
  tests are leaner and behave consistently with each other.

- **HUDI-2422** — Add rollback plan and rollback.requested instant.
  Rollback currently determines what to delete by listing files at
  rollback time; add an explicit rollback-planning phase that first
  computes and serializes the full list of files-to-delete into a
  `HoodieRollbackPlan`, published as a new `<instant>.rollback.requested`
  timeline file, before actually executing the rollback
  (`<instant>.rollback.inflight` / `.rollback`). Follow-ups noted on this
  ticket: upgrade/downgrade handling for in-flight rollbacks that predate
  this change, updating the CLI's rollback tooling, and retiring the old
  `ListingBasedRollbackRequest` class once the new plan-based
  `HoodieRollbackRequest` serialization is in place.

- **HUDI-2432** — Fix restore by adding a requested instant and restore
  plan. Restore internally issues N rollbacks (processed newest-to-oldest)
  and does not publish those individual rollbacks to the timeline until
  the whole restore commits — so if restore fails partway through, a
  retry may only see a subset of the still-needed rollbacks and apply an
  incomplete set to the metadata table. Needs its own restore-plan file
  (serializing the full list of instants to roll back) so a retried
  restore can tell which rollbacks were already applied versus still
  pending, mirroring the rollback-plan approach.

- **HUDI-2436** — Investigate rollback log-file bookkeeping for cloud
  stores without append support. Open question raised from PR review: for
  cloud stores that don't support file append (unlike HDFS), if a crash
  happens mid-commit or mid-rollback, it's unclear whether the log file
  involved in the crash is correctly included or excluded when the
  rollback plan collects files to delete/log, and whether a retried
  rollback replays cleanly to the metadata table in that case. Needs
  follow-up with the RFC's author to confirm the exact failure scenario
  before a fix is scoped.

- **HUDI-2444** — Fix missing files in clean/rollback metadata when
  retried after a failed attempt. If a clean or rollback operation fails
  on its first attempt and is then retried, the commit metadata produced
  by the retry can omit files that were already deleted during the first
  (failed) attempt. Since every file affected by clean/rollback needs to
  be reflected in what's applied to the metadata table, the retry's
  metadata needs to account for files removed in earlier attempts too.

- **HUDI-2452** — Spark-on-Hudi: metadata key-length/file-not-found error
  with a non-empty record key. Reported externally: querying via Spark
  with metadata table enabled produces a "key length <= 0" / file-not-found
  error even though the data's primary key is non-empty. Reporter attached
  a GitHub issue (apache/hudi#3688) with error details for investigation.

- **HUDI-2458** — Relax metadata-table compaction fencing on in-flight
  data-table requests. Compaction of the metadata table currently only
  runs if there are no in-flight requests on the data table. For large,
  continuously-running deployments this can starve metadata-table
  compaction indefinitely if the data table always has *something* in
  flight (e.g. clustering or a backfill). Filed as a problem statement
  only — no proposed fix or mechanism is described yet.

- **HUDI-2459** — Support async compaction for metadata table.
  Metadata-table compaction is currently inline (synchronous) only.
  Because metadata-table compaction is fenced on there being no in-flight
  data-table requests (see HUDI-2458), a data table whose
  compaction/clustering keeps failing could end up never compacting its
  metadata table either. Need a strategy for running metadata-table
  compaction asynchronously instead, while still correctly reconciling
  file adds/removes recorded by intervening rollbacks (e.g. a file added
  by one commit attempt, rolled back, then re-added under a retried
  attempt, should end up reflected once, correctly, regardless of whether
  compaction has run yet).

- **HUDI-2460** — Async cleaning with metadata table. Cleaning of the
  metadata table is currently inline only; relax this so cleaning can also
  run asynchronously.

- **HUDI-2468** — Fix rollback of the first commit after it's been synced
  to the metadata table. Rolling back a table's very first commit
  (including a bootstrap commit) after it has already been synced to the
  metadata table hits a bootstrap check: the code compares the metadata
  table's last-synced instant against the data timeline, finds the
  (in-flight, being-rolled-back) commit no longer looks "active," and
  decides the metadata table needs re-bootstrapping — but re-bootstrap is
  itself only allowed when there are no in-flight instants on the data
  table, and this very commit is in flight. All of `TestBootstrap` fails
  under this condition when metadata is enabled. Possible fix under
  consideration: pass the current in-flight instant being operated on into
  the metadata table writer so it can be excluded from that in-flight
  check, but there may be a cleaner approach.

- **HUDI-2472** — Track and fix test failures caused by enabling metadata
  table by default. Turning metadata table on by default (HUDI-2276)
  breaks a number of existing tests, mostly in hudi-spark-client. Tracking
  ticket to work through them module by module and fix (rather than
  permanently disable metadata in the test) where possible. Known so far:
  several MOR rollback/compaction tests that roll back the first commit
  hit the bootstrap issue tracked separately in HUDI-2468; some tests
  using the legacy test-table harness fail and are candidates for the
  HoodieTestTable rewrite; one deltastreamer test also fails, cause not
  yet identified. hudi-client-common,
  hudi-flink-client, hudi-common, hudi-timelineserver, hudi-sync,
  hudi-spark2/3, and hudi-examples currently pass with metadata enabled.

- **HUDI-2474** — Refresh timeline before every operation when metadata is
  enabled. With metadata enabled, the table's timeline needs to be
  refreshed before every operation, or some completed states can be
  missed; at minimum this is required for delta-streamer's continuous
  mode, where several tests currently fail without it.

- **HUDI-2475** — Upgrade/downgrade infra for enabling metadata table by
  default. Filed with only this title as of right now — no body text,
  design reasoning, or proposed sequencing has been written into the
  ticket yet. It exists as a placeholder flagging that rolling out the
  synchronous metadata design (HUDI-2285) to an already-running
  deployment (a writer plus separate async table-service processes) is a
  question that needs an answer, without yet specifying what that answer
  looks like.

- **HUDI-2476** — Fix retried compaction commit clobbering already-synced
  metadata state. Compaction (and clustering) reuses the same instant time
  on retry. Walk-through: commits c1, c2 land, compaction cc3 begins and
  syncs to the metadata table before crashing prior to committing on the
  data table, then c4 (and possibly more commits) land normally. When
  compaction is retried in the data table, the pending cc3 is first rolled
  back (itself an upsert into the metadata table), and then compaction
  re-runs under the same instant time cc3 — but the metadata table already
  has a completed delta-commit for cc3 from the earlier (crashed) attempt,
  so the second attempt's write to the metadata table fails. Proposed fix:
  when a commit instant is being retried, delete its previously-completed
  metadata table instant before re-applying, so the merged log state
  correctly reflects only the retried attempt's files.

- **HUDI-2477** — Restore fails after rollback.requested instant is added,
  with metadata enabled. Restore schedules a rollback for each of the N
  commits being restored (each producing a `rollback.requested` instant on
  the timeline — required by the new rollback-plan design, HUDI-2422 —
  but the *completed* rollback is intentionally never published) and only
  publishes the overall restore commit at the end. With metadata enabled,
  finalizing that restore commit triggers the metadata table's bootstrap
  check, which sees the last-synced instant is no longer "active" on the
  data timeline and decides to re-bootstrap — but re-bootstrap requires no
  pending data-table operations, and the still-open `rollback.requested`
  instants count as pending, so it fails there (potentially after having
  already deleted the existing metadata table in the process). The same
  failure shape can occur when rolling back a bootstrap commit. Open
  question: even with metadata enabled, should the rollback.requested
  instant be left on the timeline after restore commits, or cleaned up?

- **HUDI-2478** — Handle failure mid-way through metadata-table bucket
  initialization. If the writer process crashes partway through
  instantiating the metadata table's (sharded) buckets, retrying that
  initialization should complete cleanly rather than leaving the metadata
  table in a partially-initialized state.

Stated priority in Jira: HUDI-2276, 2303, 2432, 2452, 2458, 2459, 2460,
2472, 2475, 2477, and 2478 are all marked Priority: Blocker. HUDI-2285,
2395, 2422, 2436, 2444, 2468, 2474, and 2476 are marked Priority: Major.
No single item is marked above the others, and Blocker is the majority
label across this list, not an exception.
