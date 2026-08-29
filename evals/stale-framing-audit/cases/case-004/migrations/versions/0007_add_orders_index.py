"""add orders index

Revision ID: 0007
Revises: 0006
"""
from alembic import op


def upgrade():
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])


def downgrade():
    op.drop_index("ix_orders_customer_id", table_name="orders")
