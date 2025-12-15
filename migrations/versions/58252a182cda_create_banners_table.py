"""create_banners_table

Revision ID: 58252a182cda
Revises: 396a856de9da
Create Date: 2025-11-10 14:19:51.690883

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "58252a182cda"
down_revision = "396a856de9da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create banners table."""
    op.create_table(
        "banners",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("fallback_image", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subtitle", sa.String(), nullable=False),
        sa.Column("cta_label", sa.String(), nullable=False),
        sa.Column("target_type", sa.String(), nullable=False),
        sa.Column("target_id", sa.String(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("start_at", sa.DateTime(), nullable=True),
        sa.Column("end_at", sa.DateTime(), nullable=True),
        sa.Column("aspect_ratio", sa.String(), nullable=False, server_default="9:14"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for better query performance
    op.create_index("idx_banners_priority", "banners", ["priority"])
    op.create_index("idx_banners_start_at", "banners", ["start_at"])
    op.create_index("idx_banners_end_at", "banners", ["end_at"])
    op.create_index("idx_banners_target", "banners", ["target_type", "target_id"])


def downgrade() -> None:
    """Drop banners table."""
    op.drop_index("idx_banners_target", table_name="banners")
    op.drop_index("idx_banners_end_at", table_name="banners")
    op.drop_index("idx_banners_start_at", table_name="banners")
    op.drop_index("idx_banners_priority", table_name="banners")
    op.drop_table("banners")
