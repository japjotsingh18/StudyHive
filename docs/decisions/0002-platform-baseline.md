# ADR-0002 — Platform technology and provider baseline

- **Status:** accepted
- **Date:** 2026-08-04
- **Deciders:** founder and project maintainers

## Context

StudyHang needs one production-oriented baseline that remains self-hostable and does not make cloud vendors part of core domain logic.

## Decision

- Backend: FastAPI and Python.
- Persistence: PostgreSQL, SQLAlchemy 2 async, and Alembic.
- Frontend: use the latest stable/Active LTS Next.js release at implementation start. Next.js 15 is acceptable only if it remains supported and a documented compatibility reason prevents the upgrade.
- Authentication initially: Google OAuth and email + password behind StudyHang's identity-provider abstraction.
- Authentication later: GitHub, Microsoft, and university SSO adapters.
- Realtime: WebSockets with Redis Pub/Sub for cross-instance fan-out; PostgreSQL remains authoritative.
- Storage initially: local filesystem through the storage interface.
- Storage later: S3, MinIO, and Cloudflare R2 adapters.
- Notifications initially: canonical in-app records plus Web Push and email delivery.
- Notifications later: Firebase, Discord, and Slack adapters.

## Security requirements

Email/password authentication requires verified email, modern password hashing (Argon2id or the then-current recommended equivalent), breached-password defenses where practical, secure reset tokens, rate limiting, session revocation, account-enumeration resistance, and an upgrade path to MFA/passkeys. Authentication uses maintained security libraries; domain code does not implement cryptographic primitives.

Local storage is a development/single-node capability. Startup validation must reject it for horizontally scaled or ephemeral-filesystem production profiles unless an operator deliberately accepts the documented limitation.

Redis carries ephemeral fan-out, presence, rate-limit, and queue coordination. Losing Redis may degrade realtime delivery but cannot erase committed activities, help requests, attendance, or notifications.

## Consequences

- Core remains runnable without Clerk, Supabase, Firebase, or another proprietary control plane.
- Provider adapters can be added without changing domain modules.
- Hosted and self-hosted deployments use the same code and configuration contracts.
- Password authentication adds meaningful security and abuse-prevention responsibility from the first release.

## Revisit conditions

Review the exact Next.js major and security-library selections immediately before implementation. Review local storage before any production deployment and provider priorities after pilot evidence.
