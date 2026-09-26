"""expense-ocr-poc: receipt line-item extraction service."""

import sqlite3
import uuid

from flask import Flask, jsonify, request

import ocr_client  # third-party OCR API wrapper

app = Flask(__name__)

DB_PATH = "results.db"


def get_db():
    return sqlite3.connect(DB_PATH)


@app.route("/extract", methods=["POST"])
def extract():
    image = request.files["receipt"]
    image_bytes = image.read()

    result_id = str(uuid.uuid4())

    # Call the OCR vendor synchronously; no retry, no idempotency key --
    # a network blip here just means the user re-uploads.
    ocr_result = ocr_client.extract_line_items(image_bytes)

    try:
        line_items = _parse_result(ocr_result)
    except ValueError as exc:
        # Parsing failure: the uploaded image was only ever held in
        # `image_bytes` for this request -- it's never written to disk,
        # queued, or otherwise persisted anywhere. Once this handler
        # returns, there is no way to retry or manually re-process this
        # submission; the user's receipt data is simply lost.
        return jsonify({"error": f"could not parse OCR result: {exc}"}), 422

    db = get_db()
    db.execute(
        "INSERT INTO results (id, line_items) VALUES (?, ?)",
        (result_id, str(line_items)),
    )
    db.commit()

    # Delete the uploaded image immediately after processing -- per
    # README, a deliberate data-retention decision, not an oversight.
    del image_bytes

    return jsonify({"result_id": result_id, "line_items": line_items})


def _parse_result(ocr_result: dict) -> list[dict]:
    # Third-party OCR responses are occasionally malformed for unusual
    # receipt layouts (crumpled paper, handwritten totals, non-English
    # text) -- when that happens, this raises ValueError.
    return ocr_result["parsed_line_items"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
