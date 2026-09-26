"""billing/charge_worker.py -- renewal processing (excerpt)"""


def process_renewal(event):
    sub = event["subscription_id"]
    amount = event["amount_cents"]

    # (1) charge the customer -- no idempotency key is passed to Ridgeline
    result = ridgeline.charge(customer=event["customer_id"], amount=amount)
    log.info("ridgeline.charge() call returned, response received")

    # (2) apply any active discount to the ledger entry -- BUG: discount
    # can be None if the subscription's discount expired between event
    # creation and processing, and this line doesn't guard for that
    adjusted = apply_discount_adjustment(sub, result)  # <- crashes here

    # (3) only after both of the above succeed does this record the charge
    # outcome anywhere durable
    ledger.record_charge(sub, result.charge_id, result.status)
    queue.ack(event)


def apply_discount_adjustment(sub, charge_result):
    discount = get_active_discount(sub)  # returns None if expired
    return charge_result.amount * discount.rate  # AttributeError if None
