---
name: 17-reliability-resilience-testing
description: Design or execute authorized reliability and resilience tests for dependency failure, retry, recovery, failover, data consistency, and service objectives. Use when fault behavior and recovery guarantees must be assessed.
---

# Reliability and Resilience Testing

Disruptive tests require an isolated environment, an approved fault scope, monitoring, rollback, stop conditions, and named owners.

## Procedure

1. Model dependencies, failure modes, SLOs, RTO, RPO, critical data, and expected degraded behavior.
2. Cover timeout, retry and backoff, circuit breaking, partial failure, restart, failover, dependency unavailability, network degradation, clock issues, duplicate or out-of-order messages, and backup/restore as relevant.
3. For each scenario define the injected condition, blast radius, steady-state metric, expected detection, recovery behavior, allowable loss or duplication, and abort threshold.
4. Execute only with explicit authorization. Observe system, application, data, queues, logs, alerts, and user experience before, during, and after recovery.
5. Reconcile data and prove that retry or recovery did not create silent corruption.

## Output Contract

Return scenario, injection, approval, steady-state evidence, observed degradation, recovery time, loss/duplication, reconciliation, status, and residual risk.
