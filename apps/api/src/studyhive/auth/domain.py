"""Framework-independent authentication types and policies."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class AccountStatus(StrEnum):
    """Documented internal account lifecycle states used by Sprint 1."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DISABLED = "disabled"
    ERASED = "erased"


@dataclass(frozen=True, slots=True)
class PolicyAcknowledgement:
    """A versioned policy acceptance captured during registration."""

    key: str
    version: str


@dataclass(frozen=True, slots=True)
class SessionCredential:
    """One browser session secret and its CSRF binding."""

    token: str
    token_digest: str
    csrf_token: str
    csrf_digest: str


@dataclass(frozen=True, slots=True)
class SessionBootstrap:
    """Safe account and session state returned to first-party clients."""

    session_id: UUID
    user_id: UUID
    user_public_id: str
    account_status: AccountStatus
    expires_at: datetime
    recent_authentication_until: datetime
    email_verification: str
    profile_completion: str


@dataclass(frozen=True, slots=True)
class AuthContext:
    """Server-derived principal context attached to an authenticated request."""

    session_id: UUID
    session_family_id: UUID
    user_id: UUID
    user_public_id: str
    account_status: AccountStatus
    expires_at: datetime
    recent_authentication_until: datetime
    csrf_digest: str


class AuthError(Exception):
    """Safe application error translated by the HTTP adapter."""

    def __init__(
        self,
        code: str,
        message: str,
        status: int,
        *,
        retryable: bool = False,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.retryable = retryable
        self.retry_after = retry_after


class PasswordPolicy:
    """Validate password bounds without composition-rule theater."""

    _COMMON_PASSWORDS = frozenset(
        {
            "123456789012",
            "letmeinplease",
            "password1234",
            "qwertyuiop12",
            "studyhive123",
        }
    )

    def __init__(self, minimum_length: int, maximum_length: int) -> None:
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length

    def validate(self, password: str, normalized_email: str) -> None:
        """Reject unsafe passwords with field-safe validation errors."""

        if len(password) < self.minimum_length:
            raise AuthError(
                "validation_failed",
                f"Password must contain at least {self.minimum_length} characters.",
                422,
            )
        if len(password) > self.maximum_length:
            raise AuthError(
                "validation_failed",
                f"Password must contain at most {self.maximum_length} characters.",
                422,
            )
        normalized_password = password.casefold()
        email_local_part = normalized_email.partition("@")[0]
        if (
            normalized_password in self._COMMON_PASSWORDS
            or normalized_password == email_local_part
            or email_local_part in normalized_password
        ):
            raise AuthError(
                "validation_failed",
                "Choose a password that is not based on your email or a commonly used password.",
                422,
            )


class AuthorizationPolicy:
    """Deny product access by default while permitting Sprint 1 bootstrap."""

    @staticmethod
    def can_access_account_bootstrap(account_status: AccountStatus) -> bool:
        """Allow pending/active identities to finish later onboarding phases."""

        return account_status in {AccountStatus.PENDING, AccountStatus.ACTIVE}
