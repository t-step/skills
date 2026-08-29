# Context

Support ticket, escalated by a support lead who wants to know if this is a
bug worth a hotfix:

> Customer placed an order, immediately refreshed their order history page,
> and for about a second and a half it showed nothing / an incomplete
> total before the correct total appeared. They didn't file a complaint but
> our support rep flagged it as "looks broken." Is `order_summary_view`
> out of sync with the real order data? Do we need to fix this before it
> happens to more customers?

Files in this directory (`order_events.py`, `summary_projector.py`) are the
complete evidence available about this system for this audit, along with
the documented SLA and DLQ behavior described in `summary_projector.py`'s
own docstring -- there is nothing else to consult.
