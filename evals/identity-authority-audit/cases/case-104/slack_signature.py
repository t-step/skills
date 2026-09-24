"""Verifies that an incoming request really was sent by Slack.

This proves the *message* is genuine (Slack's signing secret produced
this signature) -- it says nothing about whether the Slack user named in
the payload is allowed to do what the payload asks for.
"""

import hashlib
import hmac
import time

SLACK_SIGNING_SECRET = "slack-signing-secret"


def verify_slack_signature(request) -> bool:
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "0")
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False  # replay protection

    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    computed = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(computed, request.headers.get("X-Slack-Signature", ""))
