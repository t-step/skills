from flask import Blueprint, jsonify, request

from app import services

bp = Blueprint("todos", __name__)


@bp.get("/todos")
def get_todos():
    from app.db import get_session

    session = get_session()
    items = services.list_todos(session)
    return jsonify([{"id": i.id, "title": i.title, "done": i.done} for i in items])


@bp.post("/todos")
def post_todo():
    from app.db import get_session

    session = get_session()
    item = services.create_todo(session, request.json["title"])
    return jsonify({"id": item.id, "title": item.title, "done": item.done}), 201
