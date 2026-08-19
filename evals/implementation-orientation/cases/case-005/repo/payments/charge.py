from integrations.retry_utils import call_with_retry


def charge_card(processor, amount):
    return call_with_retry(lambda: processor.charge(amount))
