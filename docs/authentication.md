# Authentication

Sprint 1 implements StudyHive's email/password authentication foundation. This document describes
the implemented boundary; the final product, architecture, database, API, engineering, design, and
roadmap documents remain authoritative.

## Implemented provider and routes

The enabled provider is `password`. `GET /api/v1/auth/providers` exposes that public capability.
Google OAuth, email verification, password recovery, and profile onboarding remain Sprint 2 work.

Browser routes:

- `/register` creates an account after versioned terms and privacy acknowledgement.
- `/login` creates a server-managed session.
- `/account` is protected and shows only the minimal account bootstrap.

API routes:

- `POST /api/v1/auth/registrations` requires `Idempotency-Key`.
- `POST /api/v1/auth/login` accepts email, password, and `remember_me`.
- `GET /api/v1/auth/session` validates the current session.
- `POST /api/v1/auth/session-refresh` rotates the current session token.
- `POST /api/v1/auth/logout` revokes the current session.
- `GET /api/v1/me` returns minimal account, verification, role, scope, and capability state.

All success and error responses use the Part 5 envelopes and carry an `X-Request-ID`. Authentication
errors do not distinguish an unknown email from an incorrect password.

## Session and browser security

The opaque session secret is stored only in a `SameSite=Lax`, `HttpOnly` cookie. The database stores
only its SHA-256 digest. A separate readable CSRF cookie is bound to the session by its stored digest;
unsafe authenticated requests require the matching `X-CSRF-Token` header and an allowed `Origin`.

Session validation enforces the configured idle timeout. Session refresh rotates the secret while
preserving the original absolute expiry. Reuse of a rotated secret revokes its session family and
produces an audit event. Logout revokes the current session and expires both browser cookies.
Passwords are hashed using the maintained Argon2 implementation supplied by `pwdlib`; plaintext
passwords and session/CSRF secrets are never logged.

Set `STUDYHIVE_SESSION_COOKIE_SECURE=true` behind HTTPS in staging and production. Configure
`STUDYHIVE_WEB_ORIGIN` to the exact browser origin. Session and password policy settings are listed in
`.env.example` and validated at startup.

## Account bootstrap boundary

Registration creates a pending `User`, primary `EmailAddress`, `PasswordCredential`, policy-consent
records, and a session. `/api/v1/me` deliberately reports `profile_completion: incomplete` and
`university_verification: unverified`; it does not create or return a Sprint 2 Profile or university
record.

## Operations

Authentication emits structured application logs and append-only audit records for registration,
login, session rotation/reuse, and logout. Redis-backed login and registration rate limits fall back
to a conservative per-process limiter if Redis is temporarily unavailable. See
`docs/runbooks/authentication.md` for incident handling.
