"""Primary login flow -- WebAuthn/passkey only, no password fallback."""

import time
from flask import session


def complete_webauthn_login(user_id: str, assertion: dict) -> None:
    verify_webauthn_assertion(user_id, assertion)  # raises on failure

    session["user_id"] = user_id
    session["amr"] = ["webauthn"]
    session["auth_time"] = int(time.time())


def verify_webauthn_assertion(user_id: str, assertion: dict) -> None:
    ...  # standard WebAuthn signature/challenge verification, not relevant here
