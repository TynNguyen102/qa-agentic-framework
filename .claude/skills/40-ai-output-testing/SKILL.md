---
name: 40-ai-output-testing
description: Test AI/LLM-backed product behavior — answer invariants, run-to-run consistency, grounding against authoritative data, streaming/event contract, internal-detail leakage, and model/prompt version regression. Use when a feature's output is produced by a model rather than by deterministic code.
---

# AI and Model Output Testing

> **Tóm tắt (VI):** Test đầu ra AI/LLM — invariant / consistency (lặp N) / grounding (đối chiếu DB) / leak / injection / đổi-model. Dùng khi output do model sinh, không phải code tất định.

Model output is non-deterministic. A single bad sample is an observation, not a defect. State which oracle class each check uses before running anything, or the result cannot support PASS/FAIL.

Read `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml` and the `product_truth`, `security_and_privacy` and `nonfunctional_and_operational` dimensions in `Config/QA-Agent/professional-coverage-model.yaml`. Fluency is not correctness: an answer that reads well and states a wrong number is the primary defect class here, not an edge case.

## Oracle classes

Every check must declare one:

- `INVARIANT` — must hold on every single run (no secret/PII in output, answer language follows the configured rule, response validates against the declared schema, retrieved data respects the caller's role and tenant). One violation is a defect.
- `DISTRIBUTIONAL` — must hold across N repeated runs (consistency of language, structure or substance for the same input). Report the variance rate over a stated N; never assert this class from one sample.
- `GROUNDED` — every entity, number and claim must reconcile with an authoritative layer (DB/API/event). Verified by readback, not by rereading the answer.
- `PRODUCT_QUALITY` — the output meets spec but is weak (terse, unhelpful, poorly worded). Record separately; this is feedback for the PO, not a defect.

## Procedure

1. Fix and record the run context: model id and version, prompt version, temperature/seed when exposed, retrieval corpus snapshot, tool/function set, user locale, role and tenant. An output captured without its run context is not reproducible and cannot be retested — treat it as `INSUFFICIENT_CONTEXT`.
2. Test `INVARIANT` checks first: output language rule, refusal and out-of-scope behavior, declared output schema/format, citation presence when the feature promises sources, and leakage of secrets, personal data, internal identifiers, infrastructure hostnames or raw internal events.
3. Test `DISTRIBUTIONAL` checks by repeating the same prompt in N fresh sessions (state N; N=1 proves nothing). Record variance in language, structure and substance separately — the same answer in two languages and two different answers in one language are different defects.
4. Test `GROUNDED` checks by reconciling every cited value against the authoritative layer, routing the query through `38-query-data-by-assurance-level`. Confirm the model queried what it claims: compare the reported query and source against the real schema, and check the retrieved scope against the caller's permissions and tenant.
5. Test the streaming/event contract separately from the rendered answer: event ordering and sequence numbers, a terminal event on every run, behavior on stop/cancel/timeout mid-run, partial output handling, and the rule that no raw internal event or reasoning trace reaches the UI unless the design says it should.
6. Test adversarial input only under an explicit rules-of-engagement: prompt injection carried in retrieved content or user data, instruction override, and attempts to read across tenant or role boundaries. Route depth to `23-security-testing`; do not improvise intrusive probes.
7. Treat a model, prompt-version or provider change as a regression event: rerun the retained baseline set and compare invariant pass rate, grounding accuracy and variance against the previous version. Report the delta; a provider swap that lowers detection or answer quality is a finding even when nothing errors.
8. Classify with `bug-basis-profile.yaml`. Separate model-capability limits that match the approved spec from behavior that violates it, and separate both from `PRODUCT_QUALITY` feedback.

## Hard rules

- Never report a `DISTRIBUTIONAL` finding from a single run, and never state a variance rate without N.
- Never accept the model's own account of its query, source or reasoning as evidence — reconcile against the authoritative layer.
- Never paste raw model transcripts containing personal data, secrets or internal identifiers into a defect, report or artifact; redact to the minimum needed to reproduce.
- Do not treat a refusal, a hedge or an unexpected phrasing as a defect unless it violates a declared rule.

## Output Contract

Return coverage-unit ID, run context (model/prompt version, locale, role, tenant, corpus snapshot), the oracle class of every check, N and observed variance for distributional checks, grounding reconciliation results with the layer used, invariant violations, streaming/event contract results, baseline-vs-current comparison when a version changed, classification per `bug-basis-profile.yaml`, redaction status, and residual risk.

## Reusable per-project harness (prepare once, rerun on every model/prompt change)

The distributional, invariant and regression checks are only cheap to repeat if the project keeps three standing assets. Build them once under the project's module (not in this skill), and rerun them whenever the model, prompt or provider changes:

- **Question bank** — an editable, version-controlled file of prompts tagged by dimension (`lang`, `ground`, `nodata`, `halluc`, `perm`, `inject`, `ambiguous`, `format`, `scope`), each carrying its `language`, `expect_lang`, the check intent and its oracle class. Adding a case must not require code changes — a non-engineer can extend coverage by editing the file.
- **Repeatable runner** — reads the bank, sends each case over the real API with its run context, repeats each case `--repeat N` times, and auto-scores only the machine-checkable invariants (answer language, refusal presence, citation presence, secret/PII leak regex). It records raw responses for the `GROUNDED` and human oracles it cannot score, and separates NEED_DATA from PASS (a skipped or errored call is never a pass).
- **Live reproduction demo** — a headed browser run that replays a confirmed finding step by step for a human to watch and for evidence capture; keep it runnable by name so it can be re-shown without rewriting code.

Record the model id/version with every run so a later run against a new provider is a true baseline diff. When invoked for a deep pass, run the machine-scorable dimensions first (fast, deterministic verdicts), then hand the `GROUNDED`/model-comparison dimensions to the ground-truth owner (AI/DS) and report those as BLOCKED until that data exists — never fabricate a grounding verdict to fill the gap.
