"""remove_price_from_booking_seats

Revision ID: 6a6366df244e
Revises: 04b299e86d68
Create Date: 2025-11-20 23:57:01.738681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a6366df244e'
down_revision = '04b299e86d68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove price column from booking_seats table."""
    # Drop the price column (Float type)
    op.drop_column('booking_seats', 'price')


def downgrade() -> None:
    """Add back price column to booking_seats table."""
    # Add back the price column
    op.add_column('booking_seats',
        sa.Column('price', sa.Float(), nullable=False, server_default='0.0')
    )

