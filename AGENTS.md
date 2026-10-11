---
document_id: DOC-AGENTS
title: "AGENTS.md (interim agent entry file)"
version: 0.2.0
revision: REV-003
status: INTERIM
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-AGENTS
normative_status: Normative
source: "REV-003 Phase 0c (docs/300 section 11); replaced by the full entry file in Phase 1"
---

# AGENTS.md (INTERIM)

This file is Normative. It is an interim entry file and will be replaced in Phase 1 of `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`.

## What this repository is

AISOP is a self-describing package of standard operating procedures for AI-assisted software work: plan, prototype, package, review, and hand off without losing features or context. It is used two ways: as zip packages traded between people and AI tools, and as this GitHub repository.

## First steps

1. Run `python tools/run_all_audits.py --quiet`. PASS: trust the tree. FAIL: report the failing tool verbatim and stop structural work; a red audit on a fresh clone is a bug to report, not to work around.
2. Read `README_START_HERE.md`, then `docs/000_DOCUMENTATION_INDEX.md`.
3. Tell the user in one sentence what you will change before touching files.

## Normative vs informative

Normative means binding on anyone modifying this package. Only `docs/005_PRODUCT_REQUIREMENTS.md` and `requirements/requirements_catalog.json` define `REQ-*` requirements. The Normative governance SOPs (`docs/080` to `docs/165`) bind process. Informative documents are reference. `docs/010`, `docs/055` and `docs/170` to `docs/290` are informative domain guides, never requirements.

## Hard rules

- Do not load the domain guides (`docs/170` to `docs/290`) wholesale; open one only when the task needs it.
- Never delete or renumber a `REQ-*`, `FEAT-*`, or `TEST-*` ID; mark it Superseded instead.
- Bump `revision` and `last_updated` in the header of every controlled document you change.
- Keep tooling Python standard library only.
- New behaviour lands as REQ + FEAT + TEST + traceability row in the same change.

## Delivery

End every substantial task with the fifteen-field final package report in `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` and the `python tools/run_all_audits.py --quiet` result.
