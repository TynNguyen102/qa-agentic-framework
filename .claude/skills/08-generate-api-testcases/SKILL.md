---
name: 08-generate-api-testcases
description: Generate API testcases from live OpenAPI/Swagger, business rules, state models, security requirements, and integration contracts. Use when an endpoint, service, API change, or backend User Story needs detailed positive, negative, boundary, authorization, state, and readback cases.
---

# Generate API Testcases

Read `Config/QA-Agent/professional-coverage-model.yaml` and `Config/QA-Agent/api-coverage-profile.yaml`. Use the latter as the API denominator/checklist; do not copy its entries into every testcase.

## Inputs and gates

Require a confirmed API protocol and contract/version or mark contract-derived expectations `NEED_CONFIRM`. Read canonical and title profiles. Use the active project's configured test management profile (QMetry or TestRail, per `qa-config.yaml`) only for import-ready output.

## Workflow

1. Identify REST/HTTP, SOAP, GraphQL, gRPC, WebSocket, SSE, async-event or other protocol. Inventory operation/message, contract version, source/retrieval time, authentication/authorization, states, side effects, consumers and dependencies. Apply the matching `protocol_extensions` profile; never force REST rules onto another protocol.
2. For OpenAPI/HTTP, apply version-aware schema and serialization checks from `api-coverage-profile.yaml`, including references/dialect, composition/conditional schemas, additional properties, parameter encoding, multipart/binary/streaming and conditional/cache semantics when present. Treat examples as examples, not rules.
3. When authorized evidence exists, reconcile documented operations with gateway/runtime/frontend/log inventory; classify undocumented, deprecated and old-version surfaces rather than assuming Swagger is complete.
4. Generate valid, alternate, missing, null, wrong-type, boundary, enum, pattern, format, oversized, malformed, unexpected-property, and cross-field cases using one-invalid-dimension first, then selected pairwise/risk-based combinations.
5. Map applicable OWASP API1–API10 risks per operation to deterministic cases/authorized security scenarios or `N/A_WITH_REASON`; include sensitive-flow abuse, API inventory and unsafe upstream-consumption checks, not only authentication.
6. Cover state, idempotency, duplicate/concurrent requests, pagination/filter/sort, timeout/retry, rollback, versioning, compatibility, observability and cross-layer readback as applicable.
7. Derive status/error/idempotency expectations from the operation and business contract; do not hardcode universal 400/401/403/404/409 behavior or assume repeated responses are byte-identical.
8. Keep deterministic negative cases separate from seeded, authorized property/fuzz testing. Record excluded combinations and residual risk.

## Output

Emit API coverage-unit/operation denominator plus canonical cases with protocol, request/message dimension, payload/data, expected contract, expected business result, oracle layers, cleanup, source, priority, security mapping and residual risk. Do not promise exhaustive combinations.

Do not combine design, automation generation, execution, and test management PASS updates into one unreviewed step. Route reviewed cases to workflow 11, execute through 13/14, then update the test management tool only from evidence-backed results.
