---
document_id: DOC-165
title: "AI Agent Handoff Protocol"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-165
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# AI Agent Handoff Protocol

## Purpose

Give AI collaborators enough context to modify the package without drifting, dropping features, or inventing structure that conflicts with the current files.

## Required handoff bundle

When asking an AI agent to revise a package, provide:

- current zip or repository path;
- package version and revision;
- relevant issue or workplan;
- required constraints;
- audit reports;
- files expected to change;
- explicit non-regression expectations.

## Agent instructions

The agent should:

1. inspect actual files before drafting replacements;
2. run baseline audits before edits;
3. preserve existing features unless removal is requested;
4. update revisions on touched controlled files;
5. update changelog, requirements, tests, and traceability when needed;
6. run audits after edits;
7. deliver a zip package and report what passed or failed.

## Diagnostic harness rule

Every substantial code or package update should include a diagnostic command that produces a report a user can paste back into a future AI conversation.
