"""Redis-backed authentication abuse controls with conservative local fallback."""

import asyncio
import logging
import time
from dataclasses import dataclass

from redis.asyncio import Redis
from redis.exceptions import RedisError

from studyhive.auth.ports import RateLimitDecision

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class _LocalWindow:
    count: int
    expires_at: float


class RedisRateLimiter:
    """Bound counters across replicas while remaining safe during Redis degradation."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self._local_windows: dict[str, _LocalWindow] = {}
        self._local_lock = asyncio.Lock()

    async def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        """Increment one fixed window and return safe retry guidance."""

        redis_key = f"studyhive:auth-limit:{key}"
        try:
            count = await self._redis.incr(redis_key)
            if count == 1:
                await self._redis.expire(redis_key, window_seconds)
            ttl = await self._redis.ttl(redis_key)
            return RateLimitDecision(count <= limit, max(ttl, 1) if count > limit else None)
        except (OSError, RedisError):
            logger.warning(
                "authentication rate limiter using local fallback",
                extra={"event_key": "auth.rate_limit_fallback"},
            )
            return await self._check_local(key, limit, window_seconds)

    async def _check_local(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        now = time.monotonic()
        async with self._local_lock:
            window = self._local_windows.get(key)
            if window is None or window.expires_at <= now:
                window = _LocalWindow(count=0, expires_at=now + window_seconds)
                self._local_windows[key] = window
            window.count += 1
            is_allowed = window.count <= limit
            retry_after = max(int(window.expires_at - now), 1) if not is_allowed else None
            return RateLimitDecision(is_allowed, retry_after)
