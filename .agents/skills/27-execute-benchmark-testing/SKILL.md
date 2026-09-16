---
name: 27-execute-benchmark-testing
description: Execute an approved benchmark protocol repeatedly in a controlled environment and compare candidate results with a reproducible baseline and variance analysis. Use after workflow 20 is approved.
---

# Execute Benchmark Testing

Do not alter the approved protocol during a run without recording a new version.

## Procedure

1. Verify approval, protocol version, build artifacts, environment fingerprint, dataset, dependencies, cache state, and monitoring.
2. Perform prescribed warmups and repetitions. Retain raw results for every iteration.
3. Record environmental noise, resource contention, failures, and deviations. Stop at approved thresholds.
4. Compare baseline and candidate using the protocol's percentiles, variance, outlier, and regression rules.
   - Evaluate absolute SLA and relative delta together; do not declare PASS from a favorable percentage when the absolute target fails.
5. Repeat or reject contaminated runs transparently; do not select only favorable measurements.

## Output Contract

Return protocol version, baseline/candidate identifiers, environment fingerprint, raw evidence paths, iteration results, variance, deltas, threshold decision, deviations, and reproducible conclusion.
