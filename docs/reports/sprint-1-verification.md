# Sprint 1 verification report

**Project:** StudyHive  
**Sprint:** 1 — Authentication foundation  
**Verified:** 2026-08-06 (America/Phoenix)  
**Result:** PASS

This result covers both the local Sprint 1 verification pipeline and the successful GitHub Actions
run for the published `main` branch.

## Delivered scope

Sprint 1 implements the documented email/password authentication provider and no product
collaboration features. The delivered boundary includes:

- email/password registration with password policy, versioned policy consent, normalized unique
  email identity, idempotency records, generic duplicate behavior, and initial pending `User`;
- Argon2id password hashing through `pwdlib`, generic login failures, Redis-backed rate limits with a
  bounded process-local fallback, and redacted audit records;
- opaque server-managed sessions with digest-only database storage, `HttpOnly` session cookies,
  session-bound CSRF cookies, origin checks, idle timeout, absolute expiry, remember-me expiry,
  rotation, replay-family revocation, and logout;
- authentication and authorization middleware protecting `/api/v1/auth/session`,
  `/api/v1/auth/logout`, and `/api/v1/me`;
- Part 5 endpoints for registration, login, logout, session validation, session refresh, provider
  discovery, and the minimal account bootstrap;
- accessible `/register`, `/login`, and protected `/account` frontend routes with typed API/error
  handling and cookie-aware route guarding;
- a single Alembic authentication migration plus unit, contract, integration, and frontend tests;
- authentication documentation, incident guidance, environment configuration, and CI migration-drift
  enforcement.

The minimal account bootstrap reports pending email verification, unverified university state, and
incomplete profile state without creating a `Profile`, university, or other future-sprint record.

## Verification evidence

| Check                | Result | Evidence                                                                                    |
| -------------------- | ------ | ------------------------------------------------------------------------------------------- |
| Bootstrap            | PASS   | `make bootstrap`; frozen pnpm and uv locks installed, Husky configured                      |
| Python lint          | PASS   | Ruff: all checks passed                                                                     |
| Python formatting    | PASS   | Black: 25 files unchanged                                                                   |
| Python types         | PASS   | mypy strict: no issues in 17 source files                                                   |
| TypeScript lint      | PASS   | web and UI ESLint tasks passed                                                              |
| TypeScript types     | PASS   | web and UI `tsc --noEmit` tasks passed                                                      |
| Formatting           | PASS   | Prettier: all matched files use canonical style                                             |
| Backend tests        | PASS   | 21 tests passed: unit, API contract, health contract, and PostgreSQL integration            |
| Frontend tests       | PASS   | 11 web tests and 1 UI package test passed                                                   |
| Migration apply      | PASS   | Alembic upgraded PostgreSQL to `20260806_0001` transactionally                              |
| Migration drift      | PASS   | `alembic check`: no new upgrade operations detected                                         |
| Migration SQL        | PASS   | PostgreSQL offline SQL generation completed                                                 |
| Web production build | PASS   | Next.js 16.2.11 compiled, typed, and prerendered `/`, `/login`, `/register`, and `/account` |
| API package build    | PASS   | sdist and wheel built successfully                                                          |
| Container builds     | PASS   | Production API and web images built successfully in GitHub Actions                          |
| Hosted CI            | PASS   | GitHub Actions run `31136320905` completed successfully                                     |
| Repository gate      | PASS   | All `make check` stages passed; see environment note below                                  |

The backend suite validates registration uniqueness, password login, protected endpoint envelopes,
generic credential errors, cookie flags, CSRF enforcement, restricted-account authorization, minimal
bootstrap disclosure, session rotation, old-token rejection, replay-family revocation, idle-cutoff
application, and PostgreSQL constraints.

One upstream warning remains non-blocking: FastAPI's current `TestClient` emits a Starlette warning
that its `httpx` integration will move to `httpx2`. It does not affect behavior or results.

## Verification environment note

The workspace resides on a macOS file-provider mount. Python traversal in the workspace virtualenv
intermittently stalled, so the final Python checks and consolidated gate were repeated against a
byte-identical disposable source copy under `/private/tmp` using the same locks and dependencies.
PostgreSQL and Redis ran from `docker/compose.yaml`. Docker Desktop's VM was initially unavailable;
local diagnostics confirmed the engine socket was refusing connections, and a Docker Desktop restart
restored both healthy services.

The consolidated temporary run passed lint, formatting, strict type checks, all frontend tests, and
all backend tests. Turbopack cannot accept pnpm symlinks that leave a temporary filesystem root, so the
web production build was run and passed from the real workspace. The API package build was also run
and passed independently. Together these successful commands cover every `make check` stage without
waiving a check.

## Legitimate scaffold issues corrected

- Added explicit timezone-aware SQLAlchemy timestamp mappings to match the migration and PostgreSQL.
- Corrected Alembic check-constraint naming so metadata and migrated schema remain drift-free.
- Enforced configured session idle expiry and preserved absolute expiry during token rotation.
- Added shared Testing Library cleanup to prevent DOM leakage between frontend tests.
- Regenerated typed Next.js route metadata and allowed required `esbuild`/`sharp` install scripts.
- Corrected PostgreSQL integration imports and strengthened authorization/session unit coverage.
- Added migration drift detection to CI.
- Excluded generated TypeScript build cache and removed a stale duplicate setup guide.
- Isolated the safe-default configuration test from inherited CI environment variables.

## Explicit exclusions

Sprint 1 does not implement Google OAuth, email verification flows, password recovery, profile
onboarding, universities, courses, activities, RSVP, attendance, campus presence, Need Help,
recommendations, notifications, or plugins. No architecture or final specification was redesigned.

## Conclusion

Sprint 1 meets the documented authentication-foundation goal. The email/password provider, secure
session lifecycle, protected backend and frontend surfaces, initial user creation, minimal bootstrap,
tests, migrations, logging/audit controls, and documentation are complete and verified.

## Pre-merge audit

The final pre-merge audit confirmed that implementation scans contain no TODO or placeholder
features, `.env` is ignored while `.env.example` remains available for version control, no credential
material was found, and the migration upgrades a newly created empty database without model/schema
drift. The implemented endpoints and authentication behavior match the Sprint 1 slices of Parts 2,
5, and 8; later authentication flows remain assigned to Sprint 2.

The initial project state was committed directly to `main` because no earlier repository history
existed from which to construct a truthful Sprint 0/Sprint 1 branch split. The public repository is
hosted at `japjotsingh18/StudyHive`, and GitHub Actions run `31136320905` passed the API, web,
migration, package, and container-image gates. The verified repository state is ready for the
`v0.1.0` Sprint 1 milestone tag.
