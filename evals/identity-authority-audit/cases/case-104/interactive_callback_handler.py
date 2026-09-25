"""Handles Slack interactive-component callbacks (button clicks) for the
expense-approval workflow."""

import json

import expense_service
from slack_signature import verify_slack_signature


def approve_expense_callback(request):
    """Handles the "Approve" button on an expense card posted to Slack."""
    if not verify_slack_signature(request):
        return {"error": "invalid signature"}, 401

    payload = json.loads(request.form["payload"])
    expense_id = payload["actions"][0]["value"]
    slack_user_id = payload["user"]["id"]

    # The signature proves this request really came from Slack. It says
    # nothing about whether slack_user_id is the person who's supposed to
    # approve this expense -- that question is never asked here.
    expense_service.approve(expense_id, approver_user_id=slack_user_id)
    return {"text": "Expense approved."}, 200


def add_comment_callback(request):
    """Handles the "Add comment" button on the same expense card."""
    if not verify_slack_signature(request):
        return {"error": "invalid signature"}, 401

    payload = json.loads(request.form["payload"])
    expense_id = payload["actions"][0]["value"]
    slack_user_id = payload["user"]["id"]
    comment_text = payload["actions"][0].get("comment_text", "")

    internal_user_id = map_slack_user_to_internal_user(slack_user_id)
    if not expense_service.user_can_view(expense_id, internal_user_id):
        return {"text": "You don't have access to this expense."}, 403

    expense_service.add_comment(expense_id, internal_user_id, comment_text)
    return {"text": "Comment added."}, 200


def map_slack_user_to_internal_user(slack_user_id: str) -> str:
    ...  # looks up the SSO-linked internal user id; not relevant to this audit
