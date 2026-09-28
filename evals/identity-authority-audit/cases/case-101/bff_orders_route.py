"""BFF (Backend-for-Frontend) route for the order-detail page.

Runs server-side. The browser only ever holds an HttpOnly, Secure session
cookie (`sid`) issued at login; that cookie is opaque to JavaScript and is
never exchanged for anything, forwarded anywhere, or returned to the
client in a response body or header.
"""

import time

import requests
from flask import Flask, abort, jsonify, request

from session_store import load_session  # internal Redis-backed session store
from token_exchange import exchange_for_orders_api

app = Flask(__name__)

ORDERS_API_BASE = "https://orders.internal.example.com"


@app.route("/bff/orders/<order_id>", methods=["GET"])
def get_order(order_id: str):
    sid = request.cookies.get("sid")
    if not sid:
        abort(401, "no session")

    session = load_session(sid)  # {"user_id": ..., "account_id": ..., "expires_at": ...}
    if session is None or session["expires_at"] < time.time():
        abort(401, "session missing or expired")

    # Exchange the BFF's own session context for a short-lived, downstream-
    # scoped credential. The browser never sees this token; it is created
    # here, used here, and discarded here.
    downstream_token = exchange_for_orders_api(
        user_id=session["user_id"],
        account_id=session["account_id"],
    )

    resp = requests.get(
        f"{ORDERS_API_BASE}/orders/{order_id}",
        headers={"Authorization": f"Bearer {downstream_token}"},
        timeout=5,
    )

    if resp.status_code == 404:
        abort(404, "order not found")
    if resp.status_code == 403:
        abort(403, "not authorized for this order")
    resp.raise_for_status()

    # Only the order fields the frontend needs are relayed; the downstream
    # token itself is never included in this response.
    return jsonify(resp.json())
