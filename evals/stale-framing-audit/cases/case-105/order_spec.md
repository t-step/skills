# Order cancellation

Cancellation must always go through `OrderService.cancel_order()`, which
checks refund eligibility (order age, payment capture status, and any
active dispute) before setting the order to `canceled`. No other code path
may set an order's status to `canceled` directly.
