from dependency_injector import containers, providers

from src.application.use_cases.authentication.forgot_password_use_case import (
    ForgotPasswordUseCase,
)
from src.application.use_cases.authentication.sign_up_use_case import SignUpUseCase
from src.application.use_cases.banner.create_banner_use_case import (
    CreateBannerUseCase,
)
from src.application.use_cases.banner.delete_banner_use_case import (
    DeleteBannerUseCase,
)
from src.application.use_cases.banner.get_active_banners_use_case import (
    GetActiveBannersUseCase,
)
from src.application.use_cases.banner.get_banner_use_case import GetBannerUseCase
from src.application.use_cases.banner.update_banner_use_case import (
    UpdateBannerUseCase,
)
from src.application.use_cases.booking.create_booking_use_case import (
    CreateBookingUseCase,
)
from src.application.use_cases.booking.delete_booking_use_case import (
    DeleteBookingUseCase,
)
from src.application.use_cases.booking.get_all_bookings_use_case import (
    GetAllBookingsUseCase,
)
from src.application.use_cases.booking.get_booking_use_case import GetBookingUseCase
from src.application.use_cases.booking.get_user_bookings_use_case import (
    GetUserBookingsUseCase,
)
from src.application.use_cases.booking.process_vnpay_ipn_use_case import (
    ProcessVNPayIPNUseCase,
)
from src.application.use_cases.booking.process_vnpay_return_use_case import (
    ProcessVNPayReturnUseCase,
)
from src.application.use_cases.booking.update_booking_use_case import (
    UpdateBookingUseCase,
)
from src.application.use_cases.payment.create_payment_use_case import (
    CreatePaymentUseCase,
)
from src.application.use_cases.cast.create_cast_use_case import CreateCastUseCase
from src.application.use_cases.cast.delete_cast_use_case import DeleteCastUseCase
from src.application.use_cases.cast.get_cast_use_case import GetCastUseCase
from src.application.use_cases.cast.get_casts_use_case import GetCastsUseCase
from src.application.use_cases.cast.update_cast_use_case import UpdateCastUseCase
from src.application.use_cases.cinema.create_cinema_use_case import (
    CreateCinemaUseCase,
)
from src.application.use_cases.cinema.delete_cinema_use_case import (
    DeleteCinemaUseCase,
)
from src.application.use_cases.cinema.get_cinema_use_case import GetCinemaUseCase
from src.application.use_cases.cinema.get_cinemas_by_city_use_case import (
    GetCinemasByCityUseCase,
)
from src.application.use_cases.cinema.get_cinemas_use_case import GetCinemasUseCase
from src.application.use_cases.cinema.update_cinema_use_case import (
    UpdateCinemaUseCase,
)
from src.application.use_cases.film.create_film_use_case import CreateFilmUseCase
from src.application.use_cases.film.get_film_use_case import GetFilmUseCase
from src.application.use_cases.film.get_films_use_case import GetFilmsUseCase
from src.application.use_cases.film.search_films_use_case import SearchFilmsUseCase
from src.application.use_cases.film_cast.create_film_cast_use_case import (
    CreateFilmCastUseCase,
)
from src.application.use_cases.film_cast.delete_film_cast_use_case import (
    DeleteFilmCastUseCase,
)
from src.application.use_cases.film_cast.get_film_cast_use_case import (
    GetFilmCastUseCase,
)
from src.application.use_cases.film_cast.update_film_cast_use_case import (
    UpdateFilmCastUseCase,
)
from src.application.use_cases.film_format.create_film_format_use_case import (
    CreateFilmFormatUseCase,
)
from src.application.use_cases.film_format.delete_film_format_use_case import (
    DeleteFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_format_use_case import (
    GetFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_formats_use_case import (
    GetFilmFormatsUseCase,
)
from src.application.use_cases.film_format.update_film_format_use_case import (
    UpdateFilmFormatUseCase,
)
from src.application.use_cases.film_promotion.create_film_promotion_usecase import (
    CreateFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.delete_film_promotion_usecase import (
    DeleteFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotion_usecase import (
    GetFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotions_by_film_id_usecase import (
    GetFilmPromotionsByFilmIdUseCase,
)
from src.application.use_cases.film_promotion.update_film_promotion_usecase import (
    UpdateFilmPromotionUseCase,
)
from src.application.use_cases.film_review.create_film_review_use_case import (
    CreateFilmReviewUseCase,
)
from src.application.use_cases.film_review.delete_film_review_use_case import (
    DeleteFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_review_use_case import (
    GetFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_by_film_id_use_case import (
    GetFilmReviewsByFilmIdUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_use_case import (
    GetFilmReviewsUseCase,
)
from src.application.use_cases.film_review.update_film_review_use_case import (
    UpdateFilmReviewUseCase,
)
from src.application.use_cases.film_trailer.create_film_trailer_usecase import (
    CreateFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.delete_film_trailer_usecase import (
    DeleteFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.get_film_trailer_usecase import (
    GetFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.get_film_trailers_by_film_id_usecase import (
    GetFilmTrailersByFilmIdUseCase,
)
from src.application.use_cases.film_trailer.reorder_film_trailers_usecase import (
    ReorderFilmTrailersUseCase,
)
from src.application.use_cases.film_trailer.update_film_trailer_usecase import (
    UpdateFilmTrailerUseCase,
)
from src.application.use_cases.genre.create_genre_use_case import CreateGenreUseCase
from src.application.use_cases.genre.delete_genre_use_case import DeleteGenreUseCase
from src.application.use_cases.genre.get_genre_use_case import GetGenreUseCase
from src.application.use_cases.genre.get_genres_use_case import GetGenresUseCase
from src.application.use_cases.genre.get_random_genres_use_case import (
    GetRandomGenresUseCase,
)
from src.application.use_cases.genre.update_genre_use_case import UpdateGenreUseCase
from src.application.use_cases.hall.create_hall_use_case import CreateHallUseCase
from src.application.use_cases.hall.delete_hall_use_case import DeleteHallUseCase
from src.application.use_cases.hall.get_hall_use_case import GetHallUseCase
from src.application.use_cases.hall.get_halls_by_cinema_use_case import (
    GetHallsByCinemaUseCase,
)
from src.application.use_cases.hall.get_halls_use_case import GetHallsUseCase
from src.application.use_cases.hall.update_hall_use_case import UpdateHallUseCase
from src.application.use_cases.hall_layout.create_hall_layout_use_case import (
    CreateHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.get_hall_layout_use_case import (
    GetHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.update_hall_layout_use_case import (
    UpdateHallLayoutUseCase,
)
from src.application.use_cases.image.finalize_temp_image_use_case import (
    FinalizeTempImagesUseCase,
)
from src.application.use_cases.image.upload_and_associate_images_use_case import (
    UploadAndAssociateImagesUseCase,
)
from src.application.use_cases.image.upload_temp_image_use_case import (
    UploadTempImagesUseCase,
)
from src.application.use_cases.payment_method.create_payment_method_use_case import (
    CreatePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.delete_payment_method_use_case import (
    DeletePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_active_payment_methods_use_case import (
    GetActivePaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.get_payment_method_use_case import (
    GetPaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_payment_methods_use_case import (
    GetPaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.update_payment_method_use_case import (
    UpdatePaymentMethodUseCase,
)
from src.application.use_cases.seat_category.create_seat_category_use_case import (
    CreateSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.delete_seat_category_use_case import (
    DeleteSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.get_seat_categories_use_case import (
    GetSeatCategoriesUseCase,
)
from src.application.use_cases.seat_category.get_seat_category_use_case import (
    GetSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.update_seat_category_use_case import (
    UpdateSeatCategoryUseCase,
)
from src.application.use_cases.service.create_service_use_case import (
    CreateServiceUseCase,
)
from src.application.use_cases.service.delete_service_use_case import (
    DeleteServiceUseCase,
)
from src.application.use_cases.service.get_service_use_case import GetServiceUseCase
from src.application.use_cases.service.get_services_use_case import GetServicesUseCase
from src.application.use_cases.service.update_service_use_case import (
    UpdateServiceUseCase,
)
from src.application.use_cases.showtime.create_showtime_use_case import (
    CreateShowTimeUseCase,
)
from src.application.use_cases.showtime.delete_showtime_use_case import (
    DeleteShowTimeUseCase,
)
from src.application.use_cases.showtime.get_showtime_use_case import (
    GetShowTimeUseCase,
)
from src.application.use_cases.showtime.get_showtimes_by_cinema_use_case import (
    GetShowTimesByCinemaUseCase,
)
from src.application.use_cases.showtime.get_showtimes_by_film_use_case import (
    GetShowTimesByFilmUseCase,
)
from src.application.use_cases.showtime.get_showtimes_by_hall_use_case import (
    GetShowTimesByHallUseCase,
)
from src.application.use_cases.showtime.get_showtimes_use_case import (
    GetShowTimesUseCase,
)
from src.application.use_cases.showtime.update_showtime_use_case import (
    UpdateShowTimeUseCase,
)
from src.application.use_cases.user.get_user_use_case import GetUserUseCase
from src.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from src.application.use_cases.voucher.create_voucher_use_case import (
    CreateVoucherUseCase,
)
from src.application.use_cases.voucher.delete_voucher_use_case import (
    DeleteVoucherUseCase,
)
from src.application.use_cases.voucher.get_voucher_by_code_use_case import (
    GetVoucherByCodeUseCase,
)
from src.application.use_cases.voucher.get_voucher_use_case import GetVoucherUseCase
from src.application.use_cases.voucher.get_vouchers_use_case import GetVouchersUseCase
from src.application.use_cases.voucher.update_voucher_use_case import (
    UpdateVoucherUseCase,
)
from src.application.use_cases.voucher.validate_voucher_use_case import (
    ValidateVoucherUseCase,
)


class UseCaseContainer(containers.DeclarativeContainer):
    """Container for application use cases."""

    repositories = providers.DependenciesContainer()
    cloudinary = providers.DependenciesContainer()
    firebase = providers.DependenciesContainer()
    database = providers.DependenciesContainer()
    email = providers.DependenciesContainer()
    payment_gateway = providers.DependenciesContainer()
    config = providers.Dependency()

    upload_temp_images_use_case = providers.Factory(
        UploadTempImagesUseCase,
        image_repository=repositories.image_repository,
        image_service=cloudinary.cloudinary_image_service,
        sessionmaker=database.sessionmaker,
    )

    finalize_temp_images_use_case = providers.Factory(
        FinalizeTempImagesUseCase,
        image_repository=repositories.image_repository,
        image_service=cloudinary.cloudinary_image_service,
        sessionmaker=database.sessionmaker,
    )

    upload_and_associate_images_use_case = providers.Factory(
        UploadAndAssociateImagesUseCase,
        image_repository=repositories.image_repository,
        image_service=cloudinary.cloudinary_image_service,
        sessionmaker=database.sessionmaker,
    )

    get_active_banners_use_case = providers.Factory(
        GetActiveBannersUseCase,
        banner_repository=repositories.banner_repository,
        sessionmaker=database.sessionmaker,
    )

    create_banner_use_case = providers.Factory(
        CreateBannerUseCase,
        banner_repository=repositories.banner_repository,
        sessionmaker=database.sessionmaker,
    )

    get_banner_use_case = providers.Factory(
        GetBannerUseCase,
        banner_repository=repositories.banner_repository,
        sessionmaker=database.sessionmaker,
    )

    update_banner_use_case = providers.Factory(
        UpdateBannerUseCase,
        banner_repository=repositories.banner_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_banner_use_case = providers.Factory(
        DeleteBannerUseCase,
        banner_repository=repositories.banner_repository,
        sessionmaker=database.sessionmaker,
    )

    sign_up_use_case = providers.Factory(
        SignUpUseCase,
        auth_service=firebase.firebase_auth_service,
        user_repository=repositories.user_repository,
        sessionmaker=database.sessionmaker,
    )

    forgot_password_use_case = providers.Factory(
        ForgotPasswordUseCase,
        email_service=email.email_service,
        auth_service=firebase.firebase_auth_service,
        config=config,
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_repository=repositories.user_repository,
        sessionmaker=database.sessionmaker,
    )

    get_user_use_case = providers.Factory(
        GetUserUseCase,
        user_repository=repositories.user_repository,
        sessionmaker=database.sessionmaker,
    )

    create_genre_use_case = providers.Factory(
        CreateGenreUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_genre_use_case = providers.Factory(
        DeleteGenreUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    get_genre_use_case = providers.Factory(
        GetGenreUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    get_genres_use_case = providers.Factory(
        GetGenresUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    get_random_genres_use_case = providers.Factory(
        GetRandomGenresUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    update_genre_use_case = providers.Factory(
        UpdateGenreUseCase,
        genre_repository=repositories.genre_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_format_use_case = providers.Factory(
        CreateFilmFormatUseCase,
        film_format_repository=repositories.film_format_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_film_format_use_case = providers.Factory(
        DeleteFilmFormatUseCase,
        film_format_repository=repositories.film_format_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_format_use_case = providers.Factory(
        GetFilmFormatUseCase,
        film_format_repository=repositories.film_format_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_formats_use_case = providers.Factory(
        GetFilmFormatsUseCase,
        film_format_repository=repositories.film_format_repository,
        sessionmaker=database.sessionmaker,
    )

    update_film_format_use_case = providers.Factory(
        UpdateFilmFormatUseCase,
        film_format_repository=repositories.film_format_repository,
        sessionmaker=database.sessionmaker,
    )

    create_cast_use_case = providers.Factory(
        CreateCastUseCase,
        cast_repository=repositories.cast_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_cast_use_case = providers.Factory(
        DeleteCastUseCase,
        cast_repository=repositories.cast_repository,
        sessionmaker=database.sessionmaker,
    )

    get_cast_use_case = providers.Factory(
        GetCastUseCase,
        cast_repository=repositories.cast_repository,
        sessionmaker=database.sessionmaker,
    )

    get_casts_use_case = providers.Factory(
        GetCastsUseCase,
        cast_repository=repositories.cast_repository,
        sessionmaker=database.sessionmaker,
    )

    update_cast_use_case = providers.Factory(
        UpdateCastUseCase,
        cast_repository=repositories.cast_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_promotion_use_case = providers.Factory(
        CreateFilmPromotionUseCase,
        film_promotion_repository=repositories.film_promotion_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_film_promotion_use_case = providers.Factory(
        DeleteFilmPromotionUseCase,
        film_promotion_repository=repositories.film_promotion_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_promotion_use_case = providers.Factory(
        GetFilmPromotionUseCase,
        film_promotion_repository=repositories.film_promotion_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_promotion_by_film_in_use_case = providers.Factory(
        GetFilmPromotionsByFilmIdUseCase,
        film_promotion_repository=repositories.film_promotion_repository,
        sessionmaker=database.sessionmaker,
    )

    update_film_promotion_use_case = providers.Factory(
        UpdateFilmPromotionUseCase,
        film_promotion_repository=repositories.film_promotion_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_trailer_use_case = providers.Factory(
        CreateFilmTrailerUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_film_trailer_use_case = providers.Factory(
        DeleteFilmTrailerUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_trailer_use_case = providers.Factory(
        GetFilmTrailerUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_trailers_by_film_id_use_case = providers.Factory(
        GetFilmTrailersByFilmIdUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    update_film_trailer_use_case = providers.Factory(
        UpdateFilmTrailerUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    reorder_film_trailers_use_case = providers.Factory(
        ReorderFilmTrailersUseCase,
        film_trailer_repository=repositories.film_trailer_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_cast_use_case = providers.Factory(
        CreateFilmCastUseCase,
        film_cast_repository=repositories.film_cast_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_cast_use_case = providers.Factory(
        GetFilmCastUseCase,
        film_cast_repository=repositories.film_cast_repository,
        sessionmaker=database.sessionmaker,
    )

    update_film_cast_use_case = providers.Factory(
        UpdateFilmCastUseCase,
        film_cast_repository=repositories.film_cast_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_film_cast_use_case = providers.Factory(
        DeleteFilmCastUseCase,
        film_cast_repository=repositories.film_cast_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_use_case = providers.Factory(
        CreateFilmUseCase,
        film_cast_repository=repositories.film_cast_repository,
        film_genre_repository=repositories.film_genre_repository,
        film_promotion_repository=repositories.film_promotion_repository,
        film_trailer_repository=repositories.film_trailer_repository,
        film_repository=repositories.film_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_use_case = providers.Factory(
        GetFilmUseCase,
        film_repository=repositories.film_repository,
        sessionmaker=database.sessionmaker,
    )
    get_films_use_case = providers.Factory(
        GetFilmsUseCase,
        film_repository=repositories.film_repository,
        sessionmaker=database.sessionmaker,
    )

    search_films_use_case = providers.Factory(
        SearchFilmsUseCase,
        film_repository=repositories.film_repository,
        sessionmaker=database.sessionmaker,
    )

    create_film_review_use_case = providers.Factory(
        CreateFilmReviewUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_review_use_case = providers.Factory(
        GetFilmReviewUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_reviews_use_case = providers.Factory(
        GetFilmReviewsUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )

    get_film_reviews_by_film_id_use_case = providers.Factory(
        GetFilmReviewsByFilmIdUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )

    update_film_review_use_case = providers.Factory(
        UpdateFilmReviewUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )
    create_voucher_use_case = providers.Factory(
        CreateVoucherUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    get_voucher_use_case = providers.Factory(
        GetVoucherUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    get_voucher_by_code_use_case = providers.Factory(
        GetVoucherByCodeUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    get_vouchers_use_case = providers.Factory(
        GetVouchersUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    update_voucher_use_case = providers.Factory(
        UpdateVoucherUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_voucher_use_case = providers.Factory(
        DeleteVoucherUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    validate_voucher_use_case = providers.Factory(
        ValidateVoucherUseCase,
        voucher_repository=repositories.voucher_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_film_review_use_case = providers.Factory(
        DeleteFilmReviewUseCase,
        film_review_repository=repositories.film_review_repository,
        sessionmaker=database.sessionmaker,
    )

    create_cinema_use_case = providers.Factory(
        CreateCinemaUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    get_cinema_use_case = providers.Factory(
        GetCinemaUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    get_cinemas_use_case = providers.Factory(
        GetCinemasUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    get_cinemas_by_city_use_case = providers.Factory(
        GetCinemasByCityUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    update_cinema_use_case = providers.Factory(
        UpdateCinemaUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_cinema_use_case = providers.Factory(
        DeleteCinemaUseCase,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    create_hall_use_case = providers.Factory(
        CreateHallUseCase,
        hall_repository=repositories.hall_repository,
        cinema_repository=repositories.cinema_repository,
        sessionmaker=database.sessionmaker,
    )

    get_hall_use_case = providers.Factory(
        GetHallUseCase,
        hall_repository=repositories.hall_repository,
        sessionmaker=database.sessionmaker,
    )

    get_halls_use_case = providers.Factory(
        GetHallsUseCase,
        hall_repository=repositories.hall_repository,
        sessionmaker=database.sessionmaker,
    )

    create_hall_layout_use_case = providers.Factory(
        CreateHallLayoutUseCase,
        hall_repository=repositories.hall_repository,
        seat_row_repository=repositories.seat_row_repository,
        seat_repository=repositories.seat_repository,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    update_hall_layout_use_case = providers.Factory(
        UpdateHallLayoutUseCase,
        hall_repository=repositories.hall_repository,
        seat_row_repository=repositories.seat_row_repository,
        seat_repository=repositories.seat_repository,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    get_hall_layout_use_case = providers.Factory(
        GetHallLayoutUseCase,
        hall_repository=repositories.hall_repository,
        seat_row_repository=repositories.seat_row_repository,
        seat_repository=repositories.seat_repository,
        sessionmaker=database.sessionmaker,
    )

    get_halls_by_cinema_use_case = providers.Factory(
        GetHallsByCinemaUseCase,
        hall_repository=repositories.hall_repository,
        sessionmaker=database.sessionmaker,
    )

    update_hall_use_case = providers.Factory(
        UpdateHallUseCase,
        hall_repository=repositories.hall_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_hall_use_case = providers.Factory(
        DeleteHallUseCase,
        hall_repository=repositories.hall_repository,
        sessionmaker=database.sessionmaker,
    )

    create_seat_category_use_case = providers.Factory(
        CreateSeatCategoryUseCase,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    get_seat_category_use_case = providers.Factory(
        GetSeatCategoryUseCase,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    get_seat_categories_use_case = providers.Factory(
        GetSeatCategoriesUseCase,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    update_seat_category_use_case = providers.Factory(
        UpdateSeatCategoryUseCase,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_seat_category_use_case = providers.Factory(
        DeleteSeatCategoryUseCase,
        seat_category_repository=repositories.seat_category_repository,
        sessionmaker=database.sessionmaker,
    )

    create_service_use_case = providers.Factory(
        CreateServiceUseCase,
        service_repository=repositories.service_repository,
        sessionmaker=database.sessionmaker,
    )

    get_service_use_case = providers.Factory(
        GetServiceUseCase,
        service_repository=repositories.service_repository,
        sessionmaker=database.sessionmaker,
    )

    get_services_use_case = providers.Factory(
        GetServicesUseCase,
        service_repository=repositories.service_repository,
        sessionmaker=database.sessionmaker,
    )

    update_service_use_case = providers.Factory(
        UpdateServiceUseCase,
        service_repository=repositories.service_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_service_use_case = providers.Factory(
        DeleteServiceUseCase,
        service_repository=repositories.service_repository,
        sessionmaker=database.sessionmaker,
    )

    create_showtime_use_case = providers.Factory(
        CreateShowTimeUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    get_showtime_use_case = providers.Factory(
        GetShowTimeUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    get_showtimes_use_case = providers.Factory(
        GetShowTimesUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    get_showtimes_by_film_use_case = providers.Factory(
        GetShowTimesByFilmUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    get_showtimes_by_hall_use_case = providers.Factory(
        GetShowTimesByHallUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    get_showtimes_by_cinema_use_case = providers.Factory(
        GetShowTimesByCinemaUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    update_showtime_use_case = providers.Factory(
        UpdateShowTimeUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_showtime_use_case = providers.Factory(
        DeleteShowTimeUseCase,
        showtime_repository=repositories.showtime_repository,
        sessionmaker=database.sessionmaker,
    )

    create_booking_use_case = providers.Factory(
        CreateBookingUseCase,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        showtime_repository=repositories.showtime_repository,
        seat_repository=repositories.seat_repository,
        sessionmaker=database.sessionmaker,
    )

    get_booking_use_case = providers.Factory(
        GetBookingUseCase,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        sessionmaker=database.sessionmaker,
    )

    update_booking_use_case = providers.Factory(
        UpdateBookingUseCase,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_booking_use_case = providers.Factory(
        DeleteBookingUseCase,
        booking_repository=repositories.booking_repository,
        sessionmaker=database.sessionmaker,
    )

    get_all_bookings_use_case = providers.Factory(
        GetAllBookingsUseCase,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        sessionmaker=database.sessionmaker,
    )

    get_user_bookings_use_case = providers.Factory(
        GetUserBookingsUseCase,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        sessionmaker=database.sessionmaker,
    )

    process_vnpay_return_use_case = providers.Factory(
        ProcessVNPayReturnUseCase,
        payment_gateway=payment_gateway.vnpay_gateway,
        booking_repository=repositories.booking_repository,
        sessionmaker=database.sessionmaker,
    )

    process_vnpay_ipn_use_case = providers.Factory(
        ProcessVNPayIPNUseCase,
        payment_gateway=payment_gateway.vnpay_gateway,
        payment_repository=repositories.payment_repository,
        booking_repository=repositories.booking_repository,
        booking_seat_repository=repositories.booking_seat_repository,
        sessionmaker=database.sessionmaker,
    )

    create_payment_use_case = providers.Factory(
        CreatePaymentUseCase,
        payment_repository=repositories.payment_repository,
        booking_repository=repositories.booking_repository,
        payment_gateway=payment_gateway.vnpay_gateway,
        sessionmaker=database.sessionmaker,
    )

    create_payment_method_use_case = providers.Factory(
        CreatePaymentMethodUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )

    get_payment_method_use_case = providers.Factory(
        GetPaymentMethodUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )

    get_payment_methods_use_case = providers.Factory(
        GetPaymentMethodsUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )

    get_active_payment_methods_use_case = providers.Factory(
        GetActivePaymentMethodsUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )

    update_payment_method_use_case = providers.Factory(
        UpdatePaymentMethodUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )

    delete_payment_method_use_case = providers.Factory(
        DeletePaymentMethodUseCase,
        payment_method_repository=repositories.payment_method_repository,
        sessionmaker=database.sessionmaker,
    )
