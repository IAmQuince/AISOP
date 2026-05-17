---
document_id: DOC-000-FEATURE-INVENTORY
title: "Feature Inventory"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-FEATURE-INVENTORY
normative_status: Normative
source: "Generalized AI-assisted coding SOP source text"
---

# Feature Inventory

## Purpose

This file records the current feature set of the package using stable feature IDs. Future edits should update this file before changing or removing package behavior.

FEAT-001
Name: Generalized AI-assisted coding SOP package
Description: Provides a cleaned, generalized set of AI-assisted coding workflow documents.
Status: Current
Preserve: Yes
Verification: TEST-PKG-002

FEAT-002
Name: Structured markdown documentation library
Description: Splits the source material into topical markdown documents under `docs/`.
Status: Current
Preserve: Yes
Verification: TEST-DOC-003

FEAT-003
Name: Document-control metadata
Description: Adds a machine-readable document-control header to each markdown document.
Status: Current
Preserve: Yes
Verification: TEST-DOC-001

FEAT-004
Name: Machine-referenceable package requirements
Description: Captures package-level requirements using stable `REQ-*` IDs and mirrors them into JSON.
Status: Current
Preserve: Yes
Verification: TEST-DOC-002

FEAT-005
Name: Acceptance test plan
Description: Defines `TEST-*` acceptance items linked to requirement IDs.
Status: Current
Preserve: Yes
Verification: TEST-TEST-001

FEAT-006
Name: Package structure audit
Description: Provides `tools/package_structure_audit.py` to validate required files, metadata, naming, and personal-reference cleanup.
Status: Current
Preserve: Yes
Verification: TEST-AUDIT-001

FEAT-007
Name: Smoke test harness
Description: Provides `tests/smoke_test.py` for a minimal executable package check.
Status: Current
Preserve: Yes
Verification: TEST-SMOKE-001

FEAT-008
Name: Reports folder
Description: Stores audit and smoke-test reports under `reports/`.
Status: Current
Preserve: Yes
Verification: TEST-AUDIT-001, TEST-SMOKE-001

FEAT-009
Name: Example package skeleton
Description: Includes root docs, `docs/`, `tools/`, `tests/`, `reports/`, `requirements/`, `config/`, and `src/` folders to model a future code package.
Status: Current
Preserve: Yes
Verification: TEST-PKG-001

## REV-002 Feature Additions

FEAT-010 GitHub-ready repository substrate
: Adds root repository files, `.github/` templates, CI workflow stubs, and repository bootstrap documentation.

FEAT-011 AISOP practice-space doctrine
: Documents GitHub branches, issues, pull requests, and releases as mechanisms for exploring and comparing practices.

FEAT-012 Dual zip/GitHub release workflow
: Preserves local zip-package handoff while preparing for GitHub tags and downloadable releases.

FEAT-013 Security and safety baseline
: Adds security policy, safety classification, local secret scan, and release-gate language.

FEAT-014 License and attribution decision gate
: Adds explicit license-decision blocking file and attribution/notice workflow.

FEAT-015 Repository health audit
: Adds a runnable audit for GitHub/community/repository-readiness files.

FEAT-016 Release packaging tool
: Adds deterministic release zip generation and dry-run verification.

FEAT-017 AI agent handoff protocol
: Adds explicit rules for handing the package to AI without feature loss or interface drift.

FEAT-018 Contribution and review workflow
: Adds issue templates, pull request checklist, and contribution SOP.

FEAT-019 Expanded requirements traceability
: Adds requirements and tests covering GitHub readiness, release discipline, safety, security, and licensing.
