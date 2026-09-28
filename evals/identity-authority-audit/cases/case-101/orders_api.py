"""Orders API: the downstream resource server. Only ever called by the BFF
(or other internal services), never directly by a browser."""

import jwt
from flask import Flask, abort, jsonify, request

import db  # internal Postgres access layer

app = Flask(__name__)

JWT_PUBLIC_KEY = "<STS public key, loaded at process start>"
EXPECTED_AUDIENCE = "orders-api"
EXPECTED_ISSUER = "https://sts.internal.example.com"


def authenticate_request():
    """Validate the bearer token's signature, issuer, audience, and
    expiry. Returns the decoded claims, or aborts the request."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, "missing bearer token")
    token = auth_header[len("Bearer "):]

    try:
        claims = jwt.decode(
            token,
            JWT_PUBLIC_KEY,
            algorithms=["RS256"],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
    except jwt.InvalidAudienceError:
        abort(401, "token not issued for orders-api")
    except jwt.ExpiredSignatureError:
        abort(401, "token expired")
    except jwt.InvalidTokenError:
        abort(401, "invalid token")

    return claims


def require_scope(claims: dict, needed: str):
    granted = set(claims.get("scope", "").split())
    if needed not in granted:
        abort(403, f"token missing required scope: {needed}")


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id: str):
    claims = authenticate_request()
    require_scope(claims, "orders:read")

    order = db.query_one("SELECT * FROM orders WHERE id = %s", [order_id])
    if order is None:
        abort(404, "order not found")

    # Resource-level authorization: the order must actually belong to the
    # account the exchanged token was issued for. Audience/scope checks
    # only establish that *some* caller with orders:read authority is
    # asking; they say nothing about whether this specific order is theirs.
    if order["account_id"] != claims["account_id"]:
        abort(403, "order does not belong to the authenticated account")

    return jsonify(order)


@app.route("/orders/<order_id>/cancel", methods=["POST"])
def cancel_order(order_id: str):
    claims = authenticate_request()
    require_scope(claims, "orders:write")

    order = db.query_one("SELECT * FROM orders WHERE id = %s", [order_id])
    if order is None:
        abort(404, "order not found")

    if order["account_id"] != claims["account_id"]:
        abort(403, "order does not belong to the authenticated account")

    db.execute(
        "UPDATE orders SET status = 'cancelled', updated_at = now() WHERE id = %s",
        [order_id],
    )
    return jsonify({"status": "cancelled"})
