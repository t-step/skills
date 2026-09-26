# Context

An SRE on the storefront team messages you:

> For the last several hours, our DB connection pool utilization has
> been spiking to 100% for about 10-15 seconds, on a suspiciously regular
> interval, then recovering on its own. During each spike we get a burst
> of slow homepage loads and a handful of request timeouts, then
> everything's fine again until the next one. There's been no code
> deploy today. The only change today was a config change this morning
> to `homepage-svc`'s cache TTLs (ticket TICKET-5521), and this started
> not long after that went out. First instinct is we might just need to
> scale up the database, or there's a slow query that snuck in
> somewhere -- can you dig in and tell us what's actually going on?

You have `homepage-svc`'s working directory as currently deployed, DB
connection-pool metrics, Redis cache hit/miss counters, and the slow
query log, all covering the same several-hour window. There is no ticket
queue, chat transcript, or person to ask beyond this message -- work from
what you can find.
