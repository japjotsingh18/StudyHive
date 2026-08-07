# StudyHive web

The Next.js application owns student and administration route composition, frontend feature modules, public assets, and web-specific tests. It consumes authoritative API contracts and never accesses PostgreSQL directly.

Sprint 1 provides accessible email/password registration and login forms plus the protected
`/account` bootstrap route. The route contains account/session status only; profile onboarding
and all collaboration features remain assigned to later sprints.

## Commands

Run from the repository root:

- `pnpm --filter @studyhive/web dev`
- `pnpm --filter @studyhive/web lint`
- `pnpm --filter @studyhive/web typecheck`
- `pnpm --filter @studyhive/web test`
- `pnpm --filter @studyhive/web build`
