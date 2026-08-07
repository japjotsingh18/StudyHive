# Phase 7 — Development Roadmap

This roadmap is outcome-based. Dates are set only after maintainer capacity and pilot partners are known. A milestone exits when its evidence gate passes, not when a calendar expires.

## Milestone 0 — Product and governance approval

**Outcome:** contributors share one product boundary and one safe technical direction.

Deliverables:

- approve Phases 1–8 and ADR-0001;
- naming/trademark and repository identity review;
- establish maintainers, decision process, security contact, and release ownership;
- approve plugin/event/self-hosting architecture and select a reference plugin;
- validate critical journeys with student interviews/prototypes;
- decide pilot eligibility, minimum age, supported regions, and reliability policy owner;
- create public project board and label taxonomy.

Exit gate: open decisions that could change the runtime, data model, or MVP boundary have named owners and resolution dates; no application code begins before ADR-0001.

## Milestone 1 — Contributor foundation (`0.1.0-dev`)

**Outcome:** a clean checkout becomes a tested local system with one command path.

Deliverables:

- monorepo/tooling, web/API shells, local PostgreSQL/Redis/provider fakes;
- Compose profile for web, API, worker, realtime, PostgreSQL, Redis, MinIO, and local mail;
- lint, formatting, type checking, test, build, migrations, API-client generation;
- CI, dependency/security checks, preview environments;
- observability baseline, structured problem responses, feature flags;
- design tokens and accessible primitive baseline;
- architecture decision and runbook templates.

Exit gate: a first-time contributor completes setup on supported macOS/Linux from documentation; CI and local `make check` agree; no secret-bearing provider account is required for basic work.

## Milestone 2 — Identity and academic graph (`0.2.0`)

**Outcome:** a verified student can establish academic context at any supported university.

Deliverables:

- identity-provider contract, local/OIDC/email adapter path, callbacks, and domain user lifecycle;
- onboarding, profiles, privacy, study styles;
- university/domain/department/course/term/section catalog;
- course membership and catalog suggestion/moderation queue;
- authorization matrix and block/report foundations;
- global-safe institutional-domain handling.

Exit gate: onboarding and missing-catalog journeys pass end-to-end; wrong-university and hidden-profile access tests pass; at least one US and one non-US institution fixture works.

## Milestone 3 — Activity coordination core (`0.3.0`)

**Outcome:** students can create, discover, join, leave, bookmark, and waitlist without capacity errors.

Deliverables:

- location inventory and snapshots;
- generalized Activity aggregate/types and create/edit/cancel flows;
- discovery filters, course session list, session detail;
- participant and waitlist state machine;
- transactional capacity, promotion offer, and idempotency;
- dashboard session sections and deterministic recommendation v0;
- host roster read model.

Exit gate: concurrency tests never exceed capacity or duplicate position; material edits reschedule future work; critical web flows pass accessibility review.

## Milestone 4 — Smart RSVP and notification engine (`0.4.0`)

**Outcome:** roster accuracy improves automatically and failures are recoverable.

Deliverables:

- durable scheduled tasks/outbox and worker leasing;
- immediate, morning-of, 3h, 2h, and 1h policies;
- yes/no confirmation, timeout removal, and waitlist promotion;
- canonical in-app inbox and preferences;
- FCM adapter plus selected transactional-email fallback;
- retries, dead letters, reconciliation, task-generation rescheduling;
- time-travel/DST/duplicate execution test suite.

Exit gate: simulated provider outage and worker crash lose no canonical task; 99% scheduling objective passes representative load; every automated removal is explainable/audited.

## Milestone 5 — Live coordination, Campus Presence, and reliability (`0.5.0`)

**Outcome:** students can trust live session status and understand attendance-based trust signals.

Deliverables:

- authenticated WebSocket invalidation/fan-out;
- opt-in expiring Campus Presence with thresholded campus/course counts;
- short-lived Need Help Now requests, safe candidate matching, private invitations, and conversion to an ad-hoc Activity;
- arrival/late/can't-make-it workflow and host console;
- active/ending-soon/completed lifecycle and continuation timeout;
- immutable reliability ledger, versioned policy, snapshots, appeals;
- reliability privacy/host disclosure controls;
- fairness analysis tooling using de-identified pilot aggregates.

Exit gate: reconnect/resync and Redis-degraded mode pass; presence never survives expiry/Redis loss as stale visibility; low-volume identities cannot be inferred from aggregate views; help matching respects blocks, consent, limits, and no-penalty decline; ledger rebuild is deterministic; privacy and dignity review approves all reliability surfaces.

## Milestone 6 — Private pilot (`0.6.0-alpha`)

**Outcome:** selected course cohorts complete dependable sessions safely.

Deliverables:

- pilot onboarding/admin runbooks and catalog seeding;
- moderation queue, reports, blocks, suspension, appeals;
- data export/deletion and retention jobs;
- SLO dashboards, alerts, incident response, restore drill;
- performance, security, accessibility, and privacy review;
- feedback loop and baseline product metrics.

Exit gate: PRD MVP release gate passes; pilot partner and maintainers sign off; no unresolved critical/high defects.

## Milestone 7 — Public beta (`0.9.0-beta`)

**Outcome:** multiple universities can adopt StudyHang with a sustainable community process.

Potential scope, prioritized by pilot evidence:

- session chat and pinned messages;
- course notes/resources with scanning, search, and moderation;
- richer course discussion;
- calendar export/subscription;
- verified location improvements;
- Active LTS Next.js upgrade and dependency review;
- localization foundation and broader global verification;
- maintainer ladder, triage rotation, and release automation.

Exit gate: selected P1 capability quality gates pass; support/moderation capacity matches projected growth; beta SLOs hold under load test.

## Milestone 8 — Stable release (`1.0.0`)

**Outcome:** core contracts, operations, and governance are dependable enough for broad adoption.

Deliverables:

- documented compatibility/deprecation policy;
- stable REST/realtime v1 and migration policy;
- upgrade, backup, recovery, and self-host evaluation docs;
- external security assessment and accessibility conformance report;
- sustained maintainer ownership across critical modules;
- institutional pilot evidence and public impact report.

Exit gate: no known contract-breaking work is required for committed 1.x scope; operations and governance do not depend on one person.

## Post-1.0 / Phase 2

Candidates, each requiring a separate PRD and privacy review:

- institution administration and imports;
- LMS/SIS integrations;
- opt-in partner matching;
- native mobile clients;
- self-host/federated deployment profile;
- AI flashcards, quizzes, summaries, matching, and exam plans.

AI work additionally requires content rights, consent, model/provider disclosure, retention, evaluation, safety, cost, and opt-out decisions. No AI milestone is scheduled merely because data exists.

## Cross-cutting workstreams

| Workstream | Every milestone must include |
| --- | --- |
| Accessibility | keyboard/screen-reader/zoom/contrast checks and regression tests |
| Security/privacy | threat-model delta, authz tests, dependency review, data inventory update |
| Reliability | operational metrics, retry/failure paths, runbook owner |
| Docs/community | user docs, contributor notes, changelog, labeled starter issues |
| Product learning | hypothesis, event instrumentation, guardrail review, feedback synthesis |

## Release and versioning policy

- `0.x` may evolve quickly but breaking API/data changes are documented.
- Release candidates freeze migrations/contracts except blocker fixes.
- Semantic Versioning begins as a commitment at `1.0`.
- Changelog follows Keep a Changelog categories.
- Database compatibility follows expand/migrate/contract.
- Feature flag removal is part of milestone completion, not permanent debt.

## Scope control

A feature enters the active milestone only with:

1. a user problem and owner;
2. acceptance and non-goals;
3. privacy/safety classification;
4. architecture/data/API impact;
5. test and observability plan;
6. documentation and rollout plan.

Chat, notes, social graphs, AI, and institution integrations cannot bypass this gate by being listed in the original vision.
