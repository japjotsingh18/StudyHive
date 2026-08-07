from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient
from studyhive.auth.api import (
    AuthenticationMiddleware,
    AuthorizationMiddleware,
    install_auth_error_handlers,
    router,
)
from studyhive.auth.domain import (
    AccountStatus,
    AuthContext,
    AuthError,
    PolicyAcknowledgement,
    SessionBootstrap,
    SessionCredential,
)
from studyhive.auth.security import SessionTokenFactory
from studyhive.auth.service import AuthResult
from studyhive.core.config import Environment, Settings

SESSION_ID = UUID("00000000-0000-0000-0000-000000000101")
FAMILY_ID = UUID("00000000-0000-0000-0000-000000000102")
USER_ID = UUID("00000000-0000-0000-0000-000000000103")
NOW = datetime(2026, 8, 6, 3, 0, tzinfo=UTC)
VALID_SESSION = "valid-session"
VALID_CSRF = "valid-csrf"
WRONG_PASSWORD = "incorrect password"  # noqa: S105 - inert test fixture


class StubAuthenticationService:
    def __init__(self) -> None:
        self.logout_calls = 0
        self.account_status = AccountStatus.PENDING

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
        del original_email, password, policy_acknowledgements
        del idempotency_key, request_id, client_key
        return auth_result()

    async def login(
        self,
        *,
        email: str,
        password: str,
        remember_me: bool,
        request_id: str,
        client_key: str,
    ) -> AuthResult:
        del remember_me, request_id, client_key
        if email == "unknown@example.edu" or password == WRONG_PASSWORD:
            raise AuthError(
                "invalid_credentials",
                "The email or password is incorrect.",
                HTTPStatus.UNAUTHORIZED,
            )
        return auth_result()

    async def authenticate_token(self, token: str) -> AuthContext | None:
        if token != VALID_SESSION:
            return None
        return auth_context(self.account_status)

    async def refresh(self, *, token: str, csrf_token: str, request_id: str) -> AuthResult:
        del request_id
        if token != VALID_SESSION or csrf_token != VALID_CSRF:
            raise AuthError(
                "csrf_validation_failed", "The request could not be verified.", HTTPStatus.FORBIDDEN
            )
        return auth_result()

    async def logout(self, context: AuthContext, request_id: str) -> None:
        del context, request_id
        self.logout_calls += 1


def test_session_endpoint_returns_canonical_problem_for_anonymous_request() -> None:
    client, _ = build_client()

    response = client.get("/api/v1/auth/session", headers={"X-Request-ID": "req_contract"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers["X-Request-ID"] == "req_contract"
    assert response.json()["error"]["code"] == "authentication_required"


def test_registration_requires_idempotency_key() -> None:
    client, _ = build_client()

    response = client.post(
        "/api/v1/auth/registrations",
        json={
            "email": "student@example.edu",
            "password": "violet orbit correct staple",
            "policy_acknowledgements": [
                {"key": "terms_of_service", "version": "1"},
                {"key": "privacy_policy", "version": "1"},
            ],
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["error"]["code"] == "missing_header"


def test_login_sets_http_only_session_and_csrf_cookies() -> None:
    client, _ = build_client()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.edu",
            "password": "violet orbit correct staple",
            "remember_me": False,
        },
    )

    assert response.status_code == HTTPStatus.OK
    cookies = response.headers.get_list("set-cookie")
    assert any(
        f"studyhive_session={VALID_SESSION}" in cookie and "HttpOnly" in cookie
        for cookie in cookies
    )
    assert any(
        f"studyhive_csrf={VALID_CSRF}" in cookie and "HttpOnly" not in cookie for cookie in cookies
    )
    assert response.json()["data"]["relationships"]["user"]["data"]["id"] == "usr_contract"


def test_login_uses_same_generic_error_for_unknown_email_and_wrong_password() -> None:
    client, _ = build_client()

    unknown = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.edu", "password": "anything", "remember_me": False},
    )
    wrong = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.edu",
            "password": WRONG_PASSWORD,
            "remember_me": False,
        },
    )

    assert unknown.status_code == wrong.status_code == HTTPStatus.UNAUTHORIZED
    assert unknown.json()["error"]["message"] == wrong.json()["error"]["message"]


def test_protected_account_bootstrap_returns_no_email_or_future_profile_fields() -> None:
    client, _ = build_client()
    client.cookies.set("studyhive_session", VALID_SESSION)

    response = client.get("/api/v1/me")

    assert response.status_code == HTTPStatus.OK
    attributes = response.json()["data"]["attributes"]
    assert attributes["profile_completion"] == "incomplete"
    assert attributes["university_verification"] == "unverified"
    assert "email" not in attributes


def test_authorization_middleware_denies_restricted_account() -> None:
    client, service = build_client()
    service.account_status = AccountStatus.SUSPENDED
    client.cookies.set("studyhive_session", VALID_SESSION)

    response = client.get("/api/v1/me")

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["error"]["code"] == "account_suspended"


def test_logout_rejects_missing_csrf_and_revokes_valid_request() -> None:
    client, service = build_client()
    client.cookies.set("studyhive_session", VALID_SESSION)
    client.cookies.set("studyhive_csrf", VALID_CSRF)

    rejected = client.post("/api/v1/auth/logout")
    accepted = client.post(
        "/api/v1/auth/logout",
        headers={"X-CSRF-Token": VALID_CSRF, "Origin": "http://localhost:3000"},
    )

    assert rejected.status_code == HTTPStatus.FORBIDDEN
    assert rejected.json()["error"]["code"] == "csrf_validation_failed"
    assert accepted.status_code == HTTPStatus.NO_CONTENT
    assert service.logout_calls == 1


def build_client() -> tuple[TestClient, StubAuthenticationService]:
    settings = Settings.model_validate(
        {
            "environment": Environment.TEST,
            "web_origin": "http://localhost:3000",
            "session_cookie_secure": False,
        }
    )
    application = FastAPI()
    service = StubAuthenticationService()
    application.state.settings = settings
    application.state.authentication_service = service
    application.add_middleware(AuthorizationMiddleware, settings=settings)
    application.add_middleware(AuthenticationMiddleware, settings=settings)
    install_auth_error_handlers(application)
    application.include_router(router)
    return TestClient(application), service


def auth_result() -> AuthResult:
    return AuthResult(
        SessionBootstrap(
            session_id=SESSION_ID,
            user_id=USER_ID,
            user_public_id="usr_contract",
            account_status=AccountStatus.PENDING,
            expires_at=NOW + timedelta(hours=8),
            recent_authentication_until=NOW + timedelta(minutes=15),
            email_verification="pending",
            profile_completion="incomplete",
        ),
        SessionCredential(
            token=VALID_SESSION,
            token_digest=SessionTokenFactory.digest(VALID_SESSION),
            csrf_token=VALID_CSRF,
            csrf_digest=SessionTokenFactory.digest(VALID_CSRF),
        ),
    )


def auth_context(account_status: AccountStatus = AccountStatus.PENDING) -> AuthContext:
    return AuthContext(
        session_id=SESSION_ID,
        session_family_id=FAMILY_ID,
        user_id=USER_ID,
        user_public_id="usr_contract",
        account_status=account_status,
        expires_at=NOW + timedelta(hours=8),
        recent_authentication_until=NOW + timedelta(minutes=15),
        csrf_digest=SessionTokenFactory.digest(VALID_CSRF),
    )
