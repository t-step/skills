"""Order-detail page route.

Reachable without an active session on purpose: a user following a link
from email, Teams, or a bookmark may not have a session yet, and the app
sends them through login rather than dead-ending on a blank error page.
"""

from flask import Blueprint, abort, redirect, render_template, session

from db import get_account_ids_for_user, get_order_by_id

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders/<order_id>", methods=["GET"])
def view_order(order_id: str):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(f"/login?continue=/orders/{order_id}")

    order = get_order_by_id(order_id)
    if order is None:
        abort(404)

    # Session presence only establishes who is asking. Whether this user
    # may see this specific order is a separate check, made here, every
    # time, against the order's own account rather than the user's login
    # state.
    if order["account_id"] not in get_account_ids_for_user(user_id):
        abort(403)

    return render_template("order_detail.html", order=order)
