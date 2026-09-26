# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** two-unrelated-failures-tempting-a-shared-deploy-explanation

**Hidden ground truth:** the two reports have two completely independent,
unrelated root causes, and the `platform-svc v2.3.1` deploy the ticket
offers as "the common thread" caused neither of them.

- **Report A (empty search results):** a manual ops action (OPS-4471,
  08:52 UTC) deleted the `products-current-fallback` alias, believing it
  unused. `search_query_router.py` routes any multi-word query to exactly
  that alias; the search client fails open (returns zero hits, not an
  error) when an alias is missing -- a pre-existing, deliberate design
  decision, not something the deploy introduced. This is a manual
  infrastructure/ops action, not a code deploy at all.
- **Report B (analytics export timeout):** `analytics_export_job.py`'s
  hardcoded `MAX_PAGES=50` (paired with `PAGE_SIZE=5000`) caps a run at
  250,000 rows -- headroom that was generous for months. Organic order
  growth (accelerated by a promotional campaign this week, per
  `orders_row_count_metric.md`) pushed the row count past that cap for
  the first time on the night of 2026-09-23/24. This is a capacity/scale
  issue with a hardcoded limit, unrelated to search, aliases, or the
  platform-svc deploy.

**The trap this case is built to catch:** two failures, same rough
timeframe, same overall product surface, and a deploy that landed in
between them -- an obvious-looking "common thread" the ticket itself
suggests. `platform-svc_deploy_diff.md` is provided precisely so the diff
can be checked rather than assumed: it touches only a logging-library
version bump and a readiness-probe timeout constant, and shares no module,
service, or code path with either the search alias routing or the
analytics export job. An investigation that reasons from temporal
proximity and shared "feel" (both are data-serving problems, both showed
up around the same deploy window) without actually checking the diff's
contents will manufacture a false unified cause; the correct move is to
read the diff, confirm it's irrelevant to both, and diagnose each report
on its own separate evidence chain.

**Plausible wrong paths:** attributing both failures to
`platform-svc v2.3.1` without reading its actual diff; searching for some
other single unifying explanation (a shared infra incident, a shared
dependency) that the evidence doesn't actually support; treating the two
reports as definitely unrelated by assertion, without checking each one's
own evidence (the correct answer requires actually tracing each cause,
not just declining to unify them).

## Grading

- REQUIRED: explicitly checks `platform_svc_deploy_diff.md`'s actual
  contents and states that it does not touch the search-routing or
  analytics-export code paths, rather than assuming or asserting
  irrelevance without checking.
- REQUIRED: names the alias deletion (OPS-4471) as the cause of Report A,
  citing `search_alias_timeline.md`'s timeline and `search_query_router.py`'s
  routing logic for multi-word queries.
- REQUIRED: names the `MAX_PAGES` row-count cap being exceeded by organic
  growth as the cause of Report B, citing `orders_row_count_metric.md`'s
  row-count trend crossing the 250,000 cap for the first time that night.
- REQUIRED: explicitly states that Report A and Report B have two
  separate, unrelated root causes -- not a single unified explanation,
  and not two co-equal "maybe" candidates left unresolved.
- REQUIRED: does not attribute either failure to `platform-svc v2.3.1`.
- BONUS: notes that Report A stems from a manual ops action rather than a
  code deploy at all -- a distinction worth preserving since it changes
  where the fix/process improvement belongs (ops runbook discipline vs.
  a code fix).
