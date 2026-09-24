"""Internal expense-approval domain logic."""


def approve(expense_id: str, approver_user_id: str) -> None:
    """Marks an expense approved. Trusts approver_user_id as given."""
    expense = load_expense(expense_id)
    expense["status"] = "approved"
    expense["approved_by"] = approver_user_id
    save_expense(expense)


def get_assigned_approver(expense_id: str) -> str:
    """The internal user id who is actually authorized to approve this
    specific expense (its manager-of-record, per the org chart)."""
    expense = load_expense(expense_id)
    return expense["assigned_approver_user_id"]


def user_can_view(expense_id: str, internal_user_id: str) -> bool:
    """Whether internal_user_id is on the expense's visibility list
    (submitter, assigned approver, or same-team viewer)."""
    expense = load_expense(expense_id)
    return internal_user_id in expense["visible_to_user_ids"]


def add_comment(expense_id: str, internal_user_id: str, text: str) -> None:
    expense = load_expense(expense_id)
    expense.setdefault("comments", []).append(
        {"by": internal_user_id, "text": text}
    )
    save_expense(expense)


def load_expense(expense_id: str) -> dict:
    ...  # DB lookup, not relevant to this audit


def save_expense(expense: dict) -> None:
    ...  # DB write, not relevant to this audit
