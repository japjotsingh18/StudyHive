# Part 2 — Product Requirements Document

**Product:** StudyHang (working name)  
**Status:** canonical product specification for planning; implementation not authorized by this document  
**Version:** 1.0 draft  
**Last updated:** 2026-08-04  
**Depends on:** accepted Part 1 and ADR-0001 through ADR-0003

## 0. Product frame

### Product objective

StudyHang helps university students find reliable classmates to study with, coordinate academic Activities, and improve follow-through. The MVP is successful when it makes it materially easier to answer:

1. Who relevant can I study with?
2. What academic Activities can I join now or soon?
3. Who is genuinely attending?
4. Where is opt-in academic activity happening on campus?
5. Can an eligible classmate help me right now?

### MVP boundary

MVP includes only capabilities that directly improve partner discovery, Activity coordination, immediate help, attendance accuracy, or safety/accountability.

| Release | Included product scope |
| --- | --- |
| **MVP / private pilot** | Authentication, verified profiles, university/course graph, Activities, RSVP/waitlist, attendance/live state, Campus Presence, Need Help Now, reliability, focused dashboard/search/recommendations, notifications, moderation/privacy/accessibility |
| **Version 1.1** | Reputation categories, anonymous post-Activity feedback, and persistent Project Teams if MVP evidence supports them |
| **Phase 2 / public beta candidate** | Activity chat, course discussion, notes/resources, richer announcements, saved searches, calendar integrations, broader recommendations |
| **Later** | Direct messages, social graph, AI, tutoring/marketplace, clubs, hackathons, research/career modules, deep LMS integrations |

The presence of a chapter in this PRD does not place it in MVP. Every chapter states its release classification.

### Canonical terminology

- **Activity:** internal and product umbrella for an organized academic gathering.
- **Activity type:** Study Session, Homework Group, Lab, Project Meeting, Exam Review, Research Discussion, Interview Practice, Office-Hours Meetup, Hackathon Prep, or Ad-Hoc Help Meetup.
- **Participant:** a student with a participation record for an Activity, including waitlisted or removed states.
- **Campus Presence:** a student's deliberate, temporary, coarse campus availability signal.
- **Need Help request:** a short-lived, course-scoped request for immediate assistance.
- **Reliability:** private-by-default evidence of follow-through, not popularity or academic ability.

### Product roles

| Role | Scope |
| --- | --- |
| Visitor | Public landing, policies, university discovery where enabled |
| Authenticated user | Account exists but university may be unverified |
| Verified student | Verified at a supported university; normal product access |
| Activity host | Manages one Activity and its current roster |
| Course moderator | Moderates one course's community surfaces and announcements |
| University administrator | Manages one university's catalog, domains, branding, roles, and reports |
| Safety moderator | Handles reports and policy actions in an assigned scope |
| Instance administrator | Operates the deployment; access to student content is limited and audited |

Roles are additive and scoped. Being an administrator never silently makes a person a course member or Activity participant.

### Shared experience requirements

- Mobile-first and fully usable from 320px width through large desktop.
- WCAG 2.2 AA target, including keyboard, screen reader, 200% zoom, contrast, reduced motion, and touch targets.
- Every collection supports bounded pagination or progressive loading.
- Every screen defines loading, empty, filtered-empty, error, permission, stale, and offline behavior.
- Times always show an unambiguous absolute value and relevant timezone; relative time is secondary.
- Optimistic feedback is limited to reversible actions. Capacity, RSVP, attendance, matching, and reliability show server-confirmed outcomes.
- Status meaning never depends only on color, animation, icons, or stars.
- Destructive and trust-affecting actions state consequences before confirmation.
- Students are never publicly ranked by reliability, activity count, popularity, or study streak.

### North-star and guardrail measures

**North-star:** weekly dependable academic collaborations—completed Activities with at least two arrived participants, plus accepted Need Help matches that result in a completed Ad-Hoc Help Meetup.

Supporting measures:

- verified-user activation and time to first relevant Activity/help outcome;
- join-to-arrival and reconfirmed-to-arrival rates;
- roster accuracy reported by hosts and participants;
- waitlist seat recovery;
- Need Help time to mutual acceptance;
- compatibility coverage, recommendation-to-join, and compatible-pair repeat collaboration;
- Activity goal/outcome reporting and Completed/Partial/Not Completed/Not Reported distribution;
- recurring-series follow/auto-join, reconfirmation, attendance, and cancellation behavior;
- repeat collaboration/hosting;
- percentage of pilot students reporting a useful new academic connection.

Guardrails:

- report, block, suspension, and appeal rates;
- notification opt-out and volume;
- Campus Presence inference or disclosure incidents;
- cross-university privacy incidents;
- reliability appeal overturn rate and cohort fairness signals;
- accessibility defects and task failure rates.

Targets are set after baseline pilot data; zero privacy/security incidents is always the objective.

---

## 1. Authentication and account lifecycle

**Release:** MVP

### Purpose and problem solved

Establish a secure account, verify that a person belongs to a university community, and preserve a clear distinction between identity, university eligibility, and product authorization.

### User stories

- As a new student, I can create an account with Google or email/password.
- As an email/password user, I can verify my email and securely recover access.
- As a student, I can verify my university even when its domain does not end in `.edu`.
- As a returning student, I can log in and return to the task that prompted authentication.
- As a user, I can view/sign out active sessions and log out this device.
- As a suspended or deleted user, I receive a clear, safe account-state explanation and permitted next steps.

### Primary flows

#### Google sign-up/login

1. User chooses Google.
2. User completes provider consent.
3. StudyHang links the verified provider subject to an existing account only when secure linking rules succeed; otherwise it creates a pending account.
4. New users continue to email/university verification and onboarding.
5. Returning active users return to their original destination or dashboard.

#### Email/password sign-up

1. User enters email, password, and required policy consent.
2. Product confirms submission without leaking whether an address was previously registered.
3. A time-limited verification message is sent.
4. User verifies and proceeds to university verification/onboarding.
5. If the email is already attached, the product offers login/recovery through non-enumerating copy.

#### Password reset

1. User submits an email.
2. Product always shows the same confirmation response.
3. A single-use, expiring reset link is sent when eligible.
4. User sets a new valid password; existing sessions are revoked by default, with explicit confirmation.
5. User receives a security notification.

#### University verification

1. User searches/selects a university.
2. User supplies an institutional email when their authenticated email is not already an approved domain.
3. Product verifies ownership and matches the domain to a verified university-domain record.
4. Unknown domains enter a review/request flow without granting verified access.
5. Verified university becomes the user's active university context.

#### Onboarding

1. Identity: display name and photo choice.
2. University: verified institution or pending request.
3. Academic context: major, graduation year, at least one course; section optional.
4. Collaboration preferences: study styles, availability, languages.
5. Privacy/presence: visibility explanation; Campus Presence stays off.
6. Notifications: explain value before asking browser permission.
7. Review and enter dashboard.

### UX requirements

- Authentication pages are narrow, calm, and free from product-navigation distractions.
- Password requirements are visible before submission and update as the user types.
- Resend actions show cooldown and destination in partially masked form.
- Google and email/password remain equally understandable; no deceptive provider preference.
- Onboarding saves progress and supports Back without data loss.
- Missing university/course flows never dead-end onboarding.
- Error copy distinguishes invalid input, expired link, provider interruption, and account state without leaking sensitive details.

### Business rules

- Email verification is required before normal product access.
- University verification is required to discover students, use Campus Presence/Need Help, join Activities, or publish content.
- A verified email domain is evidence of affiliation, not an administrative role.
- One provider identity maps to at most one account. Account linking requires recent authentication to both identities or an approved recovery process.
- Email comparison is normalized case-insensitively while preserving display form.
- Passwords are never displayed or emailed. A changed password revokes reset tokens.
- University verification may expire or require reverification according to university policy, but historical participation remains.
- Logout affects the current session; “log out all devices” revokes all user sessions.
- Suspended accounts cannot authenticate into product features. They may access appeal, export, and policy/support surfaces as permitted.
- Deleted accounts cannot be restored through ordinary login after the recovery window.

### Validation rules

- Email must be syntactically valid, normalized, within length limits, and not on a disposable-domain denylist when policy enables it.
- Password must meet current length and breached/common-password policy; composition tricks are not the sole strength measure.
- Verification/reset tokens are single use and expire.
- Display name and onboarding text are length-limited and reject control characters/impersonation patterns.
- Graduation year and university/course selections must be within configured catalog/policy ranges.
- Policy consent version and timestamp are required.

### Permissions

| Action | Visitor | Authenticated unverified | Verified student | Admin/moderator |
| --- | ---: | ---: | ---: | ---: |
| Sign up/login/reset | Yes | Yes | Yes | Yes |
| Complete profile | No | Yes | Yes | Yes |
| Browse protected university community | No | No | Yes, scoped | Yes, scoped |
| Reverify/change university | No | Yes | Yes | Yes; no bypass without audit |
| Suspend account | No | No | No | Safety/admin only, scoped |

### Edge cases

- Google returns an email already used by a password account: require secure linking; never auto-merge on email alone when assurance is insufficient.
- User loses access to institutional email: allow support/reverification without exposing old address.
- University uses multiple domains or no student domain: support reviewed domain/administrator verification paths.
- User belongs to multiple universities: MVP supports one active verified university context; future expansion may support multiple verified affiliations.
- Verification arrives after token expiry: offer resend without restarting onboarding.
- Suspended while logged in: revoke access promptly and preserve unsent local form data only when safe.
- Deleted user appears in historical Activity records: display an anonymized deleted-user label according to retention policy.

### Acceptance and success criteria

- Google and email/password users can complete account creation, verification, onboarding, logout, and recovery without administrator intervention in normal cases.
- Unauthorized/unverified users cannot reach protected discovery, Activity, presence, or matching actions.
- Account-linking and recovery do not disclose whether an unrelated account exists.
- Suspended/deleted states are enforced consistently across active sessions.
- Median onboarding completion and abandonment are measurable by step without collecting sensitive field contents.

### Future improvements

GitHub, Microsoft, university SSO, multiple affiliations, MFA/passkeys, institutional provisioning, recovery codes, and delegated organization policies.

---

## 2. Student profiles

**Release:** MVP core; public activity feed and richer statistics are Phase 2

### Purpose and problem solved

Give students enough academic and collaboration context to decide whether they are compatible study partners without turning profiles into popularity pages.

### User stories

- As a student, I can present my university, courses, study preferences, availability, languages, and a short bio.
- As a student, I control which fields other students can see.
- As a prospective partner, I can understand mutual courses and compatible study styles.
- As a host, I can see the limited reliability context allowed for my Activity roster.
- As a student, I can understand my own statistics, streak, and reliability history.

### Profile fields and release behavior

| Field | Required | Default visibility | Notes |
| --- | ---: | --- | --- |
| Display name | Yes | University | Real-name requirement is instance policy; pseudonyms must not impersonate |
| Photo | No | University | Generated initials fallback; moderation/reportable |
| University | Yes | University | Verified status shown without email |
| Major | No | University | Free-text initially with normalized suggestions |
| Graduation year | No | Private | May be shown as broad cohort instead of exact year |
| Courses | At least one for activation | Mutual-course context | Per-course visibility controls |
| Study preferences | Recommended | Matching only by default | Structured compatibility inputs described below |
| Availability | No | Matching only by default | Coarse recurring blocks, not personal calendar details |
| Languages | No | University | Self-described; no proficiency ranking required |
| Bio | No | University | Plain text, bounded |
| Reliability | System | Self exact; host coarse | Never globally searchable/rankable |
| Statistics | System | Self by default | Hosted, joined, attended, completed help outcomes |
| Study streak | System | Self by default | Weekly consistency, not daily pressure |
| Recent activity | System | Private by default | Only visible Activities appear to others |

### Study Preferences

Study Preferences are MVP inputs to compatibility. They are self-described, editable, and never treated as academic ability or a fixed personality profile.

| Preference | Supported values |
| --- | --- |
| Study styles | Quiet Study, Discussion, Problem Solving, Coding, Exam Revision, Group Learning |
| Study pace | Slow and thorough, Balanced, Fast-paced |
| Preferred session length | 30 minutes, 1 hour, 2 hours, 4+ hours |
| Preferred time | Morning, Afternoon, Evening, Night, plus coarse recurring availability blocks |
| Modality | In person, Online, Either |
| Interaction | Silent, Minimal speaking, Conversational, Discussion-led |
| Environment | Library, Coffee shop, Campus common area, Online, Dorm/private space preference |
| Learning method | Explain concepts, Practice problems, Discussion, Silent work |
| Course confidence | Building foundations, Comfortable, Advanced; optional and set separately per course |

`Dorm/private space` is a compatibility preference only. It never publishes a home/dorm location or makes private residences an approved Activity venue.

### Primary flows

#### View another student

1. Viewer reaches a profile through a shared course, Activity, or accepted match.
2. Product applies university, block, relationship, and field-visibility rules.
3. Viewer sees mutual course context, compatible preferences, and allowed Activities.
4. Viewer can navigate to shared academic context or report/block; MVP has no direct message action.

#### Edit profile/privacy

1. User edits fields and sees per-field visibility descriptions.
2. Validation occurs without discarding other changes.
3. User previews “what another student sees.”
4. Save confirms changed visibility and removes newly hidden data from discovery promptly.

#### Edit Study Preferences

1. Student chooses values and coarse availability in plain language.
2. Product previews how each preference affects Activity/partner compatibility and who may see it.
3. Student can mark a preference “No preference,” omit course confidence, or disable its use in partner discovery.
4. Saving recalculates future compatibility; it never retroactively changes attendance or reliability.

### UX requirements

- Lead with academic compatibility, not counts, followers, or badges.
- Own profile clearly separates editable information from computed statistics.
- Reliability uses neutral explanatory copy and links to details/appeal.
- Availability uses coarse blocks such as weekday mornings/evenings; never display a detailed personal calendar.
- Preferences are grouped by pace, duration, time, modality, interaction, environment, and learning method with short examples.
- Course confidence uses neutral labels and is never shown as a grade, rank, or verified expertise claim.
- Empty optional fields do not create a visibly incomplete/shaming profile.
- Block/report actions are available but visually secondary.

### Business rules

- University email and authentication-provider identifiers are never profile fields.
- Mutual courses may be shown even if the full course list is hidden, only when both users legitimately share that course.
- Statistics count eligible Activities, not deleted drafts, duplicate joins, or cancelled-by-host participation.
- Hosted Session/Joined Session labels in product copy become Hosted Activities/Joined Activities.
- A study streak is the number of consecutive calendar weeks, in the user's chosen timezone, with at least one eligible attended/completed Activity. The current week cannot break the streak until it ends.
- Streak freezes rather than resets when the account is suspended or no supported courses exist, subject to policy.
- Recent Activity never reveals private/unlisted Activity participation to unauthorized viewers.
- Study Preferences are used only for compatibility/recommendations the student enabled. They do not affect account access, reliability, or course eligibility.
- Course confidence is course-specific; no global “beginner/advanced student” label exists.
- Changing preferences immediately affects new recommendations but does not remove existing Activity participation.
- Plugins may add namespaced optional profile panels later but cannot override core identity/privacy/reliability fields.

### Validation rules

- Name, major, bio, and language entries have explicit lengths and safe Unicode rules.
- Photo must pass type, size, crop, and moderation/scanning policy before publication.
- Graduation year is within configured historical/future bounds.
- Study Preference values come from controlled sets; availability uses a valid timezone and non-overlapping normalized blocks.
- At most one pace, session-length bucket, modality, and interaction default is active; multi-select styles, environments, learning methods, and time blocks deduplicate.
- Course visibility changes cannot grant access to a course the viewer cannot otherwise see.

### Permissions

- User edits only their own profile.
- University/safety moderators may hide policy-violating name/photo/bio with an audited reason; they do not rewrite a student's preferences.
- Hosts see a participant's coarse reliability band and evidence count only for current/recent roster decisions.
- Other students cannot search/filter by exact reliability, graduation year, or hidden availability.
- Another student sees compatibility reasons only within a legitimate Activity/shared-course/mutual-discovery context and only from preferences permitted for matching.
- Blocked users see neither profile nor presence/matching suggestions, subject to safe concealed-resource behavior.

### Edge cases

- Student changes university: old university-scoped visibility is removed; memberships enter inactive/history state until policy review.
- Hidden course is the only mutual context: show “shared academic context” only if revealing the course would violate preference.
- New user has no reliability/streak: show `New` and constructive onboarding, not zero.
- Moderated photo/name: retain private original only according to evidence policy; show neutral fallback.
- Account deleted: public profile disappears; historical attribution is anonymized or retained only where legally required.

### Acceptance and success criteria

- A student can complete a useful profile without exposing exact schedule, email, or private course history.
- Viewers see only fields allowed by both resource visibility and relationship context.
- Profile completion improves relevant Activity/partner matching without becoming a hard requirement for optional fields.
- Exact reliability and private statistics never appear in global search or public ranking.

### Future improvements

Multiple university affiliations, skills/topics, preferred group size, accessibility preferences with careful privacy, per-Activity preference overrides, endorsements limited to verified collaboration, plugin panels, and richer privacy audiences.

---

## 3. Universities and academic catalog

**Release:** MVP catalog and scoped administration; automated LMS integrations are later

### Purpose and problem solved

Represent any university consistently so students find the right classmates and Activities without hardcoded institutions or fragmented duplicate courses.

### User stories

- As a student, I can find my university, department, course, and optional section.
- As a student, I can request a missing or incorrect catalog entry.
- As a university administrator, I can manage approved domains, catalog records, branding, and scoped roles.
- As an operator, I can import a reviewed course catalog without overwriting local moderation decisions.

### Catalog hierarchy

University → Department → Course → Section. Terms/semesters contextualize sections. Activities attach to a course and may optionally attach to a section.

### Primary flows

#### Find or request university/course

1. Student searches normalized names, codes, aliases, and location.
2. Verified records appear first with country/campus disambiguation.
3. If absent, student submits a structured request and possible official source.
4. Product detects likely duplicates and shows pending status.
5. A catalog moderator approves, rejects with reason, edits, or merges.

#### Course import

1. Authorized admin uploads/maps a supported structured file.
2. Product previews create/update/archive/conflict counts.
3. Admin resolves required conflicts and confirms.
4. Import runs with visible progress and a reversible/audited result where possible.
5. Existing memberships and historical Activities are preserved when records are renamed/merged.

### UX requirements

- Search shows university country/campus and course department/title to prevent mistaken selection.
- Pending/unverified records are visually distinct and cannot masquerade as official.
- Branding never reduces accessibility or hides StudyHang safety/legal navigation.
- Import preview uses plain-language consequences and downloadable error details.
- Student-facing catalog screens do not expose administrator contact information unless explicitly published.

### Business rules

- `.edu` is not required; universities may have multiple verified domains.
- Domain ownership/approval is evidence of affiliation, not proof of every student's status beyond email control.
- University branding includes name, logo, theme tokens, support/policy links, and approved domains; it cannot change core safety language or reliability policy invisibly.
- Course codes are unique only within the correct university/catalog scope.
- Cross-listed courses may share an equivalence relationship while retaining official codes.
- Sections belong to one course/term; students may join a course without a section.
- Merge operations preserve stable links, membership, Activity history, and aliases.
- Deleting a catalog record with history is prohibited; archive/merge instead.
- Course import is idempotent for the same source/version and never silently removes user-created content.

### Validation rules

- University names, domains, country, timezone, and official-source fields are validated and normalized.
- Domains must be syntactically valid and unique to an active verification relationship unless an approved shared-domain exception exists.
- Course/section codes and terms are bounded, safe text.
- Import rejects malformed rows and cross-university references; partial-import policy is explicit before confirmation.
- Logos meet file safety, size, contrast/fallback, and rights requirements.

### Permissions

- Students view verified catalog, join courses, and submit change requests.
- Course moderators cannot change university domains/branding.
- University admins manage only their university's catalog, domains, branding, roles, and imports.
- Instance admins resolve cross-university duplicates and global policy, with audited access.
- Imported instructor/admin identities do not receive roles without explicit provisioning/acceptance.

### Edge cases

- Shared university system domain: require additional verification/context rather than guessing campus.
- Renamed department/course: preserve aliases and historical display snapshots.
- Same course code in different terms: course identity remains stable; sections/offerings vary.
- Import removes a course currently in use: archive future discovery, retain history, and alert admin.
- Student-requested university is approved later: notify requester and allow onboarding continuation.

### Acceptance and success criteria

- Users can model and join courses at US and non-US universities without code changes.
- Duplicate/merge behavior preserves memberships and Activity history.
- University admins cannot affect another university.
- Catalog requests/imports expose status and errors rather than silently failing.

### Future improvements

Canvas, Moodle, Blackboard and SIS connectors, automated term rollover, verified instructor roles, multi-campus institutions, federated catalog sharing, and institution-specific policy modules.

---

## 4. Courses

**Release:** MVP membership and Activity context; discussion, notes/resources, pinned messages, and richer announcements are Phase 2 unless needed for safety/coordination

### Purpose and problem solved

Create the academic boundary through which students discover relevant people and Activities.

### User stories

- As a student, I can join multiple courses and optionally identify my section.
- As a member, I can see course Activities and the permitted member directory.
- As a moderator, I can post a course announcement and manage course-specific safety issues.
- As a future contributor, I can use discussion/notes/resources without turning the MVP into a general content platform.

### Course areas and release scope

| Area | MVP behavior | Later behavior |
| --- | --- | --- |
| Overview | course identity, term/section context, membership, next Activities | richer course home |
| Members | privacy-filtered members with relevant study preferences | topic/skill discovery |
| Activities | create/discover course Activities | calendar/integration views |
| Announcements | moderator/host safety and coordination announcements | scheduled/rich announcements |
| Discussion | not in MVP, except structured Activity updates | threaded course feed |
| Notes/resources | not in MVP | versioned library/search/comments |
| Pinned messages | Activity-level essential notice only | course/chat pins |

### Primary flows

#### Join/leave course

1. Student opens a course and chooses Join.
2. Student optionally selects term/section and course-list visibility.
3. Membership activates and relevant Activities become eligible for discovery.
4. Leaving warns about upcoming hosted/joined Activities; unresolved obligations must be handled first.

#### Browse members

1. Member opens Members.
2. Product returns only same-course users whose privacy allows discovery.
3. Filters are limited to collaboration-relevant fields such as study style/language/availability—not reliability ranking.
4. Profile access preserves blocks and field visibility.

### UX requirements

- Course code and full title are always paired where ambiguity exists.
- MVP navigation does not show dead Discussion/Notes tabs; later modules appear only when enabled.
- Empty Activity list offers create Activity or set Need Help Now, not generic posting.
- Leaving course explains effects on discovery, presence course labels, recommendations, and future notifications.

### Business rules

- One active membership per user/course; optional section can change without leaving the course.
- Course membership is required to create or ordinarily join course-scoped Activities.
- A course member list is not public outside the course/university policy.
- Course moderators may moderate course content but cannot alter attendance/reliability facts.
- Announcements cannot impersonate university emergency communications.
- Course archive blocks new memberships/Activities but preserves historical access according to policy.
- Muted course suppresses ordinary activity notifications but not accepted RSVP/cancellation/safety notices.

### Validation rules

- Section must belong to the selected course/term.
- Membership visibility and notification options must be valid supported values.
- Announcement titles/body/links are bounded and sanitized.
- Leaving is blocked while the user hosts a future Activity unless they cancel/transfer it.

### Permissions

- Verified students join visible courses at their university.
- Members view Activities and privacy-eligible member context.
- Course moderators manage announcements/content reports in their course.
- University admins archive/merge courses and appoint scoped moderators.
- Nonmembers may see limited course catalog metadata but not member lists/private Activities.

### Edge cases

- Student switches sections: future section-restricted Activity eligibility updates; existing participation requires explicit handling.
- Course merged/cross-listed: memberships and Activities remain reachable through aliases.
- Moderator is no longer a student: role can remain only through explicit admin policy.
- User is blocked by another member: neither appears to the other in member discovery or partner suggestions.

### Acceptance and success criteria

- Joining a course immediately improves Activity and partner relevance.
- Course privacy prevents membership enumeration by outsiders.
- MVP course experience remains useful without discussion or notes.
- Leaving/archiving never strands hosted Activities or deletes history silently.

### Future improvements

Discussion feed, notes/resources, pins, richer announcements, instructor verification, assignments/topics, calendars, LMS sync, and course-specific plugins.

---

## 5. Activities

**Release:** MVP

### Purpose and problem solved

Give students one dependable object for organizing any academic collaboration without redesigning participation whenever the format changes.

### User stories

- As a student, I can create an Activity for a course with clear purpose, time, place, capacity, and expectations.
- As a student, I can find and join Activities relevant to my courses and preferences.
- As a host, I can edit, duplicate, cancel, archive, and manage an Activity without corrupting participant history.
- As a plugin author later, I can propose additional Activity types without changing core participation rules.

### Activity types

Study Session, Homework Group, Lab, Project Meeting, **Project Team Formation**, Exam Review, Research Discussion, Interview Practice, Office-Hours Meetup, Hackathon Prep, and Ad-Hoc Help Meetup. Each has a stable key and localized label/description. Type does not imply official university sponsorship.

### Core fields

| Field | Product requirement |
| --- | --- |
| Course/section | one course required; section optional and cannot contradict membership |
| Type | one enabled Activity type |
| Title/description | clear purpose, scope, and preparation expectations |
| Primary goal | one specific outcome the group intends to achieve; required for publication |
| Compatibility profile | intended interaction, pace/level, modality, environment, and optional topic/exam tag |
| Time | date, start, end, Activity timezone |
| Location | approved campus zone/place, online link policy, or permitted structured venue |
| Capacity | includes host; bounded by policy/location |
| Visibility | course, section, university, or unlisted; MVP does not support globally public Activities |
| Join policy | open or host approval; open is MVP default |
| Requirements | materials, prerequisites, accessibility, experience expectations; cannot discriminate unlawfully |
| Tags | controlled collaboration tags plus bounded future taxonomy |
| Host | one accountable primary host; optional co-host later |

### Activity goals

Every published Activity has one primary goal written as a concrete group outcome, for example `Complete Homework 5`, `Review Exam 2 recursion topics`, or `Find two teammates for the SER 315 project`. The scheduled duration is the estimated time for that goal.

The host may add up to five optional objective checklist items, but the single primary goal remains visible on cards, detail, RSVP, live view, and outcome. Goals describe collaboration—not promises of grades or guaranteed learning.

Project Team Formation adds three structured requirements:

- number of teammate openings, 1–10;
- desired skills/topics from bounded course-relevant suggestions plus safe custom entries;
- project/team decision deadline.

Joining a Project Team Formation Activity means joining the formation meeting, not automatically becoming a persistent team member. Participants may indicate `Interested in joining the team`; the host cannot privately reject people through reliability or protected-trait criteria.

### Primary flows

#### Create

1. Student starts from a course, dashboard, search, or accepted Need Help match.
2. Student selects type and completes purpose, time, place, people, and visibility.
3. Product validates conflicts, timezone, membership, location, capacity, and safety rules inline.
4. Student previews the exact participant-facing summary.
5. Student saves Draft or Publishes. Publishing makes the host a confirmed participant and schedules lifecycle/notification behavior.

#### Edit

1. Host edits permitted fields.
2. Product identifies material changes: course/section, start/end, location, capacity reduction, visibility, requirements.
3. Host sees affected participants and notification consequences.
4. Material change requires confirmation; participants receive a change summary and may reconfirm/leave as policy requires.

#### Duplicate

Creates a new Draft copying type, course, description, tags, duration, capacity, requirements, and visibility. It never copies participants, chat, attendance, reliability, timestamps, or private links. Host must choose a new time and review location.

#### Create a recurring Activity

1. Host selects Weekly, weekday, local start/end, timezone, location, and end date or occurrence count.
2. Product previews every occurrence and daylight-saving/timezone consequences.
3. Host publishes the series and first eligible occurrence.
4. Each occurrence becomes an independent Activity 14 days before its start, or immediately when already inside that window.
5. Students choose `Join this occurrence`, `Follow series`, or `Auto-join future occurrences`.
6. Every occurrence runs its own capacity, waitlist, Smart RSVP, attendance, outcome, and reliability lifecycle.

`Follow series` sends a bounded notice when a new occurrence opens but reserves no seat. `Auto-join` attempts to add the student to each new occurrence in subscription order; capacity may place them on the waitlist, and ordinary 3-hour confirmation still applies. Students can stop auto-join at any time without leaving already created occurrences.

The host can edit/cancel `This occurrence` or `This and future occurrences`. Completed/past occurrences never change. Cancelling the series cancels future created occurrences with participant notices and prevents new ones.

#### Delete, cancel, archive

- Delete is available only for a Draft with no external history and uses a short recoverable window where supported.
- A Published/Upcoming/Check-in/Live Activity is Cancelled, never deleted.
- Completed, Cancelled, and Expired Activities may be archived from personal default views; archival does not erase shared history.

### UX requirements

- Use a full page/step grouping rather than a long modal.
- Show timezone and human-readable duration beside date/time controls.
- Location selection includes accessibility and reveal policy.
- Requirements use constructive language; discriminatory/exclusionary text is reportable.
- Capacity copy says whether host counts and shows seats/waitlist implications.
- Destructive cancellation is visually separate from ordinary Save.
- Participant view leads with type, course, time, location, status, available seats, expectations, and primary action.
- Primary goal and estimated duration appear together; the completion prompt reuses the exact goal wording.
- Recurrence is stated in natural language with end date, next occurrence, follow/auto-join status, and exception dates.

### Business rules

- Host must be a verified member of the Activity course and is automatically confirmed.
- Start must be in the future when first published; end must follow start and remain within configured duration limits.
- Capacity includes host and cannot fall below current capacity-consuming participants without resolving them explicitly.
- Section visibility requires a section and eligible section membership.
- Exact private residential locations are prohibited in MVP.
- Online Activities must use allowed link schemes and reveal links only to eligible participants when configured.
- A material time change increments the confirmation cycle and invalidates obsolete reminders.
- Primary goal is required to publish. Editing it materially after people join sends an Activity update but does not reset RSVP unless requirements/scope also change substantially.
- MVP recurrence is weekly only, with at most 16 occurrences and no end date more than 16 weeks after the first start.
- Each recurring occurrence is operationally independent; cancelling/completing one does not alter others unless host explicitly selects future scope.
- Auto-join never guarantees capacity and never bypasses confirmation, requirements, suspension, blocks, or schedule-conflict warnings.
- Project Team Formation is a lightweight recruiting Activity, not a persistent team workspace; personal contact sharing remains subject to mutual consent.
- Host transfer is not MVP; host must cancel if unable to host. Co-host/transfer is future expansion.
- Plugin-defined Activity types must use core lifecycle/permission contracts and declare additional validated requirements; they cannot bypass safety or attendance policy.

### Validation rules

- Title, description, requirements, tags, capacity, duration, time horizon, and link/location fields meet configured bounds.
- Course, section, host, visibility, and location relationships are valid.
- Start time handles daylight-saving ambiguous/nonexistent local times with explicit correction.
- Tag count and combinations are bounded; duplicate tags collapse.
- Material edit requires current Activity version and explicit confirmation.
- Goal is 3–160 characters; objective list has at most five items of 3–120 characters each.
- Compatibility profile values use the controlled Study Preference vocabulary; expected course confidence may be Any or one/more adjacent levels.
- Recurrence weekday/time/timezone, count/end date, and exception scope are valid and within the 16-week limit.
- Project teammate openings cannot exceed Activity capacity minus host; deadline cannot precede Activity start and must be within the course/project policy horizon.

### Permissions

- Verified course members create course Activities.
- Host edits/cancels their Activity and views the host roster.
- Participants edit only their own participation/attendance intent.
- Course moderators may hide/cancel policy-violating Activities with reason and audit, but cannot pose as host.
- University/safety admins act only within scope and with audited reason.
- Unlisted visibility requires a valid share context but still enforces university/course eligibility policy.

### Edge cases

- Host creates an Activity starting inside the RSVP windows: participant confirmation is collected at join; elapsed reminders are skipped.
- Time/location changes while someone is responding: latest version wins and product requests reconfirmation if necessary.
- Capacity lowered below waitlist plus participants: waitlist may remain; confirmed participants cannot be silently removed.
- Course archived before Activity: upcoming Activity is reviewed/cancelled by host/admin; history remains.
- Host suspended: Activity is frozen from new joins and must be cancelled or reassigned through an audited admin process.
- Duplicate Activity accidentally published: host cancels duplicate; participants receive clear correction.
- Daylight-saving change occurs mid-series: preserve the chosen local weekday/time and show changed UTC offset in preview/notification.
- Auto-join student loses course eligibility or has a block/suspension: skip that occurrence and explain privately.
- Host edits only one recurring location/time: mark it as an exception without rewriting the series pattern.
- Team-formation Activity ends without filling roles: outcome records roles still open and offers a Version 1.1/publish-another-Activity path; it does not imply participant failure.

### Acceptance and success criteria

- Two engineers following the rules produce the same publish/edit/cancel outcomes for every state.
- No edit silently changes time/location/capacity for participants.
- Historical Activities cannot be erased to manipulate attendance/reliability.
- Activity type expansion does not create parallel RSVP/attendance semantics.
- Every published Activity exposes a specific primary goal and scheduled duration.
- Recurring occurrences never share RSVP, attendance, outcome, or reliability state.
- Project Team Formation supports course/skills/deadline discovery without creating an undeclared persistent team.
- Creation-to-publication completion and validation failure reasons are measurable.

### Future improvements

Co-hosts/host transfer, richer recurrence patterns, richer online/hybrid locations, templates, calendar sync, approval questions, plugin types, institutional Activities, and persistent Project Teams.

---

## 6. Activity lifecycle

**Release:** MVP

### Purpose and problem solved

Make every Activity state and legal transition predictable for students, hosts, reminders, attendance, and history.

### User stories

- As a participant, I can tell exactly what an Activity's current state means and what I can do next.
- As a host, I can publish, start, end, cancel, and narrowly correct an Activity through legal transitions.
- As a browsing student, I can distinguish an actually Live Activity from one that is merely scheduled.
- As a participant, I am not penalized when an Activity never validly starts.

### State definitions

| State | Meaning | Primary actions |
| --- | --- | --- |
| Draft | private, not joinable, no participant effects | edit, publish, duplicate, delete |
| Published | visible/joinable but outside Upcoming window | edit, join, bookmark, cancel |
| Upcoming | start is within 24 hours | confirm, join/waitlist, edit with warnings, cancel |
| Check-in | opens 15 minutes before scheduled start | check in, running late, can't attend, host start |
| Live | Activity has started | join if allowed, arrive, leave, chat later, complete |
| Ending | planned end is near/passed or activity confirmation is pending | continue, complete |
| Completed | ended with participation history finalized | view history, archive, limited correction/reopen |
| Cancelled | host/moderator terminated before normal completion | view reason/history, duplicate |
| Expired | published Activity passed completion grace without valid start/attendance | view/duplicate; no attendance penalty by default |

Published, Upcoming, and Check-in are product states derived from publication and time but have identical stable transition rules across clients.

### Transition rules

| From | To | Trigger |
| --- | --- | --- |
| Draft | Published | host publishes valid future Activity |
| Draft | deleted | host deletes unused Draft |
| Published | Upcoming | 24 hours before start |
| Published/Upcoming | Cancelled | host or authorized moderator cancels |
| Upcoming | Check-in | 15 minutes before start |
| Check-in | Live | host starts, or valid automatic-start rule succeeds |
| Published/Upcoming/Check-in | Expired | end + 15-minute grace passes with no valid start/check-in evidence |
| Live | Ending | planned end approaches/passes or still-active prompt awaits response |
| Ending | Live | eligible user confirms Continue |
| Live/Ending | Completed | host ends or automatic completion succeeds |
| Completed | Live | narrowly permitted correction within 15 minutes |

Cancelled and Expired do not return to active states. Duplicate creates a new Draft.

### Primary flow

1. Host publishes.
2. Product changes time-based display states automatically.
3. Check-in opens 15 minutes before start.
4. Activity becomes Live when host starts or when the configured automatic-start evidence exists (MVP: host check-in plus at least one other arrival, or explicit host Start).
5. Ending appears 15 minutes before planned end and whenever a still-active decision is due.
6. Activity completes explicitly or automatically; attendance/reliability finalize after the correction window.

### UX requirements

- Every state has a written label, explanation, relevant timestamp, and next action.
- Countdown is secondary to absolute time.
- Cancelled/Expired pages retain enough information to explain what happened without presenting active actions.
- Host controls show consequences and which state transition will occur.
- Realtime state change preserves focus and announces concise updates.

### Business rules

- Server-authoritative time determines transitions.
- Activity cannot enter Live before Check-in except authorized host early start within 15 minutes.
- Automatic start never uses mere page presence or Campus Presence.
- Completion locks ordinary RSVP/attendance actions after a 15-minute correction window.
- Reopen is only for accidental completion, only by host/moderator within 15 minutes, and is audited/notified. It cannot reopen Cancelled/Expired.
- Expired Activity does not create no-show evidence unless check-in/live evidence establishes that the Activity occurred.
- Cancellation includes a reason category; participant fault is never inferred from host cancellation.

### Validation and permissions

- Only legal source/target pairs are accepted.
- Stale state/version actions are rejected with current state displayed.
- Host controls ordinary start/complete/reopen/cancel.
- Authorized moderator can cancel for policy/safety and correct state with reason.
- Participant continuation signals influence Ending but cannot edit state directly.

### Edge cases

- Device clock is wrong: absolute server state wins.
- Host offline at start but attendees arrive: automatic start requires defined evidence; otherwise remains Check-in and later expires without penalty.
- Activity crosses midnight/timezone/DST: lifecycle follows stored instant and Activity timezone display.
- Completion and Continue arrive simultaneously: first legal transition wins; clients resync.
- Reopened Activity passes original end: it returns to Ending immediately and requires deliberate continuation.

### Acceptance and success criteria

- Every possible state exposes a deterministic set of actions and next transitions.
- Duplicate jobs/taps do not transition twice.
- Cancelled/Expired Activities never generate participant no-show penalties.
- Hosts and participants can explain why the current state exists.

### Future improvements

Recurring-series state, co-host quorum, institution-managed lifecycle, configurable check-in windows, and longer audited correction workflows.

---

## 7. Smart RSVP

**Release:** MVP, defining product capability

### Purpose and problem solved

Keep Activity rosters accurate by repeatedly turning passive joins into explicit, time-bounded attendance intentions and recovering unused seats.

### User stories

- As a participant, I know what I joined, when I must reconfirm, and what happens if I do not respond.
- As a host, I see confirmed, pending, declined, waitlisted, offered, and removed people accurately.
- As a waitlisted student, I receive a fair, time-bounded offer when a seat opens.
- As a late joiner, I can join without being subjected to already elapsed reminders.

### Participant states

Requested (future approval policy), Confirmed, Pending Confirmation, Declined, Waitlisted, Offered, Offer Expired, Left, Removed, Arrived, Running Late, Cancelled Late, and No Show. Host is Confirmed at publication.

### Standard timeline

| Time | Behavior |
| --- | --- |
| Immediately after join | receipt with Activity summary, current status, calendar-friendly time, leave action, and future confirmation expectation |
| Morning of | reminder at 08:00 Activity-local time when start is 10:00 or later; earlier Activities receive one consolidated reminder 2 hours before start |
| 3 hours before | status becomes Pending Confirmation; ask “Are you still attending?” with explicit Yes / Release my seat |
| 2 hours before | remind only still-pending participants |
| 1 hour before | remove still-pending participants, explain reason, and begin waitlist promotion |

Quiet hours may delay ordinary reminders but cannot delay a required confirmation past its deadline; onboarding/preferences explain this exception. Duplicate reminders within a short consolidated window are combined.

### Primary flows: join and confirmation

#### Normal join, more than 3 hours before

1. Product atomically assigns Confirmed or Waitlisted.
2. Confirmed participant receives timeline.
3. At 3 hours, participant becomes Pending Confirmation.
4. Yes returns to Confirmed; No becomes Declined and releases seat.
5. No response at 1 hour becomes Removed with reason `confirmation_timeout`.

#### Late join

- Between 3 hours and 1 hour: joining includes an explicit “Yes, I plan to attend” confirmation, so status begins Confirmed; applicable remaining reminders may occur.
- Between 1 hour and Check-in: join requires explicit intent and is not auto-removed for missing an elapsed confirmation.
- During Check-in/Live: join is permitted only by visibility/capacity/host policy and immediately asks arrival intent/check-in.

#### Leave/cancel attendance

Participant chooses Leave/Can't attend, sees timing consequence in neutral language, and confirms. Seat releases immediately. Activity history preserves the timing category; exact reason is optional/private and not shown to host unless user shares it.

### Waitlist promotion

1. Lowest eligible waitlist position receives one offer.
2. Offer reserves the seat during its response window.
3. Offer window: 30 minutes when start is over 3 hours away; 15 minutes at 1–3 hours; 5 minutes under 1 hour/check-in.
4. Accept becomes Confirmed and records explicit intent. Decline/expiry offers next eligible person.
5. Blocked, suspended, course-ineligible, already-conflicting, or unreachable candidates are skipped with auditable reason but retain fair treatment for future Activities.

### Host dashboard and overrides

Host sees grouped counts and students: Confirmed, Pending, Waitlisted, Offered, Declined/Left, Removed, and later attendance groups. Host may:

- remove a participant with policy reason;
- increase capacity and trigger promotions;
- close joining/waitlist;
- restore an erroneously removed participant only when a seat exists and the student accepts;
- resend a required prompt within rate limits;
- mark attendance later, but cannot fabricate a participant's RSVP response.

Host cannot skip the waitlist to favor another student unless a documented requirement/eligibility rule applies and the action is visible/audited.

### UX requirements

- Confirmation surface always repeats Activity, time, location summary, deadline, and consequence.
- Buttons use meaningful labels, never contextless Yes/No after scrolling.
- Status and deadline remain visible on dashboard/detail/notification.
- After timeout, explain “Your seat was released because the confirmation deadline passed” and offer waitlist/rejoin if eligible.
- Host roster does not use reliability color as the primary grouping.
- Countdown updates do not create urgency animation or shame.

### Business rules

- Capacity is never exceeded by concurrent joins/offers.
- One active participation identity exists per student/Activity; leaving/rejoining adds history rather than duplicates.
- Host counts toward capacity and cannot be auto-removed.
- Yes/No/leave/promote actions are idempotent.
- Material time/location changes may require reconfirmation and generate a new confirmation cycle.
- Host cancellation stops future RSVP actions and creates no participant penalty.
- Early cancellation (3+ hours) is treated as responsible behavior; late categories feed reliability policy only after Activity completion.
- Ignored waitlist offers do not affect reliability.

### Validation rules

- Response must be legal for current participant/Activity state and current deadline.
- Offer acceptance requires unexpired offer, eligibility, and reserved capacity.
- Capacity changes remain within location/instance limits.
- Host override requires allowed reason and current state.
- Running-late estimate must be a supported interval or bounded custom duration.

### Permissions

- Participant controls their RSVP/leave/late intent.
- Host views/manages only their Activity roster within allowed overrides.
- Course moderator sees roster only when needed for an active report/safety duty, with audit.
- Other participants see only product-approved aggregate/identity information, never private cancellation reasons.

### Edge cases

- Activity published less than 3 hours before start: joining is explicit confirmation; elapsed notifications are skipped.
- Activity time changes across reminder boundary: obsolete prompts become invalid; participant sees latest time and new deadline.
- Participant responds Yes at same instant timeout runs: first valid state transition wins and UI explains/refetches; no duplicate seat.
- Promoted student has notification delivery failure: in-app offer remains; short windows may skip only according to disclosed reachable-channel policy.
- Full Activity has pending people: waitlist is not promoted until a seat actually releases.
- Participant was removed but Activity capacity later grows: they may rejoin/waitlist; restoration is not automatic.

### Acceptance and success criteria

- Confirmed roster never exceeds capacity.
- Every automated removal/promotion is explainable by state, deadline, and notification history.
- Duplicate job delivery never duplicates a notification effect, participant, or offer.
- Confirmation response, confirmed-to-arrived, waitlist recovery, and host roster-accuracy metrics are measurable.

### Future improvements

Approval questions, deposits/credits only after ethics review, calendar response sync, co-host overrides, custom institutional timing policies, and accessibility-specific reminder accommodations.

---

## 8. Live attendance

**Release:** MVP; QR and location verification are future

### Purpose and problem solved

Record whether expected participants actually arrived, give hosts a live operational view, and produce fair reliability evidence.

### User stories

- As a participant, I can say I'm here, running late, or unable to attend.
- As a late participant, I can give an estimated arrival and check in later.
- As a host, I can see live counts and correct attendance mistakes.
- As a student, I can review my attendance history and appeal errors.

### Primary flow

1. Check-in opens 15 minutes before start.
2. Eligible participant sees `I'm Here`, `Running Late`, and `Can't Attend`.
3. I'm Here records arrival time; Running Late requests 5/10/15/30/60-minute estimate; Can't Attend records late cancellation category.
4. Host dashboard updates with Confirmed Not Arrived, Arrived, Running Late, Can't Attend, and No Response.
5. Running Late participant can update estimate, arrive, or cancel.
6. At completion/grace reconciliation, remaining eligible confirmed participants become No Show only if the Activity actually occurred.
7. Participant can view the result and request correction/appeal.

### UX requirements

- Check-in choices are large, labeled, and accessible on mobile.
- Display server-recorded time and clear correction action.
- Host dashboard uses grouped lists and counts; realtime updates preserve focus.
- Connection loss shows updates paused and reconciles before host actions.
- Manual host marking clearly identifies “Marked by host” to the participant.

### Business rules

- Self check-in is permitted only from Check-in through Activity completion grace and only for eligible participants.
- Campus Presence, opening the page, chat activity, or push delivery is not attendance evidence.
- MVP does not require GPS; location verification is future and opt-in/policy-reviewed.
- Host may mark Arrived, Running Late, Can't Attend, or No Show, but every change records actor/time/reason and notifies affected participant.
- Participant's explicit check-in normally outranks host No Show unless fraud/safety review intervenes.
- No Show finalizes only when Activity reached Live/Completed with credible occurrence evidence.
- Attendance correction window is 24 hours for participant request; moderator appeal remains available per retention policy.
- Leaving a Live Activity after meaningful attendance records checkout, not a no-show.

### Validation rules

- Attendance action must be legal for current state/time and participant.
- Estimated arrival is positive and no more than 60 minutes unless host extends Activity.
- Manual changes require a reason for downgrading Arrived or assigning No Show.
- Same action retry returns current result without duplicate history.

### Permissions

- Participant manages own arrival/late/can't-attend response.
- Host views and corrects their Activity attendance.
- Other participants see aggregate live count and allowed identities, not private late reasons/estimates unless shared.
- Safety moderator reviews disputed/tampered attendance in scope.

### Edge cases

- Participant checks in then loses connection: arrival remains recorded.
- Host and participant mark conflicting status: preserve both evidence; deterministic precedence plus appeal notice.
- Host never starts Activity but several participants check in: automatic-start rule may establish occurrence; otherwise moderation/reconciliation prevents unfair penalties.
- Participant arrives after being marked No Show but before completion grace: Arrived replaces provisional No Show with history.
- Activity cancelled while live for safety: attendance remains factual; cancellation changes reliability treatment.

### Acceptance and success criteria

- Host sees authoritative attendance changes within the realtime objective under normal conditions.
- No Show cannot be created for an Activity that did not occur.
- Participants can identify who/what set their attendance and appeal it.
- Attendance history deterministically feeds reliability after correction rules.

### Future improvements

Rotating QR check-in, NFC/beacon or privacy-reviewed location verification, check-out, attendance quorum, co-host verification, and offline signed check-in.

---

## 9. Live Activities

**Release:** MVP

### Purpose and problem solved

Tell students whether an Activity is truly happening now, keep status fresh, and end stale Activities automatically.

### User stories

- As a student nearby, I can tell whether an Activity is Live, Ending, or Completed.
- As a participant, I can join an eligible Live Activity, check in, or leave.
- As a host, I can see elapsed time, roster status, continue, or complete.
- As a participant, I can confirm the Activity is still active if the host is busy.

### Primary flow

1. Activity enters Live through lifecycle rules.
2. Live view shows elapsed time, planned end, location, participant count, and attendance groups appropriate to role.
3. At 60 minutes after Live start, or at planned end if sooner, eligible checked-in people receive “Is this Activity still active?”
4. `Continue` keeps/returns Live and schedules the next decision at the later of 60 minutes or planned end policy interval.
5. `End Activity` completes immediately after confirmation.
6. If no eligible response arrives within 15 minutes, Activity completes automatically.

### Activity outcome

Completion creates a factual outcome summary:

| Outcome field | Behavior |
| --- | --- |
| Primary goal status | Completed, Partially Completed, Not Completed, or Not Reported |
| Topics covered | host selects/adds up to 10 concise course-relevant topics |
| Attendance | derived from finalized attendance; never manually retyped into outcome |
| Actual duration | derived from Live start through completion, excluding later corrections |
| Planned duration | retained for comparison without grading the group |
| Team formation result | for Project Team Formation: openings filled/still open; no persistent roster in MVP |

When a host manually completes, the product asks for goal status and topics. The host may choose `Finish without reporting outcome`, which produces Not Reported—not Not Completed. Automatic completion also produces Not Reported and prompts the host to finish the outcome within 24 hours.

Participants can view the shared outcome and flag an inaccurate goal/topic summary. They cannot edit it in MVP. Host may edit within 24 hours; every change is visible in outcome history. Attendance corrections follow Chapter 8 and automatically update the attendance portion.

Goal status does not affect individual reliability in MVP. It informs the group's history, recommendation quality, and aggregate product analytics only. It is not a grade or instructor assessment.

### Join/leave Live

- Join is available only if visibility, course eligibility, host policy, time, and capacity allow it.
- Live join collects attendance intent immediately and may place the student on a live waitlist only if the host allows it.
- Leaving offers `Done studying` (checkout) or `Can't continue`; both preserve prior attendance.
- A participant who never arrived and leaves Live is treated according to late-cancellation policy, not checkout.

### UX requirements

- Timer is informative, not a productivity surveillance tool; it measures Activity elapsed time, not individual work.
- Still-active prompt includes Activity context and response deadline.
- Browsing cards show Live/Ending/Completed in text plus when status was last confirmed.
- Auto-completion confirmation explains that chat/history remains accessible according to policy.
- Completion keeps the primary goal visible and makes Completed/Partial/Not Completed/Not Reported equally available without celebratory or shaming defaults.
- Outcome shows planned versus actual duration, topics, and attendance using plain factual labels.
- Host dashboard prioritizes people needing action over decorative metrics.

### Business rules

- Timer uses server Live start time and continues across reconnects.
- Checked-in participant or host may Continue; only host/authorized moderator may explicitly End in MVP.
- One Continue response is enough to keep active; End by host wins over participant Continue if processed first.
- Automatic completion is idempotent and cannot complete Cancelled Activity.
- Completed Activity may be reopened only under lifecycle correction rule.
- Live presence is separate from Campus Presence and does not automatically make a student discoverable elsewhere.
- Outcome is scoped to people who can view the Activity. Aggregate course analytics suppress small groups and never expose an individual's goal performance.
- Host has 24 hours after completion to report/edit goal status and topics; later correction requires moderator-supported reason.
- Anonymous participant feedback is not collected in MVP.

### Validation and permissions

- Continue/End must be within eligible state/window.
- Live join cannot exceed capacity or bypass blocks/requirements.
- Host sees roster details; ordinary viewers see privacy-safe aggregate and permitted public Activity fields.
- Moderator may end an unsafe/policy-violating Activity with reason.
- Only host records/edits shared goal status/topics in the ordinary window; participants may flag inaccuracies and moderators may correct with audit.

### Edge cases

- No network at prompt: current Live status remains until deadline/reconciliation; clients resync.
- Activity planned for under an hour: prompt at planned end.
- Very long Activity: repeated confirmation intervals prevent stale Live status.
- All participants leave: host is prompted to end; if no response, automatic completion follows.
- Host leaves but others remain: Activity can continue through participant signal; host transfer remains future.
- Host never submits outcome: status remains Not Reported permanently after the window; product never converts it to Not Completed.
- Attendance changes after outcome: attendance summary updates while original duration/goal report remains attributable.

### Acceptance and success criteria

- Live status is never based solely on scheduled time.
- Stale Activities automatically complete after defined no-response window.
- Join/leave does not erase attendance already earned.
- Browsers can distinguish recently confirmed Live from Ending/stale state.
- Every Completed Activity exposes attendance, planned/actual duration, and an explicit goal state including Not Reported.
- Outcome completion rate, goal-status distribution, topic coverage, and planned-versus-actual duration are measurable only at appropriate aggregate scope.

### Future improvements

Co-host control, participant-voted ending, planned extensions, live agenda, check-out summaries, anonymous participant feedback in Version 1.1, and institution-managed official activities.

---

## 10. Campus Presence

**Release:** MVP

### Purpose and problem solved

Answer “Is anyone studying on campus right now?” and support spontaneous matching without requiring continuous location tracking or exposing individual whereabouts.

### Presence model

Presence has two independent choices:

1. **Visibility:** Invisible or Visible.
2. **Intent:** Busy, Available, Looking for Study Partner, or Currently Studying.

Invisible is the default and means the student contributes to no live campus count or matching pool. Visible requires an approved campus zone and expiry. Intent controls interaction eligibility:

| Intent | Aggregate counts | Can receive Need Help invitation | May appear as individual suggestion |
| --- | ---: | ---: | ---: |
| Busy | Yes | No | No |
| Available | Yes | Yes, preferences permitting | Only with separate partner-discovery consent |
| Looking for Study Partner | Yes | Yes | Yes, privacy-filtered/consented |
| Currently Studying | Yes, including selected course | Optional | Only with separate consent |

### User stories

- As a student, I can become visible at a library/approved zone for a limited time.
- As a privacy-conscious student, I remain invisible by default and can disappear immediately.
- As a student, I can see thresholded counts and course distribution at nearby campus study zones.
- As a student looking for a partner, I can signal intent without publishing my exact coordinates.
- As a busy student, I can contribute to aggregate activity while declining invitations.

### Primary flows

#### Become visible

1. Student opens Campus Presence and sees a concise privacy explanation.
2. Student selects an approved campus zone manually; optional coarse device location may suggest zones only after permission.
3. Student selects intent, optional course, and duration: 30, 60, or 120 minutes.
4. Student confirms what will be visible and whether they can receive invitations.
5. Presence appears in aggregate after privacy thresholds; persistent header/control shows remaining time and Go Invisible.

#### Browse campus

1. Student sees approved locations ordered by proximity only when location permission exists, otherwise by campus/default popularity.
2. Each location shows current visible count, thresholded course breakdown, Active Activities, and last-updated freshness.
3. Heatmap/list never reveals a precise person's position.
4. Selecting a location shows eligible public Activities and, only with mutual/explicit discovery settings, limited nearby partner suggestions.

#### Renew/change/end

Student can extend within maximum, change intent/course, switch zone with reconfirmation, or Go Invisible immediately. Expiry requires a new deliberate renewal; no silent indefinite presence.

### UX requirements

- Presence toggle always says whether the student is currently Invisible/Visible and until when.
- Permission request explains that device location is optional and used only to suggest approved zones.
- Heatmap has an accessible list/table equivalent and never relies only on color intensity.
- Course counts below the configured privacy threshold display as “Other courses” or are omitted.
- Nearby student cards, when enabled, show course/study compatibility and broad zone—not exact seat/floor—until mutual acceptance.
- Busy status suppresses invitations visibly.

### Business rules

- Default is Invisible for every new account/device and after logout, suspension, or expiry.
- Presence requires verified university status.
- Only approved public/campus zones are supported; no private homes in MVP.
- Maximum presence duration is 120 minutes before explicit renewal.
- Public location total is shown only when at least 3 visible students are present. A course breakdown appears only when that course has at least 3 visible students. Threshold values are instance policy but cannot be lower than the safety minimum without an explicit documented fork/policy review.
- Hidden small groups may contribute to the location total but not a revealing category.
- Presence does not prove attendance, create reliability evidence, or expose a person's exact route/history.
- Individual partner discoverability is a separate explicit consent; Visible alone means aggregate visibility.
- Blocked users are excluded from each other's individual suggestions and matching; aggregates remain non-identifying.
- Presence history is not offered as a profile feature.

### Validation rules

- Zone is active, approved, and belongs to the student's current university context.
- Duration and intent are supported values.
- Currently Studying course must be an active membership and visibility-eligible.
- Device coordinates, if used for suggestions, must not be stored as the canonical presence location.
- Updates from a stale/expired presence cannot revive it without explicit renewal.

### Permissions

- Verified student manages only own presence.
- Other students see thresholded aggregates and consented suggestions.
- University admins manage approved zones and view aggregate operational analytics, not a live individual-location dashboard.
- Safety moderators may access narrowly scoped evidence only for a reported incident under audit/retention policy.
- Plugins receive aggregates only by default; individual presence capability is prohibited in MVP.

### Edge cases

- Only one/two visible students: location/course counts are hidden even from another nearby student.
- Student goes offline: presence expires on schedule; offline alone does not immediately expose or hide a person unpredictably.
- Realtime presence service failure: product marks counts unavailable/stale and clears ephemeral presence rather than claiming visibility is current.
- Student switches course while studying: aggregate categories update subject to thresholds.
- Student blocks someone after suggestion: suggestion and pending invitation disappear promptly.
- University spans campuses/timezones: zones and display context identify campus clearly.

### Acceptance and success criteria

- A new user is never visible without deliberate action.
- Go Invisible and expiry remove individual matching eligibility immediately and aggregates within the realtime objective.
- No UI reveals a course/location group below the privacy threshold.
- Campus view helps students discover active zones/Activities, measured without retaining movement history.
- Zero individual-presence disclosure incidents is the guardrail.

### Future improvements

Opt-in friend visibility, privacy-preserving occupancy integrations, campus map partnerships, accessibility/crowding details, verified room availability, and institution-configured zones. Background presence remains out of scope without a separate privacy review.

---

## 11. Need Help Now

**Release:** MVP

### Purpose and problem solved

Help a student obtain immediate, course-relevant peer assistance when scheduling a future Activity is too slow.

### User stories

- As a student stuck on a course topic, I can request help now with a clear expiry.
- As an available classmate, I can privately accept or decline a relevant invitation.
- As either party, I can avoid revealing identity/location until both sides agree.
- As a student, I can stop a request and avoid repeated/unwanted invitations.

### Request fields

Course, short topic, help mode (`in_person`, `online`, or `either`), optional approved campus zone, desired duration (15/30/45/60 minutes), language preference, and expiry (default 15 minutes; max 30). Free-form topic explicitly warns against sharing exam answers or sensitive information.

### Matching eligibility

A candidate must:

- be an active verified student in the same tenant/university context;
- have active membership in the course or an explicitly eligible equivalent/cross-listing;
- be Available, Looking for Study Partner, or Currently Studying with invitations enabled, or have separately enabled online help availability;
- match help mode/zone constraints where applicable;
- not be blocked in either direction;
- not be suspended, over invitation limits, in quiet hours, or already committed to a conflicting accepted Activity;
- satisfy language preference when marked required;
- not be the requester.

Reliability may break ties among otherwise eligible candidates but cannot create a hard exclusion by itself. New users remain eligible.

### Initial matching algorithm

Deterministic score, applied after eligibility:

| Signal | Priority contribution |
| --- | ---: |
| Same exact course/section | highest; section is a small tie-breaker |
| Explicit Looking/Available status | high |
| Same approved zone for in-person | high |
| Study-style/help-mode compatibility | medium |
| Language match | medium |
| Prior successful collaboration with requester | medium |
| Currently studying the course | medium |
| Coarse reliability band/confidence | small tie-breaker only |
| Invitation fatigue/recent decline | strong negative/suppression |

Candidates with equal scores are rotated fairly rather than always favoring the same people. The product does not claim AI matching.

### Primary flow

1. Requester presses Need Help and enters request details.
2. Product previews privacy, expiry, candidate scope, and expected conduct.
3. Request becomes Searching; requester can cancel at any time.
4. Wave 1 privately invites up to 3 highest eligible candidates for 3 minutes.
5. If nobody accepts, Wave 2 invites up to 5 additional candidates for 5 minutes, optionally broadening from same zone to online/either only when requester pre-authorized it.
6. If still unmatched, product offers: extend once up to total 30 minutes, create/publish a future Activity, adjust mode/topic, or end.
7. First valid acceptance creates a provisional match; requester has 2 minutes to confirm when more than one candidate responded.
8. Mutual acceptance reveals agreed display identity and broad meeting context, then creates an Ad-Hoc Help Meetup Activity.
9. Other pending invitations close with “Another student connected” and no penalty.

### UX requirements

- Searching state shows elapsed/remaining time, current scope, cancel, and what will happen next.
- Candidate invitation states course/topic, mode, broad zone, estimated duration, expiry, and Accept/Decline; it does not reveal exact location/private profile fields.
- No infinite spinner: every wave has a deadline and recovery actions.
- Decline requires no reason; optional feedback is private and not shown to requester.
- Mutual match provides safety guidance, block/report, and a public meeting-location reminder.
- Requester cannot message candidates directly before acceptance in MVP.

### Business rules

- One active Need Help request per requester.
- Default expiry is 15 minutes; one extension may reach 30 total.
- Wave/limit values are product policy and displayed where relevant.
- A candidate receives at most 3 Need Help invitations per hour and 10 per day by default; declines/busy status reduce future invitations.
- Requester may create at most 3 requests per day initially, with abuse-aware adjustments for pilots.
- Decline, ignore, timeout, or cancel has no reliability effect.
- A completed Ad-Hoc Help Activity may contribute ordinary attendance/reliability evidence only if both parties mutually accepted and valid attendance occurred.
- Matching never exposes a list of all online/nearby students.
- Exact location is an approved meeting place and is revealed only after mutual acceptance.
- Academic-integrity policy prohibits requests for live exam answers, impersonation, or prohibited assignment completion.

### Validation rules

- Topic is bounded, nonempty, sanitized, and checked against policy/reporting rules without pretending automated checks are perfect.
- Course membership and help mode are valid.
- In-person request requires an approved active zone; online request follows safe-link policy after match.
- Duration/expiry/language are supported values.
- Accept is valid only for an active invitation and eligible candidate.

### Permissions

- Verified course member creates a request.
- Eligible candidates receive only invitations selected for them.
- Requester and accepted helper see the matched Activity and progressively disclosed details.
- Moderators access request content only for reports/safety, with audit.
- University admins see aggregate demand/outcome analytics, not individual help topics by default.

### Edge cases

- Two candidates accept simultaneously: both responses are recorded, requester selects within 2 minutes; unselected candidate receives neutral closure.
- Requester cancels as candidate accepts: first valid state wins; no Activity is created without mutual confirmation.
- Presence expires during matching: candidate remains eligible only if their invitation/availability policy permits; in-person location is reconfirmed before acceptance.
- No candidate exists: offer future Activity and notification when relevant Activity appears; never fabricate “students nearby.”
- Candidate reports request: close their invitation immediately; safety policy may pause request.
- Requester repeatedly rejects helpers: rate/fatigue rules protect candidates; no public consequence.

### Acceptance and success criteria

- Every request reaches matched, cancelled, expired, or converted-to-future-Activity state within a bounded time.
- Candidates are never identifiable before appropriate consent.
- Blocks, busy status, quiet hours, invitation caps, and university/course scope are enforced.
- Time to first acceptance, mutual-acceptance rate, completed help outcomes, declines, fatigue, reports, and fallback-to-Activity are measurable.

### Future improvements

Group help requests, trusted-peer circles, online availability schedules, mentor/tutor routing, calendar-aware matching, topic taxonomy, accessibility matching, and opt-in intelligent ranking after fairness/privacy evaluation.

---

## 12. Reliability score

**Release:** MVP

### Purpose and problem solved

Give students and hosts a fair, explainable signal of follow-through so rosters become more dependable without shaming new users or measuring academic ability.

### User stories

- As a student, I can see my exact score, band, contributing outcomes, and how to improve.
- As a host, I can see a coarse reliability band and evidence count for current participants.
- As a student, I can appeal an incorrect attendance outcome.
- As a new student, I can participate without being treated as unreliable.

### Scoring model

Reliability is a decayed evidence estimate from eligible participation outcomes. It is not manually editable.

For each eligible outcome, assign quality `q`, weight `w`, and age decay `d`:

| Outcome | q | w | Product rationale |
| --- | ---: | ---: | --- |
| Arrived/attended | 1.00 | 1.00 | fulfilled commitment |
| Hosted and completed valid Activity | 1.00 | 0.50 additional | accountable hosting, bounded bonus |
| Running late then arrived ≤15 min | 0.80 | 1.00 | attended with manageable delay |
| Running late then arrived >15 min | 0.60 | 1.00 | partial follow-through |
| Cancelled/released seat ≥3h early | 1.00 | 0.25 | responsible low-weight behavior |
| Cancelled 1–3h before | 0.40 | 0.75 | limited recovery time |
| Cancelled <1h / never arrived after late | 0.10 | 1.00 | last-minute impact |
| Ignored required confirmation and removed | 0.25 | 0.50 | lower severity than no-show |
| No show at an Activity proven to occur | 0.00 | 1.50 | highest roster impact |

Age decay is `d = 0.5^(age_in_days / 90)`, so evidence has a 90-day half-life.

The score is:

`round(100 × (8 + Σ(d × w × q)) / (10 + Σ(d × w)))`

The `8/10` prior begins internally at 80 and prevents extreme scores from one event. Product displays `New` rather than a number until at least 3 eligible primary outcomes exist. The hosted bonus is not a primary outcome for that threshold.

### Display bands

| Display | Rule |
| --- | --- |
| New | fewer than 3 eligible primary outcomes |
| Highly reliable | score 90–100 and at least 5 primary outcomes |
| Usually reliable | score 75–89, or 90+ with only 3–4 outcomes |
| Building consistency | score 60–74 |
| Reconfirmation recommended | score below 60 |

The user sees exact score and band. Hosts see band plus eligible-outcome count; ordinary students do not see the score. A five-star visualization, if used, is derived from the score and always accompanied by text; it is not a separate metric.

### Primary flow

1. Eligible attendance/cancellation fact finalizes after the correction window.
2. Reliability event appears in the student's private history with neutral explanation.
3. Score recomputes under the active policy version.
4. Student is notified only for material band change or negative new evidence, not every small point change.
5. Host roster reflects the latest coarse band on next authorized view.

### Appeals

1. Student selects an event and `Request review` within 30 days.
2. Student chooses reason and optional bounded explanation/evidence.
3. Event becomes Disputed and is excluded from score while open.
4. Scoped moderator reviews Activity/attendance history and may uphold, correct, or void.
5. Student receives decision and score recalculates. A further appeal follows instance policy.

### UX requirements

- Explain what reliability measures and explicitly what it does not measure.
- Use neutral event copy: “No arrival was recorded,” not “You failed.”
- Show decay and new-user behavior in plain language without requiring formula comprehension.
- Provide concrete improvement guidance: confirm, release seats early, check in.
- Hosts cannot sort/search the platform globally by exact score.
- Low band never blocks safety-critical information or account access.

### Business rules

- Only Activities proven to occur create no-shows.
- Host cancellation, Activity expiration, moderation cancellation, waitlist decline/expiry, Need Help decline/ignore, and ordinary Campus Presence do not reduce score.
- One source outcome creates at most one primary reliability event.
- Policy version is recorded; historical scores can be rebuilt consistently.
- Disputed/voided/expired evidence is excluded as defined.
- Host manual downgrade alone is reviewable evidence and not unquestionable truth.
- Exact event history is private to the student and authorized appeal moderators.
- Reliability is a small matching tie-breaker, never the sole eligibility gate.

### Abuse prevention

- Self-hosted solo/private Activities and repeated pairs may require corroboration before reliability credit.
- Suspicious reciprocal hosting/check-ins, impossible overlaps, mass manual attendance changes, and unusual score farming enter review; they are not publicly labeled.
- Hosts cannot edit scores or delete negative history.
- Moderator changes require reason/audit and cannot target a protected group policy.
- Fairness review compares error/appeal outcomes across cohorts only with privacy-preserving, appropriate data.

### Validation and permissions

- Outcome, Activity occurrence, timing, and source evidence must be valid and unique.
- Appeal is within window, belongs to requester, and is not already open.
- Student views own exact score/events.
- Host views coarse band/count only for their relevant Activity roster and bounded time.
- Moderator views event evidence only for assigned appeal/report.
- Plugins receive no individual reliability data by default.

### Edge cases

- Score rounds across a band boundary: use unrounded internal result for band, rounded number for display.
- Policy changes: new snapshots use new policy; product explains material change and preserves auditability.
- Student has old events only: decay moves estimate gradually toward prior; it does not plummet from inactivity alone.
- Corrected No Show becomes Arrived: void original evidence and recalculate, preserving history.
- Account deletion: remove public/private access and apply retention/anonymization policy to factual Activity records.

### Acceptance and success criteria

- Same eligible history/policy/time yields the same score and band.
- New users are displayed as New and remain eligible for Activities/matching.
- Every score-changing event has a human-readable source and appeal path.
- Hosts never receive exact scores/event histories through normal product surfaces.
- Appeal frequency, overturn rate, roster accuracy, and cohort guardrails are monitored before stronger use of the score.

### Future improvements

Version 1.1 may add separate Communication, Helpfulness, and Preparedness categories based on eligible post-Activity feedback. They remain distinct from Reliability, require sufficient evidence, and never rewrite attendance facts. Later improvements include policy simulation, institution-specific reviewed policy variants, confidence intervals, emergency grace workflows, verified checkout/duration, and richer anti-collusion review. Reliability never expands into academic performance or a generic popularity score.

---

## 13. Chat and messaging

**Release:** Activity chat and course discussion are Phase 2 candidates; direct messages are later. MVP uses structured host updates and notification replies/actions only.

### Purpose and problem solved

Support academic coordination in the correct context without allowing generic messaging to overshadow Activity discovery and accountability.

### User stories

- As an Activity participant, I can coordinate materials, arrival, and changes with the group.
- As a course member, I can discuss course-relevant topics in a moderated space.
- As a user, I can edit/delete my message and report harmful content.
- As a host/moderator, I can pin essential context without rewriting another person's message.
- Later, as two mutually eligible students, I can direct-message under strict privacy/safety controls.

### Channel types

| Channel | Membership | Lifecycle |
| --- | --- | --- |
| Activity chat | host plus eligible participants | opens at publication/join; read-only after configured post-completion period |
| Course discussion | active course members | follows course term/archive policy |
| Direct message | mutually eligible, not blocked users | later release; explicit request/acceptance may be required |

### Core behavior

- Text messages with created/edited timestamp.
- Edit retains “Edited” label and moderation history.
- User delete replaces content with a deleted marker; moderation evidence retention is separate/private.
- Attachments/images use the file safety flow before publication.
- Links are clearly identified; unsafe schemes blocked; preview is optional and privacy-safe.
- Replies reference a message with graceful deleted/unavailable fallback.
- Reactions are from a controlled, accessible set and show aggregate counts; no anonymous harassment reactions.
- Pinned messages retain original author and show who pinned.
- Typing indicators are ephemeral, optional, and never attendance/presence evidence.
- Read receipts are off by default for groups; MVP/Phase 2 may provide last-read position and unread count instead of per-person receipts.

### Primary flow

1. Eligible member opens channel and sees context/header, rules, pins, and chronological messages.
2. User composes text/attachment/reply and sees upload/scanning state where applicable.
3. Message appears only after accepted; failure retains draft and offers retry.
4. New messages do not steal scroll position; user receives a new-message control.
5. User can edit/delete/report from accessible message actions.

### UX requirements

- Channel header preserves course/Activity identity and status.
- Composer remains accessible above mobile keyboard/safe area.
- Message actions work by keyboard and do not rely on hover.
- Timestamps, author, reply context, edited/deleted, pin, and attachment status are screen-reader understandable.
- Loading older messages preserves reading position.
- Completed/archived channel state is explicit before user composes.

### Business rules

- Activity membership changes update chat access promptly. Removed participants retain only the history policy permits and cannot send.
- Course leave removes send access; historical read access follows course policy.
- Direct messages never bypass blocks, suspension, university scope, or safety restrictions.
- Editing/deleting does not erase moderation/audit evidence during its lawful retention.
- A pin is not an official university announcement unless posted through that separate role/surface.
- Message content does not affect reliability.
- No end-to-end encryption claim in initial releases.

### Validation rules

- Text, reply depth, reactions, attachment count/size/type, links, and rate meet limits.
- Sender remains eligible at send time.
- Edit/delete targets sender-owned message and allowed time/policy.
- Pin action targets same channel and active eligible message.

### Permissions

- Eligible members read/send according to channel.
- Author edits/deletes own message.
- Activity host pins/unpins Activity messages and may remove content only through disclosed moderation policy.
- Course/safety moderators act in scope with reason/audit.
- Instance operators do not browse messages absent authorized support/safety process.

### Edge cases

- Sender removed while message sends: eligibility at acceptance decides; client reconciles.
- Attachment scan fails after upload: no attachment publication; safe retry/remove.
- Replied-to message deleted: retain minimal “Original message unavailable” reference.
- User blocks participant in shared Activity: hide direct interaction and apply group-safety policy without silently ejecting either person unless necessary.
- Offline composition: retain local draft; never claim delivered until confirmed.

### Acceptance and success criteria

- Messaging improves Activity coordination without being required to RSVP/check in.
- Ineligible/blocked users cannot send or retrieve protected channel content.
- Edit/delete/pin/report history is explainable to moderators.
- Chat notification volume and reports remain within guardrails before direct messages launch.

### Future improvements

Direct messages, threads, polls, code/math formatting, translation, voice/video integrations, retention controls, and plugin bots with explicit identity/permissions.

---

## 14. Notes and resources

**Release:** Phase 2; not MVP

### Purpose and problem solved

Keep useful course materials discoverable, attributable, versioned, and moderated instead of scattered across chats.

### User stories

- As a course member, I can upload a PDF, image, Markdown document, or slides I have the right to share.
- As a student, I can search, preview, bookmark, and mark a resource helpful.
- As an author, I can upload a corrected version without losing history.
- As a course member, I can comment or report academic-integrity/copyright issues.

### Primary flow

1. Member chooses course and Upload Note/Resource.
2. User supplies title, description, category, tags, source/rights attestation, and files.
3. Upload shows progress, then Processing/Scanning.
4. Ready content becomes visible under selected permission; rejected content explains safe next action.
5. Author may publish a new version with change note; prior version remains history according to policy.

### Categories

Lecture notes, study guide, formula/reference sheet, worked practice, slides, lab reference, project resource, and external link. Official university/instructor material is not labeled official without verified authority.

### UX requirements

- Never show Published before scanning/processing succeeds.
- File type, size, author, version, updated date, accessibility/extracted-text availability, and permission are visible.
- PDF/slides preview has download and accessible alternative where available.
- “Helpful” replaces popularity-oriented Like in primary copy; bookmarks are private.
- Upload interruption retains metadata and offers retry.

### Business rules

- Notes belong to a course and author; optional Activity link is contextual.
- User must attest sharing rights and academic-integrity compliance.
- Prohibited: leaked exams, unauthorized answer keys, personal student records, malware, and copyrighted material without rights.
- New version does not overwrite attribution/comments silently; version-specific comments remain anchored where possible.
- Helpful reaction is one per user/versioned note and can be removed.
- Bookmark is private.
- Search indexes only Ready content the viewer can access.
- Deleting author account follows attribution/anonymization and shared-resource policy; it does not necessarily erase lawfully shared course value.
- Future AI processing is off by default and requires separate consent/rights/provider policy.

### Validation rules

- Supported type, actual content signature, size/page limits, nonempty title, category, tags, and rights attestation.
- Course membership/permission valid at final publication, not only upload start.
- Markdown and links are sanitized; images/PDF/slides pass scanning.
- New version must reference same logical note and allowed file/category compatibility.

### Permissions

- Active course members view course-visible Ready notes.
- Eligible members upload according to course policy.
- Author edits metadata, versions, and requests removal.
- Course moderator hides/quarantines reported content; copyright/safety operator handles escalations.
- Nonmembers and plugins receive no file/content access without explicit scoped policy.

### Edge cases

- Course archived: existing resources become read-only; new upload disabled.
- Author leaves course: existing accepted resources follow policy; author cannot add versions unless membership restored.
- Scan service unavailable: remain Processing and notify later; never fail open.
- Copyright report targets one version: quarantine affected material while preserving case/history.
- Search extraction fails: file may remain downloadable with “Text search unavailable.”

### Acceptance and success criteria

- Only scanned, authorized, Ready content is discoverable/downloadable.
- Version/author/rights/moderation state is never ambiguous.
- Students can find relevant resources without browsing chat history.
- Report/takedown and accessibility guardrails are operational before launch.

### Future improvements

Collaborative Markdown, OCR, citations, collections, instructor verification, open educational resource licensing, export, and separately governed AI summary/flashcard/quiz plugins.

---

## 15. Student dashboard

**Release:** MVP with focused sections; announcements/streak richness later

### Purpose and problem solved

Give each student one prioritized answer to “What should I do next?” without becoming a generic engagement feed.

### User stories

- As a participant, I immediately see RSVP/check-in/help actions needing attention.
- As a student, I see today's and upcoming relevant Activities.
- As a student, I can see campus study density and start Need Help Now.
- As a student, suggested Activities show Study Compatibility and the primary goal.
- As a student, I understand my private reliability/streak summary.

### Priority order

1. Safety/account state notices.
2. Waitlist offer or Need Help mutual-match response with deadline.
3. Required RSVP confirmation.
4. Check-in/Running Late action for imminent/live Activity.
5. Today's Activities.
6. Active Need Help request/search state.
7. Campus Presence control and nearby aggregate locations.
8. Upcoming and suggested Activities.
9. Recent courses/announcements.
10. Private reliability and study streak summaries.

### Primary flow

1. Student opens dashboard.
2. Product composes bounded sections using current university/timezone and permissions.
3. Student completes action inline or opens its detail.
4. Section updates from authoritative result; failure is local to the section where safe.
5. “See all” navigates to full filtered view rather than infinitely extending dashboard.

### UX requirements

- Only one top Action Needed region; deadlines sorted soonest first.
- Today uses a chronological agenda with status and location.
- Presence card always shows current Invisible/Visible state before campus counts.
- Need Help primary action is available but not shown during suspension/unverified state.
- Reliability/streak never outranks time-sensitive coordination.
- Skeletons match final section; partial errors support per-section retry.

### Business rules

- Dashboard is personalized and never shared-cache/public.
- Past/expired actions disappear or become explanatory history promptly.
- Suggestions exclude joined/cancelled/ineligible/blocked/hidden Activities.
- Compatibility shown here follows Chapter 17 coverage/privacy rules and is never a public profile attribute.
- Announcement count is bounded and scoped to active courses.
- Study streak and reliability are private summaries.
- A pending Need Help request replaces the create prompt with current search state.

### Validation and permissions

- Every item is reauthorized when action occurs.
- Dashboard cannot grant access not available on underlying resource.
- Unverified user receives onboarding/verification dashboard, not protected previews.
- Admin role does not alter student dashboard unless user explicitly switches to admin workspace.

### Edge cases

- No courses: focus on join-course flow, not empty recommendations.
- No Activities: offer create/Need Help/Campus Presence, subject to verification.
- Timezone changes mid-day: recompose Today with clear timezone; never duplicate Activity.
- One section fails: remaining sections stay usable with request ID/retry.
- Offline cached dashboard: label stale and disable authoritative actions until reconnection/recheck.

### Acceptance and success criteria

- Students can identify and complete the most urgent coordination action without searching.
- No expired confirmation/offer remains actionable.
- Dashboard improves time to first relevant Activity/help outcome.
- Section engagement is measured without optimizing for compulsive feed use.

### Future improvements

Calendar view, configurable section order, richer announcements, progress reflection, course widgets, and accessibility-preserving plugin panels.

---

## 16. Search

**Release:** MVP for universities, courses, Activities, approved locations, and privacy-eligible students; notes/tags and saved searches later

### Purpose and problem solved

Let students directly find academic context, people, Activities, and campus places without exposing protected membership/location data.

### User stories

- As a student, I can find a course or Activity by code, title, tag, time, or location.
- As a student, I can find compatible same-university classmates who opted into discovery.
- As a visitor/onboarding user, I can find a university.
- Later, as a course member, I can search notes/resources and save a useful query.

### Search domains and MVP rules

| Domain | Who can search | Key filters/sorts |
| --- | --- | --- |
| Universities | visitor/eligible users | name, country/campus; relevance/name |
| Courses | university-scoped users | code, title, department, term; relevance/code |
| Activities | verified eligible users | course, type, status, time, seats, zone, tags; recommended/soonest/newest |
| Students | verified same-university/shared-context users | mutual course, study style, language, broad availability; relevance only |
| Locations | verified university users | approved zone/building/accessibility; relevance/distance when permitted |
| Notes | Phase 2 course members | title/content/category/tag/type; relevance/recent/helpful |

### Primary flow

1. User enters query or opens domain search.
2. Short global results group by type and show only a few authorized matches.
3. “See all” opens domain page with explicit filters/sort.
4. Applied filters are visible/removable and represented in shareable navigation where privacy-safe.
5. Pagination preserves stable ordering and does not reveal hidden result counts.

### UX requirements

- Search is a full page on mobile; desktop quick search may use an overlay for navigation.
- Results show why they match: mutual course, Activity type/time, university/campus—not reliability.
- No-results distinguishes no data, restrictive filters, missing catalog, and permission/verification.
- Recent searches remain local/private by default and can be cleared.
- Accessible list view is primary; map/heatmap is complementary.

### Business rules

- Authorization/filtering occurs before pagination/count display.
- Student search excludes users who disabled discovery, blocked viewer, are suspended, or lack legitimate university context.
- Presence does not make a student globally searchable; nearby suggestions follow Campus Presence consent.
- Unlisted Activities are not searchable.
- Exact total counts may be omitted for high-churn/private domains.
- Search query/content is not used to train AI or shared with plugins by default.

### Validation rules

- Query length/characters/rate are bounded; empty query follows domain browse behavior.
- Filters/sorts are allowlisted, compatible, and scoped.
- Time range is valid and timezone explicit.
- Location distance requires permission/current campus and never stores raw search coordinates beyond necessity.

### Permissions

Search returns only resources the actor could open. Admin search is a separate workspace with explicit audited purpose; student search does not gain admin data because the user has a role.

### Edge cases

- Result becomes private between search/open: open returns concealed unavailable state.
- Duplicate university/course aliases: show canonical record and matched alias.
- Block occurs between pages: subsequent pages and cached items remove blocked user.
- Search index delay: recently created Activity remains reachable from direct/course/dashboard and eventually appears; freshness indicator only where needed.

### Acceptance and success criteria

- Search never reveals protected course membership, presence, private Activity, or reliability.
- Students can find known courses/Activities using common aliases/codes.
- Search-to-join/help/profile outcomes are measurable by domain without storing sensitive query content unnecessarily.

### Future improvements

Saved searches/alerts, typo/synonym administration, federated catalogs, notes full text, semantic search after governance, and accessible campus maps.

---

## 17. Study Compatibility and recommendations

**Release:** MVP compatibility for Activities and mutually discoverable study partners, plus deterministic Activity suggestions and Need Help candidate ranking

### Purpose and problem solved

Match students on how they study—not only shared course/time—and surface useful Activities/partners with an explainable score. This is a core differentiator from generic group messaging products.

### User stories

- As a student, I see Activities from my courses that fit my availability/preferences.
- As a student, I see a compatibility percentage and truthful reasons such as shared quiet/evening/Exam 2 preferences.
- As an opt-in student, I can evaluate a mutually discoverable study partner without exposing private schedule details.
- As a student, I understand why an Activity was recommended and can dismiss it.
- As a Need Help requester, eligible candidates are ranked fairly and privately.

### Compatibility eligibility

Compatibility is calculated only after permission and hard eligibility:

- Activity: viewer can open/join it, belongs to the relevant course context, and has no blocking/suspension/visibility conflict.
- Student partner: both are verified in the permitted university/course context, both opted into partner discovery, neither blocked the other, and neither is Busy.
- A hard modality conflict (`online only` versus `in person only`) or no overlap in required time removes a candidate rather than presenting a misleading low score.

Compatibility never grants access or guarantees a good partnership.

### Compatibility formula

For each comparable dimension, multiply its weight by its match value. Exact match is `1.0`, compatible/adjacent match is `0.5`, and conflict is `0`. Multi-select values use overlap divided by the combined unique selected values. Missing/`No preference` dimensions are removed from both numerator and denominator.

`Compatibility = round(100 × matched_weight / comparable_weight)`

| Dimension | Weight | Match behavior |
| --- | ---: | --- |
| Same course | 15 | exact active course required; shared section is an explanation/tie-breaker |
| Shared goal/topic | 10 | same exam/assignment/topic exact; related course tag adjacent |
| Study style | 15 | Quiet, Discussion, Problem Solving, Coding, Exam Revision, Group Learning overlap |
| Interaction style | 10 | silent/minimal/conversational/discussion compatibility matrix |
| Preferred time/availability | 15 | fixed Activity fits stated block, or partner blocks overlap |
| Modality | 10 | in-person/online/either |
| Session length | 10 | exact bucket or adjacent bucket |
| Study pace/course confidence | 7 | exact/adjacent level; teaching-help intent may make complementary levels compatible |
| Learning method | 4 | Explain, Practice, Discussion, Silent overlap |
| Environment | 4 | Library, Coffee Shop, Campus Common Area, Online, or private-space preference |

Deterministic compatibility details:

- Ordered adjacent pairs scoring `0.5`: Silent↔Minimal speaking, Minimal speaking↔Conversational, Conversational↔Discussion-led; Slow↔Balanced, Balanced↔Fast; 30m↔1h, 1h↔2h, 2h↔4+h; Building↔Comfortable, Comfortable↔Advanced. Non-adjacent ordered values score `0`.
- `Either` modality scores `1` with In person or Online. In-person-only versus online-only is a hard conflict.
- For a fixed Activity time, availability scores `1` when fully contained in a preferred block, `0.5` when at least half overlaps, otherwise `0`. For partner blocks, at least 60 minutes overlap scores `1`, 30–59 minutes scores `0.5`, and less than 30 scores `0`.
- Multi-select Study Style, Learning Method, and Environment score `intersection count ÷ union count`.
- Shared goal/topic scores `1` for the same explicit assignment/exam/topic identifier, `0.5` for overlapping general course topic/tag, and `0` otherwise.
- Building↔Advanced scores `1` only when the Advanced student explicitly selected Explain concepts/“open to helping” and the other student requested that mode; otherwise it scores `0`.

The percentage is displayed only when comparable weight is at least 60. Otherwise show `Limited compatibility information` with available reasons and an invitation to complete preferences. The product may show coverage privately, for example `Based on 8 of 9 preferences`.

Compatibility is separate from reliability. Reliability is not part of the percentage.

### Compatibility interpretation

| Score | Label |
| --- | --- |
| 90–100 | Excellent match |
| 75–89 | Strong match |
| 60–74 | Good potential |
| Below 60 | Some preferences differ |

Labels avoid claiming scientific certainty. Users may still join/connect at any score.

Example:

```text
Compatibility 94% · Excellent match

✓ Same course: CSE 340
✓ Both prefer quiet study
✓ Evening availability overlaps
✓ Both preparing for Exam 2
```

Show the top four positive reasons and, when useful, at most one respectful difference such as `Different preferred session lengths`. Never expose hidden raw availability or course-confidence values.

### Recommendation ranking

Exclude cancelled/completed/expired, inaccessible, blocked-host, already-declined, conflicting, and full-without-waitlist Activities. Rank eligible candidates using:

1. Study Compatibility score and coverage;
2. start time/useful horizon and seat availability;
3. approved-zone proximity only with permission/selected zone;
4. prior successful collaboration as a moderate tie-breaker;
5. host coarse reliability as a small tie-breaker, never part of compatibility or a hard exclusion;
6. freshness and a diversity cap so one course/host/type does not dominate.

For student-partner suggestions, compatibility is the primary ordering after eligibility, with fairness rotation so the same high-scoring people are not always shown first. Need Help keeps its urgency-specific Chapter 11 ranking but may use compatibility as one medium-weight signal.

### Explanations and controls

Each suggestion includes compatibility plus truthful reasons such as “In CSE 340,” “Both prefer quiet evening study,” or “Matches your 2-hour preference.” User can inspect calculation, dismiss Activity/person, mute type/course/host suggestions, or edit the relevant preference. Dismissal is private and does not penalize anyone.

### Primary flow

1. Product builds an eligibility-safe candidate set for the current student.
2. Candidates receive deterministic compatibility/recommendation scores and diversity limits.
3. Dashboard/discovery shows a bounded set with compatibility and truthful reasons when coverage is sufficient.
4. Student opens, joins, dismisses, or changes the preference behind a reason.
5. Product revalidates eligibility at action time and removes stale suggestions.

### UX requirements

- Recommendations are visually labeled and never mixed invisibly with chronological results.
- Compatibility percentage is prominent but never styled as a guarantee, grade, or public popularity score.
- “Why this?” explains inputs and links to relevant preference/privacy control.
- Empty recommendations offer course/availability completion or direct search, not invented results.
- New users receive course/time-based suggestions without requiring behavioral history.

### Business rules

- Recommendations cannot expand resource permissions.
- Compatibility is personal to the viewing student/relationship. It is not globally searchable, publicly ranked, or used to reject a participant automatically.
- Hosts do not see a participant's exact compatibility score in open-join Activities. In approval-based future flows, preference alignment may be shared only with both-side consent and cannot include hidden raw fields.
- Presence is used only while valid and with consent; raw location history is not a feature.
- Exact reliability and protected profile fields are not displayed as reasons.
- User dismissal/mutes apply promptly.
- Initial ranking is deterministic and versioned for evaluation; no AI claim.
- Need Help ranking follows Chapter 11 and is not exposed as a browsable student ranking.
- Activity outcome topics/goals may improve future recommendations only within permitted context; goal failure never reduces compatibility or reliability.

### Validation and permissions

- Every candidate passes current eligibility at display and action time.
- Recommendation reason must correspond to an actually used, permitted signal.
- Student/partner recommendations require explicit discoverability consent from both sides.
- Percentage display requires at least 60 comparable weight and uses the published formula/version.
- Admin cannot pay/promote an Activity without a separate disclosed sponsored-content policy; not planned.

### Edge cases

- No availability supplied: rank by course/time only and state limited personalization.
- Two users have 100% on only a few fields: suppress percentage below coverage threshold.
- One user changes preferences: future scores recalculate; existing participation and previously recorded outcomes do not change.
- Complementary beginner/advanced pairing: treat as compatible only when the advanced student/Activity explicitly welcomes explaining/teaching; never assume labor.
- Conflicting Activities: do not recommend both as simultaneously attendable; may show alternatives.
- User's presence expires: recompute/remove proximity reason.
- Reliability is disputed: disputed evidence excluded from score; recommendation remains eligible.

### Acceptance and success criteria

- Every recommendation is explainable and openable by the viewer.
- Given the same eligible inputs and compatibility version, the same percentage/reasons are produced.
- Example preference fixtures reproduce expected exact, adjacent, conflict, missing-data, and coverage-threshold outcomes.
- Suggestions improve relevant Activity views/joins without increasing reports or notification fatigue.
- New users and low-history users receive useful results.
- No protected field or precise presence is leaked through reasons/order.

### Future improvements

Course discovery, team compatibility, group-level compatibility, post-collaboration preference learning with consent, collaborative filtering with privacy safeguards, calendar-aware ranking, controlled experimentation, and audited AI ranking only after fairness/consent review.

---

## 18. Notifications

**Release:** MVP in-app center, Web Push, and email; Firebase/Discord/Slack later

### Purpose and problem solved

Deliver time-sensitive coordination reliably without notification fatigue or making external channels canonical.

### User stories

- As a participant, I receive confirmation, RSVP, change, cancellation, waitlist, check-in, and live-status notices.
- As an available student, I receive bounded Need Help invitations according to preferences.
- As a user, I can read notifications in-app and control channel/category/quiet hours.
- As a user, I can mute ordinary Activity/course messages without missing critical accepted commitments.

### Notification categories and default priority

| Category | Examples | Priority |
| --- | --- | --- |
| Safety/account | suspension, security change, report outcome | critical/high |
| Activity critical | cancellation, major time/location change | high |
| Time-bound action | waitlist offer, RSVP deadline, match confirmation, check-in | high |
| Reminder | morning, upcoming, running-late follow-up | normal/high near deadline |
| Need Help invitation | private candidate invitation | normal; bounded |
| Recurring series | new occurrence, auto-join/waitlist result, series change/cancellation | normal/high when commitment changes |
| Course/Activity update | announcement, future chat | normal/low |
| Digest | suggested Activities/course activity | low |

### Channels

- In-app notification is canonical and created first.
- Web Push is initial external realtime delivery when permission/device supports it.
- Email initially covers verification/security and selected critical Activity notices; ordinary reminders are configurable.
- Firebase, Discord, and Slack are later adapters with explicit linking/permissions.

### Primary flows

#### Permission/onboarding

1. Product first explains concrete value after the user joins/creates an Activity.
2. User enables Web Push through browser prompt.
3. Product confirms/test status and provides recovery if denied/unsupported.

#### Notification center

1. User sees All/Unread, grouped by Today/Earlier.
2. Row includes written type, full context, timestamp, deadline, read state, and one relevant action.
3. Opening validates current resource/action; stale notices explain final state.
4. Mark all read uses a cutoff so newly arriving items remain unread.

#### Preferences

User controls category × channel, university/course/Activity mutes where appropriate, digest cadence, timezone, and quiet hours. Product previews critical exceptions.

### Scheduling and deduplication rules

- All required times derive from authoritative Activity/help state and timezone.
- Quiet hours defer ordinary notifications to the next permitted time.
- A deadline-driven RSVP/waitlist/match/check-in notice may bypass quiet hours only when the user accepted that commitment/invitation policy; copy explains this.
- Multiple same-Activity changes within a short window consolidate unless safety/deadline requires immediate delivery.
- Obsolete scheduled notices are cancelled after time/state changes.
- Same logical notice/channel is delivered at most once from the user's perspective despite retries.
- Series followers receive one new-occurrence notice; auto-join subscribers receive the ordinary join/waitlist receipt for each created occurrence and then its normal RSVP timeline.
- Muting a series suppresses follow/new-occurrence notices but not critical notices for occurrences the student already joined.
- Digest never includes content/resource the user can no longer access.

### UX requirements

- Badges have accessible text and never become an engagement-pressure mechanic.
- Actions use full labels and show deadlines/consequence.
- Denied push does not block core use; in-app remains available.
- Preference changes use plain-language examples.
- Mute explains what remains critical.

### Business rules

- Account/security/legal notices cannot be disabled where required.
- Critical Activity notices are limited to commitments the user made or Activities they host.
- Need Help invitation caps follow Chapter 11 and Busy/quiet preferences.
- Push/email contents minimize private location/topic detail on locked/shared devices; full context appears after authenticated open.
- Failed external delivery never removes in-app record.
- Invalid device subscriptions are deactivated; logout removes/rotates device association according to policy.
- Reliability point changes are not spammed; only material band/negative-event notices.

### Validation and permissions

- Notification recipient remains entitled to resource context at creation/open.
- Deep link and action cannot execute without fresh authorization/state validation.
- Email/push destination is verified/active.
- User manages own preferences/devices; admins cannot silently opt users into marketing/digests.

### Edge cases

- Push denied/unsupported: show non-blocking status; in-app/email policy continues.
- Timezone changes after scheduling: Activity-critical times remain tied to Activity instant; display/user quiet hour recalculates safely.
- Notification opened after action expiry: explain expiration and current status.
- Same user on multiple devices: each may receive push, but in-app read state synchronizes.
- Course muted but joined Activity changes: Activity commitment notice still sends.

### Acceptance and success criteria

- Required RSVP/waitlist/cancellation notifications are created on time and remain actionable/explainable.
- User can predict which categories/channels are enabled and what mute excludes.
- Notification volume, delivery/action latency, opt-out, invalid token, and fatigue/report metrics are measurable.
- External-provider failure does not corrupt product state.

### Future improvements

Firebase delivery adapter, Discord/Slack linked channels, SMS for institution-approved critical use, richer digests, calendar-based reminders, and per-Activity temporary preferences.

---

## 19. Administration and moderation

**Release:** MVP minimum safe operations; richer university analytics/import/integrations later

### Purpose and problem solved

Allow authorized people to maintain trustworthy university/course data and respond to abuse without granting broad, invisible access to student activity.

### User stories

- As a university admin, I can manage university branding, domains, catalog, approved campus zones, and scoped roles.
- As a course moderator, I can review course reports and make proportionate content/Activity decisions.
- As a safety moderator, I can review reports, warn/suspend within scope, and document reasons.
- As an operator, I can monitor aggregate health without browsing student content.
- As a reported user, I receive permitted notice and appeal information.

### Workspaces

| Workspace | Capabilities |
| --- | --- |
| University | branding, domains, departments/courses/sections, imports, zones, university roles, aggregate adoption |
| Course | announcements, course membership/content reports, moderator assignment where allowed |
| Safety | report queue, evidence view, warning/restriction/suspension, appeals, block guidance |
| Instance operations | configuration/health/quotas/jobs/providers/plugins; no routine content browsing |

### Primary flow: report and moderation

1. Student reports a user, profile, Activity, message/note (when enabled), Need Help request, or catalog item.
2. Reporter chooses reason, optional detail, immediate block, and urgent-safety guidance.
3. Product acknowledges with case reference and hides/limits target for reporter as appropriate.
4. Report enters scoped queue with severity/safety triage.
5. Moderator reviews minimum necessary evidence and conflict-of-interest constraints.
6. Moderator dismisses, requests information, warns, hides content, restricts capability, removes from Activity, suspends, or escalates.
7. Affected parties receive policy-appropriate outcome/appeal notice; reporter receives limited status without private enforcement details.

### Actions

- Warning: documented policy education; no public badge.
- Content/profile hide: removes visibility while preserving appeal evidence.
- Activity cancellation/removal: stops unsafe coordination with participant notice.
- Capability restriction: e.g., no Activity creation, messaging, presence, or Need Help for a period.
- Course/university suspension: blocks scoped participation.
- Instance suspension/ban: serious/repeated abuse; access to appeal/export as policy permits.
- Reversal/expiry: separate audited action, never erase prior action.

### Analytics

MVP admin analytics are aggregate and operational: verified/active users, course coverage, Activities created/completed, confirmation/arrival rates, Need Help outcomes, presence-zone aggregate use, notification health, reports by category/status, and moderation response time. No individual “productivity,” location history, message surveillance, or public ranking.

Small cohorts are suppressed. Admin access to reliability fairness/appeal aggregates is separated from individual score browsing.

### UX requirements

- Admin workspace is visibly distinct from student mode and shows current role/scope.
- High-impact actions require reason, consequence preview, and confirmation; severe actions may require reauthentication/two-person approval later.
- Queue shows urgency, age, scope, conflict, and next action—not sensational content previews.
- Evidence display minimizes sensitive content and warns before graphic material where applicable.
- Every action page shows audit history and appeal status.

### Business rules

- Least privilege and university/course scope apply to every admin action.
- Administrators cannot modify reliability scores directly or fabricate RSVP/attendance.
- Moderators cannot handle cases involving themselves or close conflicts; reassign/escalate.
- Student content access requires a case/support purpose and is audited.
- Reporters and subjects cannot see moderator private notes/other users' data.
- Warnings/suspensions have reason code, scope, start/end, actor, and appeal path.
- Bans do not silently delete evidence or shared academic history.
- University branding/settings cannot weaken core privacy, safety, accessibility, or truthful status language.
- Analytics never expose presence groups below privacy thresholds.

### Validation rules

- Admin role/scope is current; action target is within scope.
- Required reason, duration, evidence reference, and notification policy are complete.
- Domain/catalog/zone/import inputs follow Chapters 3 and 10.
- Conflicting or duplicate active enforcement actions are reconciled explicitly.
- Destructive purge is not an ordinary moderation action.

### Permissions

- Course moderators: assigned courses only, limited actions.
- University admins: own university catalog/roles/aggregate analytics; safety powers only when separately granted.
- Safety moderators: assigned scope/cases and minimum evidence.
- Instance admins: operations/global roles; content access is not automatic.
- Every privileged view/action is attributable and reviewable.

### Edge cases

- Report crosses university scopes: route to instance/senior safety moderation.
- Moderator is blocked by subject: admin case access follows duty, but personal product surfaces remain blocked.
- Subject deletes account during case: preserve minimum lawful evidence; continue anonymized case.
- Urgent physical safety: show local emergency guidance and escalation; product does not claim to be emergency response.
- False/malicious reporting: protect subjects, rate-limit abuse, and moderate reporter behavior without discouraging good-faith reports.

### Acceptance and success criteria

- Every privileged action has actor, scope, reason, time, outcome, and appeal/audit history.
- Cross-university/course privilege tests prevent unauthorized administration.
- Moderation response/appeal outcomes are measurable without exposing case content in analytics.
- Operators can diagnose service health without routine access to student content.

### Future improvements

Two-person approval, institution policy packs, delegated department admins, advanced import tooling, transparency reports, case SLAs, legal hold, plugin review, and verified LMS/SIS administration.

---

## 20. Accessibility and responsive experience

**Release:** MVP, cross-cutting release gate

### Purpose and problem solved

Ensure students can discover partners, RSVP, check in, request help, and manage privacy regardless of disability, input method, device, or motion/visual preference.

### User stories

- As a keyboard user, I can complete every core journey without a pointer.
- As a screen-reader user, I understand page structure, changing status, deadlines, and errors.
- As a low-vision user, I can zoom and use light/dark themes without clipped controls.
- As a motion-sensitive user, I can use realtime/presence views without unnecessary animation.
- As a mobile user, I can complete urgent RSVP/check-in/help actions one-handed with adequate targets.

### Requirements by area

| Area | Requirement |
| --- | --- |
| Structure | semantic landmarks/headings, skip link, logical reading/tab order |
| Keyboard | all controls/actions reachable; visible focus; no traps; dialogs return focus |
| Screen readers | labeled controls, meaningful status, concise live announcements, accessible errors |
| Contrast | WCAG 2.2 AA text/non-text; status not color-only |
| Zoom/reflow | 200% zoom and 320px width without two-dimensional scrolling except legitimate data tables |
| Motion | honor reduced motion; no essential animation, flashing, auto-advancing content |
| Touch | minimum 44×44 CSS px targets for core mobile actions |
| Forms | persistent labels/instructions, field errors, error summary, retained input |
| Time/status | written absolute time/timezone; icons/countdowns supplementary |
| Realtime | preserve focus/reading position; batch polite announcements; explicit reconnect/stale state |
| Maps/heatmaps | equivalent list/table and non-color representation |
| Documents | accessible metadata/download and extracted-text/alternative path where possible |

### Core journey acceptance

Authentication/onboarding, course join, Activity create/join, RSVP, waitlist offer, check-in, live continuation, Campus Presence visibility, Need Help request/acceptance, report/block, reliability appeal, and account deletion/export must pass keyboard and screen-reader scripted tests before pilot.

### Primary flow: accessibility validation

1. Feature owner identifies affected critical journeys and states.
2. Design/content review verifies semantics, focus order, status language, reflow, contrast, and motion behavior.
3. Automated checks run during development.
4. Manual keyboard, screen-reader, zoom, mobile, and reduced-motion scripts run before release.
5. Defects receive severity/owner; critical-journey blockers are fixed before launch or receive an explicit time-bounded exception.
6. Regression evidence remains with the feature's acceptance record.

### UX requirements

- Primary actions use visible text; icon-only actions have accessible names/tooltips where appropriate.
- Focus never moves merely because realtime data changes.
- Countdown changes are not announced every second/minute; announce material deadline/state changes.
- Skeletons are not exposed as meaningful content and stop motion under reduced-motion preference.
- Validation explains correction, not only that input is invalid.
- Plain language and consistent terminology reduce cognitive load.

### Business rules

- Accessibility defects in a critical journey can block release.
- An extension/plugin cannot ship in a core slot without the same accessibility bar.
- University branding cannot lower contrast or remove focus indicators.
- Captcha/security control must have an accessible alternative.
- User accessibility preferences are not exposed to other students or used for unrelated recommendations.

### Validation and permissions

Accessibility has no privileged bypass. Automated checks supplement, not replace, manual testing with representative assistive technologies. Test evidence identifies browser/OS/technology and expected outcome.

### Edge cases

- Large text during a time-bound prompt: deadline/action remains visible without trapping scroll.
- Screen reader during rapid attendance changes: counts update through restrained summary rather than reading every row.
- Browser denies motion/theme preference: product remains usable with explicit settings where provided.
- Heatmap unavailable: accessible list remains fully functional.
- Uploaded note lacks accessible source: label limitation and provide author improvement/request path.

### Acceptance and success criteria

- WCAG 2.2 AA target met for all MVP surfaces with documented, owned exceptions only.
- Critical tasks complete at keyboard/screen reader/200% zoom without loss of information/action.
- Accessibility defects, task failures, and remediation time are tracked by severity.
- Usability research includes disabled students and mobile/low-bandwidth conditions.

### Future improvements

Localization/bidirectional text, captions/transcripts for future media, personalized density/text controls, formal conformance report, broader assistive-technology matrix, and institutional accessibility integrations.

---

## 21. Privacy, safety, and user control

**Release:** MVP, cross-cutting release gate

### Purpose and problem solved

Let students collaborate without involuntary exposure of identity, course membership, location, availability, or attendance history.

### User stories

- As a student, I control profile/course/discovery visibility and can preview it.
- As a student, I can be Invisible on campus and block/report another user.
- As a student, I can export or delete my account.
- As a student, I understand what administrators/hosts can see.
- As a cautious user, I can participate without a public activity history.

### Visibility controls

| Data | Default | Available control |
| --- | --- | --- |
| Profile | same university | private/university according to required minimum identity context |
| Courses | mutual-context only | per-course hidden/university where allowed |
| Availability | matching only | off/matching visibility |
| Hosted/joined Activities | private | individual Activity visibility governs |
| Reliability | exact self; coarse authorized host | cannot opt into public ranking |
| Campus Presence | Invisible | temporary Visible + intent + discoverability consent |
| Need Help | private invitations | requester controls mode/zone/expiry; no public listing |
| Study streak/statistics | private | optional university/shared context later |

### Primary flows

1. **Visibility:** student changes a field/resource audience, previews the result, saves, and sees discovery/cache propagation status.
2. **Block/report:** student blocks and/or reports from contextual surfaces; interaction/matching stops immediately where required.
3. **Export:** student reauthenticates, requests export, tracks status, and receives an expiring secure result.
4. **Delete:** student reviews consequences, resolves hosted Activities, reauthenticates, enters deletion workflow, and receives completion/recovery information.

### Anonymous mode

MVP does not offer anonymous participation in Activities or Need Help because accountability/safety require a verified internal identity. “Anonymous mode” means privacy-preserving browsing/contribution to eligible aggregate campus counts without individual discoverability. Other students do not receive a named presence identity unless the student separately opts into partner discovery or mutually accepts a match.

Future anonymous posting requires a separate abuse/safety design and remains accountable to moderators internally.

### Blocking

1. User blocks another user from profile/message/Activity/report context.
2. Block applies in both users' discovery, partner suggestions, Need Help matching, individual presence suggestions, direct interaction, and future messaging.
3. Shared course/Activity may still show minimal operational information needed for safety/roster; product avoids revealing who blocked whom.
4. User can review/unblock from settings. Unblock does not restore old invitations/messages automatically.

### Reporting

Report flow follows Chapter 19. Blocking is offered alongside report but neither requires the other. Urgent danger copy directs users to appropriate local/emergency resources without claiming real-time StudyHang monitoring.

### Data export

User requests export after recent authentication. Product confirms scope/status and provides an expiring secure download when ready. Export includes profile/preferences, memberships, owned content, Activity participation/history, notification preferences, reliability events/appeals, reports submitted where disclosure is permitted, and plugin data included through declared export contracts. It excludes other users' private data and moderator confidential notes.

### Account deletion

1. User reviews consequences, hosted upcoming Activities, retained/anonymized shared history, and recovery window.
2. User resolves/transfers/cancels hosted future Activities and reauthenticates.
3. Account enters deletion-pending; access/tokens/presence/help requests are revoked promptly.
4. During configured short recovery window, user may cancel deletion through secure recovery unless legal/safety restriction applies.
5. Product deletes or anonymizes profile, credentials, tokens, private preferences, and content according to ownership/retention; shared factual/audit/moderation records retain minimum lawful form.
6. Completion notice is sent and non-personal completion evidence retained.

### UX requirements

- Privacy settings use audience examples and a “View as another student” preview.
- Presence state is globally visible to self and has immediate Go Invisible.
- Delete/export are findable, not dark-patterned, and use plain-language timelines.
- Block confirmation explains shared-context limitations.
- Privacy changes show whether cached/search/presence results may take a short time to disappear.

### Business rules

- Collect only data required for disclosed purposes; future AI is not a reason to collect more.
- University email, password/auth identifiers, exact private location, device tokens, moderation evidence, and reliability details are restricted.
- Analytics exclude free-form content, emails, precise location, and secrets.
- Presence is ephemeral with no product movement-history feature.
- Consent withdrawal stops future use/delivery where applicable without rewriting legitimate historical facts.
- Admin/provider/plugin access follows minimum purpose, scope, audit, and retention.
- Privacy settings cannot override safety requirements by exposing more than platform maximums.

### Validation and permissions

- Visibility audience is supported for field/resource and never broader than parent context.
- Export/deletion requires recent authentication and active request limits.
- Block target differs from actor; duplicate block is harmless.
- Only user controls ordinary privacy/export/deletion; authorized safety/legal holds are exceptional, disclosed where lawful, and audited.

### Edge cases

- Blocked users share a small Activity: preserve necessary host/attendance operation while suppressing discovery/direct interaction; safety support offered.
- Deletion while appeal/report open: restrict access and retain minimum case evidence according to policy.
- Export contains deleted message references: include user's own available content and safe placeholders, not others' private text.
- User goes Invisible during active mutual match: existing accepted Activity persists, but campus discoverability ends.
- University admin requests student data: require valid scoped product/legal process; role alone is not blanket access.

### Acceptance and success criteria

- Privacy defaults match this PRD across profile, search, recommendations, presence, help, chat, and admin views.
- Blocked users cannot be matched or individually suggested to one another.
- Go Invisible and account suspension/deletion revoke ephemeral presence/help eligibility promptly.
- Export/deletion complete within published policy and expose status.
- Zero cross-university or individual-presence disclosure incidents is the guardrail.

### Future improvements

Multiple privacy audiences, trusted circles, institution-specific residency/retention profiles, privacy dashboard, consent receipts, portable data formats, and separately reviewed anonymous community participation.

---

## 22. Future modules

**Release:** post-MVP; descriptions only

Future modules must have a separate PRD, threat/privacy model, release owner, extension/core decision, success measures, and explicit non-goals. They cannot weaken core authorization, Activity lifecycle, reliability, or consent.

### Version 1.1 committed candidates

#### Reputation categories

Keep MVP to the single Reliability score. Version 1.1 may add:

- Communication: timely, clear coordination around accepted commitments;
- Helpfulness: whether collaboration was useful to peers;
- Preparedness: whether the participant brought/understood agreed prerequisites.

Categories are not combined into one prestige score, do not affect MVP Reliability, and display only after at least five eligible feedback observations from at least three distinct collaborators. Users see explanations and appeals; hosts see only policy-approved coarse context.

#### Anonymous feedback

Only verified attendees may submit one feedback response within 48 hours of Activity completion. Feedback is anonymous to the recipient/host but attributable to safety moderators under an abuse investigation. MVP outcome facts remain non-anonymous and host-authored.

Version 1.1 should begin with structured feedback and optional private product feedback—not unrestricted anonymous public comments. Small-count results are suppressed, blocks/reports apply, retaliation is prohibited, and anonymous feedback never directly changes Reliability without a separate reviewed evidence policy.

#### Persistent Project Teams

MVP validates demand through the Project Team Formation Activity. Version 1.1 may add a persistent team with:

- course/project, team goal, deadline, open seats, desired skills, and roles;
- Interested, Invited, Active, Left, and Removed membership states;
- mutual join/approval and a clear team-owner/moderator model;
- linked Project Meeting Activities, shared outcomes, and later chat/resources;
- privacy, removal, ownership transfer, archive, report, and course-end rules.

The team cannot expose private contact information before mutual acceptance, rank applicants by protected traits, or treat reliability/compatibility as an automatic acceptance decision.

| Module | Product opportunity | Required gate |
| --- | --- | --- |
| AI | opt-in study matching, flashcards, quizzes, summaries, exam plans | content rights/consent, provider disclosure, evaluation, safety, cost, retention, human correction, opt-out |
| Marketplace | discover approved academic tools/services | payments, fraud, endorsements, conflicts, ranking transparency, refunds, tax/legal review |
| Tutoring | connect learners with peer/professional tutors | credential/payment/safeguarding, academic integrity, disputes, marketplace policy |
| Mentorship | longer-term peer/junior relationships | consent, boundaries, matching fairness, safety/escalation, no coercive reputation |
| Project Teams | persistent course project recruiting and collaboration after the MVP formation Activity | membership consent, roles/skills fairness, ownership/removal, deadline/archive, privacy |
| Hackathons | teams, preparation Activities, event spaces | event organizer verification, team privacy, external event integration |
| Research | reading groups, project teams, lab collaboration | IP/confidentiality, role verification, data controls, institution policy |
| Career | interview practice, project portfolios, employer events | commercial influence disclosure, profile privacy, anti-discrimination |
| Events | broader campus academic events | organizer verification, ticket/capacity rules, public visibility and safety |
| Clubs | persistent communities and leadership | governance transfer, moderation capacity, membership privacy, anti-spam |
| LMS integrations | Canvas/Moodle/Blackboard course/term sync | administrator consent, least privilege, data mapping, sync conflicts, retention |
| Calendar/conferencing | Google/Microsoft calendar, Zoom/Teams | delegated permissions, update/cancellation consistency, provider failure |

### Shared future-module rules

- Optional modules are visibly optional and uninstall/disable safely.
- Plugins receive least-privilege declared permissions and no direct core-table access.
- Future features do not enter MVP merely because architecture supports them.
- AI never becomes required to find/join/host an Activity or understand reliability.
- Commercial modules cannot buy placement in student/Activity recommendations without a separate transparent policy.

---

## 23. MVP end-to-end acceptance journeys

### Journey A — first useful collaboration

1. Student signs up with Google or email/password.
2. Verifies email/university and completes minimum onboarding.
3. Joins a course.
4. Completes Study Preferences and sees an explainable compatible Activity/partner, Campus Presence zone, or creates Need Help.
5. Joins/matches and reaches a valid attendance outcome.

**Pass:** no unsupported-university/course dead end; protected features require verification; time to useful outcome is measurable.

### Journey A2 — purposeful recurring collaboration

1. Host publishes a weekly Activity with primary goal, compatibility profile, and bounded series.
2. Students follow or auto-join; each occurrence independently confirms/waitlists.
3. One occurrence changes without modifying past/other exceptions.
4. Completed occurrence records goal status, topics, attendance, and actual duration.

**Pass:** no shared RSVP/attendance/outcome state across occurrences; series actions state exact scope; Not Reported is never treated as Not Completed.

### Journey B — accurate roster

1. Host publishes limited-capacity Activity.
2. Concurrent students join/waitlist without exceeding capacity.
3. Required confirmation/removal occurs on schedule.
4. Released seat promotes fairly with bounded offer.
5. Host sees authoritative state and participants understand each transition.

**Pass:** no duplicate/over-capacity state; every removal/offer is explainable.

### Journey C — live accountability

1. Check-in opens.
2. Participants arrive/run late/cancel.
3. Activity becomes Live only with valid evidence.
4. Still-active prompt continues/ends; stale Activity auto-completes.
5. Attendance finalizes and reliability recalculates/appeals correctly.

**Pass:** Activity that did not occur creates no no-shows; same evidence produces same score.

### Journey D — spontaneous campus collaboration

1. Student explicitly becomes Visible at approved zone with intent/duration.
2. Campus view shows only threshold-safe aggregates.
3. Student creates Need Help request.
4. Eligible bounded candidates receive private invitations.
5. Mutual acceptance creates Ad-Hoc Help Activity; both can check in/complete.
6. Presence expires/goes Invisible.

**Pass:** no individual is exposed before consent; block/quiet/limits work; decline has no penalty.

### Journey E — safety and control

1. Student blocks/reports another user.
2. Matching/discovery/direct interactions stop appropriately.
3. Scoped moderator handles report with audit and appeal.
4. Student exports/deletes account with clear status and retention behavior.

**Pass:** no cross-scope admin access; ephemeral presence/help revoked promptly.

---

## 24. MVP release gate

MVP may enter private pilot only when:

- [ ] all five end-to-end journeys pass with representative roles and failure cases;
- [ ] authentication, university/course scope, blocks, and admin permissions pass negative authorization tests;
- [ ] Activity lifecycle and RSVP timing pass timezone/DST/duplicate/concurrency product acceptance;
- [ ] Campus Presence defaults Invisible, expires, and suppresses low-volume groups;
- [ ] Need Help matching enforces eligibility, consent, limits, timeouts, and safe fallback;
- [ ] reliability formula, decay, New state, correction, and appeals reproduce expected fixtures;
- [ ] Study Compatibility fixtures reproduce exact/adjacent/conflict/missing/coverage cases and never expose hidden preferences;
- [ ] every published Activity has a primary goal; every completion has a factual outcome with explicit Not Reported behavior;
- [ ] weekly recurrence preview, auto-join/follow, occurrence independence, exception editing, cancellation scope, and DST behavior pass acceptance;
- [ ] Project Team Formation handles openings/skills/deadline without creating an implicit persistent team;
- [ ] critical flows pass keyboard, screen-reader, contrast, zoom, reduced-motion, mobile, and low-connectivity review;
- [ ] reports, moderation, suspension, export, deletion, and incident processes are operational;
- [ ] notification timing/preferences/failure behavior are understood by pilot users;
- [ ] no chat, notes, DM, AI, marketplace, or social scope has silently entered MVP;
- [ ] student usability research validates comprehension of RSVP consequences, presence visibility, matching disclosure, and reliability;
- [ ] product analytics measure outcomes/guardrails without sensitive-content or movement tracking.

## 25. Product decisions to validate during research

These do not reopen Part 1 architecture; they calibrate product policy before implementation:

1. Whether the 3-person aggregate threshold is sufficient for each pilot campus/zone layout.
2. Campus Presence default durations and the comprehension of Visible versus individual discoverability.
3. Need Help wave sizes, invitation caps, match confirmation, and acceptable time-to-help.
4. Whether open joining or host approval should be default for specific Activity types.
5. Reliability outcome weights/bands and student comprehension/fairness before host disclosure.
6. Exact account deletion recovery and moderation/appeal retention periods with legal review.
7. Which Activity types need unique requirements in MVP versus type labels only.
8. Compatibility weights/adjacency language and whether students understand percentage plus coverage without treating it as certainty.
9. Weekly-series auto-join adoption, fairness under capacity, 14-day creation window, and 16-occurrence limit.
10. Whether host-authored goal outcomes are sufficiently accurate before Version 1.1 anonymous feedback.

Research may adjust numerical policy values through a versioned PRD decision. It may not introduce public reliability ranking, background location tracking, unbounded invitations, or mandatory AI.
