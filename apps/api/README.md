# StudyHive API

The Python backend release owns FastAPI composition, domain/application modules, HTTP and realtime adapters, worker entry points, provider adapters, SQLAlchemy persistence, Alembic migrations, and backend tests.

Sprint 1 adds the email/password authentication provider, session lifecycle, protected API
middleware, minimal account bootstrap, persistence, audit records, and rate limits. It does not
add Google OAuth, recovery, verification workflows, Profile data, or collaboration domains.

## Commands

Run from the repository root:

- `./scripts/uv.sh run --package studyhive-api uvicorn studyhive.main:app --reload`
- `./scripts/uv.sh run pytest apps/api/tests`
- `./scripts/uv.sh run ruff check apps/api`
- `./scripts/uv.sh run mypy`
- `make db-upgrade`

Alembic revisions belong in `migrations/versions/` and must follow the expand–migrate–contract
policy. The Sprint 1 revision creates only authentication-owned tables. Use the root
`make db-upgrade` command so Alembic receives the correct configuration path.

The browser authentication contract is documented in `docs/authentication.md`. Session and CSRF
secrets must never be logged or returned in response bodies.
