"""Creates a ServiceNow incident from an alert-manager webhook payload."""

import json
import os
from pathlib import Path

SNOW_INSTANCE = os.environ["SNOW_INSTANCE"]
TOKEN_PATH = Path.home() / ".snow_token"  # written by `make login`, see README.md


def _load_token():
    # Refresh token belongs to whichever human ran `make login` last --
    # ServiceNow's audit log records every ticket this bridge creates as
    # created by that person's user account, indistinguishable from a
    # ticket they filed by hand.
    return json.loads(TOKEN_PATH.read_text())["refresh_token"]


def create_incident(alert):
    token = _load_token()
    payload = {
        "short_description": alert["title"],
        "urgency": _map_priority(alert["severity"]),
        "assignment_group": os.environ.get("DEFAULT_ASSIGNMENT_GROUP", "network-ops"),
    }
    return _post_incident(SNOW_INSTANCE, token, payload)


def _map_priority(severity):
    return {"critical": 1, "high": 2, "medium": 3, "low": 4}.get(severity, 3)


def _post_incident(instance, token, payload):
    raise NotImplementedError("ServiceNow REST client omitted for this excerpt")
