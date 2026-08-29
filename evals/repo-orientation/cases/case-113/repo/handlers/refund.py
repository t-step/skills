from flask import Blueprint, jsonify, request

refund_bp = Blueprint("refund", __name__)


@refund_bp.route("/process", methods=["POST"])
def process_refund():
    order_id = request.json.get("order_id")
    return jsonify({"order_id": order_id, "refund_status": "processed"})
