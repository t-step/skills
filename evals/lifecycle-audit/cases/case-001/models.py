"""orders/models.py -- excerpt from the orders service."""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, default=OrderStatus.PENDING.value)
    is_flagged_for_review = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Populated by the nightly search-index build (see search/indexer.py).
    # Not written anywhere else in this service.
    workflow_state_cache = Column(String, nullable=True)

    refund = relationship("Refund", back_populates="order", uselist=False)

    @property
    def workflow_state(self) -> str:
        """Human-facing label shown in the ops dashboard's order list.

        Recomputed from current field values every time it's accessed --
        never stored on this row. `workflow_state_cache` is a separate,
        periodically-refreshed copy used only by the search index (see
        search/indexer.py); this property does not read it.
        """
        if self.is_flagged_for_review:
            return "Needs Attention"
        if self.refund is not None and self.refund.status == "pending":
            return "On Hold"
        if self.status == OrderStatus.DELIVERED.value:
            return "Complete"
        if self.status == OrderStatus.CANCELLED.value:
            return "Cancelled"
        return "In Progress"


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, issued, denied
    amount_cents = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="refund")
