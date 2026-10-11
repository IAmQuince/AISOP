---
document_id: DOC-TPL-INDEX
title: "Templates"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-TPL-INDEX
normative_status: Informative
tier: 1
summary: "Which template to use at each stage of a project, and what each one is for."
source: "REV-003 Phase 2 template"
---

# Templates

Fill-in forms for your own project. Copy one, replace the `<...>` prompts, and delete what does not apply. Each template names the AISOP document it comes from (`derived_from`); the full documents win on conflict.

## One template per stage

| Stage | Use this | The full SOP behind it |
|---|---|---|
| concept | `CONCEPT_BRIEF_TEMPLATE.md` | `docs/030` (method edition) |
| plan | `PLANNING_DOCUMENT_TEMPLATE.md` | `docs/040` (method edition) |
| prototype | `examples/hello_aisop/hello_aisop.py` as the pattern | `docs/050` |
| migrate | `AGENT_HANDOFF_BUNDLE_TEMPLATE.md` | `docs/060` (method edition) |
| package | `FINAL_PACKAGE_REPORT_TEMPLATE.md` | `docs/070` (method edition) |

## Package files

`README_START_HERE_TEMPLATE.md`, `CHANGELOG_TEMPLATE.md`, `FEATURE_INVENTORY_TEMPLATE.md`, `KNOWN_LIMITATIONS_TEMPLATE.md`: the intake documents every package carries. `ID_RECORD_FORMATS.md` gives the record shapes for requirements, tests, risks, debts, decisions, and questions.

## Working with an AI

`USER_PROFILE_TEMPLATE.md` tells the AI who you are. `FIRST_SESSION_PROMPTS.md` holds three prompts to copy. `MANUAL_AUDIT_CHECKLIST.md` checks a package by hand when you cannot run Python.
