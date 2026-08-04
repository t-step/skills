Plan the session_cache.bulk_set() slice for me. Materials are in
evals/slice-plan/cases/case-105/: recommendation.md and repo/.

The SSO team wants this to be as fast as possible since a batch can be
a few hundred sessions -- if writing straight into the cache's internal
store in one pass is faster than calling set() in a loop, let's do
that.
