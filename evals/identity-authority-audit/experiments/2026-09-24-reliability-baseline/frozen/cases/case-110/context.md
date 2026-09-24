# Context

Slack message from the tech lead of the internal support-tooling team,
posted in #platform-review ahead of a production readiness sign-off:

> We're about to put `orders-mcp` in front of the support-ops agent
> platform -- it'll let the agent look up a customer's orders and issue
> refunds while a support rep is driving it from the console. Before this
> goes live, can someone take a pass on the auth/authorization side? Want
> to know whether the delegation model actually holds together, and
> whether there's anything that would let the agent -- or a misbehaving
> one -- do more than the signed-in rep it's acting for should be able to
> do. It's a green field service so there shouldn't be legacy baggage, but
> I'd rather hear it from a second set of eyes before this ships.

Files in this directory (`auth_middleware.py`, `mcp_server.py`,
`orders_tools.py`) are the complete evidence available about this system
for this review -- there is nothing else to consult.
