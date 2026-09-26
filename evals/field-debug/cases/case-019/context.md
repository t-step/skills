# Context

The fulfillment platform on-call engineer messages you:

> Since yesterday's release of `order-events-producer` v2.6, the
> `shipping-label-consumer` service has been rejecting every single
> `order.created` event it receives -- no shipping labels have been
> generated since the release went out. The producer team says they
> made "a small field rename as part of the fulfillment-methods
> refactor" and that it shouldn't require any consumer-side changes.
> Can you confirm what's actually wrong and what needs to change?

You have `shipping-label-consumer`'s working directory as currently
deployed, its validation-rejection log since the release, a sample
payload actually emitted by the new producer version, and the producer
team's own release notes for v2.6. There is no ticket queue, chat
transcript, or person to ask beyond this message -- work from what you
can find.
