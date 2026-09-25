"""Account recovery for a user who has lost their passkey device.

Reachable from a "Lost your device?" link on the login page -- requires
knowing the account's email/phone, then a 6-digit code sent by SMS.
"""

import time
from flask import session
import sms_provider


def start_recovery(user_id: str) -> None:
    code = generate_otp()
    store_pending_otp(user_id, code)
    sms_provider.send_sms(get_phone_for_user(user_id), f"Your recovery code is {code}")


def complete_recovery(user_id: str, submitted_code: str) -> None:
    verify_otp(user_id, submitted_code)  # raises on mismatch/expiry

    # Establishes a session exactly as if this were a WebAuthn login --
    # the same claims are set, regardless of how this session was
    # actually established.
    session["user_id"] = user_id
    session["amr"] = ["webauthn"]
    session["auth_time"] = int(time.time())

    prompt_passkey_re_enrollment(user_id)


def generate_otp() -> str:
    ...  # not relevant to this audit


def store_pending_otp(user_id, code):
    ...  # not relevant to this audit


def verify_otp(user_id, submitted_code):
    ...  # not relevant to this audit


def get_phone_for_user(user_id):
    ...  # not relevant to this audit


def prompt_passkey_re_enrollment(user_id):
    ...  # not relevant to this audit
