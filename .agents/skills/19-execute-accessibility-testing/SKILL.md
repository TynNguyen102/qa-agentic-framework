---
name: 19-execute-accessibility-testing
description: Execute accessibility testing against an approved conformance target using automated scans plus manual keyboard, focus, semantics, reflow, forms, and assistive-technology checks. Use after accessibility cases and target standards are approved.
---

# Execute Accessibility Testing

Do not claim conformance from an automated scanner alone.

## Procedure

1. Confirm the approved standard, level, supported browsers, devices, assistive technologies, and in-scope journeys.
2. Run configured automated checks and retain the raw report.
3. Manually verify keyboard access, visible focus, focus order and management, bypass mechanisms, names/roles/values, headings and landmarks, forms and errors, status messages, zoom, reflow, contrast, motion, media, and touch target behavior as applicable.
4. Use representative screen readers or real-device assistive technologies when required by the target matrix.
5. Reproduce each issue without depending solely on tool output and map it to the relevant success criterion.

## Output Contract

Return journey/component, standard and criterion, user impact, steps, actual behavior, expected behavior, evidence, severity, affected assistive technology, and remediation hint.
