"""initialize tables for database

Revision ID: 01b62422d7c2
Revises:
Create Date: 2025-10-09 21:12:53.796950

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql.schema import ForeignKey

# revision identifiers, used by Alembic.
revision = "01b62422d7c2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create all cinema database."""

    # Create enum for image types
    image_type_enum = sa.Enum(
        "AVATAR", "FILM_THUMBNAIL", "FILM_BACKGROUND", "FILM_POSTER", name="image_type"
    )

    # Create enum for account types
    account_type_enum = sa.Enum("CUSTOMER", "ADMIN", name="account_type")

    # Create enum for film promotion
    film_promotion_enum = sa.Enum(
        "DISCOUNT", "FEATURED", "PREMIERE", "SPECIAL_EVENT", name="film_promotion"
    )

    # Create images table
    op.create_table(
        "images",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=True),
        sa.Column("type", image_type_enum, nullable=False),
        sa.Column("public_id", sa.String(), nullable=False),
        sa.Column("is_temp", sa.Boolean(), nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # Create indexes for common queries
    op.create_index("idx_images_owner_type", "images", ["owner_id", "type"])
    op.create_index("idx_images_is_temp", "images", ["is_temp"])
    op.create_index("idx_images_created_at", "images", ["created_at"])
    op.create_index("idx_images_type", "images", ["type"])

    # Create cities table
    op.create_table(
        "cities",
        sa.Column(
            "id",
            sa.String(),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create cinemas table
    op.create_table(
        "cinemas",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("city_id", sa.String(), ForeignKey("cities.id")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("long", sa.Float(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_cinemas_city", "cinemas", ["city_id"])

    # Create halls table
    op.create_table(
        "halls",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("cinema_id", sa.String(), ForeignKey("cinemas.id")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_halls_cinema", "halls", ["cinema_id"])

    # Create seat_categories table
    op.create_table(
        "seat_categories",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("base_price", sa.Float(), nullable=False),
        sa.Column("attributes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create seat_rows table
    op.create_table(
        "seat_rows",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("hall_id", sa.String(), ForeignKey("halls.id")),
        sa.Column("row_label", sa.String(10), nullable=False),
        sa.Column("row_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_seat_rows_hall", "seat_rows", ["hall_id"])

    # Create seats table
    op.create_table(
        "seats",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("row_id", sa.String(), ForeignKey("seat_rows.id")),
        sa.Column("category_id", sa.String(), ForeignKey("seat_categories.id")),
        sa.Column("seat_number", sa.Integer(), nullable=False),
        sa.Column("pos_x", sa.Float(), nullable=True),
        sa.Column("pos_y", sa.Float(), nullable=True),
        sa.Column("is_accessible", sa.Boolean(), default=False),
        sa.Column("external_label", sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_seats_row", "seats", ["row_id"])
    op.create_index("idx_seats_category", "seats", ["category_id"])

    # Create genres table
    op.create_table(
        "genres",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create casts table
    op.create_table(
        "casts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("biography", sa.Text(), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create film_formats table
    op.create_table(
        "film_formats",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surcharge", sa.Float(), default=0),
        sa.Column("description", sa.String, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(
            "account_type",
            account_type_enum,
            nullable=False,
            default="CUSTOMER",
        ),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create films table
    op.create_table(
        "films",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False, unique=True),
        sa.Column("votes", sa.Integer(), default=0),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        # sa.Column("thumbnail_image_url", sa.String(), nullable=True),
        # sa.Column("background_image_url", sa.String(), nullable=True),
        # sa.Column("poster_image_url", sa.String(), nullable=True),
        sa.Column("movie_begin_date", sa.DateTime(), nullable=True),
        sa.Column("movie_end_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_films_title", "films", ["title"])

    # Create film_trailers table
    op.create_table(
        "film_trailers",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("film_id", sa.String(), ForeignKey("films.id")),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_film_trailers_film", "film_trailers", ["film_id"])

    # Create film_genres junction table
    op.create_table(
        "film_genres",
        sa.Column("film_id", sa.String(), ForeignKey("films.id"), primary_key=True),
        sa.Column("genre_id", sa.String(), ForeignKey("genres.id"), primary_key=True),
    )
    op.create_index("idx_film_genres_film", "film_genres", ["film_id"])
    op.create_index("idx_film_genres_genre", "film_genres", ["genre_id"])

    # Create film_casts junction table
    op.create_table(
        "film_casts",
        sa.Column("film_id", sa.String(), ForeignKey("films.id"), primary_key=True),
        sa.Column("cast_id", sa.String(), ForeignKey("casts.id"), primary_key=True),
        sa.Column("role", sa.String(100), nullable=True),
        sa.Column("character_name", sa.String(), nullable=True),
    )
    op.create_index("idx_film_casts_film", "film_casts", ["film_id"])
    op.create_index("idx_film_casts_cast", "film_casts", ["cast_id"])

    # Create showtimes table
    op.create_table(
        "showtimes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("hall_id", sa.String(), ForeignKey("halls.id")),
        sa.Column("film_id", sa.String(), ForeignKey("films.id")),
        sa.Column("film_format_id", sa.String(), ForeignKey("film_formats.id")),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("available_seats", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_showtimes_hall", "showtimes", ["hall_id"])
    op.create_index("idx_showtimes_film", "showtimes", ["film_id"])
    op.create_index("idx_showtimes_format", "showtimes", ["film_format_id"])
    op.create_index("idx_showtimes_start_time", "showtimes", ["start_time"])

    # Create payment_methods table
    op.create_table(
        "payment_methods",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type", sa.String(100), nullable=True),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("active", sa.Boolean(), default=True),
        sa.Column("surcharge", sa.Float(), default=0),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create vouchers table
    op.create_table(
        "vouchers",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("code", sa.String(100), nullable=False, unique=True),
        sa.Column("discount_rate", sa.Float(), nullable=False),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_until", sa.DateTime(), nullable=True),
        sa.Column("max_usage", sa.Integer(), nullable=True),
        sa.Column("used_count", sa.Integer(), default=0),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_vouchers_code", "vouchers", ["code"])

    # Create bookings table
    op.create_table(
        "bookings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), ForeignKey("users.id")),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("total_price", sa.Float(), nullable=True),
        sa.Column(
            "payment_method_id",
            sa.String(),
            ForeignKey("payment_methods.id"),
            nullable=True,
        ),
        sa.Column("voucher_id", sa.String(), ForeignKey("vouchers.id"), nullable=True),
        sa.Column("payment_reference", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_bookings_user", "bookings", ["user_id"])
    op.create_index("idx_bookings_status", "bookings", ["status"])

    # Create booking_seats table
    op.create_table(
        "booking_seats",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("booking_id", sa.String(), ForeignKey("bookings.id")),
        sa.Column("showtime_id", sa.String(), ForeignKey("showtimes.id")),
        sa.Column("seat_id", sa.String(), ForeignKey("seats.id")),
        sa.Column("price", sa.Float(), nullable=False),
        # sa.Column("status", sa.String(50), nullable=True),
        # sa.Column("reserved_at", sa.DateTime(), nullable=True),
        # sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("purchased_at", sa.DateTime(), nullable=True),
        sa.Column("ticket_code", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_booking_seats_booking", "booking_seats", ["booking_id"])
    op.create_index("idx_booking_seats_showtime", "booking_seats", ["showtime_id"])
    op.create_index("idx_booking_seats_seat", "booking_seats", ["seat_id"])

    # Create payments table
    op.create_table(
        "payments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("booking_id", sa.String(), ForeignKey("bookings.id")),
        sa.Column("payment_method_id", sa.String(), ForeignKey("payment_methods.id")),
        sa.Column("external_txn_id", sa.String(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=False),
        # sa.Column("currency", sa.String(10), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_payments_booking", "payments", ["booking_id"])

    # Create services table
    op.create_table(
        "services",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        # sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create ticket_services junction table
    op.create_table(
        "ticket_services",
        sa.Column(
            "booking_seat_id",
            sa.String(),
            ForeignKey("booking_seats.id"),
            primary_key=True,
        ),
        sa.Column(
            "service_id", sa.String(), ForeignKey("services.id"), primary_key=True
        ),
        sa.Column("count", sa.Integer(), default=1),
    )

    # Create film_reviews table
    op.create_table(
        "film_reviews",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("film_id", sa.String(), ForeignKey("films.id")),
        sa.Column("author_id", sa.String(), ForeignKey("users.id")),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_film_reviews_film", "film_reviews", ["film_id"])
    op.create_index("idx_film_reviews_author", "film_reviews", ["author_id"])

    # Create film_promotions table
    op.create_table(
        "film_promotions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("film_id", sa.String(), ForeignKey("films.id")),
        sa.Column("type", film_promotion_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_until", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_film_promotions_film", "film_promotions", ["film_id"])

    # Insert cities data
    city_table = sa.table(
        "cities",
        sa.column("id", sa.String),
        sa.column("name", sa.String),
        sa.column("country", sa.String),
    )

    op.bulk_insert(
        city_table,
        [
            {"name": "Hà Nội", "country": "Vietnam"},
            {"name": "Cao Bằng", "country": "Vietnam"},
            {"name": "Tuyên Quang", "country": "Vietnam"},
            {"name": "Điện Biên", "country": "Vietnam"},
            {"name": "Lai Châu", "country": "Vietnam"},
            {"name": "Sơn La", "country": "Vietnam"},
            {"name": "Lào Cai", "country": "Vietnam"},
            {"name": "Thái Nguyên", "country": "Vietnam"},
            {"name": "Lạng Sơn", "country": "Vietnam"},
            {"name": "Quảng Ninh", "country": "Vietnam"},
            {"name": "Bắc Ninh", "country": "Vietnam"},
            {"name": "Phú Thọ", "country": "Vietnam"},
            {"name": "Hải Phòng", "country": "Vietnam"},
            {"name": "Hưng Yên", "country": "Vietnam"},
            {"name": "Ninh Bình", "country": "Vietnam"},
            {"name": "Thanh Hóa", "country": "Vietnam"},
            {"name": "Nghệ An", "country": "Vietnam"},
            {"name": "Hà Tĩnh", "country": "Vietnam"},
            {"name": "Quảng Trị", "country": "Vietnam"},
            {"name": "Huế", "country": "Vietnam"},
            {"name": "Đà Nẵng", "country": "Vietnam"},
            {"name": "Quảng Ngãi", "country": "Vietnam"},
            {"name": "Gia Lai", "country": "Vietnam"},
            {"name": "Khánh Hòa", "country": "Vietnam"},
            {"name": "Đắk Lắk", "country": "Vietnam"},
            {"name": "Lâm Đồng", "country": "Vietnam"},
            {"name": "Đồng Nai", "country": "Vietnam"},
            {"name": "Hồ Chí Minh", "country": "Vietnam"},
            {"name": "Tây Ninh", "country": "Vietnam"},
            {"name": "Đồng Tháp", "country": "Vietnam"},
            {"name": "Vĩnh Long", "country": "Vietnam"},
            {"name": "An Giang", "country": "Vietnam"},
            {"name": "Cần Thơ", "country": "Vietnam"},
            {"name": "Cà Mau", "country": "Vietnam"},
        ],
    )


def downgrade():
    """Drop all cinema database tables."""
    # Drop all tables in reverse order of creation
    op.drop_table("film_promotions")
    op.drop_table("film_reviews")
    op.drop_table("ticket_services")
    op.drop_table("services")
    op.drop_table("payments")
    op.drop_table("booking_seats")
    op.drop_table("bookings")
    op.drop_table("vouchers")
    op.drop_table("payment_methods")
    op.drop_table("showtimes")
    op.drop_table("film_casts")
    op.drop_table("film_genres")
    op.drop_table("film_trailers")
    op.drop_table("films")
    op.drop_table("users")
    op.drop_table("film_formats")
    op.drop_table("casts")
    op.drop_table("genres")
    op.drop_table("seats")
    op.drop_table("seat_rows")
    op.drop_table("seat_categories")
    op.drop_table("halls")
    op.drop_table("cinemas")
    op.drop_table("cities")

    # Drop images table and enum
    # op.drop_index("idx_images_type", table_name="images")
    # op.drop_index("idx_images_created_at", table_name="images")
    # op.drop_index("idx_images_is_temp", table_name="images")
    # op.drop_index("idx_images_owner_type", table_name="images")
    op.drop_table("images")

    op.execute("DROP TYPE IF EXISTS imagetype")
    op.execute("DROP TYPE IF EXISTS accounttype")
