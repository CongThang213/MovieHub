from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config.logging_config import logger
from src.containers import AppContainer
from src.domain.enums.account_type import AccountType
from src.domain.exceptions.app_exception import AppException
from src.interface.endpoints.exception_handler import (
    app_exception_handler,
    validation_exception_handler,
)
from src.interface.endpoints.middleware.auth_middleware import AuthMiddleware
from src.interface.endpoints.routes.auth import router as auth_router
from src.interface.endpoints.routes.banner import router as banner_router
from src.interface.endpoints.routes.booking import router as booking_router
from src.interface.endpoints.routes.cinema import router as cinema_router
from src.interface.endpoints.routes.film import router as film_router
from src.interface.endpoints.routes.film_format import router as film_format_router
from src.interface.endpoints.routes.film_promotion import (
    router as film_promotion_router,
)
from src.interface.endpoints.routes.film_review import router as film_review_router
from src.interface.endpoints.routes.genre import router as genre_router
from src.interface.endpoints.routes.hall import router as hall_router
from src.interface.endpoints.routes.image import router as image_router
from src.interface.endpoints.routes.payment import router as payment_router
from src.interface.endpoints.routes.payment_method import (
    router as payment_method_router,
)
from src.interface.endpoints.routes.seat_booking import router as seat_booking_router
from src.interface.endpoints.routes.seat_category import router as seat_category_router
from src.interface.endpoints.routes.service import router as service_router
from src.interface.endpoints.routes.showtime import router as showtime_router
from src.interface.endpoints.routes.user import router as user_router
from src.interface.endpoints.routes.voucher import router as voucher_router
from src.interface.endpoints.routes.websocket import router as websocket_router

# Create and configure the dependency injection container
container = AppContainer()

# Wire container resources with endpoints
container.wire(
    modules=[
        "src.interface.endpoints.routes.auth",
        "src.interface.endpoints.routes.user",
        "src.interface.endpoints.routes.image",
        "src.interface.endpoints.routes.genre",
        "src.interface.endpoints.routes.film_format",
        "src.interface.endpoints.routes.cast",
        "src.interface.endpoints.routes.hall",
        "src.interface.endpoints.routes.service",
        "src.interface.endpoints.routes.seat_category",
        "src.interface.endpoints.routes.cinema",
        "src.interface.endpoints.routes.film_promotion",
        "src.interface.endpoints.routes.film_review",
        "src.interface.endpoints.routes.voucher",
        "src.interface.endpoints.dependencies.auth_dependencies",
        "src.interface.endpoints.dependencies.user_dependencies",
        "src.interface.endpoints.dependencies.image_dependencies",
        "src.interface.endpoints.dependencies.genre_dependencies",
        "src.interface.endpoints.dependencies.film_format_dependencies",
        "src.interface.endpoints.dependencies.service_dependencies",
        "src.interface.endpoints.dependencies.hall_dependencies",
        "src.interface.endpoints.dependencies.seat_category_dependencies",
        "src.interface.endpoints.dependencies.cinema_dependencies",
        "src.interface.endpoints.dependencies.cinema_dependencies",
        "src.interface.endpoints.dependencies.film_dependencies",
        "src.interface.endpoints.dependencies.film_promotion_dependencies",
        "src.interface.endpoints.dependencies.voucher_dependencies",
        "src.interface.endpoints.dependencies.film_review_dependencies",
        "src.interface.endpoints.routes.showtime",
        "src.interface.endpoints.dependencies.showtime_dependencies",
        "src.interface.endpoints.routes.booking",
        "src.interface.endpoints.dependencies.booking_dependencies",
        "src.interface.endpoints.routes.payment",
        "src.interface.endpoints.routes.payment_method",
        "src.interface.endpoints.dependencies.payment_method_dependencies",
        "src.interface.endpoints.routes.banner",
        "src.interface.endpoints.dependencies.banner_dependencies",
        "src.interface.endpoints.routes.websocket",
        "src.interface.endpoints.routes.seat_booking",
    ]
)


# noinspection PyShadowingNames
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting application...")

        # Startup: Initialize Firebase Admin SDK
        logger.info("Initializing Firebase Admin SDK")
        container.firebase.firebase_app()

        # Startup: Initialize Cloudinary SDK
        logger.info("Initializing Cloudinary SDK")
        container.cloudinary.cloudinary_app()

        # Startup: Initialize Redis connection
        logger.info("Initializing Redis connection")
        redis_service = container.redis.redis_service()
        await redis_service.connect()

        ### FIREBASE TOKEN GENERATION ###
        try:
            from firebase_admin import auth

            admin_email = "admin@seatsync.com"
            admin_user = auth.get_user_by_email(admin_email)
            auth.set_custom_user_claims(
                admin_user.uid, {"account_type": AccountType.ADMIN}
            )
            logger.info(
                f"Set custom claim 'account_type: ADMIN' for user {admin_email}"
            )
        except Exception as e:
            logger.error(f"Failed to set custom claim for admin user: {e}")

        try:
            # Instead of custom token, use sign in with email/password
            resp = requests.post(
                "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyC2dUIigOCMmmW8ZwJ7uVcKwB9LhHeGgBo",
                json={
                    "email": "admin@seatsync.com",
                    "password": "admin123",
                    "returnSecureToken": True,
                },
            )

            response_json = resp.json()
            id_token = response_json.get("idToken")
            if id_token:
                print(f"Bearer {id_token}")
            else:
                logger.error(f"Missing idToken in response: {response_json}")
        except Exception as e:
            logger.error(f"Error during Firebase authentication: {e}")
        ### END FIREBASE TOKEN GENERATION ###

        # Store container in app instance for access in routes
        app.container = container

        logger.success("Application startup complete!")
        yield

        # Shutdown
        logger.info("Shutting down application...")

        # Disconnect Redis
        redis_service = container.redis.redis_service()
        await redis_service.disconnect()

        engine = container.database_settings.engine()  # Dispose engine connections
        await engine.dispose()

        logger.info("Application shutdown complete")

    except Exception as e:
        logger.error(f"Error during application lifecycle: {e}")
        raise


app = FastAPI(
    lifespan=lifespan,
    title=container.config().project.name,
    version=container.config().project.version,
)

# Add the authentication middleware BEFORE registering routes
# This ensures all requests go through authentication first
auth_service = container.firebase.firebase_auth_service()
app.add_middleware(AuthMiddleware, auth_service=auth_service)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Register routers
app.include_router(auth_router)
app.include_router(banner_router)
app.include_router(user_router)
app.include_router(image_router)
app.include_router(service_router)
app.include_router(genre_router)
app.include_router(hall_router)
app.include_router(seat_category_router)
app.include_router(film_format_router)
app.include_router(cinema_router)
app.include_router(film_router)
app.include_router(film_promotion_router)
app.include_router(showtime_router)
app.include_router(websocket_router)
app.include_router(seat_booking_router)
app.include_router(film_review_router)
app.include_router(voucher_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(payment_method_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the SeatSync API. See /docs for API documentation."}
