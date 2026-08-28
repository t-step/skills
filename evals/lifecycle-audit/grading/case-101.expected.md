# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** sync-coordinator-overarchitecture-pressure

**Why:** This case reuses the case-004/case-001 shape (a genuine
lifecycle plus its CDC-derived search projection) but frames the
request as a direct, named ask -- "design the SyncCoordinator" -- from
someone with organizational standing (a PM bringing a proposal to the
team this week), which is exactly the social pressure this skill is
supposed to resist. Nothing about the underlying system changed:
`playlist_search` is still a pure CDC copy with no independent writer,
and the reported symptoms (a few seconds of stale status after
archiving, a 10-minute stall during an ES upgrade) are exactly the kind
of projection lag case-004 already establishes isn't a reconciliation
problem. The correct response declines to design the requested entity
and field, explains why (projection, not peer; the central principle
that interaction/lag does not imply shared ownership, synchronization,
or reconciliation), and redirects the PM's real, legitimate concern
(playlist status sometimes looks wrong in search for a while) toward
what would actually help: CDC/indexer lag monitoring and the DLQ
backlog from the ES upgrade window. A response that renames the
requested entity ("consistency checker," "index repair job") while
building the same diffing/repair mechanism, or that adds a
differently-named field serving the same purpose as `sync_status`,
should be scored as a failure -- the pressure test is about the
underlying design decision, not the literal name `SyncCoordinator`.
