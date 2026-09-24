# Context

Message from a teammate who clicked through a Teams notification during
standup:

> Quick question -- I got pinged in Teams that order o_789 was updated,
> clicked the link, and it dropped me on `/orders/o_789` while I was
> logged out, then bounced me to a login page before showing anything.
> Is it a problem that `/orders/:id` is reachable without being logged in
> at all? Feels like it shouldn't be possible to hit an app URL before
> authenticating. Can you look at how this is wired up and tell me
> whether this is a vulnerability?

Files in this directory (`notifier.py`, `orders_route.py`,
`login_route.py`) are the complete evidence available about this system
for this review -- there is nothing else to consult.
