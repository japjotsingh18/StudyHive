# Contributing to StudyHive

Thank you for helping build dependable academic collaboration infrastructure.

StudyHive is currently in **Sprint 1 / pre-alpha**. The engineering foundation and authentication foundation are active, while product features remain restricted to their approved roadmap phases. Documentation, accessibility, tests, threat modeling, and bounded foundation improvements are welcome.

## Before you start

1. Read the [product requirements](docs/01-product-requirements.md), [architecture](docs/02-system-architecture.md), and [roadmap](docs/07-roadmap.md).
2. Search existing issues and discussions.
3. For non-trivial changes, open a proposal issue before investing in implementation.
4. Comment on an issue before beginning work so maintainers can confirm scope and avoid duplicate effort.
5. Follow the [Code of Conduct](CODE_OF_CONDUCT.md) and security-reporting rules in [SECURITY.md](SECURITY.md).

## What belongs in an issue first

Open a proposal before work that changes:

- the MVP boundary or product principles;
- public API/realtime contracts;
- database entities, migrations, or retention;
- authentication, authorization, reliability, moderation, or privacy;
- deployment topology or an external provider;
- a new dependency with meaningful maintenance/security cost;
- contributor governance or release policy.

Small documentation corrections, test additions, and already-scoped labeled issues can go directly to a pull request.

## Contribution workflow

1. Fork the repository and create a focused branch.
2. Keep the change within one issue's acceptance criteria.
3. Add or update tests and documentation in the same change.
4. Run focused checks while developing and `make check` before requesting review.
5. Open a pull request using the template and link the issue.
6. Respond to review with follow-up commits; do not force-push after review begins unless coordination requires it.

The eventual branch naming convention is `type/short-description`, for example `docs/reliability-policy` or `fix/waitlist-race`.

## Pull request expectations

A good pull request is small enough to review, explains the user/problem impact, names important tradeoffs, and provides evidence. UI changes include keyboard and accessibility notes plus images/video where useful. Data/API changes include migration/compatibility impact. Operational changes include rollback and observability.

Maintainers may ask to split a pull request when it combines unrelated behavior, refactoring, formatting, or dependency changes.

## Architecture rules

- Domain rules live in domain/application modules, not UI, route handlers, or worker wrappers.
- PostgreSQL is canonical; Redis and WebSockets are not sources of truth.
- API types are generated from OpenAPI for TypeScript consumers.
- Provider SDKs stay behind project-owned adapters.
- Cross-module writes use explicit application services and transactional/outbox rules.
- Never introduce a public reliability ranking, cross-university privacy leak, or globally public private-location behavior.
- AI features are Phase 2 and require a separate approved proposal.

## Tests and quality

Choose evidence based on risk:

- domain/state changes: unit and property/state-machine tests;
- persistence/capacity: real PostgreSQL integration and concurrency tests;
- API changes: OpenAPI/contract and authorization matrix tests;
- UI: user-level behavior, responsive states, keyboard, screen-reader, zoom, contrast, and reduced motion;
- scheduled work: frozen-clock, DST, retries, duplicate delivery, and recovery;
- provider changes: local fake, failure behavior, and secret-safe logs.

Do not weaken checks to make a change pass without an approved rationale.

## Commit style

Use concise imperative commits. Conventional Commit prefixes are encouraged but not required until release automation adopts them:

- `feat: add course membership policy`
- `fix: serialize waitlist promotion`
- `docs: clarify reliability visibility`
- `test: cover DST reminder scheduling`

Sign-off/DCO is not required unless maintainers adopt it in a documented governance change.

## Good first issues

Good first issues are bounded, reproducible, and low-risk. They must not require a first-time contributor to make security, privacy, migration, concurrency, moderation, or scoring-policy decisions. See [the starter backlog](docs/good-first-issues.md).

## Accessibility

Accessibility is part of acceptance, not a follow-up. Prefer native semantics, preserve visible focus, support keyboard/screen readers and 200% zoom, label state in text, and honor reduced motion. Include what you tested in the pull request.

## Security and privacy

Never put real student data, access tokens, provider keys, private locations, emails, or production logs in issues, fixtures, screenshots, commits, or pull requests. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are licensed under the Apache License 2.0.
