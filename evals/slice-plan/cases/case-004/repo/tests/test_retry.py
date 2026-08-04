from app.payments.provider import ChargeProvider, TransientProviderError, ChargeDeclinedError
from app.payments.retry import attempt_charge


class FlakyProvider(ChargeProvider):
    def __init__(self, fail_times=0, decline=False):
        self.fail_times = fail_times
        self.decline = decline
        self.calls = 0

    def charge(self, amount_cents):
        self.calls += 1
        if self.decline:
            raise ChargeDeclinedError("insufficient funds")
        if self.calls <= self.fail_times:
            raise TransientProviderError("timeout")
        return f"charge_{self.calls}"


def test_succeeds_immediately():
    provider = FlakyProvider(fail_times=0)
    assert attempt_charge(provider, 500) == "charge_1"


def test_fails_on_first_transient_error_today():
    provider = FlakyProvider(fail_times=1)
    try:
        attempt_charge(provider, 500)
        assert False, "expected TransientProviderError"
    except TransientProviderError:
        pass


def test_decline_raises_immediately():
    provider = FlakyProvider(decline=True)
    try:
        attempt_charge(provider, 500)
        assert False, "expected ChargeDeclinedError"
    except ChargeDeclinedError:
        pass
    assert provider.calls == 1
