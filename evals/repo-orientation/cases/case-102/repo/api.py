from flask import Flask, request, jsonify

from store import save_feedback

app = Flask(__name__)


@app.post("/feedback")
def post_feedback():
    save_feedback(request.json["message"])
    return jsonify({"ok": True}), 201
