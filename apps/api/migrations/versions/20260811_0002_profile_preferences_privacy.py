"""Create the Sprint 2 profile, preferences, and privacy foundation.

Revision ID: 20260811_0002
Revises: 20260806_0001
Create Date: 2026-08-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0002"
down_revision: str | Sequence[str] | None = "20260806_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create profile-owned tables and evolve consent into an event history."""

    op.add_column(
        "user_consents",
        sa.Column("event_generation", sa.Integer(), server_default="1", nullable=False),
    )
    op.add_column("user_consents", sa.Column("source", sa.String(length=40), nullable=True))
    op.add_column(
        "user_consents", sa.Column("evidence_digest", sa.String(length=64), nullable=True)
    )
    op.drop_constraint("uq_user_consents_user_id", "user_consents", type_="unique")
    op.create_unique_constraint(
        "uq_user_consents_user_id",
        "user_consents",
        ["user_id", "policy_key", "policy_version", "event_generation"],
    )
    op.create_check_constraint(
        "ck_user_consents_event_generation_positive",
        "user_consents",
        "event_generation > 0",
    )
    op.alter_column("user_consents", "event_generation", server_default=None)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("display_name", sa.String(length=320), nullable=False),
        sa.Column("major", sa.String(length=480), nullable=True),
        sa.Column("graduation_year", sa.Integer(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("discoverability", sa.String(length=20), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "char_length(btrim(display_name)) BETWEEN 1 AND 80",
            name="ck_profiles_display_name_length",
        ),
        sa.CheckConstraint(
            "major IS NULL OR char_length(btrim(major)) BETWEEN 1 AND 120",
            name="ck_profiles_major_length",
        ),
        sa.CheckConstraint("bio IS NULL OR char_length(bio) <= 500", name="ck_profiles_bio_length"),
        sa.CheckConstraint(
            "discoverability IN ('private', 'university')",
            name="ck_profiles_discoverability_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_profiles_user_id_users", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_profiles"),
        sa.UniqueConstraint("user_id", name="uq_profiles_user_id"),
    )
    op.create_table(
        "profile_field_visibilities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("field_key", sa.String(length=40), nullable=False),
        sa.Column("visibility", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "field_key IN ('display_name', 'major', 'graduation_year', 'bio', 'languages')",
            name="ck_profile_field_visibilities_field_key_allowed",
        ),
        sa.CheckConstraint(
            "visibility IN ('private', 'university')",
            name="ck_profile_field_visibilities_visibility_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.id"],
            name="fk_profile_field_visibilities_profile_id_profiles",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_profile_field_visibilities"),
        sa.UniqueConstraint(
            "profile_id", "field_key", name="uq_profile_field_visibilities_profile_id"
        ),
    )
    op.create_index(
        "ix_profile_field_visibilities_profile_id",
        "profile_field_visibilities",
        ["profile_id"],
        unique=False,
    )

    op.create_table(
        "study_preferences",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("study_pace", sa.String(length=30), nullable=True),
        sa.Column("preferred_session_length", sa.String(length=30), nullable=True),
        sa.Column("modality", sa.String(length=20), nullable=True),
        sa.Column("interaction", sa.String(length=30), nullable=True),
        sa.Column("matching_enabled", sa.Boolean(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "study_pace IS NULL OR study_pace IN "
            "('slow_and_thorough', 'balanced', 'fast_paced')",
            name="ck_study_preferences_study_pace_allowed",
        ),
        sa.CheckConstraint(
            "preferred_session_length IS NULL OR preferred_session_length IN "
            "('thirty_minutes', 'one_hour', 'two_hours', 'four_plus_hours')",
            name="ck_study_preferences_session_length_allowed",
        ),
        sa.CheckConstraint(
            "modality IS NULL OR modality IN ('in_person', 'online', 'either')",
            name="ck_study_preferences_modality_allowed",
        ),
        sa.CheckConstraint(
            "interaction IS NULL OR interaction IN "
            "('silent', 'minimal_speaking', 'conversational', 'discussion_led')",
            name="ck_study_preferences_interaction_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_study_preferences_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_study_preferences"),
        sa.UniqueConstraint("user_id", name="uq_study_preferences_user_id"),
    )
    op.create_table(
        "study_preference_values",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("study_preference_id", sa.Uuid(), nullable=False),
        sa.Column("category", sa.String(length=30), nullable=False),
        sa.Column("value", sa.String(length=40), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "category IN ('study_style', 'preferred_time', 'environment', 'learning_method')",
            name="ck_study_preference_values_category_allowed",
        ),
        sa.CheckConstraint(
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
            name="ck_study_preference_values_category_value_allowed",
        ),
        sa.CheckConstraint("position >= 0", name="ck_study_preference_values_position_nonnegative"),
        sa.ForeignKeyConstraint(
            ["study_preference_id"],
            ["study_preferences.id"],
            name=op.f("fk_study_preference_values_study_preference_id_study_preferences"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_study_preference_values"),
        sa.UniqueConstraint(
            "study_preference_id",
            "category",
            "value",
            name="uq_study_preference_values_study_preference_id",
        ),
    )
    op.create_index(
        "ix_study_preference_values_study_preference_id",
        "study_preference_values",
        ["study_preference_id"],
        unique=False,
    )
    op.create_table(
        "availability_blocks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("study_preference_id", sa.Uuid(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("local_start", sa.Time(), nullable=False),
        sa.Column("local_end", sa.Time(), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("effective_start_date", sa.Date(), nullable=True),
        sa.Column("effective_end_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "weekday BETWEEN 0 AND 6",
            name="ck_availability_blocks_weekday_allowed",
        ),
        sa.CheckConstraint(
            "local_end > local_start", name="ck_availability_blocks_end_after_start"
        ),
        sa.CheckConstraint(
            "local_end - local_start BETWEEN interval '30 minutes' AND interval '12 hours'",
            name="ck_availability_blocks_duration_allowed",
        ),
        sa.CheckConstraint(
            "date_part('minute', local_start)::integer % 15 = 0 "
            "AND date_part('second', local_start) = 0 "
            "AND date_part('minute', local_end)::integer % 15 = 0 "
            "AND date_part('second', local_end) = 0",
            name="ck_availability_blocks_quarter_hour_alignment",
        ),
        sa.CheckConstraint(
            "effective_end_date IS NULL OR effective_start_date IS NULL "
            "OR effective_end_date >= effective_start_date",
            name="ck_availability_blocks_effective_date_order",
        ),
        sa.ForeignKeyConstraint(
            ["study_preference_id"],
            ["study_preferences.id"],
            name="fk_availability_blocks_study_preference_id_study_preferences",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_availability_blocks"),
        sa.UniqueConstraint(
            "study_preference_id",
            "weekday",
            "local_start",
            "local_end",
            "timezone",
            name="uq_availability_blocks_study_preference_id",
        ),
    )
    op.create_index(
        "ix_availability_blocks_study_preference_id",
        "availability_blocks",
        ["study_preference_id"],
        unique=False,
    )

    op.create_table(
        "user_languages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("normalized_language", sa.String(length=200), nullable=False),
        sa.Column("display_label", sa.String(length=200), nullable=False),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "char_length(btrim(normalized_language)) BETWEEN 1 AND 50",
            name="ck_user_languages_normalized_language_length",
        ),
        sa.CheckConstraint(
            "char_length(btrim(display_label)) BETWEEN 1 AND 50",
            name="ck_user_languages_display_label_length",
        ),
        sa.CheckConstraint(
            "position IS NULL OR position >= 0", name="ck_user_languages_position_nonnegative"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_languages_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_languages"),
        sa.UniqueConstraint("user_id", "normalized_language", name="uq_user_languages_user_id"),
    )
    op.create_index("ix_user_languages_user_id", "user_languages", ["user_id"], unique=False)

    op.create_table(
        "user_blocks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("blocker_user_id", sa.Uuid(), nullable=False),
        sa.Column("blocked_user_id", sa.Uuid(), nullable=False),
        sa.Column("reason_category", sa.String(length=40), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "blocker_user_id <> blocked_user_id", name="ck_user_blocks_not_self_block"
        ),
        sa.CheckConstraint(
            "(active AND ended_at IS NULL) OR (NOT active AND ended_at IS NOT NULL)",
            name="ck_user_blocks_active_end_consistent",
        ),
        sa.ForeignKeyConstraint(
            ["blocked_user_id"],
            ["users.id"],
            name="fk_user_blocks_blocked_user_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["blocker_user_id"],
            ["users.id"],
            name="fk_user_blocks_blocker_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_blocks"),
    )
    op.create_index(
        "ix_user_blocks_blocked_active",
        "user_blocks",
        ["blocked_user_id", "active"],
        unique=False,
    )
    op.create_index(
        "uq_user_blocks_active_pair",
        "user_blocks",
        ["blocker_user_id", "blocked_user_id"],
        unique=True,
        postgresql_where=sa.text("active"),
    )


def downgrade() -> None:
    """Remove the Sprint 2 persistence foundation and restore Sprint 1 consent shape."""

    op.drop_index("uq_user_blocks_active_pair", table_name="user_blocks")
    op.drop_index("ix_user_blocks_blocked_active", table_name="user_blocks")
    op.drop_table("user_blocks")
    op.drop_index("ix_user_languages_user_id", table_name="user_languages")
    op.drop_table("user_languages")
    op.drop_index("ix_availability_blocks_study_preference_id", table_name="availability_blocks")
    op.drop_table("availability_blocks")
    op.drop_index(
        "ix_study_preference_values_study_preference_id",
        table_name="study_preference_values",
    )
    op.drop_table("study_preference_values")
    op.drop_table("study_preferences")
    op.drop_index(
        "ix_profile_field_visibilities_profile_id",
        table_name="profile_field_visibilities",
    )
    op.drop_table("profile_field_visibilities")
    op.drop_table("profiles")

    op.drop_constraint("ck_user_consents_event_generation_positive", "user_consents", type_="check")
    op.drop_constraint("uq_user_consents_user_id", "user_consents", type_="unique")
    op.create_unique_constraint(
        "uq_user_consents_user_id",
        "user_consents",
        ["user_id", "policy_key", "policy_version"],
    )
    op.drop_column("user_consents", "evidence_digest")
    op.drop_column("user_consents", "source")
    op.drop_column("user_consents", "event_generation")
