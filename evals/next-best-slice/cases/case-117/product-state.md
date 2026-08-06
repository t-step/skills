# Wayfinder — current product state

Wayfinder is an internal release-tracking tool with these pieces:

- `releases/` — the release lifecycle API (promote, deploy, rollback)
  and the `release_events` audit table all three write to.
- `dashboard/` — the `/deployments` dashboard, which reads `release_events`
  and renders one row per event. It has explicit render cases for
  `promote` and `deploy`; anything else currently falls through to a
  blank, unlabeled row.
- `legacy/notifier_v1.py` — the original Slack-notification module,
  superseded by `notifications/dispatcher.py` two releases ago. Nothing
  in the current codebase imports it.
- `experimental/graphql_gateway/` — a partially-built GraphQL gateway
  prototype (schema plus a few resolvers). It is not registered with the
  app's router and is not reachable from any entry point.
- `scripts/poc_bulk_import.py` — a one-off script for bulk-importing
  historical release data, written for a one-time migration. No tests,
  no docs beyond a comment reading "POC, unfinished, don't rely on
  this."
- `internal_tools/report_builder_old/` — an older internal reporting
  tool, superseded by a newer service last year. Still present in the
  repository; nothing currently imports or runs it.

No ticket, incident, user request, or documented plan exists anywhere in
this repository for any of the four items above (`notifier_v1.py`,
`graphql_gateway/`, `poc_bulk_import.py`, `report_builder_old/`) — they
are simply present in the codebase.
