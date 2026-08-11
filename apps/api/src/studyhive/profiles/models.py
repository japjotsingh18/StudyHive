"""SQLAlchemy models for profile, preference, availability, and privacy data."""

from datetime import date, datetime, time
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Time,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from studyhive.db.base import Base

if TYPE_CHECKING:
    from studyhive.auth.models import UserModel


class ProfileModel(Base):
    """One privacy-aware student profile owned by a User."""

    __tablename__ = "profiles"
    __table_args__ = (
        CheckConstraint(
            "char_length(btrim(display_name)) BETWEEN 1 AND 80",
            name="display_name_length",
        ),
        CheckConstraint(
            "major IS NULL OR char_length(btrim(major)) BETWEEN 1 AND 120",
            name="major_length",
        ),
        CheckConstraint("bio IS NULL OR char_length(bio) <= 500", name="bio_length"),
        CheckConstraint(
            "discoverability IN ('private', 'university')",
            name="discoverability_allowed",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    display_name: Mapped[str] = mapped_column(String(320), nullable=False)
    major: Mapped[str | None] = mapped_column(String(480), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    discoverability: Mapped[str] = mapped_column(String(20), nullable=False, default="university")
    version: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="profile")
    field_visibilities: Mapped[list["ProfileFieldVisibilityModel"]] = relationship(
        back_populates="profile", cascade="all, delete-orphan", passive_deletes=True
    )


class ProfileFieldVisibilityModel(Base):
    """Per-field visibility override; row absence means the canonical default."""

    __tablename__ = "profile_field_visibilities"
    __table_args__ = (
        UniqueConstraint("profile_id", "field_key"),
        CheckConstraint(
            "field_key IN ('display_name', 'major', 'graduation_year', 'bio', 'languages')",
            name="field_key_allowed",
        ),
        CheckConstraint("visibility IN ('private', 'university')", name="visibility_allowed"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    profile_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_key: Mapped[str] = mapped_column(String(40), nullable=False)
    visibility: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    profile: Mapped[ProfileModel] = relationship(back_populates="field_visibilities")


class StudyPreferenceModel(Base):
    """One User-level set of global matching preferences."""

    __tablename__ = "study_preferences"
    __table_args__ = (
        CheckConstraint(
            "study_pace IS NULL OR study_pace IN "
            "('slow_and_thorough', 'balanced', 'fast_paced')",
            name="study_pace_allowed",
        ),
        CheckConstraint(
            "preferred_session_length IS NULL OR preferred_session_length IN "
            "('thirty_minutes', 'one_hour', 'two_hours', 'four_plus_hours')",
            name="session_length_allowed",
        ),
        CheckConstraint(
            "modality IS NULL OR modality IN ('in_person', 'online', 'either')",
            name="modality_allowed",
        ),
        CheckConstraint(
            "interaction IS NULL OR interaction IN "
            "('silent', 'minimal_speaking', 'conversational', 'discussion_led')",
            name="interaction_allowed",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    study_pace: Mapped[str | None] = mapped_column(String(30), nullable=True)
    preferred_session_length: Mapped[str | None] = mapped_column(String(30), nullable=True)
    modality: Mapped[str | None] = mapped_column(String(20), nullable=True)
    interaction: Mapped[str | None] = mapped_column(String(30), nullable=True)
    matching_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    version: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="study_preference")
    values: Mapped[list["StudyPreferenceValueModel"]] = relationship(
        back_populates="study_preference", cascade="all, delete-orphan", passive_deletes=True
    )
    availability_blocks: Mapped[list["AvailabilityBlockModel"]] = relationship(
        back_populates="study_preference", cascade="all, delete-orphan", passive_deletes=True
    )


class StudyPreferenceValueModel(Base):
    """Normalized multi-select value owned by one StudyPreference."""

    __tablename__ = "study_preference_values"
    __table_args__ = (
        UniqueConstraint("study_preference_id", "category", "value"),
        CheckConstraint(
            "category IN ('study_style', 'preferred_time', 'environment', 'learning_method')",
            name="category_allowed",
        ),
        CheckConstraint(
            "(category = 'study_style' AND value IN "
            "('quiet_study', 'discussion', 'problem_solving', 'coding', "
            "'exam_revision', 'group_learning')) OR "
            "(category = 'preferred_time' AND value IN "
            "('morning', 'afternoon', 'evening', 'night')) OR "
            "(category = 'environment' AND value IN "
            "('library', 'coffee_shop', 'campus_common_area', 'online', "
            "'dorm_private_space')) OR "
            "(category = 'learning_method' AND value IN "
            "('explain_concepts', 'practice_problems', 'discussion', 'silent_work'))",
            name="category_value_allowed",
        ),
        CheckConstraint("position >= 0", name="position_nonnegative"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    study_preference_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("study_preferences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[str] = mapped_column(String(40), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    study_preference: Mapped[StudyPreferenceModel] = relationship(back_populates="values")


class AvailabilityBlockModel(Base):
    """Coarse recurring availability interval in the User's stated timezone."""

    __tablename__ = "availability_blocks"
    __table_args__ = (
        UniqueConstraint("study_preference_id", "weekday", "local_start", "local_end", "timezone"),
        CheckConstraint("weekday BETWEEN 0 AND 6", name="weekday_allowed"),
        CheckConstraint("local_end > local_start", name="end_after_start"),
        CheckConstraint(
            "local_end - local_start BETWEEN interval '30 minutes' AND interval '12 hours'",
            name="duration_allowed",
        ),
        CheckConstraint(
            "date_part('minute', local_start)::integer % 15 = 0 "
            "AND date_part('second', local_start) = 0 "
            "AND date_part('minute', local_end)::integer % 15 = 0 "
            "AND date_part('second', local_end) = 0",
            name="quarter_hour_alignment",
        ),
        CheckConstraint(
            "effective_end_date IS NULL OR effective_start_date IS NULL "
            "OR effective_end_date >= effective_start_date",
            name="effective_date_order",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    study_preference_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("study_preferences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    weekday: Mapped[int] = mapped_column(nullable=False)
    local_start: Mapped[time] = mapped_column(Time(timezone=False), nullable=False)
    local_end: Mapped[time] = mapped_column(Time(timezone=False), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    effective_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    study_preference: Mapped[StudyPreferenceModel] = relationship(
        back_populates="availability_blocks"
    )


class UserLanguageModel(Base):
    """Normalized self-described language attached to a User."""

    __tablename__ = "user_languages"
    __table_args__ = (
        UniqueConstraint("user_id", "normalized_language"),
        CheckConstraint(
            "char_length(btrim(normalized_language)) BETWEEN 1 AND 50",
            name="normalized_language_length",
        ),
        CheckConstraint(
            "char_length(btrim(display_label)) BETWEEN 1 AND 50",
            name="display_label_length",
        ),
        CheckConstraint("position IS NULL OR position >= 0", name="position_nonnegative"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    normalized_language: Mapped[str] = mapped_column(String(200), nullable=False)
    display_label: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="languages")


class UserBlockModel(Base):
    """End-dated directional block relationship between two Users."""

    __tablename__ = "user_blocks"
    __table_args__ = (
        CheckConstraint("blocker_user_id <> blocked_user_id", name="not_self_block"),
        CheckConstraint(
            "(active AND ended_at IS NULL) OR (NOT active AND ended_at IS NOT NULL)",
            name="active_end_consistent",
        ),
        Index(
            "uq_user_blocks_active_pair",
            "blocker_user_id",
            "blocked_user_id",
            unique=True,
            postgresql_where=text("active"),
        ),
        Index("ix_user_blocks_blocked_active", "blocked_user_id", "active"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    blocker_user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    blocked_user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reason_category: Mapped[str | None] = mapped_column(String(40), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    blocker: Mapped["UserModel"] = relationship(
        back_populates="blocks_created", foreign_keys=[blocker_user_id]
    )
    blocked: Mapped["UserModel"] = relationship(
        back_populates="blocks_received", foreign_keys=[blocked_user_id]
    )


class UserConsentModel(Base):
    """Append-only versioned grant or withdrawal of one policy consent."""

    __tablename__ = "user_consents"
    __table_args__ = (
        UniqueConstraint("user_id", "policy_key", "policy_version", "event_generation"),
        CheckConstraint("decision IN ('grant', 'withdraw')", name="decision_allowed"),
        CheckConstraint("event_generation > 0", name="event_generation_positive"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    policy_key: Mapped[str] = mapped_column(String(80), nullable=False)
    policy_version: Mapped[str] = mapped_column(String(40), nullable=False)
    event_generation: Mapped[int] = mapped_column(nullable=False, default=1)
    decision: Mapped[str] = mapped_column(String(10), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    surface: Mapped[str] = mapped_column(String(40), nullable=False)
    source: Mapped[str | None] = mapped_column(String(40), nullable=True)
    evidence_digest: Mapped[str | None] = mapped_column(String(64), nullable=True)

    user: Mapped["UserModel"] = relationship(back_populates="consent_events")
