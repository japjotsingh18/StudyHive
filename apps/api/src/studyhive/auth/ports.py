"""Application ports and persistence-neutral authentication records."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from studyhive.auth.domain import (
    AccountStatus,
    AuthContext,
    PolicyAcknowledgement,
    SessionBootstrap,
    SessionCredential,
)


@dataclass(frozen=True, slots=True)
class CredentialAccount:
    """Credential lookup result with only authentication-owned fields."""

    user_id: UUID
    user_public_id: str
    account_status: AccountStatus
    password_hash: str


@dataclass(frozen=True, slots=True)
class RegistrationCommand:
    """Validated atomic registration write."""

    original_email: str
    normalized_email: str
    password_hash: str
    policy_acknowledgements: tuple[PolicyAcknowledgement, ...]
    idempotency_key: str
    request_fingerprint: str
    session_credential: SessionCredential
    now: datetime
    expires_at: datetime
    recent_authentication_until: datetime
    request_id: str


@dataclass(frozen=True, slots=True)
class RegistrationResult:
    """Registration result concealed from the transport until shaped generically."""

    is_new_account: bool
    bootstrap: SessionBootstrap | None


@dataclass(frozen=True, slots=True)
class SessionWrite:
    """Fields required to establish or rotate a browser session."""

    credential: SessionCredential
    family_id: UUID
    now: datetime
    expires_at: datetime
    recent_authentication_until: datetime
    request_id: str
    audit_action: str


@dataclass(frozen=True, slots=True)
class RefreshableSession:
    """Stored session state required for CSRF validation and rotation."""

    session_id: UUID
    family_id: UUID
    user_id: UUID
    csrf_digest: str
    revoked_at: datetime | None
    revoked_reason: str | None
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class RateLimitDecision:
    """Result of one bounded abuse-control counter."""

    is_allowed: bool
    retry_after: int | None = None


class AuthenticationRepository(Protocol):
    """Persistence boundary owned by authentication application services."""

    async def register(self, command: RegistrationCommand) -> RegistrationResult: ...

    async def find_credential(self, normalized_email: str) -> CredentialAccount | None: ...

    async def create_session(self, user_id: UUID, write: SessionWrite) -> SessionBootstrap: ...

    async def authenticate_session(
        self, token_digest: str, now: datetime, idle_cutoff: datetime
    ) -> AuthContext | None: ...

    async def find_refreshable_session(self, token_digest: str) -> RefreshableSession | None: ...

    async def rotate_session(self, session_id: UUID, write: SessionWrite) -> SessionBootstrap: ...

    async def revoke_session(self, session_id: UUID, now: datetime, request_id: str) -> None: ...

    async def revoke_session_family_for_reuse(
        self, family_id: UUID, now: datetime, request_id: str
    ) -> None: ...

    async def record_login_failure(
        self, account: CredentialAccount | None, now: datetime, request_id: str
    ) -> None: ...


class RateLimiter(Protocol):
    """Abuse-control port with conservative local degradation."""

    async def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision: ...
