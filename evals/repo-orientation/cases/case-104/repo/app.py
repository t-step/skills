from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/orders/<order_id>")
def get_order(order_id):
    return jsonify({"id": order_id, "items": []})


@app.get("/orders/<order_id>/items")
def get_order_items(order_id):
    return jsonify([])
