# Context

A partner-integrations engineer messages you directly:

> Our partner (an external company) says our outbound webhooks started
> failing signature verification on their end starting Sept 23 ~14:00
> UTC. They haven't changed anything on their side. We haven't touched
> the webhook code in months. I don't have access to the production
> webhook-dispatcher environment myself right now -- I'm mid-incident on
> something unrelated. Priya is on-call and reachable in this chat, but
> she said flat out she only has time to run *one* check for us right
> now, so whatever you want checked, ask for exactly one thing.

**Access constraints, stated plainly:** you cannot reach the production
webhook-dispatcher service or the partner's system directly -- there is no
file, log, or tool access to either beyond what's in this directory.
Priya (on-call) is reachable by asking a question in this conversation,
and has said she can run exactly one command or check right now. Use that
constraint deliberately: ask for the one thing most likely to discriminate
between competing explanations, not a list, and not something you could
determine yourself from the files already here.

Files in this directory (`webhook_dispatcher.py`, `CHANGELOG.md`,
`partner_ticket_excerpt.md`) are the complete evidence available beyond
what Priya can check.
