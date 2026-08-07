# Phase 8 — Implementation Plan

Implementation starts only after the planning approval checklist is signed. Work proceeds as vertical, testable modules; application code is not included in this planning phase.

## 1. Delivery approach

- Build one deployable modular monolith and worker first.
- Ship the thinnest end-to-end slice early: authenticate → join course → create/list session.
- Treat RSVP timing and capacity as correctness-critical domain work, not controller logic.
- Use feature flags for incomplete user-facing modules, not long-lived forks.
- Keep every main-branch commit deployable/migratable.
- Prefer small RFC/ADR-backed changes and contributor-sized issues.

## 2. Team topology

The plan works for a small core team but makes ownership explicit:

| Ownership | Responsibilities |
| --- | --- |
| Product/design | research, scope, content, prototypes, accessibility acceptance |
| Web | routes, feature modules, design system, generated-client integration |
| API/domain | state machines, REST/realtime, authorization, provider ports |
| Data/operations | schema/migrations, jobs, observability, deployment, recovery |
| Trust/safety | moderation, reliability policy, appeals, privacy/retention |
| Maintainers | review, releases, community triage, governance and security response |

One person may hold multiple roles, but no critical subsystem is implicitly ownerless.

## 3. Work packages in dependency order

### WP-0 — Resolve gates

- Accept/reject ADR-0001.
- Accept the Part 1 tenant, provider, event, plugin, and self-hosting boundaries.
- Confirm working name process, license, target regions/minimum age, pilot model.
- Approve MVP exclusions and reliability visibility.
- Select Python queue library and transactional-email provider through time-boxed spikes.

**Evidence:** recorded decisions; updated docs; no unresolved stack fork.

### WP-1 — Repository foundation

- Scaffold workspaces and minimal deployable web/API/worker.
- Add typed configuration and local Docker infrastructure.
- Establish formatting, lint, typing, tests, CI, security scans, API-client generation.
- Add structured logging, request IDs, problem response, health/readiness endpoints.
- Add design tokens, story/test harness, route loading/error foundations.

**Tests:** clean bootstrap, smoke deploy, migration empty/upgrade, generated-client drift, secret scan.

### WP-2 — Identity vertical slice

- identity-provider contract, local/OIDC/email login/session verification, and callback adapter.
- Domain user/profile lifecycle and onboarding state.
- University email/domain verification and privacy settings.
- `GET /me`, profile update, own/other profile policy.
- Provider fakes and authorization test matrix.

**Tests:** invalid claims/webhook replay, suspended/deleted user, cross-university profile access, PII response snapshots.

### WP-3 — Academic catalog vertical slice

- University/domain/department/course/term/section persistence and reads.
- Course search/join/leave; onboarding course selection.
- Catalog suggestion and minimum moderator workflow.
- Seed fixtures across different countries/timezones.

**Tests:** aliases/duplicates, section-course invariant, active membership uniqueness, search pagination, wrong-scope reads.

### WP-4 — Activity creation and discovery

- Location and immutable session-location snapshot.
- Generalized Activity aggregate, initial activity types, and lifecycle; create/edit/cancel.
- Course/session discovery queries and dashboard composition.
- Session cards, creation form, detail, host actions.
- Material edit notification/task-generation contract, initially provider-faked.

**Tests:** DST/ambiguous time, lifecycle invalid transitions, visibility, blocked users, stale edit preconditions, accessibility form errors.

### WP-5 — Participation, capacity, and waitlist

- Participant state machine and immutable event records.
- Transactional join/leave/promotion and stable waitlist positions.
- Idempotency store and command handling.
- Host roster and participant action surfaces.

**Tests:** high-concurrency joins, repeated requests, leave/promotion race, expired offers, host invariant, terminal-session rejection.

### WP-6 — Durable jobs and notification inbox

- Scheduled-task/outbox repositories and worker lease loop.
- In-app notification resource/preferences.
- Delivery adapter ports, FCM, email, retries/dead letters.
- Operator views/alerts and repair/reconciliation command.

**Tests:** crash before/after commit/ack, duplicate claim, lease expiry, provider failure, preference/quiet-hour rules, token invalidation.

### WP-7 — Smart RSVP policy

- Schedule generation from session timezone and user policy.
- Immediate/morning/3h/2h/1h tasks.
- Confirmation commands, auto-removal, promotion cascading.
- Reschedule/cancel invalidation and user-facing deadline copy.

**Tests:** frozen-clock matrix, DST, late edits, duplicate tasks, no-response removal, capacity preservation, host cancellation, notification dedupe.

### WP-8 — Attendance and live status

- WebSocket authentication/subscriptions/fan-out.
- Arrival/late/can't-make-it commands and live roster.
- Active/ending/completed lifecycle, continuation prompt, timeout.
- REST resync and degraded-mode UX.

Add after the realtime foundation is stable:

- expiring, opt-in Campus Presence in approved zones;
- privacy-thresholded campus/course count projections;
- durable short-lived Need Help requests and deterministic candidate eligibility;
- bounded private invitations, progressive disclosure, and accepted-match conversion to an ad-hoc Activity.

**Tests:** unauthorized subscription, version gaps, reconnect, Redis loss, stale client event, continuation race, presence expiry/go-invisible, low-count suppression, block/quiet-hour enforcement, help-request abuse limits, no-penalty decline, focus/screen-reader update behavior.

### WP-9 — Reliability and appeals

- Versioned scoring policy and immutable reliability events.
- Deterministic snapshot projection and explainability.
- Own-detail/host-coarse authorization.
- Appeal submission/review/void/freeze and audit.
- Fairness/guardrail dashboard using de-identified aggregates.

**Tests:** golden scoring fixtures, rebuild equivalence, event dedupe/decay, dispute exclusion, host visibility, account deletion, policy version change.

### WP-10 — Trust, privacy, and pilot hardening

- Reports, blocks, moderation actions, catalog review.
- Export/deletion/retention workflows.
- Rate limits, security headers, audit trails, abuse scenarios.
- Backup restore, incident response, SLO dashboards, synthetic critical journey.
- Usability/accessibility/security/load review and pilot runbooks.

**Tests:** report authorization, block effects across discovery/realtime, deletion idempotency, backup restore, load thresholds, OWASP-oriented abuse cases.

### WP-P1 — Chat and notes after pilot evidence

Chat and notes are separate work packages with upload threat model, quarantine/scanning, content moderation, copyright policy, storage quotas, search indexing, and accessibility before release. Do not pre-create their tables or routes during MVP unless a concrete compatibility requirement exists.

## 4. Vertical slice definition of done

Every work package is complete only when it includes:

- reviewed product acceptance criteria and non-goals;
- domain and authorization rules;
- migration and rollback/expand-contract strategy;
- OpenAPI and generated client update;
- responsive UI with loading/empty/error/offline/permission states;
- unit, integration, contract, and relevant end-to-end tests;
- keyboard/screen-reader/zoom/contrast/reduced-motion evidence;
- logs, metrics, traces, alerts, and runbook for new failure modes;
- privacy/retention/analytics inventory update;
- user and contributor documentation;
- changelog entry and cleanup of completed feature flags.

## 5. Test strategy by risk

| Risk | Primary test technique |
| --- | --- |
| State transition correctness | table/property-based domain tests |
| Capacity and waitlist races | real PostgreSQL concurrent integration tests |
| Scheduled time behavior | frozen clock + timezone/DST matrix |
| Retry/idempotency | fault injection at transaction/delivery boundaries |
| Authorization/privacy | actor-resource policy matrix and response snapshots |
| API compatibility | OpenAPI schema diff + generated-client contract tests |
| Realtime correctness | integration tests with reconnect/version gaps |
| Accessibility | automated checks plus manual assistive-tech scripts |
| Performance | representative seeded data, query plans, load tests |
| Recovery | restore drill and reconciliation simulation |

## 6. Seed and fixture plan

Fixtures are deterministic and privacy-safe:

- two universities in different countries/timezones;
- departments, cross-listed courses, terms, and sections;
- users across onboarding/verification/privacy states;
- sessions in every lifecycle state and near DST boundaries;
- full session with waitlist and expiring offer;
- reliability events, disputes, and new-user state;
- notification success/failure/dead-letter examples;
- blocked/cross-university authorization pairs.

Production seed contains controlled taxonomies only; demo personas and sessions never enter production.

## 7. Observability implementation order

1. Correlation IDs, safe structured logs, and error tracking in foundation.
2. API latency/error/traffic and database pool/slow-query metrics.
3. Job lag, retries, dead letters, outbox age, provider outcomes.
4. WebSocket connection/fan-out/resync metrics.
5. Product funnel events and reliability guardrails only after consent/data review.

An alert without an owner and runbook is not considered complete.

## 8. Rollout strategy

- Local → preview → staging with synthetic data → internal dogfood → one-course pilot → multi-course pilot → second institution → public beta.
- Risky capabilities use server-evaluated flags with allowlists and kill switches.
- Schema deploys use compatible release ordering.
- Notification automation starts in observe-only/shadow mode, then sends to staff, then pilot cohort.
- Reliability computes privately in shadow mode before any host disclosure; compare events, appeals, and cohort fairness.
- Chat/uploads remain disabled until moderation and scanning are operational.

## 9. Pull request slicing

A typical vertical feature is split into reviewable changes:

1. ADR/RFC or contract update if needed.
2. Migration + repository + invariant tests.
3. Domain/application command/query + tests.
4. REST/OpenAPI + generated client.
5. UI states + accessibility tests.
6. worker/realtime/provider effects where applicable.
7. telemetry, docs, and rollout flag.

Avoid PRs that combine unrelated formatting, dependency upgrades, and feature behavior.

## 10. Performance budgets

Initial budgets are validated, not assumed:

- ordinary API p95 target under 400 ms;
- key web route Core Web Vitals in “good” range on representative mobile conditions;
- no unbounded collection or N+1 query;
- list endpoints default 20/max 100;
- WebSocket payloads minimal and versioned;
- worker due-task lag objective from PRD;
- uploads bypass application servers and have explicit quotas.

Regression thresholds and representative dataset size are committed with the first load-test suite.

## 11. Contributor onboarding plan

- Label issues only after scope, acceptance, files/modules, and test expectations are written.
- Keep “good first issue” free of auth, reliability, concurrency, migration, or incident-critical judgment.
- Pair first-time contributors with a named maintainer.
- Provide architecture tours and domain glossary.
- Maintain provider fakes and demo data so outside contributors can reproduce issues.
- Track review latency and contributor drop-off as community health signals.

## 12. Implementation approval checklist

- [ ] Product owner approves PRD and MVP exclusions.
- [ ] Maintainers accept ADR-0001 or record an alternative stack ADR.
- [ ] Design wireframes pass initial student validation.
- [ ] Data/API/state terminology is consistent across all planning docs.
- [ ] Security/trust owner accepts reliability, moderation, and retention approach.
- [ ] Milestone 1 issues are sliced, labeled, and owned.
- [ ] Only then may repository/application scaffolding begin.
