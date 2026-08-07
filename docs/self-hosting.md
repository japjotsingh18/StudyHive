# Self-Hosting Guide

**Status:** operational design. `docker compose up` is a required target, not a currently available command.

StudyHang self-hosting is intended for universities, student organizations, research labs, communities, and individuals. Self-hosted instances retain control of identity configuration, academic catalog, content, plugins, telemetry, and data.

## Supported target

After copying and completing `.env.example`, the supported Compose profile will start:

- web;
- API;
- worker;
- realtime;
- PostgreSQL;
- Redis;
- MinIO;
- initialization/migration job;
- development-only mail catcher when the development profile is selected.

No source changes are required. Branding, domains, providers, university structure, locale, quotas, and plugins are runtime configuration/data.

## Profiles

### Demo/development

For evaluation and contribution only. Uses synthetic data, development identity, local mail, and non-durable-friendly defaults. It must display a warning and refuse production mode with the development identity provider.

### Small production instance

For a trusted club/lab or limited university pilot. Requires real TLS/domain, strong secrets, SMTP/OIDC, durable database/object volumes, automated off-host backups, monitoring, and an upgrade/rollback operator.

### Institutional deployment

Uses managed/clustered infrastructure, SSO, security review, centralized audit/telemetry, data residency controls, formal recovery targets, and named operational ownership.

## Configuration groups

- instance identity, public URL, locale, timezone, branding;
- database and Redis connections/pools;
- identity providers and verified university domains;
- storage adapter, bucket, quotas, signing, scanning;
- in-app/push/email delivery;
- maps/geocoding provider;
- worker timing/retries and realtime limits;
- enabled modules/plugins and plugin secrets;
- security headers, trusted proxies, encryption/signing keys;
- logging, metrics, tracing, retention, and backups.

Typed startup validation must identify missing, conflicting, deprecated, and unsafe values without printing secret contents.

## Required operator procedures

Before this guide is marked supported, it must include tested procedures for:

1. initial install and health verification;
2. Google/OIDC/university-email configuration;
3. adding universities/domains/admins;
4. backups and full restore rehearsal;
5. upgrades, migrations, compatibility, and rollback;
6. secret and signing-key rotation;
7. storage migration/export;
8. plugin install/disable/upgrade/uninstall;
9. monitoring job lag, dead letters, disk, connections, and errors;
10. incident response, account lockout recovery, and data export/deletion.

## Privacy and outbound connectivity

A default self-hosted instance must not send product analytics, student data, or configuration to a StudyHang-operated service. Update checks, crash reporting, cloud adapters, and marketplace access are explicit opt-ins with documented payloads and disable controls.

## Backup scope

Backups must cover PostgreSQL, object storage, plugin-owned schemas/data, configuration excluding recoverable public values, and required encryption/signing key escrow. Redis is not a canonical backup source. A backup is not considered valid until restoration is tested.

## Support boundary

The project publishes supported version combinations and a troubleshooting checklist. Community templates outside that matrix may work but are not called officially supported without automated tests and a maintainer. Operators remain responsible for infrastructure security, updates, content policy, legal compliance, and incident response.
