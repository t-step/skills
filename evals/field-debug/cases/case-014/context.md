# Context

The drops team messages you:

> We ran the Friday sneaker drop for SKU `SNK-4471` this morning -- 50
> pairs, first-come-first-served, one pair per order. Finance just told us
> we have 52 confirmed orders against that SKU. We've already had to
> refund and apologize to 2 customers who won't get a pair. Nothing about
> checkout looks broken -- no errors in our dashboards, no failed
> requests, no alerts fired. The `checkout-drops` service's own inventory
> table for that SKU currently reads `available = 0`, which is what we'd
> expect if exactly 50 sold and it's just sold out -- so ops isn't sure
> where the extra 2 orders even came from. Can you figure out what
> actually happened?

You have the `checkout-drops` service's working directory as checked out
at the version running during the drop, plus request/access logs and a
database audit-history export covering the drop window. There is no
ticket queue, chat transcript, or person to ask beyond this message --
work from what you can find.
