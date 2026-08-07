"""FastAPI authentication contracts, middleware, and error translation."""

import logging
import re
import secrets
from datetime import UTC, datetime
from typing import Annotated, Any, cast

from fastapi import APIRouter, FastAPI, Header, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from studyhive.auth.domain import (
    AccountStatus,
    AuthContext,
    AuthError,
    AuthorizationPolicy,
    PolicyAcknowledgement,
    SessionBootstrap,
)
from studyhive.auth.security import SessionTokenFactory
from studyhive.auth.service import AuthenticationService, AuthResult
from studyhive.core.config import Settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")
MAX_REQUEST_ID_LENGTH = 64
MAX_IDEMPOTENCY_KEY_LENGTH = 128


class PolicyAcknowledgementRequest(BaseModel):
    """Versioned policy acceptance submitted during registration."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=80)
    version: str = Field(min_length=1, max_length=40)


class RegistrationRequest(BaseModel):
    """Email/password registration transport contract."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=1, max_length=1024)
    policy_acknowledgements: list[PolicyAcknowledgementRequest] = Field(min_length=2, max_length=8)


class LoginRequest(BaseModel):
    """Email/password login transport contract."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=1, max_length=1024)
    remember_me: bool = False


class SessionAttributes(BaseModel):
    """Safe session state; browser secret remains cookie-only."""

    expires_at: datetime
    account_status: AccountStatus
    email_verification: str
    university_verification: str
    profile_completion: str
    recent_authentication_until: datetime


class ResourceIdentifier(BaseModel):
    """Opaque typed relationship identifier."""

    type: str
    id: str


class RelationshipData(BaseModel):
    """Single resource relationship wrapper."""

    data: ResourceIdentifier


class SessionRelationships(BaseModel):
    """Session ownership relationship."""

    user: RelationshipData


class SessionResource(BaseModel):
    """Part 5 session resource representation."""

    type: str = "session"
    id: str
    attributes: SessionAttributes
    relationships: SessionRelationships
    capabilities: list[str]


class ResponseMeta(BaseModel):
    """Required request correlation and warning metadata."""

    request_id: str
    generated_at: datetime
    warnings: list[dict[str, Any]]


class SessionEnvelope(BaseModel):
    """Single session success envelope."""

    data: SessionResource
    meta: ResponseMeta
    links: dict[str, str]


class ProviderAttributes(BaseModel):
    """Public safe authentication-provider metadata."""

    key: str
    display_name: str
    is_enabled: bool


class ProviderResource(BaseModel):
    """Configured authentication-provider resource."""

    type: str = "authentication_provider"
    id: str
    attributes: ProviderAttributes


class ProviderEnvelope(BaseModel):
    """Small unpaginated provider collection."""

    data: list[ProviderResource]
    meta: ResponseMeta
    links: dict[str, str]


class AccountAttributes(BaseModel):
    """Minimal `/me` bootstrap without Sprint 2 Profile fields."""

    account_status: AccountStatus
    email_verification: str
    university_verification: str
    profile_completion: str
    roles: list[str]
    scopes: list[str]


class AccountResource(BaseModel):
    """Current User account bootstrap resource."""

    type: str = "user"
    id: str
    attributes: AccountAttributes
    capabilities: list[str]


class AccountEnvelope(BaseModel):
    """Current account success envelope."""

    data: AccountResource
    meta: ResponseMeta
    links: dict[str, str]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Resolve server-managed cookies into canonical request principal state."""

    def __init__(self, app: Any, settings: Settings) -> None:
        super().__init__(app)
        self._settings = settings

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = self._request_id(request.headers.get("X-Request-ID"))
        request.state.request_id = request_id
        request.state.auth_context = None
        session_token = request.cookies.get(self._settings.session_cookie_name)
        if session_token:
            service = get_authentication_service(request)
            request.state.auth_context = await service.authenticate_token(session_token)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        return response

    @staticmethod
    def _request_id(candidate: str | None) -> str:
        if (
            candidate
            and len(candidate) <= MAX_REQUEST_ID_LENGTH
            and re.fullmatch(r"[A-Za-z0-9._-]+", candidate)
        ):
            return candidate
        return f"req_{secrets.token_hex(16)}"


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Deny protected Sprint 1 routes unless the server-derived principal is eligible."""

    _PROTECTED_PATHS = frozenset(
        {
            "/api/v1/auth/logout",
            "/api/v1/auth/session",
            "/api/v1/me",
        }
    )

    def __init__(self, app: Any, settings: Settings) -> None:
        super().__init__(app)
        self._settings = settings

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path not in self._PROTECTED_PATHS:
            return await call_next(request)
        context = get_auth_context(request)
        if context is None:
            return problem_response(
                request,
                AuthError("authentication_required", "Authentication is required.", 401),
            )
        if not AuthorizationPolicy.can_access_account_bootstrap(context.account_status):
            return problem_response(
                request,
                AuthError(
                    "account_suspended",
                    "This account cannot access StudyHive. "
                    "Contact support for permitted next steps.",
                    403,
                ),
            )
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            csrf_error = self._validate_browser_mutation(request, context)
            if csrf_error is not None:
                return problem_response(request, csrf_error)
        return await call_next(request)

    def _validate_browser_mutation(
        self, request: Request, context: AuthContext
    ) -> AuthError | None:
        origin = request.headers.get("Origin")
        if origin is not None and origin != self._settings.web_origin:
            return AuthError("origin_not_allowed", "The request origin is not allowed.", 403)
        csrf_header = request.headers.get("X-CSRF-Token", "")
        csrf_cookie = request.cookies.get(self._settings.csrf_cookie_name, "")
        if not csrf_header or not secrets.compare_digest(csrf_header, csrf_cookie):
            return AuthError("csrf_validation_failed", "The request could not be verified.", 403)
        if not secrets.compare_digest(SessionTokenFactory.digest(csrf_header), context.csrf_digest):
            return AuthError("csrf_validation_failed", "The request could not be verified.", 403)
        return None


@router.post(
    "/auth/registrations",
    response_model=SessionEnvelope,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegistrationRequest,
    request: Request,
    response: Response,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> SessionEnvelope:
    """Create a pending email/password account and secure browser session."""

    if not idempotency_key or len(idempotency_key) > MAX_IDEMPOTENCY_KEY_LENGTH:
        raise AuthError("missing_header", "A valid Idempotency-Key header is required.", 400)
    service = get_authentication_service(request)
    result = await service.register(
        original_email=str(payload.email),
        password=payload.password,
        policy_acknowledgements=tuple(
            PolicyAcknowledgement(key=item.key, version=item.version)
            for item in payload.policy_acknowledgements
        ),
        idempotency_key=idempotency_key,
        request_id=get_request_id(request),
        client_key=client_key(request),
    )
    set_session_cookies(response, result, request.app.state.settings)
    response.headers["Location"] = "/api/v1/auth/session"
    logger.info(
        "authentication registration completed",
        extra={"event_key": "auth.registration", "request_id": get_request_id(request)},
    )
    return session_envelope(result.bootstrap, get_request_id(request))


@router.post("/auth/login", response_model=SessionEnvelope)
async def login(payload: LoginRequest, request: Request, response: Response) -> SessionEnvelope:
    """Authenticate email/password credentials and establish a rotated session."""

    service = get_authentication_service(request)
    result = await service.login(
        email=str(payload.email),
        password=payload.password,
        remember_me=payload.remember_me,
        request_id=get_request_id(request),
        client_key=client_key(request),
    )
    set_session_cookies(response, result, request.app.state.settings)
    logger.info(
        "authentication login completed",
        extra={"event_key": "auth.login", "request_id": get_request_id(request)},
    )
    return session_envelope(result.bootstrap, get_request_id(request))


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response) -> None:
    """Revoke the current session and clear browser credentials."""

    context = require_auth_context(request)
    await get_authentication_service(request).logout(context, get_request_id(request))
    clear_session_cookies(response, request.app.state.settings)


@router.get("/auth/session", response_model=SessionEnvelope)
async def get_session(request: Request) -> SessionEnvelope:
    """Return current canonical session state without rotating or refreshing it."""

    context = require_auth_context(request)
    return session_envelope(context_to_bootstrap(context), get_request_id(request))


@router.post("/auth/session-refresh", response_model=SessionEnvelope)
async def refresh_session(request: Request, response: Response) -> SessionEnvelope:
    """Rotate the presented session and detect reuse of an already rotated secret."""

    settings: Settings = request.app.state.settings
    token = request.cookies.get(settings.session_cookie_name)
    csrf_header = request.headers.get("X-CSRF-Token", "")
    csrf_cookie = request.cookies.get(settings.csrf_cookie_name, "")
    if not token:
        raise AuthError("session_expired", "Your session has expired.", 401)
    if not csrf_header or not secrets.compare_digest(csrf_header, csrf_cookie):
        raise AuthError("csrf_validation_failed", "The request could not be verified.", 403)
    origin = request.headers.get("Origin")
    if origin is not None and origin != settings.web_origin:
        raise AuthError("origin_not_allowed", "The request origin is not allowed.", 403)
    result = await get_authentication_service(request).refresh(
        token=token,
        csrf_token=csrf_header,
        request_id=get_request_id(request),
    )
    set_session_cookies(response, result, settings)
    return session_envelope(result.bootstrap, get_request_id(request))


@router.get("/auth/providers", response_model=ProviderEnvelope)
async def get_providers(request: Request) -> ProviderEnvelope:
    """List only the configured Sprint 1 email/password provider."""

    return ProviderEnvelope(
        data=[
            ProviderResource(
                id="password",
                attributes=ProviderAttributes(
                    key="password", display_name="Email and password", is_enabled=True
                ),
            )
        ],
        meta=response_meta(get_request_id(request)),
        links={"self": "/api/v1/auth/providers"},
    )


@router.get("/me", response_model=AccountEnvelope)
async def get_me(request: Request) -> AccountEnvelope:
    """Return the minimal authenticated account bootstrap for future onboarding."""

    context = require_auth_context(request)
    return AccountEnvelope(
        data=AccountResource(
            id=context.user_public_id,
            attributes=AccountAttributes(
                account_status=context.account_status,
                email_verification="pending",
                university_verification="unverified",
                profile_completion="incomplete",
                roles=[],
                scopes=[],
            ),
            capabilities=["read_account", "manage_current_session"],
        ),
        meta=response_meta(get_request_id(request)),
        links={
            "self": "/api/v1/me",
            "session": "/api/v1/auth/session",
        },
    )


def install_auth_error_handlers(application: FastAPI) -> None:
    """Install Part 5 problem-envelope handlers on the FastAPI composition root."""

    @application.exception_handler(AuthError)
    async def handle_auth_error(request: Request, error: AuthError) -> JSONResponse:
        return problem_response(request, error)

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, error: RequestValidationError
    ) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(part) for part in item["loc"] if part != "body"),
                "code": item["type"],
                "message": "This field is invalid.",
            }
            for item in error.errors()
        ]
        return problem_response(
            request,
            AuthError("validation_failed", "Some fields are invalid.", 422),
            details=details,
        )


def problem_response(
    request: Request, error: AuthError, *, details: list[dict[str, Any]] | None = None
) -> JSONResponse:
    """Translate one safe application error into the canonical problem envelope."""

    request_id = getattr(request.state, "request_id", f"req_{secrets.token_hex(16)}")
    headers = {"X-Request-ID": request_id, "Cache-Control": "private, no-store"}
    if error.retry_after is not None:
        headers["Retry-After"] = str(error.retry_after)
    return JSONResponse(
        status_code=error.status,
        headers=headers,
        content={
            "error": {
                "code": error.code,
                "message": error.message,
                "status": error.status,
                "request_id": request_id,
                "details": details or [],
                "retryable": error.retryable,
                "documentation_url": f"/docs/api/errors#{error.code}",
            },
            "meta": {"warnings": [], "rate_limit": None},
        },
    )


def set_session_cookies(response: Response, result: AuthResult, settings: Settings) -> None:
    """Set HttpOnly session and script-readable CSRF cookies with bounded lifetime."""

    max_age = max(int((result.bootstrap.expires_at - datetime.now(UTC)).total_seconds()), 1)
    response.set_cookie(
        settings.session_cookie_name,
        result.credential.token,
        max_age=max_age,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        settings.csrf_cookie_name,
        result.credential.csrf_token,
        max_age=max_age,
        httponly=False,
        secure=settings.session_cookie_secure,
        samesite="lax",
        path="/",
    )


def clear_session_cookies(response: Response, settings: Settings) -> None:
    """Expire both browser cookies after session revocation."""

    response.delete_cookie(settings.session_cookie_name, path="/")
    response.delete_cookie(settings.csrf_cookie_name, path="/")


def session_envelope(bootstrap: SessionBootstrap, request_id: str) -> SessionEnvelope:
    """Shape one application bootstrap into the canonical session envelope."""

    return SessionEnvelope(
        data=SessionResource(
            id=f"ses_{bootstrap.session_id.hex}",
            attributes=SessionAttributes(
                expires_at=bootstrap.expires_at,
                account_status=bootstrap.account_status,
                email_verification=bootstrap.email_verification,
                university_verification="unverified",
                profile_completion=bootstrap.profile_completion,
                recent_authentication_until=bootstrap.recent_authentication_until,
            ),
            relationships=SessionRelationships(
                user=RelationshipData(
                    data=ResourceIdentifier(type="user", id=bootstrap.user_public_id)
                )
            ),
            capabilities=["validate", "refresh", "logout"],
        ),
        meta=response_meta(request_id),
        links={"self": "/api/v1/auth/session", "account": "/api/v1/me"},
    )


def context_to_bootstrap(context: AuthContext) -> SessionBootstrap:
    """Map middleware principal state into the safe session representation."""

    return SessionBootstrap(
        session_id=context.session_id,
        user_id=context.user_id,
        user_public_id=context.user_public_id,
        account_status=context.account_status,
        expires_at=context.expires_at,
        recent_authentication_until=context.recent_authentication_until,
        email_verification="pending",
        profile_completion="incomplete",
    )


def response_meta(request_id: str) -> ResponseMeta:
    """Create required response correlation metadata."""

    return ResponseMeta(request_id=request_id, generated_at=datetime.now(UTC), warnings=[])


def get_authentication_service(request: Request) -> AuthenticationService:
    """Resolve the process-scoped application service from the composition root."""

    return cast(AuthenticationService, request.app.state.authentication_service)


def get_auth_context(request: Request) -> AuthContext | None:
    """Return the optional middleware-authenticated principal."""

    return cast(AuthContext | None, request.state.auth_context)


def require_auth_context(request: Request) -> AuthContext:
    """Return the principal after authorization middleware has protected the route."""

    context = get_auth_context(request)
    if context is None:
        raise AuthError("authentication_required", "Authentication is required.", 401)
    return context


def get_request_id(request: Request) -> str:
    """Return middleware-generated request correlation identity."""

    return cast(str, request.state.request_id)


def client_key(request: Request) -> str:
    """Hash the client network hint before using it as an abuse-control dimension."""

    host = request.client.host if request.client is not None else "unknown"
    return SessionTokenFactory.digest(host)[:24]
