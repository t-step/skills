# Context

Support escalates the following to your team:

> Since yesterday morning, we've been getting a steady trickle of
> customer complaints about payments being declined at checkout. It
> looks completely random -- the same customer retries with the same
> card a minute later and it goes through fine. PaymentCo (our payment
> gateway) says nothing changed on their end and their dashboard shows no
> incident. The only thing that happened around when this started is
> that platform rotated our PaymentCo API key yesterday morning as part
> of a routine quarterly security rotation (ticket SEC-2291) -- that's
> supposed to be a routine, invisible change handled by the normal deploy
> process. Our own gateway-call metrics show roughly 62% of charge
> attempts in the last day came back declined/unauthorized, versus our
> normal ~1% decline rate, but it doesn't look tied to any particular
> customer, card type, or order size we can find. Can you figure out
> what's actually happening?

You have `checkout-svc`'s working directory as currently deployed,
request-level logs against the payment gateway covering the last day,
and the deployment/rollout history for the API key rotation. There is no
ticket queue, chat transcript, or person to ask beyond this message --
work from what you can find.
