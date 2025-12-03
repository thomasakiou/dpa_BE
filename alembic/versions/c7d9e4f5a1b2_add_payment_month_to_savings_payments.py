"""Add payment_month to savings_payments

Revision ID: c7d9e4f5a1b2
Revises: b6cfbbd58899
Create Date: 2025-12-02 15:32:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7d9e4f5a1b2'
down_revision: Union[str, None] = 'b6cfbbd58899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add payment_month column to savings_payments table
    op.add_column('savings_payments', 
        sa.Column('payment_month', sa.String(20), nullable=True)
    )


def downgrade() -> None:
    # Remove payment_month column from savings_payments table
    op.drop_column('savings_payments', 'payment_month')
