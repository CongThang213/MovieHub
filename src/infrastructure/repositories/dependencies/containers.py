from dependency_injector import containers, providers

from src.infrastructure.repositories.banner_repository_impl import BannerRepositoryImpl
from src.infrastructure.repositories.booking_repository_impl import (
    BookingRepositoryImpl,
)
from src.infrastructure.repositories.booking_seat_repository_impl import (
    BookingSeatRepositoryImpl,
)
from src.infrastructure.repositories.cast_repository_impl import CastRepositoryImpl
from src.infrastructure.repositories.cinema_repository_impl import (
    CinemaRepositoryImpl,
)
from src.infrastructure.repositories.film_cast_repository_impl import (
    FilmCastRepositoryImpl,
)
from src.infrastructure.repositories.film_format_repository_impl import (
    FilmFormatRepositoryImpl,
)
from src.infrastructure.repositories.film_genre_repository_impl import (
    FilmGenreRepositoryImpl,
)
from src.infrastructure.repositories.film_promotion_repository_impl import (
    FilmPromotionRepositoryImpl,
)
from src.infrastructure.repositories.film_repository_impl import FilmRepositoryImpl
from src.infrastructure.repositories.film_review_repository_impl import (
    FilmReviewRepositoryImpl,
)
from src.infrastructure.repositories.film_trailer_repository_impl import (
    FilmTrailerRepositoryImpl,
)
from src.infrastructure.repositories.genre_repository_impl import GenreRepositoryImpl
from src.infrastructure.repositories.hall_repository_impl import HallRepositoryImpl
from src.infrastructure.repositories.image_repository_impl import ImageRepositoryImpl
from src.infrastructure.repositories.payment_repository_impl import (
    PaymentRepositoryImpl,
)
from src.infrastructure.repositories.payment_method_repository_impl import (
    PaymentMethodRepositoryImpl,
)
from src.infrastructure.repositories.seat_category_repository_impl import (
    SeatCategoryRepositoryImpl,
)
from src.infrastructure.repositories.seat_repository_impl import SeatRepositoryImpl
from src.infrastructure.repositories.seat_row_repository_impl import (
    SeatRowRepositoryImpl,
)
from src.infrastructure.repositories.service_repository_impl import (
    ServiceRepositoryImpl,
)
from src.infrastructure.repositories.showtime_repository_impl import (
    ShowTimeRepositoryImpl,
)
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.repositories.voucher_repository_impl import (
    VoucherRepositoryImpl,
)


class RepositoryContainer(containers.DeclarativeContainer):
    """Repository container for dependency injection."""

    database = providers.Dependency()

    user_repository = providers.Factory(
        UserRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    banner_repository = providers.Factory(BannerRepositoryImpl)

    image_repository = providers.Factory(
        ImageRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    genre_repository = providers.Factory(
        GenreRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    film_format_repository = providers.Factory(
        FilmFormatRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    cast_repository = providers.Factory(CastRepositoryImpl)

    film_genre_repository = providers.Factory(FilmGenreRepositoryImpl)

    film_review_repository = providers.Factory(FilmReviewRepositoryImpl)

    film_repository = providers.Factory(FilmRepositoryImpl)

    film_promotion_repository = providers.Factory(FilmPromotionRepositoryImpl)

    showtime_repository = providers.Factory(ShowTimeRepositoryImpl)
    film_trailer_repository = providers.Factory(FilmTrailerRepositoryImpl)

    film_cast_repository = providers.Factory(FilmCastRepositoryImpl)
    showtime_repository = providers.Factory(ShowTimeRepositoryImpl)

    seat_repository = providers.Factory(SeatRepositoryImpl)
    voucher_repository = providers.Factory(VoucherRepositoryImpl)
    showtime_repository = providers.Factory(ShowTimeRepositoryImpl)
    seat_category_repository = providers.Factory(SeatCategoryRepositoryImpl)
    seat_row_repository = providers.Factory(SeatRowRepositoryImpl)
    service_repository = providers.Factory(ServiceRepositoryImpl)

    cinema_repository = providers.Factory(CinemaRepositoryImpl)
    hall_repository = providers.Factory(HallRepositoryImpl)
    showtime_repository = providers.Factory(ShowTimeRepositoryImpl)

    booking_repository = providers.Factory(
        BookingRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    booking_seat_repository = providers.Factory(
        BookingSeatRepositoryImpl,
        sessionmaker=database.provided.sessionmaker,
    )

    payment_repository = providers.Factory(PaymentRepositoryImpl)

    payment_method_repository = providers.Factory(PaymentMethodRepositoryImpl)
