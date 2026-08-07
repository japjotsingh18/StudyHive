# Changelog

All notable changes to StudyHang will be documented here. The project intends to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Semantic Versioning when implementation releases begin.

## Unreleased

## [0.1.1] - 2026-08-06

### Security

- Upgraded Black to 26.3.1 and pytest to 9.0.3 to resolve their published file-write and temporary-directory vulnerabilities.
- Upgraded pytest-asyncio to the minimum pytest 9-compatible release, 1.3.0.
- Upgraded Next.js and its ESLint plugin to 16.3.0, carrying patched PostCSS 8.5.23 and Sharp 0.35.3 transitive dependencies.
- Regenerated the frozen pnpm and uv lockfiles without adding product features or changing architecture.

## [0.1.0] - 2026-08-06

### Added

- Sprint 1 email/password registration, login, logout, session management, protected API/frontend routes, initial user creation, and minimal profile bootstrap.
- Authentication and authorization middleware, abuse controls, audit logging, database migration, automated tests, documentation, and operational guidance.
- Planning-first product requirements, system architecture, database, API, folder, UI/UX, roadmap, and implementation documents.
- Canonical Part 1 vision, self-hosting, multitenancy, plugin, event-driven architecture, and open-source governance blueprint.
- Contribution, conduct, security, issue/PR template, label, and starter-issue documentation.
- Apache License 2.0.
- Accepted FastAPI/PostgreSQL/SQLAlchemy/Alembic backend and provider-neutral frontend/auth/realtime/storage/notification baseline.
- Generalized the internal collaboration aggregate from Study Session to Activity.
- Added privacy-safe Campus Presence and Need Help Now to the pre-Part-2 product architecture.
- Replaced the initial PRD draft with the complete Part 2 product-behavior specification covering all 22 requested feature groups and MVP release gates.
- Added MVP Study Preferences/Compatibility, Activity goals/outcomes, weekly recurring Activities, and lightweight Project Team Formation; reserved reputation categories, anonymous feedback, and persistent teams for Version 1.1.

### Decisions pending

- Hosted multitenancy launch scope.
- First reference plugin and production self-hosting support profile.
- Final product name and trademark policy.
