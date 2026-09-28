# Context

Slack message from an engineer who just joined the Orders team and is
reading through the checkout path for the first time:

> Trying to understand how identity actually flows from the browser to
> the Orders API before I touch anything. I can see the browser talks to
> our BFF, and the BFF apparently does some kind of token exchange before
> it calls the downstream Orders API rather than just forwarding whatever
> the browser sent. Can you walk me through what's actually happening at
> each hop, and whether that exchange step is doing anything real, or if
> it's leftover complexity from an old design and we'd lose nothing by
> just forwarding the session cookie straight through to Orders?

Files in this directory (`bff_orders_route.py`, `token_exchange.py`,
`orders_api.py`) are the complete evidence available about this system
for this review -- there is nothing else to consult.
