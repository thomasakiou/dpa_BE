"""Add financial year support

Revision ID: d8e3f6a2b3c4
Revises: c7d9e4f5a1b2
Create Date: 2025-12-02 15:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8e3f6a2b3c4'
down_revision: Union[str, None] = 'c7d9e4f5a1b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create system_settings table
    op.create_table('system_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(100), nullable=False),
        sa.Column('value', sa.String(500), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_system_settings_id'), 'system_settings', ['id'], unique=False)
    op.create_index(op.f('ix_system_settings_key'), 'system_settings', ['key'], unique=True)
    
    # Add financial_year columns to all financial tables
    op.add_column('savings', sa.Column('financial_year', sa.String(9), nullable=True))
    op.create_index(op.f('ix_savings_financial_year'), 'savings', ['financial_year'], unique=False)
    
    op.add_column('savings_payments', sa.Column('financial_year', sa.String(9), nullable=True))
    op.create_index(op.f('ix_savings_payments_financial_year'), 'savings_payments', ['financial_year'], unique=False)
    
    op.add_column('loans', sa.Column('financial_year', sa.String(9), nullable=True))
    op.create_index(op.f('ix_loans_financial_year'), 'loans', ['financial_year'], unique=False)
    
    op.add_column('shares', sa.Column('financial_year', sa.String(9), nullable=True))
    op.create_index(op.f('ix_shares_financial_year'), 'shares', ['financial_year'], unique=False)
    
    op.add_column('transactions', sa.Column('financial_year', sa.String(9), nullable=True))
    op.create_index(op.f('ix_transactions_financial_year'), 'transactions', ['financial_year'], unique=False)
    
    # Set default financial year for existing records
    op.execute("""
        UPDATE savings SET financial_year = '2024-2025' WHERE financial_year IS NULL;
        UPDATE savings_payments SET financial_year = '2024-2025' WHERE financial_year IS NULL;
        UPDATE loans SET financial_year = '2024-2025' WHERE financial_year IS NULL;
        UPDATE shares SET financial_year = '2024-2025' WHERE financial_year IS NULL;
        UPDATE transactions SET financial_year = '2024-2025' WHERE financial_year IS NULL;
    """)
    
    # Insert default financial year setting
    op.execute("""
        INSERT INTO system_settings (key, value, description)
        VALUES ('current_financial_year', '2024-2025', 'Current active financial year'),
               ('financial_year_start_date', '2024-01-01', 'Financial year start date'),
               ('financial_year_end_date', '2024-12-31', 'Financial year end date');
    """)


def downgrade() -> None:
    # Remove financial year settings
    op.execute("DELETE FROM system_settings WHERE key IN ('current_financial_year', 'financial_year_start_date', 'financial_year_end_date')")
    
    # Remove financial_year columns
    op.drop_index(op.f('ix_transactions_financial_year'), table_name='transactions')
    op.drop_column('transactions', 'financial_year')
    
    op.drop_index(op.f('ix_shares_financial_year'), table_name='shares')
    op.drop_column('shares', 'financial_year')
    
    op.drop_index(op.f('ix_loans_financial_year'), table_name='loans')
    op.drop_column('loans', 'financial_year')
    
    op.drop_index(op.f('ix_savings_payments_financial_year'), table_name='savings_payments')
    op.drop_column('savings_payments', 'financial_year')
    
    op.drop_index(op.f('ix_savings_financial_year'), table_name='savings')
    op.drop_column('savings', 'financial_year')
    
    # Drop system_settings table
    op.drop_index(op.f('ix_system_settings_key'), table_name='system_settings')
    op.drop_index(op.f('ix_system_settings_id'), table_name='system_settings')
    op.drop_table('system_settings')
