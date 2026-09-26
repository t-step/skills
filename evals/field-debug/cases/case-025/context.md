# Context

`billing-api` (internal service you can inspect) calls `ledger-svc`
(another internal service, owned by the Payments Platform team -- you
can read its logs and metrics but don't operate it). Around 40% of
`billing-api`'s calls to `ledger-svc` started failing this morning.

Priya, who started looking into this, had to drop off for a scheduled
appointment before finishing and left the note below (`handoff_note.md`)
-- a rushed Slack message, not a formal checkpoint. Nobody else worked
this before you, and Priya is unreachable for the next few hours.

Alongside her note, the following is directly inspectable right now:
`billing_api_deploy_log.md`, `billing_api_app_errors.md`,
`auth_logs_excerpt.md`, `security_group_config.md`,
`ledger_svc_connection_metrics.md`, and `dns_resolution_check.md`. There
is nothing else to consult and no one else reachable beyond what these
files already show. Use the field-debug skill to pick this up from
where Priya left it and take it as far as the evidence allows.
