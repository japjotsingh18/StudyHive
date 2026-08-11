from collections.abc import AsyncIterator, Callable
from datetime import UTC, date, datetime, time
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy import inspect, select
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import selectinload
from sqlalchemy.schema import CreateSchema, DropSchema
from studyhive.auth.models import UserModel
from studyhive.core.config import Settings
from studyhive.db.base import Base
from studyhive.profiles.models import (
    AvailabilityBlockModel,
    ProfileFieldVisibilityModel,
    ProfileModel,
    StudyPreferenceModel,
    StudyPreferenceValueModel,
    UserBlockModel,
    UserConsentModel,
    UserLanguageModel,
)


@pytest_asyncio.fixture
async def profile_sessions() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    settings = Settings()
    schema = f"test_profiles_{uuid4().hex}"
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


def _user(now: datetime) -> UserModel:
    return UserModel(
        public_id=f"usr_{uuid4().hex}",
        status="pending",
        locale="en-US",
        timezone="America/Phoenix",
        version=1,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_profile_relationships_persist_normalized_foundation(
    profile_sessions: async_sessionmaker[AsyncSession],
) -> None:
    now = datetime.now(UTC)
    owner = _user(now)
    blocked = _user(now)
    profile = ProfileModel(
        user=owner,
        display_name="Student Name",
        major="Computer Science",
        graduation_year=2028,
        bio="Interested in study groups.",
        discoverability="university",
        version=1,
        created_at=now,
        updated_at=now,
        field_visibilities=[
            ProfileFieldVisibilityModel(
                field_key="graduation_year",
                visibility="private",
                created_at=now,
            )
        ],
    )
    preferences = StudyPreferenceModel(
        user=owner,
        study_pace="balanced",
        preferred_session_length="one_hour",
        modality="either",
        interaction="minimal_speaking",
        matching_enabled=True,
        version=1,
        created_at=now,
        updated_at=now,
        values=[
            StudyPreferenceValueModel(
                category="study_style", value="quiet_study", position=0, created_at=now
            ),
            StudyPreferenceValueModel(
                category="learning_method",
                value="practice_problems",
                position=0,
                created_at=now,
            ),
        ],
        availability_blocks=[
            AvailabilityBlockModel(
                weekday=1,
                local_start=time(9, 0),
                local_end=time(10, 30),
                timezone="America/Phoenix",
                effective_start_date=date(2026, 8, 11),
                created_at=now,
            )
        ],
    )
    owner.languages.append(
        UserLanguageModel(
            normalized_language="english",
            display_label="English",
            position=0,
            created_at=now,
        )
    )
    owner.consent_events.append(
        UserConsentModel(
            policy_key="matching_preferences",
            policy_version="1",
            event_generation=1,
            decision="grant",
            occurred_at=now,
            surface="profile_onboarding",
        )
    )
    owner.blocks_created.append(UserBlockModel(blocked=blocked, active=True, created_at=now))

    async with profile_sessions.begin() as session:
        session.add_all([owner, blocked, profile, preferences])

    async with profile_sessions() as session:
        stored = await session.scalar(
            select(UserModel)
            .where(UserModel.id == owner.id)
            .options(
                selectinload(UserModel.profile).selectinload(ProfileModel.field_visibilities),
                selectinload(UserModel.study_preference).selectinload(StudyPreferenceModel.values),
                selectinload(UserModel.study_preference).selectinload(
                    StudyPreferenceModel.availability_blocks
                ),
                selectinload(UserModel.languages),
                selectinload(UserModel.consent_events),
                selectinload(UserModel.blocks_created),
            )
        )

    assert stored is not None
    assert stored.profile is not None
    assert stored.profile.display_name == "Student Name"
    assert stored.profile.field_visibilities[0].visibility == "private"
    assert stored.study_preference is not None
    assert {value.value for value in stored.study_preference.values} == {
        "quiet_study",
        "practice_problems",
    }
    assert stored.study_preference.availability_blocks[0].timezone == "America/Phoenix"
    assert stored.languages[0].normalized_language == "english"
    assert stored.consent_events[0].event_generation == 1
    assert stored.blocks_created[0].blocked_user_id == blocked.id


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("model_factory", "expected_constraint"),
    [
        (
            lambda preference_id, now: AvailabilityBlockModel(
                study_preference_id=preference_id,
                weekday=7,
                local_start=time(9, 0),
                local_end=time(10, 0),
                timezone="UTC",
                created_at=now,
            ),
            "weekday_allowed",
        ),
        (
            lambda preference_id, now: AvailabilityBlockModel(
                study_preference_id=preference_id,
                weekday=1,
                local_start=time(9, 5),
                local_end=time(10, 0),
                timezone="UTC",
                created_at=now,
            ),
            "quarter_hour_alignment",
        ),
    ],
)
async def test_availability_constraints_reject_invalid_rows(
    profile_sessions: async_sessionmaker[AsyncSession],
    model_factory: Callable[[UUID, datetime], AvailabilityBlockModel],
    expected_constraint: str,
) -> None:
    now = datetime.now(UTC)
    user = _user(now)
    preferences = StudyPreferenceModel(
        user=user,
        matching_enabled=True,
        version=1,
        created_at=now,
        updated_at=now,
    )
    async with profile_sessions.begin() as session:
        session.add_all([user, preferences])

    invalid = model_factory(preferences.id, now)
    with pytest.raises(IntegrityError) as captured:
        async with profile_sessions.begin() as session:
            session.add(invalid)

    assert expected_constraint in str(captured.value.orig)


@pytest.mark.asyncio
async def test_privacy_constraints_reject_self_block_and_duplicate_consent_generation(
    profile_sessions: async_sessionmaker[AsyncSession],
) -> None:
    now = datetime.now(UTC)
    user = _user(now)
    async with profile_sessions.begin() as session:
        session.add(user)

    with pytest.raises(IntegrityError, match="not_self_block"):
        async with profile_sessions.begin() as session:
            session.add(
                UserBlockModel(
                    blocker_user_id=user.id,
                    blocked_user_id=user.id,
                    active=True,
                    created_at=now,
                )
            )

    first = UserConsentModel(
        user_id=user.id,
        policy_key="privacy_policy",
        policy_version="1",
        event_generation=1,
        decision="grant",
        occurred_at=now,
        surface="registration",
    )
    duplicate = UserConsentModel(
        user_id=user.id,
        policy_key="privacy_policy",
        policy_version="1",
        event_generation=1,
        decision="withdraw",
        occurred_at=now,
        surface="settings",
    )
    with pytest.raises(IntegrityError):
        async with profile_sessions.begin() as session:
            session.add_all([first, duplicate])


@pytest.mark.asyncio
async def test_required_profile_indexes_exist_in_postgresql(
    profile_sessions: async_sessionmaker[AsyncSession],
) -> None:
    async with profile_sessions() as session:
        connection = await session.connection()

        def index_names(sync_connection: Connection) -> set[str]:
            inspector = inspect(sync_connection)
            tables = (
                "profile_field_visibilities",
                "study_preference_values",
                "availability_blocks",
                "user_languages",
                "user_blocks",
            )
            return {index["name"] for table in tables for index in inspector.get_indexes(table)}

        names = await connection.run_sync(index_names)

    assert {
        "ix_profile_field_visibilities_profile_id",
        "ix_study_preference_values_study_preference_id",
        "ix_availability_blocks_study_preference_id",
        "ix_user_languages_user_id",
        "ix_user_blocks_blocked_active",
        "uq_user_blocks_active_pair",
    } <= names
