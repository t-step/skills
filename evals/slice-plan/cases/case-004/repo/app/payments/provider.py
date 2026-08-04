class TransientProviderError(Exception):
    """Raised for retryable provider errors (timeouts, 5xx, rate limits)."""


class ChargeDeclinedError(Exception):
    """Raised for non-retryable errors (card declined, insufficient funds)."""


class ChargeProvider:
    def charge(self, amount_cents: int) -> str:
        raise NotImplementedError
