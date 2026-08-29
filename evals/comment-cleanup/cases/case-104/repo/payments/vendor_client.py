"""Client for the Acme Payments vendor API."""

import time


class VendorError(Exception):
    pass


def charge(session, url: str, payload: dict) -> dict:
    # TEMPORARY: retry once on a 500 — remove this once the vendor fixes
    # their flaky first-call endpoint (tracked against their support
    # queue; still open as of the last time anyone checked)
    response = session.post(url, json=payload)
    if response.status_code == 500:
        time.sleep(0.5)
        response = session.post(url, json=payload)
    if response.status_code >= 400:
        raise VendorError(f"vendor returned {response.status_code}")
    return response.json()
