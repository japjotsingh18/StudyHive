"""PostgreSQL authentication repository and transaction boundaries."""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from studyhive.auth.domain import AccountStatus, AuthContext, AuthError, SessionBootstrap
from studyhive.auth.models import (
    AuditLogModel,
    AuthSessionModel,
    EmailAddressModel,
    IdempotencyRecordModel,
    PasswordCredentialModel,
    UserConsentModel,
    UserModel,
)
from studyhive.auth.ports import (
    CredentialAccount,
    RefreshableSession,
    RegistrationCommand,
    RegistrationResult,
    SessionWrite,
)


class SqlAlchemyAuthenticationRepository:
    """Own authentication persistence using short explicit transactions."""

    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def register(self, command: RegistrationCommand) -> RegistrationResult:
        """Create a User and session atomically without disclosing duplicate email state."""

        try:
            async with self._sessions.begin() as session:
                existing_retry = await session.scalar(
                    select(IdempotencyRecordModel).where(
                        IdempotencyRecordModel.principal_key == command.normalized_email,
                        IdempotencyRecordModel.operation == "auth.registration",
                        IdempotencyRecordModel.idempotency_key == command.idempotency_key,
                    )
                )
                if existing_retry is not None:
                    if existing_retry.request_fingerprint != command.request_fingerprint:
                        raise AuthError(
                            "idempotency_key_reused",
                            "The idempotency key was already used for a different request.",
                            409,
                        )
                    return RegistrationResult(is_new_account=False, bootstrap=None)

                existing_email = await session.scalar(
                    select(EmailAddressModel.id).where(
                        EmailAddressModel.normalized_email == command.normalized_email
                    )
                )
                if existing_email is not None:
                    session.add(self._idempotency_record(command, user_id=None))
                    return RegistrationResult(is_new_account=False, bootstrap=None)

                user = UserModel(
                    public_id=f"usr_{uuid4().hex}",
                    status=AccountStatus.PENDING.value,
                    locale="en-US",
                    timezone="UTC",
                    version=1,
                    created_at=command.now,
                    updated_at=command.now,
                )
                session.add(user)
                await session.flush()
                session.add_all(
                    [
                        EmailAddressModel(
                            user_id=user.id,
                            original_email=command.original_email,
                            normalized_email=command.normalized_email,
                            is_primary=True,
                            created_at=command.now,
                            updated_at=command.now,
                        ),
                        PasswordCredentialModel(
                            user_id=user.id,
                            password_hash=command.password_hash,
                            algorithm="argon2id",
                            changed_at=command.now,
                            failed_attempts=0,
                            version=1,
                        ),
                    ]
                )
                for acknowledgement in command.policy_acknowledgements:
                    session.add(
                        UserConsentModel(
                            user_id=user.id,
                            policy_key=acknowledgement.key,
                            policy_version=acknowledgement.version,
                            decision="grant",
                            occurred_at=command.now,
                            surface="registration",
                        )
                    )
                auth_session = self._session_model(user.id, uuid4(), command)
                session.add(auth_session)
                await session.flush()
                session.add(self._idempotency_record(command, user_id=user.id))
                session.add(
                    self._audit(
                        "identity.registered",
                        user.id,
                        "user",
                        user.public_id,
                        "success",
                        command.request_id,
                        command.now,
                    )
                )
                return RegistrationResult(
                    is_new_account=True,
                    bootstrap=self._bootstrap(user, auth_session, email_is_verified=False),
                )
        except IntegrityError as error:
            if getattr(error.orig, "sqlstate", None) == "23505":
                return RegistrationResult(is_new_account=False, bootstrap=None)
            raise

    async def find_credential(self, normalized_email: str) -> CredentialAccount | None:
        """Load the minimum password-login projection by normalized email."""

        async with self._sessions() as session:
            row = (
                await session.execute(
                    select(UserModel, PasswordCredentialModel)
                    .join(EmailAddressModel, EmailAddressModel.user_id == UserModel.id)
                    .join(PasswordCredentialModel, PasswordCredentialModel.user_id == UserModel.id)
                    .where(EmailAddressModel.normalized_email == normalized_email)
                )
            ).one_or_none()
            if row is None:
                return None
            user, credential = row
            return CredentialAccount(
                user_id=user.id,
                user_public_id=user.public_id,
                account_status=AccountStatus(user.status),
                password_hash=credential.password_hash,
            )

    async def create_session(self, user_id: UUID, write: SessionWrite) -> SessionBootstrap:
        """Create a new session after successful credential authentication."""

        async with self._sessions.begin() as session:
            user = await session.get(UserModel, user_id, with_for_update=True)
            if user is None:
                raise AuthError("authentication_required", "Authentication is required.", 401)
            auth_session = AuthSessionModel(
                user_id=user.id,
                family_id=write.family_id,
                token_digest=write.credential.token_digest,
                csrf_digest=write.credential.csrf_digest,
                issued_at=write.now,
                expires_at=write.expires_at,
                last_seen_at=write.now,
                recent_authentication_until=write.recent_authentication_until,
            )
            session.add(auth_session)
            user.last_authenticated_at = write.now
            user.updated_at = write.now
            user.version += 1
            await session.flush()
            email_is_verified = await self._is_email_verified(session, user.id)
            session.add(
                self._audit(
                    write.audit_action,
                    user.id,
                    "auth_session",
                    str(auth_session.id),
                    "success",
                    write.request_id,
                    write.now,
                )
            )
            return self._bootstrap(user, auth_session, email_is_verified=email_is_verified)

    async def authenticate_session(
        self, token_digest: str, now: datetime, idle_cutoff: datetime
    ) -> AuthContext | None:
        """Resolve an active nonexpired session and current User state."""

        async with self._sessions.begin() as session:
            row = (
                await session.execute(
                    select(AuthSessionModel, UserModel)
                    .join(UserModel, UserModel.id == AuthSessionModel.user_id)
                    .where(AuthSessionModel.token_digest == token_digest)
                    .with_for_update()
                )
            ).one_or_none()
            if row is None:
                return None
            auth_session, user = row
            if (
                auth_session.revoked_at is not None
                or auth_session.expires_at <= now
                or auth_session.last_seen_at <= idle_cutoff
            ):
                return None
            auth_session.last_seen_at = now
            return AuthContext(
                session_id=auth_session.id,
                session_family_id=auth_session.family_id,
                user_id=user.id,
                user_public_id=user.public_id,
                account_status=AccountStatus(user.status),
                expires_at=auth_session.expires_at,
                recent_authentication_until=auth_session.recent_authentication_until,
                csrf_digest=auth_session.csrf_digest,
            )

    async def find_refreshable_session(self, token_digest: str) -> RefreshableSession | None:
        """Load a session including terminal state for refresh-reuse detection."""

        async with self._sessions() as session:
            auth_session = await session.scalar(
                select(AuthSessionModel).where(AuthSessionModel.token_digest == token_digest)
            )
            if auth_session is None:
                return None
            return RefreshableSession(
                session_id=auth_session.id,
                family_id=auth_session.family_id,
                user_id=auth_session.user_id,
                csrf_digest=auth_session.csrf_digest,
                revoked_at=auth_session.revoked_at,
                revoked_reason=auth_session.revoked_reason,
                expires_at=auth_session.expires_at,
            )

    async def rotate_session(self, session_id: UUID, write: SessionWrite) -> SessionBootstrap:
        """Revoke one session and issue its replacement in the same family transaction."""

        async with self._sessions.begin() as session:
            current = await session.get(AuthSessionModel, session_id, with_for_update=True)
            if current is None or current.revoked_at is not None or current.expires_at <= write.now:
                raise AuthError("session_expired", "Your session has expired.", 401)
            user = await session.get(UserModel, current.user_id, with_for_update=True)
            if user is None:
                raise AuthError("authentication_required", "Authentication is required.", 401)
            replacement = AuthSessionModel(
                user_id=user.id,
                family_id=current.family_id,
                token_digest=write.credential.token_digest,
                csrf_digest=write.credential.csrf_digest,
                issued_at=write.now,
                expires_at=write.expires_at,
                last_seen_at=write.now,
                recent_authentication_until=current.recent_authentication_until,
            )
            session.add(replacement)
            await session.flush()
            current.revoked_at = write.now
            current.revoked_reason = "rotated"
            current.replaced_by_session_id = replacement.id
            session.add(
                self._audit(
                    write.audit_action,
                    user.id,
                    "auth_session",
                    str(current.id),
                    "success",
                    write.request_id,
                    write.now,
                )
            )
            email_is_verified = await self._is_email_verified(session, user.id)
            return self._bootstrap(user, replacement, email_is_verified=email_is_verified)

    async def revoke_session(self, session_id: UUID, now: datetime, request_id: str) -> None:
        """Idempotently revoke the current session and append an audit fact."""

        async with self._sessions.begin() as session:
            auth_session = await session.get(AuthSessionModel, session_id, with_for_update=True)
            if auth_session is None or auth_session.revoked_at is not None:
                return
            auth_session.revoked_at = now
            auth_session.revoked_reason = "logout"
            session.add(
                self._audit(
                    "identity.session_revoked",
                    auth_session.user_id,
                    "auth_session",
                    str(auth_session.id),
                    "success",
                    request_id,
                    now,
                )
            )

    async def revoke_session_family_for_reuse(
        self, family_id: UUID, now: datetime, request_id: str
    ) -> None:
        """Fail closed by revoking every active session in a reused rotation family."""

        async with self._sessions.begin() as session:
            await session.execute(
                update(AuthSessionModel)
                .where(
                    AuthSessionModel.family_id == family_id,
                    AuthSessionModel.revoked_at.is_(None),
                )
                .values(revoked_at=now, revoked_reason="reuse_detected")
            )
            session.add(
                self._audit(
                    "identity.session_reuse_detected",
                    None,
                    "auth_session_family",
                    str(family_id),
                    "blocked",
                    request_id,
                    now,
                )
            )

    async def record_login_failure(
        self, account: CredentialAccount | None, now: datetime, request_id: str
    ) -> None:
        """Record a redacted login failure without logging the submitted identifier."""

        async with self._sessions.begin() as session:
            if account is not None:
                await session.execute(
                    update(PasswordCredentialModel)
                    .where(PasswordCredentialModel.user_id == account.user_id)
                    .values(failed_attempts=PasswordCredentialModel.failed_attempts + 1)
                )
            session.add(
                self._audit(
                    "identity.login",
                    account.user_id if account is not None else None,
                    "user",
                    account.user_public_id if account is not None else None,
                    "denied",
                    request_id,
                    now,
                )
            )

    @staticmethod
    def _session_model(
        user_id: UUID, family_id: UUID, command: RegistrationCommand
    ) -> AuthSessionModel:
        return AuthSessionModel(
            user_id=user_id,
            family_id=family_id,
            token_digest=command.session_credential.token_digest,
            csrf_digest=command.session_credential.csrf_digest,
            issued_at=command.now,
            expires_at=command.expires_at,
            last_seen_at=command.now,
            recent_authentication_until=command.recent_authentication_until,
        )

    @staticmethod
    def _idempotency_record(
        command: RegistrationCommand, user_id: UUID | None
    ) -> IdempotencyRecordModel:
        return IdempotencyRecordModel(
            principal_key=command.normalized_email,
            operation="auth.registration",
            idempotency_key=command.idempotency_key,
            request_fingerprint=command.request_fingerprint,
            user_id=user_id,
            outcome_status=201,
            created_at=command.now,
            expires_at=command.now + timedelta(hours=24),
        )

    @staticmethod
    def _audit(
        action: str,
        actor_user_id: UUID | None,
        target_type: str,
        target_id: str | None,
        outcome: str,
        request_id: str,
        occurred_at: datetime,
    ) -> AuditLogModel:
        return AuditLogModel(
            event_id=f"evt_{uuid4().hex}",
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            outcome=outcome,
            request_id=request_id,
            safe_metadata={},
            occurred_at=occurred_at,
        )

    @staticmethod
    async def _is_email_verified(session: AsyncSession, user_id: UUID) -> bool:
        verified_at = await session.scalar(
            select(EmailAddressModel.verified_at).where(
                EmailAddressModel.user_id == user_id,
                EmailAddressModel.is_primary.is_(True),
            )
        )
        return verified_at is not None

    @staticmethod
    def _bootstrap(
        user: UserModel, auth_session: AuthSessionModel, *, email_is_verified: bool
    ) -> SessionBootstrap:
        return SessionBootstrap(
            session_id=auth_session.id,
            user_id=user.id,
            user_public_id=user.public_id,
            account_status=AccountStatus(user.status),
            expires_at=auth_session.expires_at,
            recent_authentication_until=auth_session.recent_authentication_until,
            email_verification="verified" if email_is_verified else "pending",
            profile_completion="incomplete",
        )
