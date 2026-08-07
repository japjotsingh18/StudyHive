# Development setup

StudyHive supports current macOS and Linux environments with Docker Compose. No paid provider account, production secret, or real student data is required.

## Prerequisites

| Tool | Pinned/supported version | Purpose |
|---|---|---|
| Git | Current supported release | Source control and hooks |
| Docker + Compose | Current Docker Desktop/Engine with Compose v2+ | Reproducible local services and applications |
| Node.js | `.node-version` / `.nvmrc` (Node 24 LTS); Node 22.14+ remains accepted by package engines | Workspace tooling |
| pnpm | `package.json#packageManager` through Corepack | Deterministic Node workspace |
| Python | `.python-version` (Python 3.13) | Backend runtime; managed by uv when needed |
| uv | Repository-managed 0.12.0 or compatible installed executable | Python environment, lockfile, commands and builds |

The bootstrap script installs uv into the ignored repository-local `.tools/bin` directory when uv is unavailable. It does not modify the user's shell profile.

## Clean setup

```sh
git clone <canonical repository URL>
cd studyhive
make bootstrap
make dev
```

`make bootstrap` creates `.env` from safe local values, installs the frozen pnpm and uv workspaces, creates `.venv`, and configures Husky. `make dev` builds and starts the supported Docker Compose profile.

Stop services with `make down`.

## Local endpoints

| Service | URL | Health/purpose |
|---|---|---|
| Web | `http://localhost:3000` | Application shell and Sprint 1 authentication routes |
| API docs | `http://localhost:8000/api/docs` | Generated OpenAPI viewer |
| API liveness | `http://localhost:8000/health/live` | Process health only |
| API readiness | `http://localhost:8000/health/ready` | PostgreSQL and Redis connectivity |
| PostgreSQL | `localhost:5432` | Local canonical database |
| Redis | `localhost:6379` | Local ephemeral coordination |

All credentials in `.env.example` are development-only and must never be reused outside local/test environments.

## Commands

| Command | Purpose |
|---|---|
| `make bootstrap` | Install frozen dependencies and configure the workspace |
| `make dev` | Build and start web, API, PostgreSQL and Redis |
| `make down` | Stop the local profile without deleting volumes |
| `make lint` | Run ESLint, Ruff and Black checks |
| `make format` | Apply Prettier, Ruff safe fixes and Black |
| `make typecheck` | Run strict TypeScript and mypy checks |
| `make test` | Run Vitest and pytest suites |
| `make build` | Verify Next.js and Python package builds |
| `make check` | Run the complete required CI-equivalent quality gate |
| `make db-upgrade` | Apply Alembic migrations to the configured database |

Focused commands are documented in each application/package README.

## Local configuration

All project-owned variables use the `STUDYHIVE_` prefix. Browser-visible values use `NEXT_PUBLIC_STUDYHIVE_` and must never contain secrets. The root `.env` is ignored; `.env.example` is the complete safe local reference.

The Docker profile uses service hostnames (`postgres` and `redis`). To run the API directly on the host, override the URLs for that process:

```sh
STUDYHIVE_DATABASE_URL=postgresql+asyncpg://studyhive:studyhive@localhost:5432/studyhive \
STUDYHIVE_REDIS_URL=redis://localhost:6379/0 \
./scripts/uv.sh run --package studyhive-api uvicorn studyhive.main:app --reload
```

## Troubleshooting

### A port is already in use

Check ports `3000`, `8000`, `5432`, and `6379`. Stop the conflicting local process or deliberately change both the Compose mapping and documented local URL. Do not silently bind random ports because contributor commands and tests depend on predictable endpoints.

### Containers are unhealthy

Run `docker compose -f docker/compose.yaml ps` and inspect the unhealthy service with `docker compose -f docker/compose.yaml logs <service>`. API readiness reports PostgreSQL and Redis independently without revealing connection details.

### Dependency or lockfile drift

Bootstrap uses frozen lockfiles. If a reviewed dependency change modifies a manifest, regenerate the matching lockfile with the approved package manager, inspect the diff, and commit both. Never hand-edit `pnpm-lock.yaml` or `uv.lock`.

### Python interpreter mismatch

Run `./scripts/uv.sh python install 3.13` and repeat `make bootstrap`. uv owns `.venv`; do not install project packages into the system Python.

### File permissions after containers

Application containers run as non-root where possible and persistent data stays in named volumes. Do not solve a permission problem by recursively changing ownership outside this repository or making files world-writable.

## Data safety

- Use only synthetic fixtures.
- Never copy production databases, tokens, emails, private locations, screenshots, or logs into development.
- Redis and local storage are disposable; PostgreSQL volumes are canonical only for the local profile.
- Sprint 1 has no demo seed command. Create test accounts through `/register`; no future domain
  data is seeded.
