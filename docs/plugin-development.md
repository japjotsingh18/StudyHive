# Plugin Development

**Status:** contract proposal. The plugin runtime and SDK are not implemented.

Read [Part 1](00-part-1-vision-architecture-open-source.md#12-plugin-system) before designing a plugin. A plugin extends StudyHang through declared capabilities, versioned events, scoped APIs, namespaced storage/data, and approved UI slots. It does not import core internals or modify core tables.

## Choose the right extension type

| Need | Extension |
| --- | --- |
| Replace storage/auth/maps/notification provider | trusted provider adapter, initially first-party/in-tree |
| Send session facts to another system | out-of-process integration plugin |
| Add a substantial optional workflow | isolated backend module plugin |
| Add contextual UI | sandboxed UI extension plus backend/plugin API |
| Change colors/logo/branding | declarative theme package |

If a feature changes session capacity, RSVP, attendance, reliability, privacy, or authorization invariants, it is a core proposal—not a plugin.

## Planned plugin package

```text
example-plugin/
├── .studyhang-plugin/
│   └── manifest.yaml
├── src/
├── migrations/                     # plugin namespace only
├── ui/                             # optional sandboxed extension
├── docs/
│   ├── configuration.md
│   ├── permissions.md
│   └── operations.md
├── tests/
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Manifest contract

The versioned manifest declares identity/version, core compatibility, execution type, configuration JSON schema, requested permissions, event subscriptions, routes, UI slots, migrations, health checks, and distribution integrity.

Unknown fields fail validation unless the manifest version explicitly permits extensions. Install shows the operator a human-readable permission diff.

## Event consumer rules

- Treat delivery as at least once and deduplicate `event_id`.
- Validate event schema/version before use.
- Do not assume global ordering; use aggregate ID/version where relevant.
- Return quickly and process expensive work asynchronously.
- Use bounded retries and expose health/backlog.
- Fetch additional allowed data through the scoped Plugin API.
- Never infer access to fields omitted from an event.

## Data and migrations

- Own a plugin-specific schema/namespace.
- Never alter core tables, enums, triggers, indexes, or migrations.
- Record a migration version and support compatible upgrades.
- Disable before destructive uninstall; offer export before purge.
- Apply tenant scope to every plugin-owned record.
- Declare retention and deletion behavior for user/tenant deletion.

## UI extensions

Third-party UI runs sandboxed and receives theme tokens, locale, route/resource context, and a scoped message bridge. It does not receive raw auth tokens or parent DOM access. All UI must meet the core accessibility and responsive requirements.

Planned named slots are intentionally few, such as session actions, course tools, user settings integrations, and admin plugin configuration. Plugins cannot replace core confirmation, attendance, safety, or permission UI.

## Security checklist

- [ ] Minimum permissions requested and documented.
- [ ] Secrets stored through the plugin secret interface and never logged.
- [ ] Webhooks/events authenticated and replay-safe.
- [ ] Routes validate tenant, actor, and object scope.
- [ ] Inputs, outbound URLs, uploads, and rendered content are constrained.
- [ ] Plugin failure cannot block a core transaction.
- [ ] Disable/kill switch and operational health are tested.
- [ ] Data export, retention, uninstall, and incident behavior are documented.

## Reference plugin

The recommended first reference is a read-only calendar integration. It exercises manifest validation, session event subscription, scoped metadata access, configuration, retries, idempotency, and health without requiring message bodies, reliability data, or direct database access.

## Compatibility

Before public beta the SDK must publish supported core ranges, event/API deprecation windows, migration policy, test harness versions, signing/distribution rules, and a process for security revocation. No marketplace is promised until those controls work end to end.
