# Context

The fulfillment on-call engineer messages you:

> Since this morning's `orders-svc` deploy (v4.2.0, routine dependency
> bump), every single fulfillment request from `orders-svc` to
> `inventory-svc` has been failing with a connection error -- 100% of
> attempts, not intermittent. Nothing else changed today as far as we
> know. Can you figure out what's wrong and fix it?

You have `orders-svc`'s deployed configuration and today's deploy diff,
`inventory-svc`'s own startup log, and `orders-svc`'s error log from
after the deploy. There is no ticket queue, chat transcript, or person to
ask beyond this message -- work from what you can find.
