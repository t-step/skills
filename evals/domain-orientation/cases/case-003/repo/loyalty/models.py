"""Loyalty program models, owned by the Loyalty team. A Member is a
household-level rewards enrollment -- it is not created automatically when
a Customer signs up, and a household can span multiple Customer rows."""

from dataclasses import dataclass


@dataclass
class Member:
    id: int
    household_name: str
    points_balance: int
    tier: str  # "bronze" | "silver" | "gold"


@dataclass
class MemberCustomerLink:
    """Join table. A single Member (household) can link to more than one
    billing.Customer (e.g. two spouses, each with their own billing
    account, sharing one points balance). A Customer with no row here is
    not enrolled in the loyalty program at all."""

    member_id: int
    customer_id: int
    linked_at: str
