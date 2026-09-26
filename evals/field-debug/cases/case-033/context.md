# Context

Northwind's overnight order-fulfillment batch submits orders to Meridian
Logistics's fulfillment gateway (`gateway.meridian-fulfillment.example`),
a vendor Northwind does not operate. Northwind does not have, and has
never had, console/admin access to Meridian's internal platform, queues,
or logs -- the only interface between the two systems is the gateway API
`orders-bff` already calls. Meridian's gateway is documented to accept a
fulfillment request synchronously and then process fulfillment
asynchronously, POSTing a completion webhook back to Northwind's
registered endpoint once done.

At 08:45 UTC today, an internal dashboard flagged five orders
(`ORD-88231` through `ORD-88235`) stuck in `pending_fulfillment` well
past Meridian's documented SLA, with no completion webhook received for
any of them. Northwind's ops team opened a support ticket with Meridian
at 09:05 UTC.

You are picking up this investigation at 09:30 UTC. The files below are
the complete evidence available in this session -- there is nothing else
to consult, no one else reachable beyond what these files already show,
and no additional tool access beyond what's described in them. Use the
field-debug skill to investigate and take this as far as the evidence
actually allows.
