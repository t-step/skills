# Context

Excerpt from the orders service (`models.py`, `order_handlers.py`) and the
nightly search-indexing job (`indexer_excerpt.py`). `db.py`, `audit_log`,
`search_client`, and the ops dashboard frontend are not included -- treat
anything not shown here as not available for this review.

A recent internal ticket, forwarded for context:

> **Ticket #4021 -- "workflow_state is confusing, can we clean it up?"**
>
> Filed by an engineer new to the orders service:
>
> "I'm trying to understand the order lifecycle before I add a new ops
> dashboard filter. I see `Order.status` (pending/paid/shipped/delivered/
> cancelled) but I also see `Order.workflow_state` returning things like
> 'Needs Attention' and 'On Hold', and there's *also* a
> `workflow_state_cache` column in the `orders` table that the search
> index reads. Are these three separate state machines that all need to
> stay in sync? Should we add a scheduled job to reconcile
> `workflow_state_cache` against `workflow_state` more often than nightly,
> so the dashboard filter doesn't show stale 'On Hold' orders? Wanted a
> second opinion before I propose anything to the team."
