import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from payments.vendor_client import charge


class FakeResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body


class FakeSessionOne500ThenOk:
    def __init__(self):
        self.calls = 0

    def post(self, url, json):
        self.calls += 1
        if self.calls == 1:
            return FakeResponse(500, None)
        return FakeResponse(200, {"ok": True})


def test_charge_retries_once_on_500():
    session = FakeSessionOne500ThenOk()
    result = charge(session, "https://vendor.example/charge", {"amount": 100})
    assert result == {"ok": True}
    assert session.calls == 2
