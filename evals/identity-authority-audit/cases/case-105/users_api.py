"""Backend handler for the admin panel's user management endpoints."""

from flask import Blueprint, session, abort

users_bp = Blueprint("users", __name__)


def require_session():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    return user_id


@users_bp.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # Confirms someone is logged in. Does not check what they're allowed
    # to do -- any authenticated session can delete any user by id.
    require_session()
    db_delete_user(user_id)
    return {"status": "deleted"}, 200


@users_bp.route("/api/users/<user_id>/role", methods=["PATCH"])
def update_user_role(user_id):
    require_session()
    from flask import request

    new_role = request.json["role"]
    db_update_user_role(user_id, new_role)
    return {"status": "updated"}, 200


def db_delete_user(user_id):
    ...  # not relevant to this audit


def db_update_user_role(user_id, new_role):
    ...  # not relevant to this audit
