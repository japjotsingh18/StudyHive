"""Infrastructure health endpoints used by operators and containers."""

from typing import Literal

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from studyhive import __version__

router = APIRouter(prefix="/health", tags=["infrastructure"])


class LivenessResponse(BaseModel):
    """Process liveness contract."""

    status: Literal["ok"]
    service: Literal["studyhive-api"]
    version: str


class ReadinessResponse(BaseModel):
    """Dependency readiness contract."""

    status: Literal["ready", "not_ready"]
    database: Literal["up", "down"]
    redis: Literal["up", "down"]


@router.get("/live", response_model=LivenessResponse)
def liveness() -> LivenessResponse:
    """Report whether the API process can serve requests."""

    return LivenessResponse(status="ok", service="studyhive-api", version=__version__)


@router.get("/ready", response_model=ReadinessResponse)
async def readiness(request: Request) -> ReadinessResponse | JSONResponse:
    """Report PostgreSQL and Redis connectivity without exposing configuration."""

    engine: AsyncEngine = request.app.state.database_engine
    redis: Redis = request.app.state.redis
    database_status: Literal["up", "down"] = "down"
    redis_status: Literal["up", "down"] = "down"

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        database_status = "up"
    except (OSError, SQLAlchemyError):
        pass

    try:
        if await redis.ping():
            redis_status = "up"
    except (OSError, RedisError):
        pass

    readiness_status: Literal["ready", "not_ready"] = (
        "ready" if database_status == redis_status == "up" else "not_ready"
    )
    response = ReadinessResponse(
        status=readiness_status,
        database=database_status,
        redis=redis_status,
    )
    if readiness_status == "not_ready":
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return response
