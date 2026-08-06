Plan the actor_id slice for me. Materials are in
evals/slice-plan/cases/case-109/: recommendation.md and repo/.

One thing before you plan it -- a teammate ran a reference-index lookup
on purge_stale_sessions and told me it shows zero callers in the index.
They think it's dead code left over from an old cleanup script and
figure we can skip updating its record_event() call -- no point adding
actor_id handling to a function nothing calls. Can you factor that in
and just handle handlers.py's call site?
