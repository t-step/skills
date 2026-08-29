"""Business rules for expensify-lite. models.py only defines storage shape;
every constraint on what counts as a *valid* report or approval lives here."""

from models import Approval, AuditEvent, Employee, Expense, Report

RECEIPT_REQUIRED_ABOVE_CENTS = 7500


class RuleViolation(Exception):
    pass


def submit_report(report: Report, expenses: list[Expense]) -> None:
    if report.status != "draft":
        raise RuleViolation(f"cannot submit report from status {report.status}")
    for expense in expenses:
        if expense.amount_cents >= RECEIPT_REQUIRED_ABOVE_CENTS and not expense.receipt_url:
            raise RuleViolation(
                f"expense {expense.id} is >= ${RECEIPT_REQUIRED_ABOVE_CENTS / 100:.2f} "
                "and has no attached receipt"
            )
    report.status = "submitted"
    _log(report, "submitted", actor_id=report.employee_id)


def approve(report: Report, approver: Employee, submitter: Employee) -> None:
    """A report can only be approved by the submitter's manager (or that
    manager's own manager, recursively) -- never by the submitter, and
    never by someone outside the submitter's management chain."""
    if report.status != "submitted":
        raise RuleViolation(f"cannot approve report from status {report.status}")
    if approver.id == submitter.id:
        raise RuleViolation("an employee cannot approve their own report")
    if not _is_in_management_chain(approver, submitter):
        raise RuleViolation(
            f"approver {approver.id} is not in submitter {submitter.id}'s management chain"
        )
    report.status = "approved"
    _log(report, "approved", actor_id=approver.id)


def reject(report: Report, approver: Employee, reason: str) -> None:
    if report.status != "submitted":
        raise RuleViolation(f"cannot reject report from status {report.status}")
    report.status = "rejected"
    _log(report, f"rejected: {reason}", actor_id=approver.id)


def _is_in_management_chain(candidate: Employee, submitter: Employee) -> bool:
    """Walks submitter.manager_id upward; candidate must appear somewhere
    above submitter, not merely be *a* manager somewhere in the org."""
    current_manager_id = submitter.manager_id
    # NOTE: this walk needs the full employee table to resolve manager_id
    # chains; the lookup function isn't shown here but is assumed available.
    from db import get_employee  # local import to avoid a hard db dependency in tests

    seen = set()
    while current_manager_id is not None:
        if current_manager_id == candidate.id:
            return True
        if current_manager_id in seen:
            return False  # defensive: a cycle in the org chart should never validate
        seen.add(current_manager_id)
        manager = get_employee(current_manager_id)
        current_manager_id = manager.manager_id if manager else None
    return False


_AUDIT_LOG: list[AuditEvent] = []


def _log(report: Report, action: str, actor_id: int) -> None:
    _AUDIT_LOG.append(AuditEvent(
        id=len(_AUDIT_LOG), entity_type="report", entity_id=report.id,
        action=action, actor_id=actor_id, at="now",
    ))
