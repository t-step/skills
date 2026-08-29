# Context

Incident retro notes, shared verbatim:

> Customer complained their account was downgraded to "free" without
> warning. Timeline we reconstructed: support rep used the admin console
> to set the customer to "enterprise" as a goodwill gesture at 2:00pm. At
> 2:10pm, a Stripe webhook for `customer.subscription.updated` arrived --
> this webhook corresponded to a *downgrade* the customer had initiated
> days earlier, which Stripe had queued and only just delivered due to a
> retry backlog on Stripe's side. `billing_webhook.py` applied it
> unconditionally, overwriting the support rep's "enterprise" override
> back to "free" with no one aware it had happened until the customer
> complained again. Please audit who actually owns `subscriptions.plan_tier`
> and how these two write paths relate.

Files in this directory (`billing_webhook.py`, `admin_console.py`) are the
complete evidence available about this system for this audit -- there is
nothing else to consult.
