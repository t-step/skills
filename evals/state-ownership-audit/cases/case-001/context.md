# Context

Ticket filed by an on-call engineer after a customer briefly saw an old
price for a product they'd just repriced:

> We repriced SKU `abc-123` from $40 to $35 in the admin panel. A customer
> who had the product page open from a few minutes earlier still saw $40
> when they refreshed, for what looked like a couple hundred milliseconds
> before it corrected itself. Should we add a reconciliation job that
> periodically re-syncs the Redis cache against Postgres, so `price_cents`
> and the cache can never drift apart? Want to scope this before next
> sprint.

Files in this directory (`pricing_service.py`, `schema.sql`) are the
complete evidence available about this system for this audit -- there is
nothing else to consult.
