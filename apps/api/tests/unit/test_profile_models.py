from sqlalchemy import CheckConstraint, Index, UniqueConstraint
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


def _constraint_names(model: type[object]) -> set[str]:
    return {
        constraint.name
        for constraint in model.__table__.constraints  # type: ignore[attr-defined]
        if isinstance(constraint, CheckConstraint | UniqueConstraint)
        and constraint.name is not None
    }


def _index_names(model: type[object]) -> set[str]:
    return {
        index.name
        for index in model.__table__.indexes  # type: ignore[attr-defined]
        if isinstance(index, Index) and index.name is not None
    }


def test_profile_foundation_declares_required_tables() -> None:
    assert {
        ProfileModel.__tablename__,
        ProfileFieldVisibilityModel.__tablename__,
        StudyPreferenceModel.__tablename__,
        StudyPreferenceValueModel.__tablename__,
        AvailabilityBlockModel.__tablename__,
        UserLanguageModel.__tablename__,
        UserBlockModel.__tablename__,
        UserConsentModel.__tablename__,
    } == {
        "profiles",
        "profile_field_visibilities",
        "study_preferences",
        "study_preference_values",
        "availability_blocks",
        "user_languages",
        "user_blocks",
        "user_consents",
    }


def test_profile_and_preference_models_declare_business_constraints() -> None:
    assert "uq_profiles_user_id" in _constraint_names(ProfileModel)
    assert "ck_profiles_display_name_length" in _constraint_names(ProfileModel)
    assert "uq_profile_field_visibilities_profile_id" in _constraint_names(
        ProfileFieldVisibilityModel
    )
    assert "uq_study_preferences_user_id" in _constraint_names(StudyPreferenceModel)
    assert "ck_study_preferences_study_pace_allowed" in _constraint_names(StudyPreferenceModel)
    assert "uq_study_preference_values_study_preference_id" in _constraint_names(
        StudyPreferenceValueModel
    )
    assert "ck_study_preference_values_category_value_allowed" in _constraint_names(
        StudyPreferenceValueModel
    )


def test_availability_privacy_and_language_models_declare_constraints_and_indexes() -> None:
    availability_constraints = _constraint_names(AvailabilityBlockModel)
    assert {
        "uq_availability_blocks_study_preference_id",
        "ck_availability_blocks_weekday_allowed",
        "ck_availability_blocks_end_after_start",
        "ck_availability_blocks_duration_allowed",
        "ck_availability_blocks_quarter_hour_alignment",
        "ck_availability_blocks_effective_date_order",
    } <= availability_constraints
    assert "ix_availability_blocks_study_preference_id" in _index_names(AvailabilityBlockModel)

    assert "uq_user_languages_user_id" in _constraint_names(UserLanguageModel)
    assert "ix_user_languages_user_id" in _index_names(UserLanguageModel)
    assert "ck_user_blocks_not_self_block" in _constraint_names(UserBlockModel)
    assert {
        "uq_user_blocks_active_pair",
        "ix_user_blocks_blocked_active",
    } <= _index_names(UserBlockModel)
    assert "uq_user_consents_user_id" in _constraint_names(UserConsentModel)
    assert "ck_user_consents_event_generation_positive" in _constraint_names(UserConsentModel)
