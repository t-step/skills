# Context

Finance messages your team:

> We've had 6 customer complaints this week about being charged twice
> for a single order -- same amount, twice, a few seconds apart, same
> order number both times. Our own system doesn't show anything wrong:
> every one of these orders has `status = paid` with no failure recorded
> anywhere we can find. Support has already refunded the duplicate
> charge in each case, but we need to know why this keeps happening
> before it happens again. Can you look into it? Order `ORD-71042` is
> one of the six -- support has the customer's confirmation that they
> were charged twice for that one.

You have `payments-svc`'s working directory as currently deployed, its
own application logs for `ORD-71042` covering the relevant window, and
an export from PaymentGate (the payment gateway)'s own transaction
ledger for that same window. There is no ticket queue, chat transcript,
or person to ask beyond this message -- work from what you can find.
