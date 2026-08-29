"""HTTP layer. Field names here match models.py exactly -- this service has
no separate wire-format naming."""

from rules import approve, reject, submit_report


def post_report_submit(report_id: int) -> dict:
    report, expenses = _load(report_id)
    submit_report(report, expenses)
    return {"id": report.id, "status": report.status}


def post_report_approve(report_id: int, approver_id: int) -> dict:
    report, _ = _load(report_id)
    approver = _load_employee(approver_id)
    submitter = _load_employee(report.employee_id)
    approve(report, approver, submitter)
    return {"id": report.id, "status": report.status}


def post_report_reject(report_id: int, approver_id: int, reason: str) -> dict:
    report, _ = _load(report_id)
    approver = _load_employee(approver_id)
    reject(report, approver, reason)
    return {"id": report.id, "status": report.status}


def _load(report_id: int):
    raise NotImplementedError("db wiring omitted from this excerpt")


def _load_employee(employee_id: int):
    raise NotImplementedError("db wiring omitted from this excerpt")
