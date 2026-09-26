# Context

Northwind (a customer) opens a ticket:

> Your integration isn't syncing into our CRM anymore -- nothing new has
> shown up on our side in 3 days.

Dana Whitfield, Northwind's Integrations Ops admin, replies on the same
thread before you're looped in:

> I checked our Integration Middleware Dashboard -- everything shows
> "Delivered" for records synced yesterday and the few days before that,
> so it looks fine from where I'm sitting. Sorry, I'm out this afternoon
> for a scheduled system migration and won't be reachable until tomorrow.
> I've looped in Chris Alvarez, our CRM admin -- he can help with
> anything on the CRM side while I'm out.

You also have your own team's evidence already gathered:
`crm_sync_job_log.md` (last night's sync job's own log) and
`middleware_dashboard_export.md` (the export Dana attached before going
out). `crm_payload_mapping.md` shows what the sync job currently sends.
Priya Chen, your team's platform SRE, gathered the job log and has
already shared everything she currently has -- she's heads-down on other
work and isn't available for further back-and-forth right now.

Chris is reachable in this conversation for follow-up, but he's new to
this integration's tooling -- he'll need you to tell him exactly what to
check, not just what's wrong in general. Dana is not reachable until
tomorrow at the earliest.

Use the field-debug skill to investigate why Northwind isn't seeing new
records, using what's already here plus whatever you can usefully ask
Chris.
