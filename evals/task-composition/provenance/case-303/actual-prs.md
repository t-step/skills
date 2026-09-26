# Actual PRs/commits — case-303 (Hudi Metadata Table)

Concrete PR data for the fixture's 19 tasks, where a merged PR could be
located by searching GitHub for the Jira ID in the PR title. Not every
task's implementing PR was found this way — several stayed open/unresolved
for years (see below) and never shipped as a single identifiable PR.

| Task | PR | Title | Merged | Scope (from file diff) |
|---|---|---|---|---|
| HUDI-2276 | #3411 | Enable metadata table by default for readers and writers | **not merged** (opened 2021-08-05, superseded by later work) | Config default flip + several test/sync-module touch-ups (HoodieMetadataConfig.java, HoodieROTablePathFilter.java, hive/DLA sync configs, etc.) |
| HUDI-2422 | #3651 | Adding rollback plan and rollback requested instant | 2021-09-16 | New `HoodieRollbackPlan.avsc`; `BaseRollbackPlanActionExecutor.java`, `BaseRollbackHelper.java`, `ListingBasedRollbackStrategy.java` added; `HoodieTable.java`, `BaseRollbackActionExecutor.java`, engine-specific write clients touched across Spark/Flink/Java modules |
| HUDI-2444 | #3678 | Fixing cleaning and rollback if retried after failed attempt | 2021-09-20 | (file list not separately captured; ticket text is self-contained) |
| HUDI-2395 | #3695 | Metadata tests rewrite | 2021-09-23 | Test-only change, `HoodieTestTable`-based rewrite |
| HUDI-2474 | #3698 | Refreshing timeline for every operation in Hudi | 2021-09-28 | (file list not separately captured) |
| HUDI-2285 + HUDI-2476 | #3590 | Metadata table synchronous design. Rebased and Squashed from pull/3426 | 2021-10-06 | 30 files: `HoodieBackedTableMetadataWriter.java` (+ Spark/Flink subclasses), `HoodieTimelineArchiveLog.java`, `CleanActionExecutor.java`, `BaseCommitActionExecutor.java`, `BaseRestoreActionExecutor.java`, `BaseRollbackActionExecutor.java`, CLI commands, upgrade/downgrade handlers, `TransactionUtils.java` — **landed as one PR covering both tickets** |
| HUDI-2468 | #3843 | Metadata table support for rolling back the first commit | 2021-10-23 | `HoodieBackedTableMetadataWriter.java` (+ Spark/Flink), `HoodieTable.java`, `BaseActionExecutor.java` — same core writer file as #3590 |
| HUDI-2477 | #4518 | Removing rollbacks instants from timeline for restore operation | 2022-01-10 | `BaseRestoreActionExecutor.java` (same file #3590 also touched) |
| HUDI-2432 | #4605 | Adding restore.requested instant and restore plan for restore action | 2022-02-10 | New `HoodieRestorePlan.avsc`, `RestorePlanActionExecutor.java`, `RestoreUtils.java`; `BaseRestoreActionExecutor.java` (again — fourth ticket touching this file), `HoodieTable.java`, timeline utility classes |
| HUDI-2436 | not located | — | — | No merged PR found by title search; likely folded into one of the rollback PRs above or resolved as part of general rollback hardening |
| HUDI-2452 | not located | — | — | External bug report; fix (if any) not identified by title search |
| HUDI-2458 | none | — | **never merged / still open** | Ticket remained Open as of the most recent check (still Open years later); the "spurious deletes" simplification it proposes does not appear to have shipped as its own change |
| HUDI-2459 | none | — | **never merged / still open** | Async compaction for metadata table remained an open, unimplemented task for years past this window |
| HUDI-2460 | none | — | **never merged / still open** | Same as above, for async cleaning |
| HUDI-2472 | none identified | — | resolved 2022-01-19 (per Jira) | Tracking ticket, not a single PR; resolved incrementally as the individual test failures it named were fixed |
| HUDI-2475 | none identified | — | resolved 2024-03-29 (per Jira) | Stayed open/tracking for roughly 2.5 years past this window — the rolling-upgrade design question was not settled quickly |
| HUDI-2303 | referenced via #3411 | (fix folded into the 2276 enablement work) | — | — |
| HUDI-2478 | not located | — | — | No merged PR found by title search |

## Cross-cutting file overlap (confirmed, not part of the fixture)

`HoodieTable.java`, `BaseRollbackActionExecutor.java`,
`BaseRestoreActionExecutor.java`, and `HoodieBackedTableMetadataWriter.java`
(plus its Spark/Flink subclasses) each appear in **more than one** of the
PRs above — `BaseRestoreActionExecutor.java` alone is touched by three
separate, separately-merged PRs (#3590, #4518, #4605) spanning
2021-10-06 through 2022-02-10. This confirms the "shared-area signal" noted
in the fixture's `dependencies.md` was real, not a guess — but it is
deliberately not stated as a file-level fact in the agent-visible fixture,
since most of these PRs merged after the chosen cutoff and citing their
diffs would be hindsight the tickets themselves didn't yet contain.
