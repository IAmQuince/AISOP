---
document_id: DOC-165
title: "AI Agent Handoff Protocol"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-165
normative_status: Normative
tier: 2
summary: "What to hand an AI agent before it revises a package; agent duties are in AGENTS.md."
source: "AISOP REV-002 GitHub practice-space update"
---


# AI Agent Handoff Protocol

## Purpose

Give AI collaborators enough context to modify a package without drifting, dropping features, or inventing structure that conflicts with the current files.

## Required handoff bundle

When asking an AI agent to revise a package, provide:

- current zip or repository path;
- package version and revision;
- relevant issue or workplan;
- required constraints;
- audit reports;
- files expected to change;
- explicit non-regression expectations.

## Agent duties

For this repository the agent's duties are defined once, in `AGENTS.md`: the first-five-minutes protocol (section 5), modes and reading sets (section 6), commands (section 7), hard rules (section 8), the user profile rule (section 9), and delivery (section 10). This document does not restate them, and `AGENTS.md` wins if the two ever disagree.

In short, those sections require the agent to inspect the actual files and run the baseline audits before editing, preserve existing features unless removal is requested, update revisions, changelog, requirements, tests, and traceability, run the audits again after editing, and end with the fifteen-field final package report (`templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`).

For a downstream package that has no `AGENTS.md` of its own, give the agent `docs/001_AISOP_CORE_RULES.md` (the AISOP card) as its operating rules and the bundle above as its context.

## Diagnostic harness rule

Every substantial code or package update should include a diagnostic command that produces a report a user can paste back into a future AI conversation.
