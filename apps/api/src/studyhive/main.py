"""FastAPI composition root for the StudyHive backend release."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from studyhive import __version__
from studyhive.auth.api import (
    AuthenticationMiddleware,
    AuthorizationMiddleware,
    install_auth_error_handlers,
)
from studyhive.auth.api import (
    router as auth_router,
)
from studyhive.auth.rate_limit import RedisRateLimiter
from studyhive.auth.repository import SqlAlchemyAuthenticationRepository
from studyhive.auth.security import PasswordHasher, SessionTokenFactory
from studyhive.auth.service import AuthenticationService
from studyhive.core.config import get_settings
from studyhive.core.health import router as health_router
from studyhive.db import create_database_engine, create_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Own process-scoped dependency construction and cooperative shutdown."""

    settings = get_settings()
    app.state.database_engine = create_database_engine(settings.database_url)
    app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
    app.state.settings = settings
    app.state.authentication_service = AuthenticationService(
        SqlAlchemyAuthenticationRepository(create_session_factory(app.state.database_engine)),
        PasswordHasher(),
        SessionTokenFactory(),
        RedisRateLimiter(app.state.redis),
        settings,
    )
    yield
    await app.state.redis.aclose()
    await app.state.database_engine.dispose()


def create_app() -> FastAPI:
    """Build the FastAPI application without connecting at import time."""

    application = FastAPI(
        title="StudyHive API",
        summary="Authoritative API for StudyHive academic collaboration.",
        version=__version__,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
        lifespan=lifespan,
    )
    settings = get_settings()
    application.state.settings = settings
    application.add_middleware(AuthorizationMiddleware, settings=settings)
    application.add_middleware(AuthenticationMiddleware, settings=settings)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.web_origin],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Idempotency-Key", "X-CSRF-Token", "X-Request-ID"],
    )
    install_auth_error_handlers(application)
    application.include_router(health_router)
    application.include_router(auth_router)
    return application


app = create_app()
