# ADR-0003 — Generalized activities, Campus Presence, and Need Help Now

- **Status:** accepted
- **Date:** 2026-08-04
- **Deciders:** founder and project maintainers

## Context

“Study session” is too narrow for the long-term academic collaboration model. Scheduled sessions also fail to answer two immediate questions: “Is anyone studying here now?” and “Can someone in my course help me now?”

## Decision

### Activity aggregate

The canonical internal domain term is `Activity`. `Study Session` is one activity type and remains valid user-facing language where appropriate.

Initial activity types:

- study session;
- homework group;
- project meeting;
- project team formation;
- lab help;
- interview practice;
- research discussion;
- office-hours meetup;
- hackathon preparation;
- ad-hoc help meetup created from an accepted Need Help request.

Capacity, participation, waitlist, RSVP, attendance, location, lifecycle, chat, and notifications attach to the Activity aggregate. Type-specific behavior uses validated policy/configuration, not nullable columns for every future type.

### Campus Presence

Students may explicitly become visible in an approved campus zone for a short period. Public campus views show privacy-thresholded aggregate counts and course breakdowns, not a directory of named people. Invisible is the default.

Presence is manually selected, coarse, renewable, and expires automatically. StudyHang does not require background GPS tracking or retain a location history for product analytics.

### Need Help Now

A student may create a short-lived course-scoped help request. The system finds eligible opt-in candidates based on same tenant/university, course membership, current availability/presence, blocks, notification preferences, and safety policy. It sends private invitations rather than exposing a searchable list of online students.

Location and identity disclosure are progressive. Exact meeting context is shared only after mutual acceptance. An accepted request may create an ad-hoc Activity so attendance, safety, and completion use existing core rules.

## Privacy and abuse constraints

- invisible/default-off presence;
- explicit expiry and immediate “go invisible” control;
- approved/coarse campus zones, not arbitrary private addresses;
- minimum aggregation thresholds before course/location counts appear;
- no individual campus-presence directory;
- rate limits, request expiry, quiet hours, report/block enforcement, and repeated-decline suppression;
- no reliability penalty for declining or ignoring a help invitation;
- no plugin access to individual presence by default;
- minimal operational retention and no background movement trail.

## Consequences

- StudyHang becomes useful for spontaneous collaboration without requiring a scheduled Activity.
- The generalized aggregate supports future academic formats without duplicating participation logic.
- Presence and matching create meaningful safety, privacy, realtime, moderation, and notification scope that must be designed before implementation.
- Course-level aggregate counts may be hidden in low-volume zones to prevent inference about individuals.
