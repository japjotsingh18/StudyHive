from http import HTTPStatus

import pytest
from studyhive.auth.domain import AccountStatus, AuthError, AuthorizationPolicy, PasswordPolicy


def test_password_policy_rejects_short_password_with_safe_validation_error() -> None:
    policy = PasswordPolicy(minimum_length=12, maximum_length=128)

    with pytest.raises(AuthError) as captured:
        policy.validate("too-short", "student@example.edu")

    assert captured.value.code == "validation_failed"
    assert captured.value.status == HTTPStatus.UNPROCESSABLE_ENTITY


def test_password_policy_rejects_password_derived_from_email() -> None:
    policy = PasswordPolicy(minimum_length=12, maximum_length=128)

    with pytest.raises(AuthError) as captured:
        policy.validate("student-is-studying", "student@example.edu")

    assert captured.value.code == "validation_failed"


def test_password_policy_accepts_long_non_common_password() -> None:
    policy = PasswordPolicy(minimum_length=12, maximum_length=128)

    policy.validate("violet orbit correct staple", "student@example.edu")


@pytest.mark.parametrize("status", [AccountStatus.PENDING, AccountStatus.ACTIVE])
def test_authorization_policy_allows_bootstrap_for_eligible_accounts(
    status: AccountStatus,
) -> None:
    assert AuthorizationPolicy.can_access_account_bootstrap(status)


@pytest.mark.parametrize(
    "status",
    [AccountStatus.SUSPENDED, AccountStatus.DISABLED, AccountStatus.ERASED],
)
def test_authorization_policy_denies_bootstrap_for_terminal_or_restricted_accounts(
    status: AccountStatus,
) -> None:
    assert not AuthorizationPolicy.can_access_account_bootstrap(status)
