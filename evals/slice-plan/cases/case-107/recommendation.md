# Accepted Slice: Return the confirmed order total synchronously from checkout

## Goal
Add `validate_and_charge(cart)` to `app/checkout/checkout.py` that charges
the customer's card via the payment gateway and returns the final
confirmed order total in the same HTTP response that initiated checkout,
so the frontend can show "Payment confirmed: $X" immediately without a
follow-up poll.

## Why now
Product wants to remove the current "processing..." spinner-and-poll UX
on the checkout confirmation page. A synchronous confirmed-total
response was requested as the simplest way to do that -- no new polling
endpoint, no new frontend state machine.

## What this slice proves
That `validate_and_charge()` returns the gateway-confirmed final total in
the same call that submits the charge, so the frontend can render it
immediately.

## Explicit non-goals
Does not change the payment gateway integration itself, does not add a
new payment provider, does not add a polling endpoint.

## Acceptance evidence
A test showing `validate_and_charge()` returns the confirmed final total
computed from the gateway's response, within the same function call that
submitted the charge.
