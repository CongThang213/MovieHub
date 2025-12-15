"""add_cascade_delete_to_seat_tables

Revision ID: 396a856de9da
Revises: 01b62422d7c2
Create Date: 2025-10-31 23:54:41.976118

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "396a856de9da"
down_revision = "01b62422d7c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop existing foreign key constraints
    op.drop_constraint("seats_row_id_fkey", "seats", type_="foreignkey")
    op.drop_constraint("seat_rows_hall_id_fkey", "seat_rows", type_="foreignkey")

    # Recreate foreign key constraints with CASCADE delete
    op.create_foreign_key(
        "seats_row_id_fkey",
        "seats",
        "seat_rows",
        ["row_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "seat_rows_hall_id_fkey",
        "seat_rows",
        "halls",
        ["hall_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Drop CASCADE foreign key constraints
    op.drop_constraint("seats_row_id_fkey", "seats", type_="foreignkey")
    op.drop_constraint("seat_rows_hall_id_fkey", "seat_rows", type_="foreignkey")

    # Recreate original foreign key constraints without CASCADE
    op.create_foreign_key("seats_row_id_fkey", "seats", "seat_rows", ["row_id"], ["id"])

    op.create_foreign_key(
        "seat_rows_hall_id_fkey", "seat_rows", "halls", ["hall_id"], ["id"]
    )
