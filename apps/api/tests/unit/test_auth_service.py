from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import AsyncMock, Mock

import pytest
from studyhive.auth.ports import AuthenticationRepository, RateLimitDecision
from studyhive.auth.security import PasswordHasher, SessionTokenFactory
from studyhive.auth.service import AuthenticationService
from studyhive.core.config import Environment, Settings


class AllowingRateLimiter:
    async def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        del key, limit, window_seconds
        return RateLimitDecision(is_allowed=True)


@pytest.mark.asyncio
async def test_session_authentication_applies_configured_idle_cutoff() -> None:
    repository = Mock()
    repository.authenticate_session = AsyncMock(return_value=None)
    settings = Settings.model_validate(
        {"environment": Environment.TEST, "session_idle_minutes": 45}
    )
    service = AuthenticationService(
        cast(AuthenticationRepository, repository),
        PasswordHasher(),
        SessionTokenFactory(),
        AllowingRateLimiter(),
        settings,
    )

    before = datetime.now(UTC)
    assert await service.authenticate_token("opaque session fixture") is None
    after = datetime.now(UTC)

    _, observed_now, idle_cutoff = repository.authenticate_session.await_args.args
    assert before <= observed_now <= after
    assert observed_now - idle_cutoff == timedelta(minutes=45)
