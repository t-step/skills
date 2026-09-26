"""Confirms, from the two exports' own timestamps, that PaymentGate's
first capture (gw_88201) actually completed before payments-svc's
client-side timeout fired -- i.e. the first attempt committed despite
the caller seeing a timeout, it did not merely "fail then get retried."
"""

from datetime import datetime

FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

# From logs/payments_svc_logs.md
client_timeout_fired_at = datetime.strptime("2026-09-23T14:22:12.014Z", FMT)

# From gateway/gateway_transaction_export.md, gw_88201's completed_at
gateway_first_capture_completed_at = datetime.strptime("2026-09-23T14:22:11.981Z", FMT)

print(f"client-side timeout fired at:        {client_timeout_fired_at.time()}")
print(f"gateway's first capture completed at: {gateway_first_capture_completed_at.time()}")

assert gateway_first_capture_completed_at < client_timeout_fired_at, (
    "expected the gateway to have already completed the first capture "
    "before the client gave up waiting for it"
)

print(
    "\nCONFIRMED: PaymentGate finished processing the first capture "
    f"{(client_timeout_fired_at - gateway_first_capture_completed_at).total_seconds() * 1000:.0f}ms "
    "before payments-svc's client-side timeout fired. The first attempt "
    "committed; payments-svc just never learned that in time."
)
