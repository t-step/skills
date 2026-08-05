# Candidates on the table

Two ways to expose the on-call history now that `on_call_log` persists
it:

- **Timeline view** — on a service's detail page, show a chronological
  list of every on-call contact change for that service, oldest or
  newest first. Best for scanning a service's whole on-call history at
  once. Small: reads `on_call_log`, renders a list, no new persistence.
- **Point-in-time lookup** — add a small form to a service's detail page:
  pick a date/time, see who was on-call for that service at that moment.
  Best for a single precise lookup, e.g. reconstructing who was on-call
  during a specific past incident. Small: reads `on_call_log`, one query
  plus a date/time input, no new persistence.

Both read the same already-persisted, already-correct `on_call_log`
table; neither changes what's written to it or how it's written. Both
are similarly sized and similarly easy to remove or replace. Nothing in
review.md or retro.md favors one over the other — the
architectural-consequences note says only that "any future feature" can
read the log, without distinguishing which access pattern is actually
needed. No support ticket, incident report, user request, or usage
metric anywhere in this repository or its supporting documentation
indicates whether people need to scan a service's whole on-call history
or look up who was on-call at one specific past moment.
