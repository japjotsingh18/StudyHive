from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.schema import CreateSchema, DropSchema
from studyhive.auth.domain import AuthError, PolicyAcknowledgement
from studyhive.auth.models import AuthSessionModel, UserModel
from studyhive.auth.ports import RateLimitDecision
from studyhive.auth.repository import SqlAlchemyAuthenticationRepository
from studyhive.auth.security import PasswordHasher, SessionTokenFactory
from studyhive.auth.service import AuthenticationService
from studyhive.core.config import Environment, Settings
from studyhive.db.base import Base

PRIMARY_PASSWORD = "violet orbit correct staple"  # noqa: S105 - inert test fixture
ALTERNATE_PASSWORD = "another valid secure phrase"  # noqa: S105 - inert test fixture


class AllowingRateLimiter:
    async def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        del key, limit, window_seconds
        return RateLimitDecision(is_allowed=True)


@pytest_asyncio.fixture
async def database_sessions() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    settings = Settings()
    schema = f"test_auth_{uuid4().hex}"
    admin_engine = create_async_engine(settings.database_url)
    async with admin_engine.begin() as connection:
        await connection.execute(CreateSchema(schema))
    engine: AsyncEngine = create_async_engine(
        settings.database_url,
        connect_args={"server_settings": {"search_path": schema}},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()
        async with admin_engine.begin() as connection:
            await connection.execute(DropSchema(schema, cascade=True))
        await admin_engine.dispose()


@pytest.mark.asyncio
async def test_registration_login_rotation_and_reuse_detection_use_postgresql_constraints(
    database_sessions: async_sessionmaker[AsyncSession],
) -> None:
    settings = Settings.model_validate(
        {
            "environment": Environment.TEST,
            "database_url": Settings().database_url,
            "redis_url": "redis://localhost:6379/15",
        }
    )
    tokens = SessionTokenFactory()
    service = AuthenticationService(
        SqlAlchemyAuthenticationRepository(database_sessions),
        PasswordHasher(),
        tokens,
        AllowingRateLimiter(),
        settings,
    )
    policies = (
        PolicyAcknowledgement("terms_of_service", "1"),
        PolicyAcknowledgement("privacy_policy", "1"),
    )

    registration = await service.register(
        original_email="Student@Example.edu",
        password=PRIMARY_PASSWORD,
        policy_acknowledgements=policies,
        idempotency_key="registration-attempt-1",
        request_id="req_registration",
        client_key="client-test",
    )
    duplicate = await service.register(
        original_email="student@example.edu",
        password=ALTERNATE_PASSWORD,
        policy_acknowledgements=policies,
        idempotency_key="registration-attempt-2",
        request_id="req_duplicate",
        client_key="client-test",
    )

    assert await service.authenticate_token(registration.credential.token) is not None
    assert await service.authenticate_token(duplicate.credential.token) is None
    async with database_sessions() as session:
        assert await session.scalar(select(func.count()).select_from(UserModel)) == 1

    login = await service.login(
        email="STUDENT@example.edu",
        password=PRIMARY_PASSWORD,
        remember_me=False,
        request_id="req_login",
        client_key="client-test",
    )
    refreshed = await service.refresh(
        token=login.credential.token,
        csrf_token=login.credential.csrf_token,
        request_id="req_refresh",
    )

    assert await service.authenticate_token(login.credential.token) is None
    assert await service.authenticate_token(refreshed.credential.token) is not None
    with pytest.raises(AuthError, match="no longer be refreshed") as reused:
        await service.refresh(
            token=login.credential.token,
            csrf_token=login.credential.csrf_token,
            request_id="req_reuse",
        )
    assert reused.value.code == "session_reuse_detected"
    assert await service.authenticate_token(refreshed.credential.token) is None

    async with database_sessions() as session:
        active_sessions = await session.scalar(
            select(func.count())
            .select_from(AuthSessionModel)
            .where(AuthSessionModel.revoked_at.is_(None))
        )
    assert active_sessions == 1
