# Part 6 — Engineering Standards & Contributor Guide

**Project:** StudyHive / StudyHang (working name)  
**Status:** canonical contributor engineering handbook  
**Version:** 1.0 draft  
**Last updated:** 2026-08-04  
**Normative inputs:** finalized Parts 1–5

## 0. How to use this handbook

Every contributor, reviewer, maintainer, release manager, plugin author, and automation agent must follow this handbook before changing the project. It governs how changes are designed, implemented, tested, documented, reviewed, released, and maintained. It does not replace the Code of Conduct, Security Policy, product requirements, architecture, database design, or API specification.

### 0.1 Rule levels

| Term | Meaning |
|---|---|
| **MUST / MUST NOT** | Required for merge unless a documented exception is approved by the owning maintainers |
| **SHOULD / SHOULD NOT** | Strong default; deviations require a short rationale in the pull request |
| **MAY** | Optional technique that remains subject to architecture and quality rules |

When documents conflict, use this order: security/privacy/legal obligations; finalized product requirements; system architecture; database and API specifications; this handbook; local module guidance. Raise the conflict rather than silently choosing.

### 0.2 Definition of done

A change is done only when:

- behavior matches a linked issue/specification and handles negative/edge cases;
- module and dependency boundaries remain intact;
- tests prove the appropriate behavior and failure modes;
- security, privacy and accessibility have been considered;
- API/database/event/plugin compatibility is preserved or explicitly migrated;
- user, operator and contributor documentation is updated;
- observability and recovery are adequate for production behavior;
- required reviews and automated checks pass;
- no unresolved high-severity review comment remains.

---

## 1. Engineering principles

| Principle | Standard | Why it exists |
|---|---|---|
| Code quality | Prefer simple, explicit, typed designs; remove dead paths; make invalid states difficult to represent | Correctness and contributor trust matter more than cleverness |
| Readability | Optimize for the next unfamiliar contributor; use domain language and small coherent units | Open-source code is read and reviewed far more often than it is authored |
| Maintainability | Keep modules cohesive, dependencies directed, migrations reversible/forward-safe, and contracts versioned | The platform must evolve without recurring rewrites |
| Developer experience | One documented setup path, fast focused checks, actionable errors, deterministic fixtures and safe local defaults | Low-friction contribution increases both participation and quality |
| Security first | Threat-model boundaries; deny by default; minimize data/capabilities; never defer known critical controls | Student identity, location intent, messages and academic relationships are sensitive |
| Privacy by design | Collect the minimum, keep Presence ephemeral, suppress small cohorts and separate public/private projections | Privacy cannot be reliably bolted on after data contracts ship |
| Accessibility | Keyboard, screen reader, focus, contrast, reduced motion and responsive behavior are acceptance criteria | Accessibility is core product quality, not optional polish |
| API first | UI/mobile/plugins consume stable application contracts, not implementation details | Independent clients and self-hosted versions need predictable behavior |
| Documentation first | Cross-cutting changes update design/decision docs before or with code | Shared decisions must outlive meetings and individual maintainers |
| Testing first | Define acceptance and failure cases before implementation; add regression tests with every bug fix | Time-based/concurrent workflows cannot rely on manual confidence |
| Performance with evidence | Establish budgets, measure realistic workloads, then optimize the bottleneck | Premature optimization creates complexity; ignored performance creates unusable systems |
| Open-source friendly | Prefer inspectable, portable, license-compatible, self-hostable solutions and public decision records | Contributors and operators must not depend on private infrastructure or tribal knowledge |
| Operational ownership | The author designs logs, metrics, recovery, rollout and rollback alongside behavior | Shipping includes operating the change when dependencies fail |
| Constructive safety | Reliability and moderation features must avoid public shaming and hidden punitive automation | Product integrity includes fair, humane behavior |

### 1.1 Engineering values in practice

- Correctness beats throughput when capacity, RSVP, attendance, permissions, consent or reliability are involved.
- Boring, documented technology beats novel infrastructure unless measurements show a real gap.
- A modular monolith is not permission to create arbitrary imports; boundaries are actively enforced.
- Eventual consistency is acceptable for projections and delivery, never as an excuse for ambiguous canonical state.
- Every exception has an owner, reason, expiration/review point and follow-up issue when debt remains.
- Review feedback addresses the code and design, never the contributor.

---

## 2. Project structure and ownership

### 2.1 Canonical repository layout

| Path | Ownership and permitted contents |
|---|---|
| `apps/web/` | Next.js application: student/admin surfaces, route composition, frontend feature modules, public assets and web-specific tests |
| `apps/api/` | Python backend release: domain/application modules, HTTP adapters, worker and realtime entry points, provider adapters and backend tests |
| `packages/ui/` | Framework-compatible accessible design-system primitives, tokens, composed shared components and visual documentation |
| `packages/contracts/` | Generated/hand-reviewed shared API, event and realtime contract artifacts derived from canonical specifications; no business logic |
| `packages/types/` | Cross-package TypeScript types that are not transport-generated; must have a clear owner and stable purpose |
| `packages/utils/` | Small environment-neutral utilities with no domain ownership; a dumping ground is prohibited |
| `packages/config/` | Shared lint, format, TypeScript, test and build configuration |
| `packages/plugin-sdk/` | Versioned plugin client types/helpers, manifest validation and test fixtures; no privileged core access |
| `plugins/` | First-party/reference plugins and examples, each isolated with manifest, license/dependency and test metadata |
| `docs/` | Product, architecture, database, API, contributor, operator, RFC, ADR and user documentation |
| `scripts/` | Reusable repository automation with help, safe defaults, validation and tests for nontrivial behavior |
| `.github/` | Issue/PR templates, CODEOWNERS, workflows, labels/configuration and security/community metadata |
| `tests/` | Cross-application end-to-end, contract, load, accessibility, recovery and security suites; unit tests stay near owned code |
| `docker/` | Reference development/self-host container definitions and safe entrypoint/config templates |
| `infra/` | Optional cloud/deployment examples that remain provider-isolated; not required for local development |
| `examples/` | Minimal supported integration examples; tested or clearly version-pinned |

No new top-level directory is added without maintainer approval and a handbook/layout update. Empty speculative packages are not created for future features.

### 2.2 Placement rules

| Change | Location |
|---|---|
| Backend domain behavior | Owning module under `apps/api/`; framework-independent domain/application layers |
| REST/WebSocket adapter | Backend interface/transport area under `apps/api/`; calls application services |
| Worker job | Owning backend module plus worker adapter/registration; durable behavior stays in application layer |
| React route/feature | Feature area under `apps/web/`; shared primitive only when reused and generic |
| Shared accessible UI | `packages/ui/` after proving at least two consumers or foundational design-system need |
| API/event type | Canonical specification first, then generated/verified artifact in `packages/contracts/` |
| Unit/component test | Adjacent to the module/component using the repository naming convention |
| Integration test | Backend/frontend module test area when one application; `tests/` when crossing boundaries |
| End-to-end/load/security/recovery test | Matching suite under `tests/` |
| Documentation | `docs/`; brief package-specific usage may live beside package README |
| Static web asset | `apps/web/public/` or owned feature assets; design-system assets in `packages/ui/` |
| Plugin | Its own folder under `plugins/`; never inside core domain packages |
| Development automation | `scripts/` or package scripts; CI orchestration in `.github/workflows/` |

### 2.3 Ownership

Every major path has CODEOWNERS. Ownership means stewardship, not private control: owners review boundary changes, maintain tests/docs, triage regressions, communicate deprecations and recruit additional reviewers. A contributor may change any area through review. No area may depend indefinitely on a single maintainer.

Cross-cutting changes identify one coordinating owner and affected code owners. Generated files identify their source and regeneration command; contributors do not hand-edit them.

---

## 3. Coding standards

### 3.1 General standards

- Use repository formatters and linters without manual style debates. CI is authoritative.
- Keep domain terms aligned with canonical documents: Activity, Activity series, Campus Presence, Need Help, compatibility, reliability and University scope.
- Prefer explicit data flow and dependency injection over hidden globals, service locators or import-time side effects.
- Use early validation and clear return paths. Avoid deeply nested conditionals and boolean parameter puzzles.
- Do not duplicate business rules across UI, API, workers and plugins. UI validation improves feedback; server domain policy remains authoritative.
- Represent time with timezone-aware instants and explicit IANA timezone for wall-clock/recurrence intent. Never use local machine timezone implicitly.
- Handle money-like precision, identifiers, percentages and durations with intentional types; do not rely on floating-point for exact policy arithmetic.
- Do not catch broad errors merely to continue. Catch at the layer that can add context, recover or translate safely.
- Temporary workarounds require a linked issue, owner and removal condition.

### 3.2 Naming conventions

| Item | TypeScript/React | Python | Examples/notes |
|---|---|---|---|
| Variables/functions | `camelCase` | `snake_case` | Use verbs for behavior: `calculateCompatibility`, `calculate_compatibility` |
| Classes/components | `PascalCase` | `PascalCase` | Nouns with domain intent; React components are PascalCase |
| Constants | `UPPER_SNAKE_CASE` for true module constants | `UPPER_SNAKE_CASE` | Do not uppercase values that are merely immutable bindings |
| Types/interfaces | `PascalCase` | `PascalCase` | TypeScript interfaces do not use an `I` prefix |
| Enums/stable keys | Type name `PascalCase`, serialized values `snake_case` | Same | Wire/database values follow finalized contracts |
| TypeScript files | kebab-case; component file may match component if repository tooling requires | — | Pick one convention per package; avoid case-only renames |
| Python files/modules | — | `snake_case.py` | Packages use `snake_case` |
| Folders | kebab-case for JS packages/features | `snake_case` for Python packages | Top-level names follow Section 2 |
| Tests | Subject + behavior suffix | `test_*.py` / repository TS suffix | Test name states scenario and expected result |
| Boolean names | `is`, `has`, `can`, `should` prefix | same semantic prefix | Avoid negative double meanings such as `disableNotHidden` |
| IDs | Type-qualified at boundaries when ambiguity exists | same | Never parse or infer ordering from opaque IDs |

Names explain why the value exists, not its incidental type. Avoid `data`, `item`, `manager`, `helper`, `utils`, `misc`, `temp`, and numbered variants unless the scope makes meaning unmistakable.

### 3.3 TypeScript standards

- Strict TypeScript is mandatory. `any`, unchecked casts and non-null assertions require a narrow documented reason; prefer `unknown` plus validation.
- Transport data is validated at the boundary and represented by generated/approved contract types. Domain/UI state does not import backend ORM concepts.
- Use discriminated unions for lifecycle/result variants and exhaustive handling for stable state machines.
- Public package exports are intentional through package entry points; deep internal imports are prohibited.
- Functions and components declare meaningful input/output types. Inference is welcome for obvious local values.
- Promises are awaited/returned intentionally; unhandled asynchronous work is prohibited.
- Avoid TypeScript enums when their runtime behavior is unnecessary; stable wire values come from contract-safe literal sets/types.

### 3.4 React and Next.js standards

- Components render UI and coordinate view behavior; business policy belongs in application/domain services or shared pure policy representations approved for display only.
- Prefer server rendering/components for read composition where appropriate; introduce client components only for actual interactivity/browser APIs.
- Hooks are unconditional, focused and named by behavior. Effects synchronize with external systems, not compute ordinary derived state.
- State has one owner. Do not copy query/server state into multiple local stores without a synchronization contract.
- React Query owns remote cache; optimistic updates are limited to reversible actions and always implement rollback/refetch.
- Capacity, RSVP, attendance, matching, reliability and permission outcomes show server-confirmed state.
- Every async surface has loading/skeleton, empty, error, retry and stale/disconnected behavior as applicable.
- Error boundaries exist at route/feature boundaries with accessible recovery.
- Components accept semantic props, not styling escape hatches that bypass the design system.

### 3.5 Tailwind and UI standards

- Use design tokens and shared accessible primitives; do not scatter arbitrary colors, spacing, shadows or z-index values.
- Tailwind classes stay near the component; repeated complex patterns graduate to a component/variant, not a global utility string constant.
- Dynamic class names must be statically discoverable or explicitly safelisted through reviewed configuration.
- shadcn/ui-derived components become project-owned code and must be reviewed for accessibility, tokens and API consistency before adoption.
- Dark mode, reduced motion, zoom/reflow and responsive behavior are tested with every visual feature.
- Inline styles are reserved for truly computed values; CSS modules/global CSS require a clear use case and ownership.

### 3.6 Python and FastAPI standards

- Supported Python version and tooling are pinned at repository level. All production functions use modern type annotations; public module interfaces pass strict type checks.
- Domain and application modules do not import FastAPI request/response classes, HTTP status codes, SQLAlchemy sessions or provider SDKs.
- FastAPI adapters parse/authenticate/authorize at the boundary, call application services, and translate approved results/errors.
- Pydantic/request models are transport contracts, not persistence/domain models. ORM entities are never serialized directly.
- SQLAlchemy access is repository/unit-of-work owned. Queries are explicit, tenant-scoped and reviewed for loading/locking behavior.
- Async is used for concurrent I/O, not as decoration. Blocking work does not run on the event loop.
- Background jobs call the same application policies as HTTP and remain idempotent under duplicate delivery.
- Module import must not connect to services, apply migrations, start workers or read mutable external state.

### 3.7 Comments and docstrings

Comments explain rationale, invariants, non-obvious safety constraints, protocol quirks and links to decisions. They do not narrate syntax or preserve deleted code. TODOs include an issue reference and intended resolution.

Public APIs, extension points, complex domain policies and reusable packages require docstrings/API documentation that describe contract, parameters, result, errors, side effects, concurrency and security assumptions. Private obvious functions do not need ceremonial docstrings.

### 3.8 Imports and formatting

Automated tools own formatting and import sorting. Imports flow from standard/runtime libraries to external dependencies to workspace/public modules to local modules according to language tooling. Circular imports, wildcard imports, deep package internals and path aliases that hide boundary violations are prohibited.

### 3.9 Size recommendations

| Unit | Review signal | Required response when exceeded materially |
|---|---:|---|
| Function/method | About 40 logical lines | Extract coherent behavior or explain why locality is safer |
| React component | About 200 lines | Separate view sections/hooks/policies without fragmenting semantics |
| Production source file | About 400 lines | Split by responsibility; generated/reference vocabularies are exceptions |
| Test file | About 600 lines | Split by behavior/state-machine area while preserving readable fixtures |
| Pull request | About 400 changed production lines | Stage into reviewable commits/PRs or explain why atomicity requires size |

These are design prompts, not automated failure thresholds. Tiny fragmented functions/files can be worse than a coherent larger unit. Complexity, coupling and reviewability matter more than raw lines.

---

## 4. Architecture rules

### 4.1 Dependency direction

| Layer/module | May depend on | Must not depend on |
|---|---|---|
| Web UI/routes | Frontend feature services, contracts, UI packages | Database/ORM, worker internals, plugin private code |
| Frontend feature/application | Approved API/realtime clients, pure view models | Backend source modules, provider credentials, canonical policy mutation |
| HTTP/WebSocket adapters | Application services, transport schemas, auth context | UI, direct cross-module table writes, external calls inside transaction |
| Application services | Domain policies, owned repositories, ports, transaction/outbox abstraction | FastAPI/React, concrete provider UI, another module's repository internals |
| Domain model/policies | Domain types and pure standard-library utilities | Frameworks, database, Redis, HTTP, provider SDKs, environment variables |
| Repositories | Owned persistence models/query policy | Controllers/routes/UI, external notification/plugin calls |
| Workers | Application services and durable job interfaces | UI, route handlers, memory-only business timers |
| Realtime gateway | Authentication/subscription policy, minimal event envelopes | Canonical business mutation or history storage |
| Plugins | Public SDK/API/events and granted capabilities | Core imports, core database/Redis/filesystem/secrets |

### 4.2 Mandatory architecture rules

- Business logic never lives only in UI, route handlers, ORM callbacks, migration scripts or plugins.
- UI and plugins never access PostgreSQL, Redis, object storage credentials or internal provider APIs directly.
- Repositories do not call controllers, application services, workers, plugins or notification providers.
- Cross-module writes use the owning application's public interface. Shared database access does not mean shared ownership.
- Commands commit canonical state, audit and outbox intent together. External delivery happens after commit.
- Events are immutable, versioned, minimal and ordered only per aggregate. Corrections publish new facts.
- Redis/cache/search/recommendation/analytics projections never authorize access or become the only business record.
- Workers and event consumers are idempotent and safe after crashes, duplicates and out-of-order delivery.
- WebSocket messages are advisory/invalidation; clients resync through authoritative REST.
- Plugins run outside the trusted core, receive explicit capabilities and cannot register synchronous pre-commit hooks.
- Time-based workflows use durable scheduled work and server time, not browser/in-memory timers for correctness.
- Architecture-level changes update the C4 views and an ADR/RFC as required before merge.

### 4.3 Boundary enforcement

Use package exports, dependency rules, static import checks, CODEOWNERS and architecture tests. A boundary violation is not accepted because “it is only one import.” Temporary exceptions require an ADR or tracked removal issue, owner and date/release checkpoint.

---

## 5. Git workflow

### 5.1 Branch model

`main` is protected, always releasable and the source of normal releases. StudyHive uses short-lived trunk-based development rather than a permanent `develop` branch; a second long-lived integration branch causes drift and delays feedback.

| Branch | Purpose | Lifetime |
|---|---|---|
| `main` | Protected canonical history | Permanent |
| `feat/{issue}-{slug}` | Product/engineering capability | Days; rebase/update frequently |
| `fix/{issue}-{slug}` | Non-emergency defect | Days |
| `docs/{issue}-{slug}` | Documentation-only change | Short |
| `refactor/{issue}-{slug}` | Behavior-preserving structure change | Short |
| `chore/{issue}-{slug}` | Maintenance/tooling/dependency work | Short |
| `release/v{major}.{minor}` | Brief stabilization and supported patch line | Only while release/support policy requires |
| `hotfix/{issue}-{slug}` | Urgent supported-release correction | Until fix is merged/cherry-picked and released |
| `codex/{slug}` | Automated Codex-authored branch where tooling requires this prefix | Short; same review rules |

External contributors normally work from a fork and may use equivalent branch names. Branches do not include contributor names, secrets or issue titles containing private data.

### 5.2 Merge strategy

- Pull requests target `main` unless they are an approved supported-release patch.
- Squash merge is the default; the PR title becomes the Conventional Commit subject and the body preserves issue/decision context.
- Rebase merge is reserved for a curated series where individual commits are independently meaningful and compliant.
- Merge commits are limited to release/exception workflows approved by maintainers.
- Force-push is allowed on contributor branches with coordination, never on protected/shared release branches.
- Hotfixes merge to the supported release branch and are promptly merged/cherry-picked forward to `main` with conflict tests.
- Release branches accept fixes only, not new features/refactors/dependency churn unrelated to release safety.

### 5.3 Keeping branches current

Resolve conflicts in the contributor branch, rerun affected checks, and request re-review when resolution changes behavior. Do not “resolve” generated lockfiles/contracts by choosing one side blindly; regenerate from the reconciled sources.

---

## 6. Commit standards

StudyHive uses Conventional Commits for commit/PR titles.

| Type | Use | Example subject |
|---|---|---|
| `feat` | New user/developer capability | `feat(activities): support weekly recurrence previews` |
| `fix` | Correct incorrect behavior | `fix(rsvp): prevent late confirmation from restoring a seat` |
| `docs` | Documentation only | `docs(api): clarify cursor invalidation behavior` |
| `test` | Tests/fixtures without production behavior | `test(attendance): cover duplicate check-in events` |
| `build` | Build/package tooling | `build(web): align workspace compilation targets` |
| `ci` | Continuous-integration workflow | `ci(security): add dependency license check` |
| `perf` | Measured performance improvement | `perf(search): reduce authorized hydration queries` |
| `refactor` | Behavior-preserving structure | `refactor(presence): isolate threshold policy` |
| `style` | Formatting only; no behavior | `style(api): apply formatter updates` |
| `chore` | Maintenance not fitting another type | `chore(repo): refresh contributor labels` |
| `revert` | Revert a specific change | `revert: feat(activities): support weekly recurrence previews` |

### 6.1 Commit format

Format: `type(optional-scope): imperative summary`. Keep the subject concise, lowercase after the colon unless a proper noun requires capitalization, and omit a trailing period. The body explains motivation, important tradeoffs and migration/compatibility impact. Footers link issues (`Closes #123`), co-authors and breaking changes.

Breaking changes use `!` and a `BREAKING CHANGE:` footer, require an approved RFC/major-version or migration plan, and cannot be hidden in `chore` or dependency updates.

Commits must not contain generated noise unrelated to the change, secrets, personal student data, binaries without review, commented-out code or “fix review” messages. During review, imperfect local commits are acceptable; the final squash title/body must be clean.

---

## 7. Pull request process

### 7.1 Before opening

- Confirm or open an issue for nontrivial behavior; align on scope before large implementation.
- Read relevant canonical documents, local README/ownership and open RFC/ADR.
- Keep the change focused; separate refactors, dependency upgrades and generated churn unless inseparable.
- Run the documented focused format, lint, type, unit and relevant integration checks.
- Update tests, docs, changelog/release notes and screenshots/accessibility evidence as required.
- Self-review the diff for secrets, debug code, accidental API/schema changes and generated files.

Draft PRs are encouraged for early design/CI feedback but must not request final review until the checklist is honest and the change is coherent.

### 7.2 PR description requirements

Every nontrivial PR includes:

- problem and user/contributor impact;
- linked issue/spec/RFC/ADR;
- chosen approach and important alternatives;
- test evidence and exact affected suites;
- security/privacy/accessibility impact;
- API/database/event/plugin/backward-compatibility impact;
- rollout, migration, feature flag and rollback plan when applicable;
- UI evidence across relevant viewport/theme/state when visual;
- documentation/changelog status;
- known limitations and follow-up issues.

### 7.3 Review and approval requirements

| Change class | Minimum approval |
|---|---|
| Documentation typo/obvious low-risk maintenance | One reviewer with area authority; maintainers may fast-track after checks |
| Normal product/code change | One approving maintainer or designated reviewer plus CODEOWNER coverage |
| Authentication, authorization, privacy, reliability, moderation, secrets or security boundary | Two approvals including Security/owning maintainer |
| Public API, database migration/model, event/realtime contract, plugin capability, architecture boundary | Two approvals including relevant CODEOWNER/maintainer |
| Release workflow, dependency trust policy or governance change | Two maintainer approvals; Core Team/RFC when policy requires |

Authors do not approve their own PR. Approval becomes stale after material changes to behavior, migration, security or generated contract. Maintainers may require specialist review even when numeric approvals are met.

### 7.4 Merge rules

Before merge:

- required checks pass on the final commit;
- required approvals are current;
- all blocking conversations are resolved by reviewer or with reviewer agreement;
- no merge conflict exists;
- PR title follows Conventional Commits;
- breaking behavior has approved migration/deprecation;
- rollout owner and rollback are clear for risky changes;
- linked issue/milestone/project status is correct.

Maintainers may merge once requirements pass; contributors need not ping repeatedly. Emergency merges follow the security/incident process, require retrospective review/tests/docs and never bypass audit silently.

### 7.5 Reviewer responsibilities

Reviewers verify correctness and risks, reproduce unclear behavior, distinguish blocking issues from suggestions, explain why, and respond in a reasonable project-defined window. They do not demand unrelated refactors or personal style. Authors respond to every blocking comment with a change, evidence or reasoned discussion; silent resolution is discouraged.

Conflict resolution is evidence-driven: canonical requirements, tests, measurements, threat models and user research first. Unresolved design disagreements escalate to module maintainers, then RFC/Core Team according to Section 19.

---

## 8. Testing standards

### 8.1 Test portfolio

| Test type | Purpose | Required examples |
|---|---|---|
| Unit | Pure policy/component behavior | compatibility math, lifecycle guards, validators, formatting, UI state reducers |
| Property/model | Invariants over generated sequences | capacity never exceeded, state terminality, idempotency, recurrence/DST boundaries |
| Integration | Real owned dependencies | PostgreSQL constraints/locks/outbox, Redis TTL/degradation, storage adapter, provider contracts |
| API contract | Stable HTTP behavior | envelopes, errors, auth/field filtering, pagination, version conflict, idempotency |
| Realtime | WebSocket and multi-node behavior | authentication, subscriptions, gaps/resync, heartbeat, backpressure, Redis loss |
| Accessibility | Automated and manual interaction | keyboard order, screen reader names/live regions, focus recovery, contrast, zoom/reflow, reduced motion |
| Security | Negative/adversarial boundaries | IDOR/cross-tenant, CSRF/CORS, XSS, injection, SSRF, upload, token replay, plugin escape |
| Performance/load | Budgets and contention | hot Activity joins, search, reminder burst, reconnect storm, message/presence rate |
| End-to-end | Critical user journeys | onboarding, create/join/waitlist/RSVP/check-in, Presence, Need Help, report/block, erasure |
| Recovery/chaos | Failure behavior | worker crash, duplicate event, Redis/provider/storage loss, migration/restore |

### 8.2 Organization and naming

Tests live with their owner unless they cross applications/contracts. Name tests as behavior: condition/action/expected outcome. Python test names use `test_<behavior>_<condition>_<result>`; TypeScript descriptions use plain user/domain language. Avoid “works,” “test1,” implementation method names and issue-only names.

Arrange setup, action and assertion clearly without ceremonial comments. Prefer domain builders/factories with explicit overrides. Shared fixtures remain minimal and immutable; hidden global fixtures and order-dependent tests are prohibited.

### 8.3 Coverage expectations

Coverage is a diagnostic and regression gate, not a quality score.

- Repository coverage baseline must not decrease without an approved, explained exception.
- New/changed domain and application logic SHOULD reach at least 90% branch coverage.
- Security/permission rules and finalized state-machine/invariant transitions MUST have explicit positive and negative scenario coverage; critical matrices target complete branch/scenario coverage.
- UI components require interaction/accessibility assertions, not snapshot coverage alone.
- Generated code, declarative migration metadata and unreachable defensive provider branches may be excluded only through reviewed configuration.
- A reviewer may require tests regardless of percentage; high coverage never excuses weak assertions.

### 8.4 Determinism and test safety

Use controllable clocks, deterministic IDs/random seeds, isolated databases/namespaces and synthetic data. PostgreSQL behavior is tested on PostgreSQL, not SQLite substitution. Never call production providers or use real credentials/student data. Network tests use contract fakes or dedicated sandbox accounts and remain clearly separated.

Flaky tests are defects: quarantine only with maintainer approval, owner, linked issue and short expiration. Do not solve flakiness with arbitrary sleeps or excessive retries. Test retries may diagnose nondeterminism but cannot make a required suite appear healthy.

### 8.5 Test requirements by change

| Change | Minimum evidence |
|---|---|
| Bug fix | Reproduction test that fails before and passes after |
| API/event change | Contract fixtures for old/new clients and error cases |
| Database/migration | Upgrade from empty and supported prior snapshot, constraints/concurrency, rollback/forward plan |
| UI feature | Component/integration, accessibility checks, relevant end-to-end journey and visual states |
| Worker/retry behavior | Duplicate/crash/lease/time-boundary tests with fake clock |
| Performance change | Reproducible before/after workload and no correctness regression |
| Security fix | Private regression test where disclosure risk requires; public test after advisory policy permits |

---

## 9. Documentation standards

Documentation is part of the change, reviewed like code, and written for a named audience. A feature is incomplete when operators, integrators or contributors must inspect implementation to understand its contract.

### 9.1 Required documentation by change

| Change | Required documentation |
|---|---|
| User-facing behavior | User flow/edge states, release note and accessibility guidance where non-obvious |
| New module/cross-module dependency | Architecture/module ownership and C4 Level 2/3 update; ADR/RFC when required |
| API/realtime/event/webhook | Canonical API contract, examples, errors, compatibility/deprecation and contract fixture |
| Database/model/migration | DDS entities/relationships/index/query/retention update and migration/rollback operator note |
| Configuration/feature flag | Variable/flag reference, default, environments, security, rollout and removal plan |
| Plugin extension | Manifest/capabilities/events/config/storage/version compatibility and example |
| Operational behavior | Metrics/logs/alerts, health/degradation, backup/recovery and runbook |
| Security-sensitive behavior | Threat/privacy assumptions and safe operator/user guidance; vulnerability details follow disclosure policy |

Every feature document explains purpose, architecture/ownership, API or interaction, examples, validation/business rules, edge/failure cases, permissions/privacy, testing, operations, compatibility and future/deferred work as relevant.

### 9.2 README standards

The root README answers what StudyHive is, current maturity, key capabilities/non-goals, architecture summary, quick start, documentation map, contribution/security/community links, license and status. It does not make unverified performance/security claims or present future work as shipped.

Package/module READMEs state purpose, ownership, public entry points, dependencies, development/test instructions, extension boundaries and common failures. They do not duplicate canonical specifications; link to them and add local usage only.

### 9.3 Markdown and links

- Use descriptive headings, short paragraphs, CommonMark/GitHub-compatible tables/checklists and language-tagged examples.
- Add a blank line around headings, lists, tables and fences. Use sentence case headings.
- Links use descriptive text, relative repository paths when stable, and avoid “click here.”
- Images/diagrams include meaningful alternative text or an adjacent text explanation.
- Commands identify platform assumptions and destructive effects. Examples use placeholders, never real secrets/domains/student data.
- Avoid unexplained jargon, promotional absolutes and ableist/exclusionary language.
- Documentation checks validate links, formatting and generated references in CI.

### 9.4 Diagrams

- C4 is the maintained architecture notation: Level 1 context, Level 2 containers and Level 3 critical components. Level 4 appears only for durable complex code boundaries.
- Mermaid is preferred for reviewable ER, sequence, state and flow diagrams.
- Diagrams have a clear title/scope, match the written contract, avoid ornamental complexity and change in the same PR as the architecture.
- Do not create a new diagram when an existing canonical view can be updated. Ad hoc diagrams must not contradict C4/DDS/API sources.

### 9.5 Comments and generated reference docs

Code comments/docstrings follow Section 3.7. Generated API/contract references identify their canonical source and generator version. Generation drift is a CI error. Never hand-edit generated output to fix documentation; fix source/template and regenerate.

---

## 10. Security standards

### 10.1 Secure development requirements

- Threat-model new trust boundaries, sensitive data, authentication/authorization, uploads, callbacks, plugins and cross-tenant behavior before implementation.
- Deny by default. Derive tenant/role/relationship server-side and apply authorization before list pagination or resource disclosure.
- Use maintained libraries for cryptography, password hashing, OAuth/OIDC, parsing and sanitization. Custom cryptography is prohibited.
- Keep secrets out of source, commits, fixtures, screenshots, logs, errors, analytics, frontend bundles and generated artifacts.
- Validate input at trust boundaries and encode/sanitize output for its context. Parameterize database access.
- External URLs/providers use timeouts, size/redirect/network allowlists and SSRF defenses.
- File uploads remain quarantined until content inspection and malware policy succeed.
- Security controls fail closed where authority or sensitive source state cannot be read.

### 10.2 Secrets and environment variables

Secrets come from local ignored files, container secrets or a secret manager. `.env.example` contains names and safe placeholders only. A discovered secret is treated as compromised: stop exposure, notify maintainers/security privately, revoke/rotate, remove where feasible, assess logs/artifacts and document the incident. Rewriting Git history alone is not remediation.

Environment variables are read through validated configuration, not scattered calls. Secret values use redacted wrapper/types where practical and never stringify accidentally.

### 10.3 Automated security checks

Required CI/release checks include secret scanning, dependency vulnerability review, license policy, static analysis, type/lint checks, container/image scanning where produced, infrastructure/config scanning, and targeted dynamic/security tests. Findings are triaged by exploitability and data/tenant impact, not suppressed solely to make CI green.

Suppressions require issue, owner, rationale, scope, compensating control and expiry. Critical exploitable findings block release. High findings require maintainer/security disposition before merge/release.

### 10.4 Vulnerability reporting and disclosure

Potential vulnerabilities are reported through the private channel in `SECURITY.md`, not a public issue/PR/discussion. Maintainers acknowledge, triage, reproduce, coordinate a fix/advisory/CVE where applicable, credit the reporter by consent, and disclose after supported releases/mitigations are ready. Good-faith research under the published policy is treated respectfully.

Security fixes minimize public exploit detail until coordinated disclosure. Embargoed branches, logs and tests follow least access. After disclosure, public regression tests and lessons update standards/design where safe.

### 10.5 Security review triggers

Mandatory Security/code-owner review applies to authentication/session/recovery, authorization/roles/tenant boundaries, Presence/location/privacy, reliability/moderation, uploads/content rendering, webhook/SSRF, secrets/encryption, plugin capabilities/isolation, dependency with install/runtime scripts, or collection/retention of new personal data.

---

## 11. Dependency management

### 11.1 Adding a dependency

A dependency proposal answers:

- What maintained problem does it solve better than current platform/workspace code?
- Is it actively maintained, typed/tested, appropriately scoped and compatible with supported runtimes?
- What are direct/transitive size, build, startup, performance and operational costs?
- What network/filesystem/install-script/native-binary privileges does it use?
- Is its license compatible with the project and intended distribution?
- What is the exit/replacement strategy, especially for auth/storage/provider/plugin boundaries?

Small convenience dependencies are discouraged when a clear local implementation is safer and cheaper. Security/cryptography/protocol behavior generally favors established maintained libraries.

### 11.2 Approval and placement

Production runtime dependencies require owning maintainer approval. Security-sensitive/native/install-script or foundational dependencies require Security/relevant code-owner approval. Development-only tools require tooling owner approval when they affect all contributors/CI.

Add dependencies to the narrowest workspace/app that uses them. Root dependencies are repository-wide tooling only. Backend provider SDKs live behind adapter ports; frontend packages do not import server-only dependencies.

### 11.3 Pinning and lockfiles

- Applications and developer tooling use committed deterministic lockfiles.
- Direct dependency ranges follow ecosystem/release policy; deployed images/installations resolve from the lockfile, not floating ranges.
- Python lock/constraint artifacts and Node workspace lockfiles change only through approved tooling.
- Container base images and CI actions use immutable digest/commit pinning where practical, with automated update support.
- Never hand-resolve lockfile conflicts; reconcile manifests and regenerate.

### 11.4 Upgrade policy

Automated dependency PRs are grouped by risk/ecosystem, include release/security notes, and run full relevant checks. Patch/minor upgrades are regular maintenance; majors require migration/compatibility review. Security updates are prioritized by exploitability and supported-release exposure, not blindly merged.

Unsupported/unmaintained dependencies receive replace/remove plans. Removal deletes unused adapters/config/types/tests/docs and verifies bundle/image/license changes.

### 11.5 License policy

Dependencies and copied assets/code must have clear provenance and a license compatible with the project, distribution and plugin model. Strong copyleft/network-copyleft, source-available, noncommercial, field-of-use-restricted or unknown licenses require explicit legal/maintainer review and cannot be assumed compatible. Preserve required notices/attribution and generate a release dependency/license inventory.

---

## 12. Error handling

### 12.1 Error categories

| Category | Handling |
|---|---|
| Validation/domain | Return stable safe API error; expected outcome, usually no error-level log |
| Authentication/authorization | Conceal as specified, audit security-relevant patterns, never leak resource/credential detail |
| Concurrency/conflict | Return current version/safe next action; client refetches/reconciles |
| Dependency/provider | Timeout/circuit-break; retry only classified transient failures; preserve canonical state |
| Programming/invariant | Fail request/job safely, log error with correlation, alert by severity; never convert to misleading success |
| Cancellation/shutdown | Propagate cooperative cancellation and release resources; do not log expected shutdown as failure |

### 12.2 Layer responsibilities

- Domain errors use framework-independent stable categories and safe structured context.
- Application services translate domain/repository/provider outcomes into approved use-case results and decide compensation/retry intent.
- API adapters map approved errors to the Part 5 envelope/status without exposing internal types.
- Workers classify retryable/permanent/stale work, record attempts, and dead-letter with redacted context after policy.
- UI maps stable codes to accessible human guidance and preserves user input where safe; it does not show raw exception text.

### 12.3 Exception rules

Do not use exceptions for ordinary expected branching when a typed result is clearer. Do not catch and rethrow without added context. Preserve causal chains internally. Never catch the base process-control/cancellation classes accidentally. Cleanup uses structured context/finalization and is itself failure-aware.

Error messages state what failed and what the user/operator can do, without blame, false certainty or secrets. Stable machine codes drive clients; localized text may evolve.

### 12.4 Retries and recovery

Retry only transient, idempotent or idempotency-protected work. Use bounded exponential backoff with jitter, deadlines and attempt budgets. Do not retry validation, permission, version conflict, expired offer/prompt or permanent provider rejection unchanged. A retry storm is prevented through circuit breakers/backpressure and shared budgets.

Compensation is explicit: quarantined upload remains unavailable, plugin remains disabled, notification remains pending/failed, and projection remains stale. Never roll back a committed canonical Activity because email/plugin delivery failed.

---

## 13. Logging standards

### 13.1 Levels

| Level | Use | Example class |
|---|---|---|
| Trace | Extremely detailed short-lived local diagnostics; disabled in normal production | State-machine internal steps without personal payload |
| Debug | Developer/operator diagnostics useful for investigating a component | Cache miss class, worker claim decision with opaque ID |
| Info | Normal meaningful lifecycle/operation summary | Service start, migration version, job batch summary, plugin enabled |
| Warning | Unexpected/degraded but recovered or actionable trend | Provider circuit opened, stale projection, repeated reconnect, retry scheduled |
| Error | Operation failed or invariant/dependency requires attention | Exhausted job, unhandled request failure, object scan service failure |
| Fatal/Critical | Process cannot safely continue or data/security boundary may be compromised | Incompatible schema, missing required secret, canonical store integrity failure |

Expected user validation, `404`, normal `409` and routine rate limiting are not logged as errors. Severity follows operational action, not emotion.

### 13.2 Structured log fields

Logs are structured and include timestamp, level, service/runtime, environment, release, message/event key, request/trace/job/event ID, route/operation, duration/outcome and safe opaque tenant/actor/resource IDs only when needed. Dynamic values are fields, not string-concatenated messages.

### 13.3 Sensitive-data prohibition

Never log passwords, tokens/cookies/authorization headers, verification/recovery codes, plugin secrets, push endpoints/keys, raw email addresses, message/note bodies, upload content, exact Presence/location, hidden preferences, individual reliability evidence, confidential moderation detail, SQL parameters or full provider payloads. IP/User-Agent are security data with controlled hashing/retention and access.

Redaction occurs before data reaches the logger. “Debug only” is not permission to log sensitive data. Log access and retention follow least privilege; production log export is encrypted and auditable.

### 13.4 Logging quality

One layer logs a failure; lower layers add context through structured error propagation rather than duplicate stack spam. High-volume success paths are sampled/aggregated. Security/audit facts use the dedicated immutable audit mechanism and are not dependent on application log sampling.

---

## 14. Observability standards

### 14.1 Required signals

Every production capability identifies:

- service-level indicators for success, latency and freshness;
- structured logs with correlation and redaction;
- distributed trace spans across API/database/cache/worker/provider boundaries;
- metrics for throughput, errors, saturation, queue/oldest age, retries/DLQ and domain integrity;
- liveness/readiness/deep-diagnostic behavior;
- dashboards, alert thresholds/runbooks and an owner;
- expected degradation and recovery signal.

### 14.2 Metrics conventions

Metric names/units are stable, documented and low-cardinality. Labels use route templates, operation/event/job type, result class, runtime/release and opaque bounded tenant grouping when justified. Never label by raw User/resource ID, email, query, URL, exception message or plugin callback.

Counters only increase; gauges represent current state; histograms capture latency/size distributions with reviewed buckets. Product analytics and operational telemetry remain separated. Admin product metrics preserve cohort suppression/privacy.

### 14.3 Tracing

Trace meaningful boundaries and expensive operations, not every helper. Propagate context through durable jobs/events/webhooks using safe trace IDs without trusting external baggage. Add aggregate/job/event IDs as controlled span attributes; exclude content/secrets. Sampling retains errors/high-latency exemplars under privacy policy.

### 14.4 Health checks and alerts

- Liveness tests process health only and does not fail because an optional provider is down.
- Readiness verifies required dependency reachability/config/schema compatibility for that runtime role.
- Deep diagnostics are authenticated/operator-only and may test providers safely.
- Alerts target user-impacting symptoms, SLO burn, oldest work age, integrity/security conditions and saturation—not every isolated exception.
- Every paging alert links a runbook and has an owner, severity, silence/escalation and validation cadence.

Observability additions are tested for label cardinality, redaction and failure safety. Telemetry failure does not crash business operations unless audit/security requirements cannot be met safely.

---

## 15. Configuration standards

### 15.1 Sources and precedence

Configuration has one typed, validated composition layer. Precedence is documented and deterministic: built-in safe defaults → configuration file/profile where supported → environment variables/container secrets → explicit startup arguments for operator-only cases. Feature flags and dynamic tenant policy use their owned configuration service/data, not environment variables per request.

### 15.2 Environment variables

Names use a stable project prefix and uppercase snake case. Each variable documents purpose, type, required/default, allowed values, secret status, environments, reload/restart behavior and deprecation. Empty, missing and malformed values are distinct and validated at startup.

Do not introduce environment variables for ordinary product behavior that belongs in versioned admin configuration. Do not read variables throughout domain code. Public web variables are explicitly allowlisted and contain no secrets/internal URLs.

### 15.3 Environment profiles

| Environment | Standard |
|---|---|
| Development | Safe local defaults, local storage/mail sink, seeded synthetic demo option, verbose diagnostics without sensitive data |
| Test | Deterministic isolated values, fake clocks/providers, no developer/prod credential fallback |
| CI | Same as test with explicit service versions and no network except approved dependency/setup steps |
| Staging | Production-like topology/config, synthetic/test identities, separate credentials/data/providers |
| Production | No unsafe defaults; secret manager/container secrets, TLS/private networks, validated origins/providers, backups/alerts |

The application refuses production startup with development secrets, wildcard credentialed CORS, incompatible schema, missing encryption/signing material or local storage in an unsupported multi-node profile.

### 15.4 Feature flags

Every flag has owner, purpose, type, safe default, audience/scope, creation date, rollout/rollback metric, security/privacy behavior and removal issue/date. Flags do not bypass authorization, migrations or mandatory safety/accessibility controls. Code supports both states until rollout completes; tests cover both. Long-lived operational settings graduate from flags to owned configuration.

### 15.5 Secret rotation

Rotation supports bounded overlap for signing/session/webhook keys where protocol requires it, identifies active/retiring versions, and has an operator runbook. Secrets are never returned after initial provisioning and are redacted in admin/API/config dumps.

---

## 16. Plugin development standards

### 16.1 Lifecycle and packaging

A plugin follows discovered → validated → installed-disabled → enabled → disabled/upgrading → uninstalled. Its manifest declares stable ID/publisher/version, core/API/event compatibility, requested capabilities, configuration schema, callback/event subscriptions, storage migration version, UI slots, dependencies, license and resource/network needs.

Each plugin directory includes a README, manifest, license/provenance, security/privacy notes, configuration reference, capability rationale, event/idempotency behavior, data export/erasure/retention contract, migration/rollback guidance, tests and changelog.

### 16.2 Versioning and compatibility

Plugins use Semantic Versioning independently unless shipped as a tightly coupled first-party package. Breaking manifest/config/storage/event behavior requires a major version and migration guidance. A plugin declares a tested core compatibility range and must fail/disable safely outside it.

Configuration schemas and migrations are immutable once released. Upgrade migrations are ordered, checksummed, idempotent/restartable and run only through explicit lifecycle workflow. Downgrade is supported only when declared safe.

### 16.3 Permissions and isolation

- Request the fewest granular capabilities and tenant/resources necessary; optional features request optional grants.
- Never infer authority from installer identity, User-provided IDs, webhook payload or UI context.
- Use installation-scoped short-lived credentials and SDK/API; no core database/Redis/filesystem/secrets access.
- Store plugin data in plugin-owned isolated storage and reference core resources by opaque public ID.
- Treat webhook delivery as at least once, verify signature/timestamp, deduplicate event ID and refetch current state after version gaps.
- Sandbox UI in declared slots/origin and communicate through the approved bridge. Do not inject scripts/styles into the core page.
- Network destinations, resource limits and secret references are declared and operator-visible.

### 16.4 Hooks and dependencies

Hooks are after-commit events or explicit API commands. Plugins cannot block, mutate or veto a core transaction synchronously. Timeouts/failures degrade the plugin only.

Plugin dependencies follow Section 11 and must not rely on undeclared global packages. Bundle/runtime size and install scripts receive heightened review because operators execute third-party code.

### 16.5 Testing and review

Plugins test manifest/config validation, capability denial, tenant isolation, duplicate/out-of-order events, timeout/retry, disable/revoke, migration upgrade/failure, export/erasure and core compatibility fixtures. UI plugins meet Section 17.

First-party/reference plugins use ordinary PR/code-owner/security review. Registry publication additionally verifies identity/provenance, license, artifact digest/signature, capability clarity, privacy/security docs, maintenance contact and compatibility. Publication is not a permanent trust guarantee; vulnerable/abandoned plugins may be delisted/disabled with notice.

### 16.6 Publishing checklist

- [ ] Stable plugin ID and SemVer tag match manifest/artifact.
- [ ] Core/API/event compatibility matrix passes.
- [ ] Capabilities are minimal, explained and exercised by tests.
- [ ] Configuration has no embedded secrets and migration is verified.
- [ ] Webhooks are signed, idempotent and gap-aware.
- [ ] Storage export/erasure/retention and uninstall are documented/tested.
- [ ] Dependencies/licenses/provenance and security scans pass.
- [ ] Accessibility and sandbox behavior pass for UI extensions.
- [ ] Changelog, upgrade/rollback and maintainer contact are current.

---

## 17. Accessibility standards

StudyHive targets WCAG 2.2 AA for supported user journeys and treats accessibility defects as product defects. Automated tools assist but do not replace keyboard, screen reader, zoom/reflow and user testing.

### 17.1 Semantic structure

- Use native HTML elements and controls before ARIA. Do not recreate buttons, links, checkboxes, dialogs, tables or headings with generic elements.
- Pages have one clear primary heading and logical hierarchy/landmarks. Lists/tables use correct semantics.
- Every control has an accessible name, role, state and instructions/error association. Placeholder text is not a label.
- Images have meaningful alternative text or empty alt when decorative. Complex visuals include an equivalent summary/data view.
- ARIA is reviewed and tested with the actual interaction; invalid/redundant ARIA is removed.

### 17.2 Keyboard and focus

- All actions work by keyboard without timing traps or hover-only controls.
- Tab order follows visual/logical order. Positive `tabindex` is prohibited.
- Focus indicators are visible in all themes and not removed without an accessible replacement.
- Dialogs/popovers/menus trap/manage focus only according to their pattern, close predictably with Escape when appropriate, and restore focus to the initiator/fallback.
- Route changes, optimistic errors, inserted waitlist/RSVP prompts and realtime updates move/announce focus only when necessary; unexpected focus theft is prohibited.
- Skip links and landmarks support repeated navigation.

### 17.3 Screen readers and dynamic content

Loading, errors, confirmation, connection loss, waitlist offers, RSVP/attendance deadlines and Need Help match status have concise live-region/status behavior. Do not announce every typing/presence/count update. Status is never communicated by color/icon alone.

Controls expose server-confirmed state and disabled reason where useful. Tables/rosters have headers/captions and responsive alternatives that preserve relationships. Dates/times include understandable locale/timezone context.

### 17.4 Contrast, motion and responsive behavior

- Text, controls, focus and meaningful graphics meet AA contrast in light/dark/high-contrast-supported themes.
- Test zoom/reflow at 200% and narrow width without horizontal scrolling except intrinsically two-dimensional content with an accessible alternative.
- Touch targets and spacing support motor accessibility; destructive/urgent actions are not adjacent without protection.
- Respect reduced-motion preference. Motion is brief, purposeful and never required to understand state; no looping decorative motion.
- Skeletons avoid flashing; time limits show remaining time and support extension where the product policy allows.
- Content works in portrait/landscape and with text spacing overrides without clipping essential controls.

### 17.5 Accessibility test gates

Every UI PR includes automated accessibility checks for changed components and manual keyboard review. Critical journeys additionally run scripted screen-reader checks before release: authentication/onboarding, Course join, Activity create/join/waitlist/RSVP/check-in/live, Presence, Need Help, report/block, reliability appeal and erasure/export.

Visual evidence covers relevant theme, responsive width, focus, loading, empty, error, disabled and realtime-disconnected states. Accessibility waivers require Accessibility maintainer approval, user impact, workaround, owner and near-term remediation issue; critical journey blockers cannot ship generally.

---

## 18. Release process

### 18.1 Versioning model

The core StudyHive product uses Semantic Versioning: major for intentional breaking operator/client/plugin contracts, minor for backward-compatible capabilities, patch for backward-compatible fixes/security/maintenance. Pre-release identifiers mark alpha/beta/release candidates. Package/plugin SDKs may version independently when their compatibility contract requires it.

Database migrations do not independently define product version, but each release declares supported upgrade origins and schema compatibility. A security fix may be backported without changing minor feature scope.

### 18.2 Release cadence and branches

Normal releases are cut from `main`. A short `release/vX.Y` branch is created only when stabilization/backport support warrants it. After branching, only release fixes, documentation, version/changelog and build metadata enter the branch. Every release-branch fix is merged forward to `main`.

Release candidate tags validate artifacts, self-host upgrades, rollback posture and plugin compatibility. Tags use `vMAJOR.MINOR.PATCH` and are signed/protected where project infrastructure permits. Published artifacts are immutable; a bad artifact receives a new patch version, never replacement under the same tag.

### 18.3 Release checklist

- [ ] Scope/milestone is complete; known issues and deferred items documented.
- [ ] Required CI, contract, migration, E2E, accessibility, security and representative load/recovery checks pass.
- [ ] Dependency/license/SBOM and container/artifact provenance checks pass.
- [ ] Upgrade from every supported prior version and clean install pass.
- [ ] Backup prerequisite, migration runtime/lock risk and rollback/fix-forward runbook are verified.
- [ ] API/event/realtime/plugin compatibility and deprecations are documented/tested.
- [ ] Release notes and changelog are complete, user-oriented and accurate.
- [ ] Configuration additions/deprecations, feature flags and operator actions are documented.
- [ ] Artifacts/images are signed/checksummed, reproducible enough for policy and tested before tag promotion.
- [ ] Observability dashboards/alerts/runbooks and on-call/release owner are ready.
- [ ] Security embargo/advisory timing and supported-version backports are coordinated.

### 18.4 Changelog and release notes

`CHANGELOG.md` contains an Unreleased section and groups Added, Changed, Deprecated, Removed, Fixed and Security. Entries describe impact, not commit mechanics, and link issue/PR/migration docs. Internal refactors without operator/contributor impact may be omitted.

Release notes highlight user/administrator/plugin changes, security fixes at appropriate disclosure level, breaking/deprecated contracts, migration/config actions, compatibility matrix, known issues and contributors. Never claim “production ready,” performance or security properties without evidence and scope.

### 18.5 Rollout and rollback

Risky features use staged feature flags, canary/pilot scope, success/guardrail metrics, owner and explicit stop/rollback conditions. Database expand–migrate–contract preserves code rollback across the documented window. When schema/data change is forward-only, the runbook states fix-forward or verified backup restore; it never promises unsafe downgrade.

Rollback includes application/artifact, configuration/flags, migrations/data, workers/events, plugins and cache/projection recovery. After rollback, reconcile outbox/jobs and verify no duplicated/lost canonical effects.

### 18.6 Hotfixes

Hotfixes are the smallest safe change for severe production/security regressions. They still require focused regression tests, appropriate owner/security review, release notes/advisory and forward merge. If emergency authority shortens normal gates, retrospective review and missing tests/docs occur immediately after stabilization.

---

## 19. Open-source governance

### 19.1 Contributor ladder

| Level | Typical responsibilities | How granted |
|---|---|---|
| Community member | Uses, reports, discusses, helps others | Participation under Code of Conduct |
| Contributor | Submits accepted code/docs/design/triage | First merged contribution |
| Trusted Contributor | Regular triage, issue reproduction, documentation, focused reviews | Maintainer nomination based on sustained quality/conduct |
| Reviewer | Reviews defined areas and may provide required non-maintainer approval where policy allows | Demonstrated expertise, judgment and availability; maintainer vote |
| Maintainer | Merge/release/ownership responsibility for modules; mentors/recruits successors | Existing maintainer nomination and documented approval |
| Core Team | Project-wide stewardship, governance/security/architecture escalation | Maintainer nomination and transparent project process |

Access follows least privilege and is reviewed periodically. Roles are not rewards for commit count. Criteria include technical/product judgment, security/privacy/accessibility care, review quality, reliability, inclusive conduct and community support. Contributors may decline roles.

Inactive privileged members are moved to emeritus/previous role respectfully after contact and documented inactivity policy; they may return through a lightweight review. Conflicts of interest are disclosed and recused.

### 19.2 Decision making

Routine changes use lazy consensus in issues/PRs under maintainer ownership. Seek input from affected users/maintainers, document alternatives and allow a reasonable review period proportional to impact. Maintainers decide within owned boundaries using canonical principles/evidence.

Cross-cutting, costly-to-reverse, governance, security/privacy model, public contract or architecture changes use an RFC. If consensus remains unavailable, affected maintainers present positions; Core Team decides transparently with rationale. Code of Conduct/security cases follow their confidential processes.

No important project decision depends solely on a private meeting/chat. Publish a summary and decision record, redacting confidential/security/personal information.

### 19.3 RFC process

RFC required for new major product/module scope, architecture/runtime/data ownership, public API/event/plugin contract break, new infrastructure dependency, authentication/tenant/privacy/reliability policy change, governance or support policy.

An RFC includes problem/context, goals/non-goals, proposal, user/developer/operator impact, alternatives, architecture/data/API/security/privacy/accessibility, migration/compatibility, rollout/rollback, testing/observability, unresolved questions and owner. Lifecycle: Draft → Discussion → Accepted/Rejected/Withdrawn → Implemented/Superseded.

Accepted RFCs are not immutable: material implementation discoveries return to discussion/amendment. Rejection records reasoning so proposals are not repeatedly relitigated without new evidence.

### 19.4 Architecture Decision Records

ADRs capture a specific technical decision within approved scope: context, decision, alternatives, consequences, status, date/owners and links. Status is Proposed, Accepted, Superseded or Deprecated. ADRs are append-oriented; do not rewrite history to make old decisions look current. A superseding ADR links both directions.

RFC chooses broad direction; ADR records consequential implementation/architecture choices. Small local choices belong in PR rationale, not an ADR.

### 19.5 Issues, labels, milestones and project boards

Label taxonomy is small and composable:

| Dimension | Examples |
|---|---|
| Type | `type:bug`, `type:feature`, `type:docs`, `type:security`, `type:maintenance`, `type:rfc` |
| Area | `area:web`, `area:api`, `area:activities`, `area:presence`, `area:plugins`, `area:docs`, `area:infra` |
| Status | `status:needs-triage`, `status:needs-design`, `status:ready`, `status:blocked`, `status:needs-info` |
| Priority | `priority:critical`, `priority:high`, `priority:medium`, `priority:low` |
| Contribution | `good first issue`, `help wanted`, `mentor available` |
| Impact | `security`, `accessibility`, `performance`, `breaking-change`, `privacy` |

Critical priority is reserved for severe security/data loss/outage/core journey failure. `good first issue` means scoped, documented, reproducible, unblocked and supported—not trivial cleanup no maintainer wants.

Milestones represent releases or time-bounded initiatives with owner/scope/exit criteria. Project boards show public workflow and dependencies; they do not become a second undocumented requirements source. Stale issues are closed only after notice and may be reopened with evidence.

### 19.6 Maintainer conduct

Maintainers model the Code of Conduct, explain decisions, avoid gatekeeping, protect embargoed/private data, disclose conflicts, credit contributors, share operational burden and create paths for new maintainers. Merge/release/admin access is never used to bypass review for personal convenience.

---

## 20. Code review checklist

Reviewers select every applicable item; “not applicable” is acceptable with context for high-risk categories.

### 20.1 Scope and correctness

- [ ] The problem, requirements and non-goals are clear and linked.
- [ ] Behavior matches finalized product/system/database/API contracts.
- [ ] Positive, negative, boundary, concurrent and failure cases are correct.
- [ ] State transitions, timezones/DST, idempotency and retries are explicit where relevant.
- [ ] No unrelated behavior, generated noise, dead code or hidden follow-up remains.

### 20.2 Architecture and maintainability

- [ ] Code belongs to the correct module/layer and dependency direction is valid.
- [ ] Business logic is not trapped in UI/routes/repositories/workers/plugins.
- [ ] Cross-module writes use owner interfaces; external calls occur after commit.
- [ ] Names/types/control flow are readable; complexity and duplication are justified.
- [ ] Public extension points/contracts are intentional and documented.

### 20.3 API, events and backward compatibility

- [ ] Endpoint/envelope/error/pagination/version/idempotency behavior matches Part 5.
- [ ] Event/realtime/webhook payload is minimal, immutable, versioned and duplicate/gap-safe.
- [ ] Existing clients/plugins tolerate the change; breaking/deprecation plan is approved.
- [ ] Unknown response values/fields and old/new contract fixtures are handled safely.

### 20.4 Database and data lifecycle

- [ ] Ownership, normalization, tenant scope, nullability, constraints and indexes match DDS.
- [ ] Transactions/locks/versions prevent races without broad/long locking.
- [ ] Query plan/loading/pagination and growth impact are understood.
- [ ] Migration is expand–migrate–contract, tested from supported versions and operationally safe.
- [ ] Soft delete, retention, archive, restore, export, erasure, audit and object cleanup are addressed.

### 20.5 Security and privacy

- [ ] Authentication, authorization, tenant/relationship/field scope and concealed-resource behavior are correct.
- [ ] Input/output, CSRF/CORS/XSS/injection/SSRF/upload/replay/mass-assignment threats are addressed.
- [ ] Secrets/sensitive data are absent from source, responses, logs, errors, metrics and fixtures.
- [ ] Data collection/retention is minimal; Presence/reliability/moderation/plugin boundaries remain safe.
- [ ] Rate limits, abuse controls, audit and Security review are present where triggered.

### 20.6 Frontend and accessibility

- [ ] UI uses shared tokens/primitives and has loading/empty/error/disabled/stale/disconnected states.
- [ ] Server-confirmed outcomes are used for capacity/RSVP/attendance/matching/reliability.
- [ ] Keyboard, focus, semantics, screen reader, contrast, reduced motion, zoom/reflow and responsive behavior pass.
- [ ] Light/dark themes and relevant viewport/content extremes are verified.
- [ ] Error/recovery language is constructive and does not shame or expose private state.

### 20.7 Tests, performance and operations

- [ ] Tests prove behavior rather than implementation and include a regression case for bugs.
- [ ] Tests are deterministic, isolated, realistic and not hidden by retries/snapshots alone.
- [ ] Performance claims have representative before/after evidence; no obvious N+1/unbounded work/cardinality.
- [ ] Logs/metrics/traces/health/alerts are useful, low-cardinality and redacted.
- [ ] Dependency failure, worker retry/DLQ, rollout, rollback and recovery are safe.

### 20.8 Documentation, dependencies and release

- [ ] User/contributor/operator/API/database/architecture docs and diagrams are updated.
- [ ] New configuration/flag has owner, safe default, docs, tests and removal plan.
- [ ] Dependency need, maintenance, security, size, license, pinning and exit path are acceptable.
- [ ] Changelog/release note/migration/compatibility impact is accurate.
- [ ] PR approvals, CODEOWNERS and all required checks apply to the final diff.

---

## 21. Engineering decisions

| Standard | Why chosen | Alternatives considered | Tradeoffs and future improvement |
|---|---|---|---|
| Short-lived branches from protected `main`; no permanent `develop` | Fast integration, fewer divergent branches, always-releasable trunk | Git Flow with `develop`; direct commits | Requires strong CI/flags; release branches remain for stabilization/backports |
| Squash merge by default | Clean searchable history and Conventional PR titles | Merge every commit; rebase-only | Loses granular review commits; PR preserves discussion and curated commits may rebase |
| Conventional Commits | Consistent history/changelog/release automation | Free-form subjects | Contributors learn syntax; templates/CI provide guidance |
| Modular ownership and directed dependency checks | Prevents modular monolith decay | Social convention only; microservices | Tooling/review maintenance; extraction remains possible after evidence |
| Framework-free domain/application core | Reuse policy across HTTP/workers/tests and reduce coupling | FastAPI/ORM-centric business logic | More adapters/types; materially improves testability and stability |
| Colocated unit tests, central cross-system suites | Clear ownership with discoverable end-to-end coverage | All tests central; all tests beside code | Two locations to learn; directory guide and test commands resolve it |
| Coverage baseline + risk-based expectations, not one vanity number | Rewards meaningful assertions and critical scenario completeness | Universal 100%; no coverage gate | Requires reviewer judgment; mutation/property testing may improve signal later |
| PostgreSQL in integration tests | Validates real locking/constraints/query semantics | SQLite substitute; mocks only | Slower setup; focused suites/test containers keep feedback usable |
| Documentation and decision records in the repository | Public, versioned, reviewed and works for forks/self-hosters | Private wiki/chat only | Docs can drift; CI/owners and change checklists counter it |
| C4 + Mermaid canonical diagrams | Consistent maintainable text-reviewable architecture views | Ad hoc drawing tools; generated class diagrams everywhere | Limited visual styling; external diagrams may supplement, never replace source |
| Strict TypeScript/Python typing at boundaries | Finds contract/nullability errors early | Dynamic/partial typing | Annotation/tooling cost; narrow escape hatches require rationale |
| Size guidance as review prompts, not hard limits | Encourages cohesion without fragmentation games | Automated line limits; no guidance | Subjective; complexity/static metrics may supplement |
| Stable API/error/event contracts and generated clients later | Independent frontend/mobile/plugin development | Share backend models; handwritten duplicate types | Generation pipeline work; prevents implementation leakage |
| Security/privacy/accessibility specialist review triggers | Protects high-impact student-facing boundaries | General review only; post-release audit | Review capacity can slow PRs; contributor ladder grows specialist pool |
| Least-privilege external plugins | Preserves core security/reliability and operator trust | In-process arbitrary plugins/direct DB | More plugin setup/latency; SDK/reference runner improves experience |
| Dependencies require need, trust, license and exit review | Reduces supply-chain/maintenance burden | Add freely; ban most dependencies | Upfront review time; automation maintains inventory/upgrades |
| Typed centralized configuration | Fails early and prevents environment drift/secret leaks | Read env anywhere; config constants in code | Composition layer maintenance; dynamic config stays domain-owned |
| Structured redacted logs + low-cardinality telemetry | Operable without creating a privacy leak/cost explosion | Free-form debug logs; capture all payloads | Some debugging detail unavailable; targeted secure diagnostics/runbooks help |
| Expand–migrate–contract and explicit release migration | Safe rolling/self-host upgrades | Destructive in-place/auto-start migration | Multi-release work; significantly safer rollback/compatibility |
| Public contributor ladder and evidence-driven RFC/ADR process | Sustainable shared ownership and transparent decisions | Benevolent dictator/private core decisions; voting on every PR | More process for large choices; routine work remains maintainer/lazy consensus |
| Semantic core releases with immutable signed tags/artifacts | Predictable upgrades/security/backports | Rolling unversioned main; mutable releases | Release overhead; automation and cadence can mature |

### 21.1 Exceptions process

An exception request states the exact rule, scope, rationale/evidence, alternatives tried, risks, compensating controls, owner, expiration/review milestone and cleanup issue. Approval comes from the rule's owning maintainer plus specialist owner for security/API/database/accessibility/release boundaries. Exceptions are visible in the PR/ADR and never become precedent automatically.

Emergency exceptions are time-bounded and receive retrospective review. A repeated exception signals the standard or architecture may need an RFC update rather than permanent hidden debt.

### 21.2 Handbook maintenance

This handbook uses the same PR/review/governance rules it defines. Material changes explain contributor impact, migration and enforcement/tooling. Rules should be enforceable, teachable and periodically audited; remove obsolete rules rather than accumulating contradictions.

---

## Contributor handoff checklist

Before writing code:

- [ ] Read the Code of Conduct, contributing/security policies and Parts 1–6 relevant to the change.
- [ ] Confirm the issue is scoped/ready and identify module/code owners.
- [ ] Choose the correct directory, branch and contract/decision updates.
- [ ] Write acceptance, edge, security/privacy/accessibility and test cases.
- [ ] Ask early when the change crosses architecture, API, database, plugin or governance boundaries.

Before requesting review:

- [ ] Run focused format/lint/type/tests and relevant integration/security/accessibility checks.
- [ ] Self-review architecture, compatibility, migration, observability, rollout and rollback.
- [ ] Update documentation, diagrams, examples, changelog and generated artifacts from source.
- [ ] Complete the PR template honestly and remove secrets/debug/dead/unrelated changes.

The project's standard is not perfection on the first contribution. It is transparent scope, evidence, respectful collaboration, safe iteration and leaving the codebase easier for the next contributor to understand.
