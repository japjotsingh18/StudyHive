# Authentication incident runbook

## Triage

1. Correlate the client-visible request ID with structured API logs.
2. Check API readiness, PostgreSQL connectivity, and Redis health.
3. Inspect authentication audit event keys and aggregate counts; do not export credential fields.
4. Confirm `STUDYHIVE_WEB_ORIGIN`, secure-cookie configuration, and proxy HTTPS headers.

Repeated `auth.session_reuse_detected` events can indicate a replayed rotated session. The service
revokes the affected session family automatically. Preserve audit records, invalidate additional
sessions only through an approved operational procedure, and follow the security policy for suspected
account compromise.

If Redis is unavailable, requests continue through the bounded local rate-limit fallback. Restore
Redis promptly because limits are then process-local and less coordinated. Do not disable the fallback
or expose raw email addresses, passwords, cookies, token digests, or CSRF values while debugging.

## Recovery checks

- Confirm a fresh login succeeds and an intentionally incorrect login returns the same generic error.
- Confirm `/api/v1/auth/session` rejects an absent or revoked session.
- Confirm logout and refresh reject missing/mismatched CSRF values.
- Confirm session refresh rotates the credential and replay revokes the rotated family.
- Run `make check` and the PostgreSQL integration test before deploying a remediation.
