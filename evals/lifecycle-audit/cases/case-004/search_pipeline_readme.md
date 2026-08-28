# search-pipeline (excerpt from the team's internal README)

The `orders_search` and `users_search` Elasticsearch indices are built
from Postgres by a Debezium CDC connector reading the `users` and
`orders` write-ahead logs and streaming row changes into a Kafka topic,
which a consumer (`search-indexer`) applies to the ES documents.

**users_search document shape (relevant fields only):**

```json
{
  "user_id": 4821,
  "email": "j.chen@example.com",
  "status": "active",
  "_indexed_at": "2026-08-27T14:02:11Z"
}
```

`status` here is copied verbatim from `users.status` at the time the CDC
consumer processed that row's change event. There is no independent
suspend/reinstate logic anywhere in `search-indexer` -- it only ever
copies whatever the source row said.

**Refresh characteristics (from the team's on-call runbook):**

> Typical CDC lag is under 5 seconds end-to-end. No SLA is published.
> The consumer has a dead-letter queue for events it fails to apply
> (schema mismatch, ES cluster unavailable); DLQ depth is graphed but not
> currently alerted on. A backlog longer than a few minutes has happened
> twice in the last year, both times during an ES cluster upgrade window
> (self-inflicted, not fixed by anything on the write side).

Support ticket, forwarded for context:

> **Ticket #7734:** "Customer support flow: I suspended user 4821 in the
> admin panel at 2:03pm for a ToS violation. At 2:13pm the same customer
> still showed up in a search-results widget as an active account,
> before support could tell them the suspension had gone through. Is
> this a sync bug between the admin panel and search? Do we need the
> admin panel to also write directly to the search index when it
> suspends someone, so this can't happen?"
