---
name: 20-design-benchmark-testing
description: Design a reproducible benchmark protocol with a controlled baseline, workload, environment, metrics, repetitions, variance, and comparison rules. Use before executing comparative benchmark tests.
---

# Design Benchmark Testing

Benchmarking compares controlled implementations or versions. Keep it distinct from general load, stress, and capacity testing.

## Procedure

1. State the decision question and the baseline and candidate versions.
2. Fix hardware or infrastructure, deployment configuration, dependencies, dataset, data distribution, cache state, concurrency, and client location.
3. Define warmup, duration, iterations, workload mix, think time, sampling, percentiles, throughput, error, resource, and domain-specific metrics.
4. Define noise controls, acceptable run variance, number of repetitions, outlier treatment, and comparison thresholds before execution.
   - Define both absolute service objectives and relative baseline-to-candidate rules; do not use a universal 20% degradation threshold.
   - Treat p95 as a distribution from sufficient repeated samples, not one query measurement.
5. Specify monitoring, evidence, rollback, stop conditions, and approvals for resource-intensive runs.

## Output Contract

Return a versioned benchmark protocol containing question, baseline, candidate, environment fingerprint, data, workload, metrics, repetitions, variance rules, thresholds, risks, and exact execution command.
