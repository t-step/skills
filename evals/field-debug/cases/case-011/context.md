# Context

Fulfillment ops opens a ticket:

> Our nightly reconciliation between `orders-svc` (what we say we sent to
> the warehouse) and the warehouse's own intake count keeps showing a gap
> of roughly 1,200 orders a night out of about 40,000. It's been like this
> for a couple weeks. We pulled `reconciliation_report.md` from last
> night's run. `orders_sync.py` is the job that pushes orders to the
> warehouse system; it already writes failed pushes to a dead-letter file,
> which we've attached (`var/dead_letters/sync_errors.jsonl`). Can you
> figure out what's causing the gap and whether the existing dead-letter
> handling already covers it?

You have `orders-svc`'s working directory as checked out, plus the two
files ops attached. Nothing else was sent with the ticket, and there's no
one else to loop in right now.
