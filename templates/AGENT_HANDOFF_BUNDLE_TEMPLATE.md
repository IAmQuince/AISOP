---
document_id: DOC-TPL-HANDOFF
title: "Agent Handoff Bundle Template"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-TPL-HANDOFF
normative_status: Informative
tier: 1
summary: "What to give an AI agent before it changes a package, including during a prototype-to-package migration."
derived_from: DOC-165
source: "REV-003 Phase 2 template"
---

# Agent Handoff Bundle

Give this to the AI with the package. See `docs/165` and, for migrations, `docs/060` (method edition).

## Package
Path or zip: <...>  Version and revision: <...>

## Task
<The issue or workplan entry, one paragraph.>

## Constraints
<Target environment, allowed dependencies, safety class.>

## Evidence
<Latest audit and smoke-test output, pasted.>

## Expected changes
<Files expected to change. Everything else must stay as it is.>

## Must not break
<FEAT- IDs and behaviors that must survive, plus the frozen baseline for a migration.>

## Delivery
End with the final package report (`FINAL_PACKAGE_REPORT_TEMPLATE.md`).
