---
name: 14-professional-api-testing
description: Design and execute standards-based API testing across contract, business behavior, negative input, authorization, integration, resilience, and data readback. Use for comprehensive API assurance beyond testcase generation.
---

# Professional API Testing

Use the current live OpenAPI or authoritative service contract when required. Treat repository copies as cached references until their version is confirmed.
Read `Config/QA-Agent/professional-coverage-model.yaml` and `Config/QA-Agent/api-coverage-profile.yaml`; build operation/message coverage units and state counts before claiming breadth.

## Coverage Model

Cover as applicable and record `N/A_WITH_REASON` rather than silently omitting a dimension:

- schema, required fields, types, formats, enums, defaults, and error contract;
- content types, security schemes, headers, `allOf`/`oneOf`/`anyOf`, nullable/readOnly/writeOnly, callbacks and webhooks when present;
- positive, negative, boundary, null, empty, malformed, oversized, unsupported, and conflicting inputs;
- authentication, object- and function-level authorization, tenant isolation, and field exposure;
- CRUD semantics, idempotency, duplicate requests, retries, concurrency, race conditions, and ordering;
- pagination, filtering, sorting, search, localization, dates, time zones, and numeric precision;
- rate limits, timeouts, downstream failure, partial success, versioning, and backward compatibility;
- persistence, events, audit, cache, downstream integration, rollback, and cleanup.
- protocol-specific behavior for SOAP, GraphQL, gRPC, WebSocket, SSE or async events when discovered;
- version-aware OpenAPI/JSON Schema serialization, conditional-schema, reference, multipart/binary/stream and cache validators when present;
- OWASP API1–API10, including sensitive business-flow abuse, undocumented/version inventory and unsafe upstream API consumption.

Generate invalid data from schema constraints and business rules. Vary one invalid dimension for diagnosis, then add selected pairwise and adversarial combinations. Keep fuzzing as a separately authorized activity.

Do not assume the live description is complete. When authorized, compare it with gateway/runtime/frontend/log evidence and report shadow, deprecated, debug/admin or old-version operations as inventory findings.

Derive response codes, empty/null behavior, duplicate handling and idempotency from the current operation/business contract. Do not impose one universal status code or require repeated responses to be byte-identical.

## Execution Gates

1. Confirm environment, build, authorization, accounts, data ownership, and whether requests mutate data.
2. Use non-production environments. Require approval for writes, load, destructive payloads, or security probes.
3. Correlate request/response with logs or trace IDs when available and prove the business effect by readback.
4. Redact tokens and sensitive records from evidence.
5. Keep unexecuted, blocked and unproven coverage units visible; a green executed subset is not complete coverage.

## Output Contract

Return operation/message denominator and state counts, protocol, cases executed, request category, status, business/readback result, OWASP mapping, evidence, defects, blocked/unassessed units, residual risks and contract ambiguities.
