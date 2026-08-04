# Accepted Slice: Add Apple Pay as a supported payment method

## Goal
process_payment() should support method="apple_pay", routing to a new
apple_pay_processor.charge() the same way credit_card and paypal
already route to their processors.

## Why now
Apple Pay checkout is contractually required to launch with the iOS
app update shipping in three weeks; the processor integration (an
apple_pay_processor module) is being built by another team and will
land separately -- this slice only needs to wire routing to it.

## What this slice proves
That process_payment("apple_pay", ...) routes to
apple_pay_processor.charge() the same way the two existing methods do,
and that credit_card/paypal/unsupported behavior is unaffected.

## Explicit non-goals
Does not implement apple_pay_processor.charge() itself (owned by
another team), does not change how credit_card or paypal are routed.

## Acceptance evidence
A test showing process_payment("apple_pay", ...) calls
apple_pay_processor.charge() and returns its result, and the three
existing tests in tests/test_router.py still pass unchanged.
