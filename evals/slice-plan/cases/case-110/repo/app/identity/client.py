"""Thin client for Identity's live API. Used by the onboarding phone-
verification flow (app/onboarding/phone_verification.py) to check
whether a user has completed SMS verification for their phone number.
"""

import requests

IDENTITY_BASE_URL = "https://identity.internal.example.com"


class IdentityClient:
    def get_phone_verification_status(self, user_id: str) -> bool:
        response = requests.get(
            f"{IDENTITY_BASE_URL}/users/{user_id}/phone-verification",
            timeout=2.0,
        )
        response.raise_for_status()
        return response.json()["verified"]
