---
name: 22-contract-compatibility-testing
description: Assess backward and forward compatibility of API, event, schema, and consumer-provider contracts across current and adjacent versions. Use for release, integration, migration, or versioning risk.
---

# Contract Compatibility Testing

Identify actual consumers and supported version combinations before judging compatibility.
For API/event scope, read `Config/QA-Agent/api-coverage-profile.yaml` and preserve its protocol and operation/message IDs.

## Procedure

1. Collect authoritative OpenAPI, JSON Schema, event schema, DB interface, or consumer-driven contracts for baseline and candidate versions.
2. Map provider and consumer versions, deployment order, optionality, defaults, feature flags, and deprecation policy.
3. Examine additions, removals, renames, required-field changes, type/format/serialization changes, enum changes, nullability, defaults, semantic changes, ordering, errors, security requirements, protocol semantics and schema-dialect changes.
4. Test backward compatibility, forward tolerance, mixed-version operation, rolling deployment, stored historical data, and replayed events as applicable.
5. Identify affected consumers and migration or rollback requirements.

## Output Contract

Return a compatibility matrix linked to coverage units, change classification, evidence, affected consumers, breaking changes, deployment constraints, migration action, untested version pairs and residual risk.
