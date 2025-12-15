"""remove_config_and_type_from_payment_methods

Revision ID: 04b299e86d68
Revises: 58252a182cda
Create Date: 2025-11-20 23:32:01.661794

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "04b299e86d68"
down_revision = "58252a182cda"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove config and type columns from payment_methods table."""
    # Drop the config column (JSON type)
    op.drop_column("payment_methods", "config")

    # Drop the type column (VARCHAR)
    op.drop_column("payment_methods", "type")


def downgrade() -> None:
    """Add back config and type columns to payment_methods table."""
    # Add back the type column
    op.add_column(
        "payment_methods", sa.Column("type", sa.String(length=100), nullable=True)
    )

    # Add back the config column (JSON type)
    op.add_column(
        "payment_methods",
        sa.Column("config", postgresql.JSON(astext_type=sa.Text()), nullable=True),
    )
