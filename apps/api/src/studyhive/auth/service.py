"""Authentication application service coordinating policy, persistence, and providers."""

import hashlib
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import ClassVar
from uuid import uuid4

from anyio import to_thread

from studyhive.auth.domain import (
    AccountStatus,
    AuthContext,
    AuthError,
    PasswordPolicy,
    PolicyAcknowledgement,
    SessionBootstrap,
    SessionCredential,
)
from studyhive.auth.ports import (
    AuthenticationRepository,
    RateLimiter,
    RegistrationCommand,
    SessionWrite,
)
from studyhive.auth.security import PasswordHasher, SessionTokenFactory
from studyhive.core.config import Settings


class AuthResult:
    """Private application result containing cookie material and safe bootstrap state."""

    def __init__(self, bootstrap: SessionBootstrap, credential: SessionCredential) -> None:
        self.bootstrap = bootstrap
        self.credential = credential


class AuthenticationService:
    """Implement Sprint 1 email/password and session use cases."""

    REQUIRED_POLICIES: ClassVar[dict[str, str]] = {
        "privacy_policy": "1",
        "terms_of_service": "1",
    }

    def __init__(
        self,
        repository: AuthenticationRepository,
        password_hasher: PasswordHasher,
        token_factory: SessionTokenFactory,
        rate_limiter: RateLimiter,
        settings: Settings,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher
        self._token_factory = token_factory
        self._rate_limiter = rate_limiter
        self._settings = settings
        self._password_policy = PasswordPolicy(
            settings.password_min_length, settings.password_max_length
        )

    async def register(
        self,
        *,
        original_email: str,
        password: str,
        policy_acknowledgements: tuple[PolicyAcknowledgement, ...],
        idempotency_key: str,
        request_id: str,
        client_key: str,
    ) -> AuthResult:
        """Create a pending account and session with generic duplicate behavior."""

        normalized_email = self.normalize_email(original_email)
        self._password_policy.validate(password, normalized_email)
        self._validate_policies(policy_acknowledgements)
        await self._enforce_rate_limit(
            f"registration:{client_key}:{self.identifier_digest(normalized_email)}", 5, 900
        )
        password_hash = await to_thread.run_sync(self._password_hasher.hash, password)
        credential = self._token_factory.issue()
        now = datetime.now(UTC)
        fingerprint = self._registration_fingerprint(normalized_email, policy_acknowledgements)
        result = await self._repository.register(
            RegistrationCommand(
                original_email=original_email,
                normalized_email=normalized_email,
                password_hash=password_hash,
                policy_acknowledgements=policy_acknowledgements,
                idempotency_key=idempotency_key,
                request_fingerprint=fingerprint,
                session_credential=credential,
                now=now,
                expires_at=now + timedelta(hours=self._settings.session_absolute_hours),
                recent_authentication_until=now
                + timedelta(minutes=self._settings.recent_authentication_minutes),
                request_id=request_id,
            )
        )
        if result.bootstrap is not None:
            return AuthResult(result.bootstrap, credential)

        concealed_credential = self._token_factory.issue()
        return AuthResult(
            SessionBootstrap(
                session_id=uuid4(),
                user_id=uuid4(),
                user_public_id=f"usr_{uuid4().hex}",
                account_status=AccountStatus.PENDING,
                expires_at=now + timedelta(hours=self._settings.session_absolute_hours),
                recent_authentication_until=now
                + timedelta(minutes=self._settings.recent_authentication_minutes),
                email_verification="pending",
                profile_completion="incomplete",
            ),
            concealed_credential,
        )

    async def login(
        self,
        *,
        email: str,
        password: str,
        remember_me: bool,
        request_id: str,
        client_key: str,
    ) -> AuthResult:
        """Authenticate generically, enforce account state, and rotate into a new session."""

        normalized_email = self.normalize_email(email)
        await self._enforce_rate_limit(
            f"login:{client_key}:{self.identifier_digest(normalized_email)}", 5, 900
        )
        account = await self._repository.find_credential(normalized_email)
        if account is None:
            await to_thread.run_sync(self._password_hasher.verify_dummy, password)
            await self._repository.record_login_failure(None, datetime.now(UTC), request_id)
            raise self._invalid_credentials()
        password_is_valid = await to_thread.run_sync(
            self._password_hasher.verify, password, account.password_hash
        )
        if not password_is_valid:
            await self._repository.record_login_failure(account, datetime.now(UTC), request_id)
            raise self._invalid_credentials()
        if account.account_status in {
            AccountStatus.SUSPENDED,
            AccountStatus.DISABLED,
            AccountStatus.ERASED,
        }:
            raise AuthError(
                "account_suspended",
                "This account cannot access StudyHive. Contact support for permitted next steps.",
                403,
            )
        credential = self._token_factory.issue()
        now = datetime.now(UTC)
        expires_at = (
            now + timedelta(days=self._settings.session_remember_days)
            if remember_me
            else now + timedelta(hours=self._settings.session_absolute_hours)
        )
        bootstrap = await self._repository.create_session(
            account.user_id,
            SessionWrite(
                credential=credential,
                family_id=uuid4(),
                now=now,
                expires_at=expires_at,
                recent_authentication_until=now
                + timedelta(minutes=self._settings.recent_authentication_minutes),
                request_id=request_id,
                audit_action="identity.login",
            ),
        )
        return AuthResult(bootstrap, credential)

    async def authenticate_token(self, token: str) -> AuthContext | None:
        """Resolve a browser cookie into current canonical principal state."""

        now = datetime.now(UTC)
        return await self._repository.authenticate_session(
            self._token_factory.digest(token),
            now,
            now - timedelta(minutes=self._settings.session_idle_minutes),
        )

    async def refresh(self, *, token: str, csrf_token: str, request_id: str) -> AuthResult:
        """Rotate an eligible session and fail closed when an old token is reused."""

        now = datetime.now(UTC)
        stored = await self._repository.find_refreshable_session(self._token_factory.digest(token))
        if stored is None:
            raise AuthError("session_expired", "Your session has expired.", 401)
        if stored.revoked_at is not None:
            if stored.revoked_reason == "rotated":
                await self._repository.revoke_session_family_for_reuse(
                    stored.family_id, now, request_id
                )
                raise AuthError(
                    "session_reuse_detected",
                    "This session can no longer be refreshed. Sign in again.",
                    401,
                )
            raise AuthError("session_expired", "Your session has expired.", 401)
        if stored.expires_at <= now:
            raise AuthError("session_expired", "Your session has expired.", 401)
        if not secrets.compare_digest(self._token_factory.digest(csrf_token), stored.csrf_digest):
            raise AuthError("csrf_validation_failed", "The request could not be verified.", 403)
        credential = self._token_factory.issue()
        bootstrap = await self._repository.rotate_session(
            stored.session_id,
            SessionWrite(
                credential=credential,
                family_id=stored.family_id,
                now=now,
                expires_at=stored.expires_at,
                recent_authentication_until=now,
                request_id=request_id,
                audit_action="identity.session_rotated",
            ),
        )
        return AuthResult(bootstrap, credential)

    async def logout(self, context: AuthContext, request_id: str) -> None:
        """Idempotently revoke one current browser session."""

        await self._repository.revoke_session(context.session_id, datetime.now(UTC), request_id)

    @staticmethod
    def normalize_email(email: str) -> str:
        """Apply the documented case-insensitive comparison normalization."""

        return email.strip().casefold()

    @staticmethod
    def identifier_digest(normalized_email: str) -> str:
        """Return a redacted identifier dimension for abuse-control keys."""

        return hashlib.sha256(normalized_email.encode("utf-8")).hexdigest()[:24]

    async def _enforce_rate_limit(self, key: str, limit: int, window_seconds: int) -> None:
        decision = await self._rate_limiter.check(key, limit, window_seconds)
        if not decision.is_allowed:
            raise AuthError(
                "rate_limited",
                "Too many authentication attempts. Try again later.",
                429,
                retryable=True,
                retry_after=decision.retry_after,
            )

    @classmethod
    def _validate_policies(cls, acknowledgements: tuple[PolicyAcknowledgement, ...]) -> None:
        supplied = {item.key: item.version for item in acknowledgements}
        if any(supplied.get(key) != version for key, version in cls.REQUIRED_POLICIES.items()):
            raise AuthError(
                "validation_failed",
                "Accept the current Terms of Service and Privacy Policy to create an account.",
                422,
            )

    @staticmethod
    def _registration_fingerprint(
        normalized_email: str, acknowledgements: tuple[PolicyAcknowledgement, ...]
    ) -> str:
        payload = {
            "email": normalized_email,
            "policies": sorted((item.key, item.version) for item in acknowledgements),
        }
        encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _invalid_credentials() -> AuthError:
        return AuthError(
            "invalid_credentials",
            "The email or password is incorrect.",
            401,
        )
