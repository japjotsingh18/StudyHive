# Good First Issue Backlog

These are proposed starter issues for the planning/foundation milestones. Maintainers should create them individually only when they can provide ownership and review. Each should be tagged `good first issue`, `help wanted`, and its area label.

## Planning-ready issues

### 1. Create the StudyHang domain glossary

**Area:** docs  
**Scope:** extract canonical definitions for session, participant, confirmed, pending, waitlisted, offered, arrived, no-show, course, section, and reliability event from Phases 1–4. Add a linked `docs/glossary.md`.  
**Acceptance:** definitions do not invent new lifecycle states; all planning docs link-check; ambiguous terms are raised rather than silently resolved.

### 2. Add a planning-document link checker

**Area:** tooling/docs  
**Scope:** propose and add a lightweight CI check for broken local Markdown links and anchors.  
**Acceptance:** runs on pull requests, documents local use, ignores external network status, and fails with actionable file/line output.

### 3. Audit inclusive and blame-free RSVP copy

**Area:** design/docs  
**Scope:** review UI and PRD copy for shame, moral judgment, ambiguity, and inaccessible Yes/No labels.  
**Acceptance:** submit a table of original/proposed/reason; do not change reliability weights or policy.

### 4. Add non-US academic catalog fixtures specification

**Area:** data/docs  
**Scope:** document synthetic examples for one non-US university, departments, courses, term names, domain, and timezone.  
**Acceptance:** no real student/instructor data; covers a domain not ending in `.edu`; aligns with the normalized schema.

### 5. Build an accessibility manual-test checklist

**Area:** accessibility/docs  
**Scope:** turn Phase 6 requirements into route-level keyboard, screen-reader, zoom, contrast, touch-target, and reduced-motion checks.  
**Acceptance:** reusable checklist with expected outcomes for onboarding, join, confirm, and live attendance.

### 6. Document local provider-fake behavior

**Area:** developer experience/docs  
**Scope:** specify how fake identity, push, email, maps, and storage adapters behave in local development before implementation.  
**Acceptance:** includes success/failure/delay modes and confirms no paid account is required for core contribution.

### 7. Create an ADR template

**Area:** governance/docs  
**Scope:** add a concise status/context/decision/consequences/alternatives/revisit template and link it from CONTRIBUTING.  
**Acceptance:** matches ADR-0001 terminology and includes supersession behavior.

### 8. Create a session-tag content guide

**Area:** product/docs  
**Scope:** define stable keys and concise display descriptions for Homework, Exam Review, Coding, Lab, Project, and Interview Prep.  
**Acceptance:** tags remain course/session relevant, localization-ready, and are not duplicated with study styles.

## Not suitable as good first issues

Do not label these for first-time contributors: authentication/authorization, database migrations, capacity/waitlist transactions, scheduled jobs, WebSocket security, reliability scoring, moderation decisions, account deletion, or production deployment. They can be `help wanted` only with a detailed design and active maintainer pairing.
