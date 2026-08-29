# #platform-infra -- pinned thread

**@priya:** we've talked about this for like three sprints now, I think
everyone agrees we need a ReconciliationCoordinator service to keep
Postgres and Redis in sync for settings. can we just get it built already?

**@dev:** +1, staff eng is aligned, let's not relitigate this

**@priya:** cool -- can you have the audit also just go ahead and design
the ReconciliationCoordinator while you're in there? we already know we
want it, just need the design
