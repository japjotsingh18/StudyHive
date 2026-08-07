# Security Policy

## Supported versions

StudyHang is pre-alpha and has no supported production release. Security fixes apply to the default branch until versioned releases begin. A supported-version table will be published before public beta.

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities, leaked secrets, private student data, or abuse paths.

Use GitHub's private vulnerability reporting feature when enabled. If it is not available, contact the repository owner privately through the GitHub profile and share only enough detail to establish a secure reporting channel. A dedicated security address and response key must be published before private pilot.

Include, when safe:

- affected component and version/commit;
- impact and prerequisites;
- minimal reproduction using synthetic data;
- suggested mitigation if known;
- whether any real data or production system may be involved.

Do not access other users' data, degrade service, send unsolicited notifications, perform denial-of-service testing, upload malware, or use social engineering.

## Response targets

Before beta these are goals, not a bug-bounty promise:

- acknowledge a credible report within three business days;
- establish severity and next update within seven business days;
- coordinate disclosure after a fix or mitigation is available;
- credit reporters who request it and acted in good faith.

## High-priority areas

- Clerk token/webhook validation and account linking;
- cross-university or blocked-user authorization bypass;
- session private location disclosure;
- capacity/RSVP state tampering;
- reliability event or moderation evidence exposure;
- signed upload/download abuse and malicious files;
- WebSocket subscription authorization;
- notification token exposure or notification spoofing;
- secrets in logs, builds, previews, or repository history.

## Security baseline before pilot

Threat models, dependency/secret/SAST/container scanning, rate limits, audit logging, backup restore, incident response, provider-key rotation, data retention, and abuse tests are release gates described in the planning documents.
