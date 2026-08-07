# Deployment Guide

**Status:** architecture plan. No deployable application images or templates exist yet.

StudyHang uses the same versioned source and container artifacts for self-hosted and cloud profiles. Platform templates configure infrastructure; they do not fork product code.

## Deployables

| Component | Required | State |
| --- | --- | --- |
| Web | yes | stateless Next.js |
| API | yes | stateless FastAPI REST |
| Worker | yes | scheduled tasks, outbox, notifications |
| Realtime | yes for live features | stateless WebSocket gateway; Redis fan-out |
| PostgreSQL | yes | canonical durable state |
| Redis | yes | queue/cache/rate limit/fan-out; not canonical |
| Object storage | required for uploads | local/MinIO/S3-compatible/cloud adapter |
| Email/identity providers | profile-dependent | provider-neutral configuration |

## Target profiles

- **Local/demo:** Docker Compose, synthetic data, development identity, MinIO, mail catcher.
- **Small self-host:** Compose or single-node orchestrator with durable volumes, real domain/TLS, SMTP/OIDC, backups, and monitoring.
- **Cloud startup:** Vercel optional for web; Railway/Render/Fly.io or managed containers for API/worker/realtime; managed data services.
- **Institution/enterprise:** Kubernetes/container platform, private networking, managed data, SSO, centralized secrets/telemetry, policy-specific isolation.

## Platform capability matrix

Every template must document:

- WebSocket connection and idle limits;
- long-running worker support;
- release/migration job semantics;
- private networking and egress controls;
- managed PostgreSQL backup/PITR and Redis durability expectations;
- object storage signed URL/CORS behavior;
- region/data residency and log retention;
- secrets, autoscaling, health checks, rolling deployment, and rollback.

Supported examples may include Vercel, Railway, Render, Fly.io, DigitalOcean, AWS, Azure, and Google Cloud, but support is earned through tested templates and named maintainers.

## Release sequence

1. Back up and validate environment/configuration.
2. Run one compatible expand migration job.
3. Deploy API/worker/realtime versions compatible with old and new schema.
4. Deploy web.
5. Run resumable backfills if needed.
6. Validate health, error rate, job lag, outbox age, and synthetic journey.
7. Contract/drop migrations occur only in a later release.

## Production gate

- [ ] TLS, trusted proxies, domains, CORS/CSP, and session settings verified.
- [ ] Non-development identity and secrets configured.
- [ ] PostgreSQL backup/PITR and restore drill complete.
- [ ] Object storage durable, private, lifecycle-controlled, and scanned.
- [ ] Worker/outbox/realtime health and alerts configured.
- [ ] SMTP/push/provider failure behavior tested.
- [ ] Rate limits, quotas, retention, moderation, and incident contacts configured.
- [ ] Rollback is compatible with the deployed schema.

## Infrastructure as code

Cloud templates live under documented deployment directories only after maintainers can test and support them. Template inputs map to the same environment/configuration contract used by Compose. No template may hide mandatory external telemetry or a proprietary control-plane dependency.
