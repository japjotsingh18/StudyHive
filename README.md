# StudyHive

> An open-source academic collaboration platform for finding dependable classmates, organizing academic Activities, and improving accountability.

StudyHive is not a general-purpose chat product. Its core promise is: **help a student find the right people to collaborate with, see where academic activity is happening, and know who is actually coming.**

## Project status

**Sprint 1 / pre-alpha.** The engineering foundation and email/password authentication are
implemented. Product collaboration features remain intentionally unimplemented.

## Quick start

Prerequisites are Git, Docker with Compose, Node.js matching `.node-version`, and Corepack. From a clean clone:

```sh
make bootstrap
make dev
```

The web foundation is available at `http://localhost:3000`, API documentation at `http://localhost:8000/api/docs`, and API health at `http://localhost:8000/health/ready`.

Email/password registration is available at `/register`, login at `/login`, and the protected
minimal account bootstrap at `/account`. See [Authentication](docs/authentication.md) for the
API, cookie, CSRF, and session contracts.

Run the complete local quality gate with `make check`. See [Development Setup](docs/development-setup.md) for focused commands and troubleshooting.

## Product principles

- Academic outcomes before engagement metrics.
- Dependable coordination before more chat features.
- Privacy and dignity by default; reliability informs, never shames.
- Any university, department, course, section, timezone, and accessible study location.
- Mobile-first and usable with assistive technology.
- Open governance, documented decisions, and a low-friction contributor path.
- One provider-neutral codebase for hosted and self-hosted deployments.
- Optional capabilities extend through least-privilege plugins and versioned events.

## Current architecture brief

[Part 1 — Vision, Architecture, and Open-Source Philosophy](docs/00-part-1-vision-architecture-open-source.md) is the canonical pre-implementation architecture brief. It defines the core/module/plugin boundary, multitenancy, provider abstractions, event contracts, self-hosting model, and open-source governance direction.

## Planning set

| Phase | Artifact | Decision it enables |
| --- | --- | --- |
| 1 | [Vision and open-source philosophy](docs/00-part-1-vision-architecture-open-source.md) | Mission, boundaries and community model |
| 2 | [Product requirements](docs/01-product-requirements.md) | What ships, for whom, and how success is measured |
| 3 | [System architecture](docs/02-system-architecture.md) | Service boundaries, trust boundaries, and operational model |
| 4 | [Database design](docs/03-database-design.md) | Canonical entities, state machines, constraints, and indexes |
| 5 | [API specification](docs/04-api-specification.md) | Stable REST and realtime contracts |
| 6 | [Engineering standards](docs/05-engineering-standards.md) | Code, testing, security and contribution rules |
| 7 | [Design system](docs/06-design-system-product-design.md) | Visual, interaction and accessibility contracts |
| 8 | [Implementation roadmap](docs/07-implementation-roadmap.md) | Dependencies, phases, sprints and release gates |

## MVP in one sentence

A verified university student can join courses, see privacy-safe campus activity, request immediate help, discover or create an academic Activity, RSVP through a confirmation workflow, check in, and develop a private-by-default reliability history.

Internally, `Activity` is the canonical aggregate. Study Session, Homework Group, Project Meeting, Project Team Formation, Lab Help, Interview Practice, Research Discussion, Office-Hours Meetup, Hackathon Prep, and ad-hoc help meetups are activity types.

MVP Activities include structured goals/outcomes and weekly recurrence. Study Compatibility combines course context with pace, duration, time, modality, interaction, environment, learning method, and study style.

## Accepted technology baseline

- FastAPI, Python, PostgreSQL, SQLAlchemy 2, and Alembic.
- Latest stable/Active LTS Next.js at implementation start; Next.js 15 only if still supported and compatibility requires it.
- Google OAuth and email + password first; GitHub, Microsoft, and university SSO later.
- WebSockets and Redis Pub/Sub for realtime; PostgreSQL remains authoritative.
- Local storage first; S3, MinIO, and Cloudflare R2 adapters later.
- Web Push and email first; Firebase, Discord, and Slack notification adapters later.

The MVP deliberately excludes direct messages, friend requests, rich file chat, public note publishing, advanced recommendations, streak gamification, and all AI features. These remain in the roadmap, but do not delay proving dependable study coordination.

## Architecture decisions

The backend decision is accepted: **FastAPI + PostgreSQL + SQLAlchemy 2 + Alembic**. Prisma is not used. See [ADR-0001](docs/decisions/0001-python-orm.md).

The frontend will use the latest stable/Active LTS Next.js release available when implementation begins. Next.js 15 is used only if it remains supported and a documented compatibility reason prevents the upgrade.

Self-hosting is a first-class constraint. Google OAuth and email/password, local storage, Web Push, and email are initial capabilities behind abstractions; later identity, object-storage, and notification providers remain replaceable adapters.

## Open-source project files

- [Contribution guide](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Roadmap](ROADMAP.md)
- [Development setup contract](docs/development-setup.md)
- [Plugin development contract](docs/plugin-development.md)
- [Deployment guide](docs/deployment.md)
- [Self-hosting guide](docs/self-hosting.md)
- [Changelog](CHANGELOG.md)
- [Good first issues](docs/good-first-issues.md)
- [Security policy](SECURITY.md)
- [License](LICENSE)

## License

Apache License 2.0. See [LICENSE](LICENSE).
