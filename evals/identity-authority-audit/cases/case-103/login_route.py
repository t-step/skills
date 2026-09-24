"""Login handler and post-login redirect.

Accepts an optional `continue` target so a user arriving via a deep link
(email, chat notification, bookmark) lands back where they were headed
once they've authenticated, instead of always dropping them on the
default dashboard.
"""

from urllib.parse import urlparse

from flask import Blueprint, redirect, render_template, request, session

from credentials import verify_password

login_bp = Blueprint("login", __name__)

DEFAULT_LANDING = "/dashboard"


def _safe_continue_target(raw: str | None) -> str:
    """Return only a same-origin, relative path.

    `continue` round-trips through URLs a user clicks, so an absolute or
    scheme-relative value here would turn login into an open redirect.
    Anything that isn't a plain relative path falls back to the default
    landing page instead of being honored.
    """
    if not raw:
        return DEFAULT_LANDING

    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc or raw.startswith("//"):
        return DEFAULT_LANDING
    if not parsed.path.startswith("/"):
        return DEFAULT_LANDING

    return parsed.path + (f"?{parsed.query}" if parsed.query else "")


@login_bp.route("/login", methods=["GET"])
def login_form():
    return render_template(
        "login.html", continue_target=request.args.get("continue", "")
    )


@login_bp.route("/login", methods=["POST"])
def login_submit():
    email = request.form["email"]
    password = request.form["password"]

    user = verify_password(email, password)
    if user is None:
        return render_template("login.html", error="Invalid credentials"), 401

    session.clear()
    session["user_id"] = user["id"]

    target = _safe_continue_target(request.form.get("continue"))
    return redirect(target)
