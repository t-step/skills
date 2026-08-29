"""Billing service models. This is the only place a customer record is
created or updated -- billing owns customer identity for the whole system."""

from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    email: str
    billing_address: str
    created_at: str


@dataclass
class Invoice:
    id: int
    customer_id: int
    amount_cents: int
    status: str  # "open" | "paid" | "void"
