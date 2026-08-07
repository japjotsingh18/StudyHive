# Alembic migrations

Alembic owns every PostgreSQL schema change. Revisions live in `versions/` and follow the documented expand–migrate–contract policy.

Sprint 1 introduces the initial authentication revision in `versions/`. It creates only the documented identity, credential, session, and authentication-audit tables. A new environment must be able to run `alembic upgrade head` from an empty database, and `alembic check` must report no model/schema drift.
