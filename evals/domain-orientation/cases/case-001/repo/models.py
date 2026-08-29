"""SQLAlchemy-style models for expensify-lite. This module defines storage
shape only; business rules live in rules.py, not here."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Employee:
    id: int
    name: str
    manager_id: int | None  # None only for the CEO record


@dataclass
class Expense:
    id: int
    report_id: int
    amount_cents: int
    category: str  # "travel" | "meals" | "supplies" | "other"
    incurred_on: date
    receipt_url: str | None = None


@dataclass
class Report:
    id: int
    employee_id: int
    status: str  # "draft" | "submitted" | "approved" | "rejected"
    submitted_at: str | None = None
    expenses: list = field(default_factory=list)


@dataclass
class Approval:
    id: int
    report_id: int
    approver_id: int
    decision: str  # "approved" | "rejected"
    decided_at: str


@dataclass
class AuditEvent:
    """Generic append-only log row. Every mutating call in rules.py writes
    one of these. Nothing reads AuditEvent to make decisions -- it exists
    for after-the-fact investigation only."""

    id: int
    entity_type: str
    entity_id: int
    action: str
    actor_id: int
    at: str
