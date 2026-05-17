---
document_id: DOC-000-TRACEABILITY
title: "Requirements Traceability Matrix"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-TRACEABILITY
normative_status: Normative
source: "Generalized AI-assisted coding SOP source text"
---

# Requirements Traceability Matrix

## Purpose

This matrix links package requirements to features, tests, and files. It is intentionally small and illustrative.

| Requirement | Feature(s) | Acceptance Test(s) | Primary File(s) |
|---|---|---|---|
| REQ-PKG-001 | FEAT-009 | TEST-PKG-001 | PACKAGE_MANIFEST.md |
| REQ-PKG-002 | FEAT-001 | TEST-PKG-002 | README_START_HERE.md |
| REQ-DOC-001 | FEAT-003 | TEST-DOC-001 | all markdown files |
| REQ-DOC-002 | FEAT-004 | TEST-DOC-002 | docs/005_PRODUCT_REQUIREMENTS.md, requirements/requirements_catalog.json |
| REQ-DOC-003 | FEAT-002 | TEST-DOC-003 | docs/000_DOCUMENTATION_INDEX.md |
| REQ-FEAT-001 | FEAT-001 through FEAT-009 | TEST-FEAT-001 | FEATURE_INVENTORY.md |
| REQ-TEST-001 | FEAT-005 | TEST-TEST-001 | ACCEPTANCE_TEST_PLAN.md |
| REQ-AUDIT-001 | FEAT-006, FEAT-008 | TEST-AUDIT-001 | tools/package_structure_audit.py |
| REQ-SMOKE-001 | FEAT-007, FEAT-008 | TEST-SMOKE-001 | tests/smoke_test.py |
| REQ-GEN-001 | FEAT-001 | TEST-GEN-001 | all markdown files |
| REQ-LIMIT-001 | FEAT-001 | TEST-LIMIT-001 | KNOWN_LIMITATIONS.md |

## REV-002 Traceability Additions

| Requirement ID | Verification ID | Primary File(s) |
|---|---|---|
| REQ-REPO-001 | TEST-REPO-001 | `README.md`, `README_START_HERE.md` |
| REQ-REPO-002 | TEST-REPO-002 | `.gitignore`, `.gitattributes`, `.editorconfig` |
| REQ-REPO-003 | TEST-REPO-003 | `.github/` |
| REQ-CI-001 | TEST-CI-001 | `.github/workflows/ci.yml`, `tools/run_all_audits.py` |
| REQ-REL-001 | TEST-REL-001 | `tools/release_package.py`, `tools/archive_name_audit.py` |
| REQ-SEC-001 | TEST-SEC-001 | `SECURITY.md` |
| REQ-SEC-002 | TEST-SEC-002 | `tools/secret_scan_lite.py` |
| REQ-SAFE-001 | TEST-SAFE-001 | `SAFETY.md` |
| REQ-LIC-001 | TEST-LIC-001 | `LICENSE_DECISION_REQUIRED.md`, `NOTICE.md` |
| REQ-GOV-001 | TEST-GOV-001 | `docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md` |
| REQ-AI-001 | TEST-AI-001 | `docs/165_AI_AGENT_HANDOFF_PROTOCOL.md` |
