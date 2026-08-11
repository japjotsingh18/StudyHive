# Alembic migrations

Alembic owns every PostgreSQL schema change. Revisions live in `versions/` and follow the documented expand–migrate–contract policy.

Sprint 1 introduces the initial authentication revision in `versions/`. It creates only the documented identity, credential, session, and authentication-audit tables. A new environment must be able to run `alembic upgrade head` from an empty database, and `alembic check` must report no model/schema drift.

Sprint 2 PR 1 adds the profile, global study-preference, availability, language,
field-visibility, consent-event, and user-block persistence foundation. The revision
supports both an empty-database upgrade and an upgrade from the Sprint 1 revision;
its migration tests also verify drift detection and downgrade/re-upgrade behavior.
