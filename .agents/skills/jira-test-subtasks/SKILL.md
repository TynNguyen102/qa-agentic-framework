---
name: jira-test-subtasks
description: Draft and—with explicit approval—create the two standard Jira QA subtasks, Create Testcase and Testing, using user-configured titles and consistent descriptions. Use when a story needs its QA execution subtasks.
---

# Jira Test Subtasks

Read `Projects/<ACTIVE_PROJECT>/Config/jira-subtask-profile.yaml` first. Create exactly two subtasks unless the user requests a different scope:

1. `Create Testcase`
2. `Testing`

## Configuration Gate

The user will provide both title formats. While either title is unconfigured, return `NEED_CONFIG` for the affected title and do not invent a live Jira summary. A provisional description may still be drafted.

## Create Testcase Description

Populate these configured sections:

- Objective
- Test Basis
- Scope
- Coverage Dimensions
- Test Data And Roles
- Deliverables
- Dependencies And Blockers
- Definition Of Done

The definition of done should require reviewed, traceable cases in the canonical schema, correct title format, test-management-ready output (QMetry or TestRail) only when that tool's profile is configured, and identified data/environment dependencies.

## Testing Description

Populate these configured sections:

- Objective
- Build And Environment
- Preconditions
- Execution Scope
- Evidence Paths
- Result And Defect Links
- Regression Impact
- Definition Of Done

The definition of done should require approved scope execution, business readback, evidence, triaged failures, defect/retest links, updated coverage, and a test recommendation.

## Procedure

1. Read the parent story, acceptance criteria, comments, links, sprint, assignee rules, and Jira create metadata.
2. Build each title from the exact configured format and populate descriptions without duplicating the full story.
3. Set parent, issue type, project, assignee, labels, components, sprint, and custom fields only from confirmed Jira metadata or configured rules.
4. Produce local drafts first. Ask for explicit approval immediately before creating Jira issues.
5. After creation, read back both keys, titles, parent, issue type, fields, and links.

## Output Contract

Return configuration status, two draft payloads, validation findings, duplicate warning if any, or the two created keys with readback evidence.
