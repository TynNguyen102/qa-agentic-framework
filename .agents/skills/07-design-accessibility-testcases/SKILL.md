---
name: 07-design-accessibility-testcases
description: Design accessibility test conditions and detailed cases for web or mobile interfaces. Use when requirements, designs, UI components, or release scope need keyboard, screen-reader, semantic, visual, cognitive, and error-handling coverage before execution.
---

# Design Accessibility Testcases

Read the frontend/UI and accessibility dimensions in `Config/QA-Agent/professional-coverage-model.yaml`; link criteria to component/journey coverage units.

## Workflow

1. Confirm target platform, supported browsers/devices, user journeys, component inventory, and required accessibility standard/conformance level.
2. If the target standard is not approved, return `NEED_CONFIRM: ACCESSIBILITY_STANDARD`.
3. Design coverage for keyboard-only operation, focus order/visibility, semantics and names, forms/errors, landmarks/headings, contrast, zoom/reflow, motion, timeouts, media, touch target, orientation, and assistive technology.
4. Combine automated rules with manual and assistive-technology checks.
5. Trace each case to component/journey and applicable criterion; define severity by user impact.

## Output

Create accessibility condition/case matrix with coverage-unit ID, journey, component, criterion, method, device/AT, steps, expected accessible behavior, evidence, severity guidance, automation suitability and untested user impact. Use skill 19 for execution.
