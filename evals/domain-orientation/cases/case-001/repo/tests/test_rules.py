"""Tests asserting the actual business rules, not just CRUD round-trips."""

import pytest

from models import Employee, Expense, Report
from rules import RuleViolation, approve, submit_report


def test_submit_requires_receipt_above_threshold():
    report = Report(id=1, employee_id=10, status="draft")
    big_expense = Expense(id=1, report_id=1, amount_cents=10000, category="travel",
                           incurred_on="2026-01-01", receipt_url=None)
    with pytest.raises(RuleViolation, match="no attached receipt"):
        submit_report(report, [big_expense])


def test_submit_allows_small_expense_without_receipt():
    report = Report(id=2, employee_id=10, status="draft")
    small_expense = Expense(id=2, report_id=2, amount_cents=500, category="meals",
                             incurred_on="2026-01-01", receipt_url=None)
    submit_report(report, [small_expense])
    assert report.status == "submitted"


def test_cannot_self_approve():
    report = Report(id=3, employee_id=10, status="submitted")
    same_person = Employee(id=10, name="Alex", manager_id=99)
    with pytest.raises(RuleViolation, match="cannot approve their own report"):
        approve(report, approver=same_person, submitter=same_person)
