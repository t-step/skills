"""Retries a charge attempt against the (flaky) payment provider."""

from app.payments.provider import ChargeProvider, TransientProviderError


def attempt_charge(provider: ChargeProvider, amount_cents: int) -> str:
    """Returns a charge id on success. Raises on failure."""
    try:
        return provider.charge(amount_cents)
    except TransientProviderError:
        # No retry at all today -- a single transient blip fails the charge.
        raise
