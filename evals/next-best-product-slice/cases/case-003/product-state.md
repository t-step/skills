# Product state — Northbeam reporting

No review, retro, or backlog exists in this repository. This is a snapshot
of directly observable current product state.

Northbeam is a marketing-analytics reporting tool. `docs/onboarding.md`
describes report subscriptions as an intended part of the product:
material aimed at team leads explains that subscribing to a report should
mean a fresh copy gets delivered automatically on a chosen schedule, so a
team lead doesn't have to remember to go check it.

The backend fully implements scheduled report generation and delivery:
`ReportScheduler.subscribe(report_id, user_id, cadence)` creates a
subscription, and a nightly job renders and emails the report to every
subscribed user. This machinery is real and running in production today —
it powers the system-generated weekly "platform health" report that's
automatically emailed to Northbeam's own internal admin team every Monday.

There is no UI, CLI command, or documented API endpoint that lets an actual
team lead (a customer-facing role, distinct from Northbeam's internal admin
team) create, view, or cancel a subscription to any of their own reports.
`ReportScheduler.subscribe()` is only ever called from one place in the
codebase: a one-off internal setup script that registered the admin team's
weekly platform-health subscription when the feature was first built. No
customer-facing report has ever been subscribed to by anyone.

Every report in the product today can only be viewed by manually opening it
in the dashboard each time.
