# Sprint 0 Verification Report

**Date:** 2026-08-05  
**Status:** PASS  
**Scope:** Engineering scaffold verification only; no business features were implemented.

## Environment

| Tool    | Verified version |
| ------- | ---------------- |
| Node.js | 22.14.0          |
| pnpm    | 10.17.1          |
| Python  | 3.13.14          |
| uv      | 0.12.0           |
| Docker  | 29.4.0           |

The versions above match the repository's pinned runtime and package-manager configuration.

## Bootstrap

`make bootstrap` initially failed because the scaffold required frozen installs while both
lockfiles were absent. The missing `pnpm-lock.yaml` and `uv.lock` were generated from the
declared workspace manifests. A subsequent unmodified `make bootstrap` completed successfully:

- pnpm resolved the four workspace projects from the frozen lockfile.
- uv verified 43 packages from the frozen lockfile.
- Husky hooks were configured.
- `.env` was created locally from `.env.example` and remains ignored.

## Verification results

The final local verification command was:

```sh
TURBO_TELEMETRY_DISABLED=1 UV_NO_SYNC=1 make check
```

`UV_NO_SYNC=1` bypassed a redundant uv environment synchronization after bootstrap had already
completed the frozen sync. This was necessary after Docker Desktop caused host filesystem and
uv cache reads to stall; it did not skip any lint, formatting, type-check, test, or build command.

| Stage             | Result | Details                                                                             |
| ----------------- | ------ | ----------------------------------------------------------------------------------- |
| TypeScript lint   | PASS   | ESLint passed for `@studyhive/ui` and `@studyhive/web`.                             |
| Python lint       | PASS   | Ruff and Black checks passed.                                                       |
| Formatting        | PASS   | All Prettier-scoped files use canonical formatting.                                 |
| Type checks       | PASS   | TypeScript passed for UI and web; strict mypy passed for 8 Python source files.     |
| TypeScript tests  | PASS   | 2 test files, 2 tests passed.                                                       |
| Python tests      | PASS   | 2 test files, 2 tests passed.                                                       |
| Web build         | PASS   | Next.js 16.2.11 production build completed; `/` and `/_not-found` were prerendered. |
| UI build          | PASS   | Declaration files were emitted to `packages/ui/dist`.                               |
| API package build | PASS   | Source distribution and wheel were built successfully.                              |

## CI-only verification

The checks performed by CI outside `make check` were also executed:

- PostgreSQL 17 and Redis 8 containers started and reached healthy status.
- `make db-upgrade` completed against PostgreSQL using the CI-style localhost connection. The
  scaffold currently has no migration revision files, so Alembic validated an empty head.
- The API image built successfully as `studyhive-api:sprint-0-verification`
  (`sha256:a1a7d55df3d18face22030198c545ec7f1fba47df1d59960ebe998c12578847d`).
- The web image built successfully as `studyhive-web:sprint-0-verification`
  (`sha256:ad0cd3d47ffe258f15e53224f39413da31680da50c99696f6a67c8e96ea24f9a`).
- Temporary PostgreSQL and Redis containers and their network were stopped and removed after
  verification. The Docker images and the named PostgreSQL data volume were retained.

## Scaffold issues corrected

1. Added the missing pnpm and uv lockfiles required by frozen bootstrap and CI installs.
2. Declared the ESLint presets and plugins imported at runtime by `@studyhive/config`, fixing
   package resolution under pnpm's isolated dependency layout.
3. Corrected Ruff import ordering and replaced a magic HTTP status value in the API contract test.
4. Applied the repository's Prettier configuration to five non-canonical scaffold files.
5. Updated the Redis client annotation for the pinned Redis 6 typing API.
6. Configured Vitest to use the automatic React JSX runtime.
7. Excluded nested Next, Turborepo, and mypy caches from Docker contexts. The observed web context
   fell from approximately 87 MB of generated files to approximately 1.4 MB.
8. Made the UI declaration output directory local to `packages/ui`, preventing emitted files from
   polluting `packages/config/typescript`.
9. Removed the inaccurate Turborepo coverage output declaration because tests do not generate
   coverage artifacts. Final test/build runs no longer report missing-output warnings.

## Non-blocking observations

- pnpm reports that the transitive `esbuild` lifecycle script is not allowlisted. Tests and both
  local and container production builds pass, so no broader install-script permission was added.
- Pytest reports an upstream Starlette/FastAPI deprecation warning recommending a future `httpx2`
  migration. All tests pass; changing dependency families is outside this verification scope.
- The repository started and remains entirely untracked in Git, so there is no committed baseline
  against which to produce a conventional diff.

## Conclusion

Sprint 0's engineering foundation is reproducibly bootstrapped, passes the complete local quality
pipeline, applies its migration environment against the declared database version, and produces
both container images. No business functionality was added.
