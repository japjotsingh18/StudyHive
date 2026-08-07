# Sprint 1.1 verification report

**Project:** StudyHive  
**Release:** v0.1.1 — dependency security maintenance  
**Verified:** 2026-08-06 (America/Phoenix)  
**Result:** PENDING DEFAULT-BRANCH ALERT RECALCULATION

## Scope

Sprint 1.1 is a maintenance release for the completed Sprint 1 authentication foundation. It
contains dependency and lockfile updates only. It does not implement Sprint 2 work, product
features, architecture changes, or unrelated refactoring.

## Security updates

| Dependency               | Previous | Patched | Reason                                                            |
| ------------------------ | -------: | ------: | ----------------------------------------------------------------- |
| Black                    |   25.1.0 |  26.3.1 | Resolves GHSA-3936-cmfr-pm3m / CVE-2026-32274                     |
| pytest                   |    8.4.2 |   9.0.3 | Resolves GHSA-6w46-j5rx-g56g / CVE-2025-71176                     |
| pytest-asyncio           |    1.1.0 |   1.3.0 | Earliest release compatible with pytest 9                         |
| Next.js                  |  16.2.11 |  16.3.0 | Carries the patched PostCSS and Sharp dependency graph            |
| @next/eslint-plugin-next |  16.2.11 |  16.3.0 | Keeps framework lint rules aligned with Next.js                   |
| PostCSS                  |   8.4.31 |  8.5.23 | Resolves four path traversal, file disclosure, and XSS advisories |
| Sharp                    |   0.34.5 |  0.35.3 | Resolves GHSA-f88m-g3jw-g9cj and affected libvips advisories      |

Next.js 16.3.0 retains the existing Node.js `>=20.9.0` requirement. Its published dependency
metadata pins PostCSS 8.5.23 and accepts Sharp 0.35.3. StudyHive does not call Sharp directly.
pytest-asyncio 1.3.0 is the minimum published release whose pytest range includes version 9.

## Local verification evidence

| Check                       | Result  | Evidence                                                                   |
| --------------------------- | ------- | -------------------------------------------------------------------------- |
| Frozen pnpm resolution      | PASS    | Targeted install accepted `pnpm-lock.yaml`; expected `+11/-8` graph change |
| Frozen uv resolution        | PASS    | Installed Black 26.3.1, pytest 9.0.3, and pytest-asyncio 1.3.0             |
| Python lint                 | PASS    | Ruff reported all checks passed                                            |
| Python formatting           | PASS    | Black 26.3.1 would leave all 25 files unchanged                            |
| Python types                | PASS    | Strict mypy reported no issues in 17 source files                          |
| Backend tests               | PASS    | 21 tests passed under pytest 9.0.3 and pytest-asyncio 1.3.0                |
| Migration apply             | PASS    | Alembic upgraded the local PostgreSQL schema to head                       |
| Migration drift             | PASS    | `alembic check` reported no new upgrade operations                         |
| API package build           | PASS    | Source distribution and wheel built successfully                           |
| Frontend/UI lint            | PASS    | ESLint passed for web and shared UI packages                               |
| Frontend/UI formatting      | PASS    | Prettier reported canonical formatting                                     |
| Frontend/UI types           | PASS    | Both TypeScript projects passed `tsc --noEmit`                             |
| Frontend/UI tests           | PASS    | 11 web tests and 1 UI test passed                                          |
| Production dependency audit | PASS    | `pnpm audit --prod` reported no known vulnerabilities                      |
| Web production build        | PASS    | GitHub Actions built the Next.js 16.3.0 application successfully           |
| Container image builds      | PASS    | GitHub Actions built both production container images                      |
| Dependabot alerts           | PENDING | GitHub recalculates alerts after the patched graph reaches `main`          |
| CodeQL and secret scanning  | PASS    | All three CodeQL analyses and GitGuardian checks passed                    |

The workspace is stored on a macOS file-provider mount. Repository-level pnpm/uv commands can stall
while traversing provider-backed dependency directories, so verification used clean disposable
environments under `/private/tmp` with the committed lockfiles. Turbopack's local worker could not
bind its internal port under the execution sandbox; this is an environment restriction rather than a
source or dependency diagnostic. Post-merge GitHub Actions run `31160765387` passed the web, API,
migration, package, and container gates on `main`. Post-merge CodeQL run `31160765367` passed its
Actions, Python, and JavaScript/TypeScript analyses.

## Conclusion

Local compatibility checks, hosted CI, CodeQL, secret scanning, and container builds pass. v0.1.1
is not releasable until the patched graph is merged to the default branch and Dependabot confirms
that all seven alerts are closed.
