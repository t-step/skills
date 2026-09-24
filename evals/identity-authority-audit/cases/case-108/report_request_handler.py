"""Web route the browser calls when a user clicks "Generate report"."""

from flask import Blueprint, session, request
import permission_service
import job_queue

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/api/reports", methods=["POST"])
def generate_report():
    user_id = session["user_id"]
    project_ids = request.json["project_ids"]

    # Checked once, right now, while the user is still in an active
    # session -- this is the only point in the whole flow where the
    # user's own access is consulted.
    accessible = permission_service.get_accessible_project_ids(user_id)
    requested = [p for p in project_ids if p in accessible]
    if not requested:
        return {"error": "no accessible projects requested"}, 403

    job_id = job_queue.enqueue(
        "generate_report",
        payload={"requested_by_user_id": user_id, "project_ids": requested},
    )
    return {"job_id": job_id, "status": "queued"}, 202
