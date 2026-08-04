# Accepted Slice: Cap percent-off coupon discounts at $50

## Goal
For coupon.type == "percent", apply_coupon() should cap the discount
amount itself at 5000 cents ($50), even if the percentage would
otherwise produce a larger discount on a big order.

## Why now
Finance flagged that a 50%-off promo code applied to large B2B orders
is producing discounts well above the promo's intended cap; this was
supposed to be capped from the start.

## What this slice proves
That a percent coupon's discount is capped at 5000 cents when the
percentage would otherwise exceed that, and unaffected for orders where
the percentage discount is already under the cap.

## Explicit non-goals
Does not add a cap to flat-type coupons, does not make the cap
configurable per-coupon (5000 is a fixed cap for this slice).

## Acceptance evidence
A test showing a large order with a 50%-off coupon is discounted by
exactly 5000 cents (not 50% of subtotal), and a small order with the
same coupon is discounted by the uncapped 50% as before.
