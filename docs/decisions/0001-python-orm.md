# ADR-0001 — Resolve FastAPI and Prisma runtime incompatibility

- **Status:** accepted
- **Date:** 2026-08-03
- **Deciders:** founder and project maintainers

## Context

The requested stack names FastAPI/Python as the backend and Prisma as the ORM. Prisma's currently supported generated runtime client is TypeScript. The third-party `prisma-client-py` repository was archived on 2025-04-15 and is read-only. Depending on it for the core persistence layer would create an unacceptable security, compatibility, and contributor-maintenance risk.

Using Prisma only for migrations while FastAPI uses another model layer would create two schema representations and drift. Putting a Node/Prisma database gateway behind FastAPI would preserve both brand-name technologies but add a network hop, a new failure domain, distributed transactions, duplicated contracts, and significant local-development cost without product value.

## Decision

Use:

- FastAPI and Python for the API and workers;
- SQLAlchemy 2 async for runtime persistence;
- Alembic for migrations;
- PostgreSQL as the canonical database;
- Pydantic for API schemas;
- generated OpenAPI types for TypeScript consumers.

The conceptual `packages/database` boundary in the original brief becomes `apps/api/src/studyhang/db` plus migration and schema documentation. No Python models are imported by the frontend.

## Consequences

### Positive

- One supported Python persistence stack.
- Native async sessions, transactions, row locks, and PostgreSQL features.
- No internal database microservice.
- Strong FastAPI contributor ergonomics.

### Negative

- Deviates from the initially requested ORM.
- TypeScript consumers receive types from OpenAPI rather than Prisma.
- Contributors familiar only with Prisma must learn SQLAlchemy/Alembic.

## Alternatives

1. **Switch the API to TypeScript and use Prisma.** Acceptable if Prisma is non-negotiable; NestJS or Fastify would replace FastAPI.
2. **Node database gateway.** Rejected for MVP complexity and reliability cost.
3. **Archived Prisma Client Python.** Rejected for maintenance and security risk.
4. **Dual schema (Prisma migrations + SQLAlchemy runtime).** Rejected because schema drift is likely.

## Revisit condition

Revisit only if Prisma releases and supports an official Python client with a documented support policy, or maintainers approve moving the API runtime to TypeScript.

## Evidence

- Prisma's official generator documentation describes TypeScript output and JavaScript runtimes: <https://www.prisma.io/docs/orm/prisma-schema/overview/generators>
- The community Python client is archived: <https://github.com/RobertCraigie/prisma-client-py>
