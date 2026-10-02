# Dependencies: Hudi Metadata Table — synchronous redesign and default-on push

Only what's stated or clearly inferable from the tickets themselves is
listed here. This backlog has real, unresolved ambiguity in it — some of
it is left open below rather than resolved, because the record itself
doesn't resolve it.

## Stated or clearly inferable

- **HUDI-2432 depends on HUDI-2422.** 2432's restore-plan design is
  explicitly built on top of 2422's rollback-plan/`rollback.requested`
  mechanism ("we have already have a patch fixing rollback to add
  rollback Plan in rollback.requested meta file" is the starting point
  2432 reasons from).
- **HUDI-2477 depends on HUDI-2422.** 2477's failure is triggered
  specifically by the `rollback.requested` instant that 2422 introduces
  ("after we have added the rollback.requested instant, restore is
  breaking with metadata enabled").
- **HUDI-2472 depends on HUDI-2468 for at least part of its scope.**
  2472 (the test-failure tracking ticket) names 2468 by ID as the known
  cause of several of the rollback/compaction test failures it's tracking.
  2472 also depends on HUDI-2276's own progress in a different sense: it
  only exists because 2276's default-enablement work exposed the
  failures it tracks.
- **HUDI-2303 was discovered as a direct consequence of HUDI-2276's
  work**, not the other way around — it was filed while enabling metadata
  in tests for 2276. Resolving 2303 is functionally required before 2276
  can be defaulted, even though nothing formally links them as
  "blocks."

## Open questions the record does not resolve — flag, don't guess

- **HUDI-2477 and HUDI-2432 both concern restore's handling of pending
  rollbacks during finalization, filed a week apart (2432 on 2021-09-14,
  2477 on 2021-09-21).** Whether 2477 is a bug inside the restore-plan
  design 2432 is building, a preexisting restore defect that 2422 alone
  exposed, or something 2432's design needs to account for going forward
  is not stated — 2432 being filed first does not by itself establish
  that 2477 is downstream of it, since nothing says how far 2432's design
  had progressed by the time 2477 was filed. Treat the relationship
  between these two as unresolved rather than assuming a direction.
- **HUDI-2458 and HUDI-2459 address the same underlying constraint**
  (metadata-table compaction fenced on data-table in-flight requests) from
  two different angles — 2458 names the fencing dependency as a liveness
  problem to relax, as filed with no proposed mechanism yet; 2459
  proposes async compaction as a way around the same starvation risk.
  Nothing in either ticket says whether these are complementary (both
  needed), redundant, or competing approaches to the same problem, and
  2458 is too unscoped as filed to tell whether its eventual fix would
  even overlap with 2459's. Do not assume they're independent or that one
  supersedes the other without that being stated.
- **HUDI-2476 may not be independent of HUDI-2285.** 2476's retry/clobber
  scenario is a specific case of exactly the delta-commit-before-data-commit
  timing that 2285's synchronous design describes and is built around.
  Whether 2476 is a standalone bug fixable on its own, or a sub-problem
  inside implementing 2285's write path that isn't separately verifiable
  until 2285 exists, isn't stated.
- **Whether HUDI-2475 gates shipping HUDI-2276 is not stated.** As filed,
  2475 has only a title ("Upgrade downgrade infra for enabling metadata")
  and no body text yet — there is no design content to reason from, let
  alone a resolution. Nothing says whether the code change in 2276 is
  blocked on 2475 being solved, or whether 2475 is a parallel
  operational/rollout concern that can trail the code; a ticket this thin
  is itself a topology unknown, not just an unresolved design question.
- **HUDI-2436 is an open investigation, not a scoped fix.** Its own text
  says the reporter doesn't yet fully understand the failure scenario and
  needs to follow up with the RFC author. Any fix inferred from it is
  provisional; there's no fixed scope to depend on yet.
- **HUDI-2452 has no stated connection to any other item in this list.**
  It's an externally reported bug that surfaced around the same time.
  Whether it's actually part of this synchronous-redesign/rollout effort
  or an unrelated legacy defect that happened to appear in the same window
  is not established either way.

## Shared-area signal, not a stated dependency

HUDI-2422, 2432, 2477, 2468, and 2476 all describe touching the same
rollback/restore/bootstrap-check logic inside the metadata table's writer
— the "compare last-synced instant against the active data timeline,
decide whether to re-bootstrap" check recurs by name in 2468's and 2477's
failure descriptions, 2432 names the same rebootstrap mechanism as an
alternative it considered, and 2476's retry/clobber scenario and 2285's
synchronous design describe the same delta-commit timing mechanics. No
ticket names a shared file or class explicitly, and none states a formal
"blocks" link between this group beyond what's listed above as stated.
This is a signal to look closely at before assuming any of these can
proceed in full isolation from the others — not, on its own, a verdict
that they can't.

(HUDI-2478 was considered for this group but excluded: its own text is
about crash-recovery during metadata-table bucket initialization —
"process crashes mid-way while instantiating buckets" — a different
mechanism, not the rollback/restore bootstrap-check logic above. Nothing
in the ticket's filed text supports grouping it with this cluster.)
