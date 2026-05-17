---
document_id: DOC-000-ACCEPTANCE-TEST-PLAN
title: "Acceptance Test Plan"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-ACCEPTANCE-TEST-PLAN
normative_status: Normative
source: "Generalized AI-assisted coding SOP source text"
---

# Acceptance Test Plan

## Purpose

This document maps package requirements to testable acceptance items. It is intentionally small so the package remains a lightweight reference example.

TEST-PKG-001
Linked requirement: REQ-PKG-001
Type: Automated/manual
Command: `python tools/package_structure_audit.py`
Expected result: Zip/internal package naming rule is documented and package structure is valid.
Status: Implemented

TEST-PKG-002
Linked requirement: REQ-PKG-002
Type: Automated
Command: `python tools/package_structure_audit.py`
Expected result: `README_START_HERE.md` exists and is non-empty.
Status: Implemented

TEST-DOC-001
Linked requirement: REQ-DOC-001
Type: Automated
Command: `python tools/package_structure_audit.py`
Expected result: Every markdown file includes required document-control metadata.
Status: Implemented

TEST-DOC-002
Linked requirement: REQ-DOC-002
Type: Automated/manual
Command: `python tests/smoke_test.py`
Expected result: Requirement IDs are present, unique enough for this package, and mirrored into `requirements/requirements_catalog.json`.
Status: Implemented

TEST-DOC-003
Linked requirement: REQ-DOC-003
Type: Automated
Command: `python tools/package_structure_audit.py`
Expected result: `docs/000_DOCUMENTATION_INDEX.md` exists and is non-empty.
Status: Implemented

TEST-FEAT-001
Linked requirement: REQ-FEAT-001
Type: Automated/manual
Command: `python tests/smoke_test.py`
Expected result: `FEATURE_INVENTORY.md` exists and contains `FEAT-*` entries.
Status: Implemented

TEST-TEST-001
Linked requirement: REQ-TEST-001
Type: Automated/manual
Command: `python tests/smoke_test.py`
Expected result: `ACCEPTANCE_TEST_PLAN.md` exists and contains `TEST-*` entries linked to `REQ-*` IDs.
Status: Implemented

TEST-AUDIT-001
Linked requirement: REQ-AUDIT-001
Type: Automated
Command: `python tools/package_structure_audit.py`
Expected result: Audit completes and writes `reports/package_structure_audit_report.txt`.
Status: Implemented

TEST-SMOKE-001
Linked requirement: REQ-SMOKE-001
Type: Automated
Command: `python tests/smoke_test.py`
Expected result: Smoke test completes and writes `reports/smoke_test_report.txt`.
Status: Implemented

TEST-GEN-001
Linked requirement: REQ-GEN-001
Type: Automated
Command: `python tools/package_structure_audit.py`
Expected result: Personal-reference scan passes.
Status: Implemented

TEST-LIMIT-001
Linked requirement: REQ-LIMIT-001
Type: Manual/automated
Command: `python tools/package_structure_audit.py`
Expected result: `KNOWN_LIMITATIONS.md` exists and is non-empty.
Status: Implemented

## REV-002 Acceptance Tests

TEST-REPO-001 GitHub README exists
: Verifies `README.md` exists and points users to `README_START_HERE.md` and the practice-space documents. Requirement: REQ-REPO-001.

TEST-REPO-002 Repository hygiene files exist
: Verifies `.gitignore`, `.gitattributes`, and `.editorconfig` exist. Requirement: REQ-REPO-002.

TEST-REPO-003 GitHub templates exist
: Verifies `.github/` issue templates, pull request template, and workflows exist. Requirement: REQ-REPO-003.

TEST-CI-001 CI workflow exists
: Verifies `.github/workflows/ci.yml` calls `python tools/run_all_audits.py`. Requirement: REQ-CI-001.

TEST-REL-001 Release dry run passes
: Verifies `python tools/release_package.py --dry-run` completes and confirms package/root naming. Requirement: REQ-REL-001.

TEST-SEC-001 Security policy exists
: Verifies `SECURITY.md` exists and documents reporting/no-secrets rules. Requirement: REQ-SEC-001.

TEST-SEC-002 Secret scan runs
: Verifies `python tools/secret_scan_lite.py` writes `reports/secret_scan_lite_report.txt`. Requirement: REQ-SEC-002.

TEST-SAFE-001 Safety baseline exists
: Verifies `SAFETY.md` exists and defines safety classes. Requirement: REQ-SAFE-001.

TEST-LIC-001 License decision gate exists
: Verifies `LICENSE_DECISION_REQUIRED.md` exists and no public-ready license status is claimed. Requirement: REQ-LIC-001.

TEST-GOV-001 Practice-space doctrine exists
: Verifies `docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md` exists and explains branches as practice explorations. Requirement: REQ-GOV-001.

TEST-AI-001 AI handoff protocol exists
: Verifies `docs/165_AI_AGENT_HANDOFF_PROTOCOL.md` exists and requires baseline inspection, audit reports, revision updates, and non-regression discipline. Requirement: REQ-AI-001.
