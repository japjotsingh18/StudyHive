import asyncio
import os
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from sqlalchemy import inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from studyhive.core.config import Settings

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
ALEMBIC_CONFIG = REPOSITORY_ROOT / "apps/api/alembic.ini"


async def _create_database(database_name: str, base_url: str) -> None:
    admin_url = make_url(base_url).set(database="postgres")
    engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as connection:
        await connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    await engine.dispose()


async def _drop_database(database_name: str, base_url: str) -> None:
    admin_url = make_url(base_url).set(database="postgres")
    engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as connection:
        await connection.execute(
            text(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = :database_name AND pid <> pg_backend_pid()"
            ),
            {"database_name": database_name},
        )
        await connection.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))
    await engine.dispose()


@contextmanager
def migrated_database() -> Iterator[str]:
    base_url = Settings().database_url
    database_name = f"test_migration_{uuid4().hex}"
    database_url = (
        make_url(base_url).set(database=database_name).render_as_string(hide_password=False)
    )
    asyncio.run(_create_database(database_name, base_url))
    try:
        yield database_url
    finally:
        asyncio.run(_drop_database(database_name, base_url))


def _alembic(database_url: str, *arguments: str) -> None:
    environment = os.environ.copy()
    environment["STUDYHIVE_ENVIRONMENT"] = "test"
    environment["STUDYHIVE_DATABASE_URL"] = database_url
    subprocess.run(  # noqa: S603 - fixed interpreter and repository-owned Alembic arguments
        [sys.executable, "-m", "alembic", "-c", str(ALEMBIC_CONFIG), *arguments],
        cwd=REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


async def _table_names(database_url: str) -> set[str]:
    engine = create_async_engine(database_url)
    async with engine.connect() as connection:
        names = await connection.run_sync(lambda sync: set(inspect(sync).get_table_names()))
    await engine.dispose()
    return names


async def _seed_sprint_one(database_url: str) -> None:
    engine = create_async_engine(database_url)
    async with engine.begin() as connection:
        await connection.execute(
            text(
                "INSERT INTO users "
                "(id, public_id, status, locale, timezone, version, created_at, updated_at) "
                "VALUES (:id, :public_id, 'pending', 'en-US', 'UTC', 1, now(), now())"
            ),
            {"id": uuid4(), "public_id": f"usr_{uuid4().hex}"},
        )
        user_id = await connection.scalar(text("SELECT id FROM users LIMIT 1"))
        await connection.execute(
            text(
                "INSERT INTO user_consents "
                "(id, user_id, policy_key, policy_version, decision, occurred_at, surface) "
                "VALUES (:id, :user_id, 'privacy_policy', '1', 'grant', now(), 'registration')"
            ),
            {"id": uuid4(), "user_id": user_id},
        )
    await engine.dispose()


async def _consent_generation(database_url: str) -> int:
    engine = create_async_engine(database_url)
    async with engine.connect() as connection:
        generation = await connection.scalar(
            text("SELECT event_generation FROM user_consents LIMIT 1")
        )
    await engine.dispose()
    assert isinstance(generation, int)
    return generation


def test_empty_database_upgrades_to_sprint_two_head_without_drift() -> None:
    with migrated_database() as database_url:
        _alembic(database_url, "upgrade", "head")
        assert {
            "profiles",
            "profile_field_visibilities",
            "study_preferences",
            "study_preference_values",
            "availability_blocks",
            "user_languages",
            "user_blocks",
        } <= asyncio.run(_table_names(database_url))
        _alembic(database_url, "check")


def test_sprint_one_data_upgrades_and_rolls_forward_again() -> None:
    with migrated_database() as database_url:
        _alembic(database_url, "upgrade", "20260806_0001")
        asyncio.run(_seed_sprint_one(database_url))
        _alembic(database_url, "upgrade", "head")
        assert asyncio.run(_consent_generation(database_url)) == 1

        _alembic(database_url, "downgrade", "20260806_0001")
        _alembic(database_url, "upgrade", "head")
        assert asyncio.run(_consent_generation(database_url)) == 1
