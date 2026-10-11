---
document_id: DOC-000-ACCEPTANCE-TEST-PLAN
title: "Acceptance Test Plan"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-ACCEPTANCE-TEST-PLAN
normative_status: Normative
tier: 2
summary: "Every TEST-* acceptance item, the requirement it verifies, and how to run it."
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

TEST-LIC-001 Resolved license present and NOTICE consistent
: Verifies the license file named in `config/package_metadata.json` (`LICENSE.txt`) exists and contains "MIT License", and that `NOTICE.md` names the license and the file. Command: `python tools/repo_health_audit.py`. Requirement: REQ-LIC-001. (Rewritten in REV-003 under the same ID.)

TEST-GOV-001 Practice-space doctrine exists
: Verifies `docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md` exists and explains branches as practice explorations. Requirement: REQ-GOV-001.

TEST-AI-001 AI handoff protocol exists
: Verifies `docs/165_AI_AGENT_HANDOFF_PROTOCOL.md` exists and requires baseline inspection, audit reports, revision updates, and non-regression discipline. Requirement: REQ-AI-001.

## REV-003 Acceptance Tests

TEST-CI-002 CI push trigger covers the default branch
: `python tools/repo_health_audit.py` verifies that `on.push.branches` in `.github/workflows/ci.yml` contains the configured `default_branch`. Requirement: REQ-CI-002.

TEST-REL-002 Release from a renamed working copy
: `python tests/smoke_test.py` copies the tree into a folder with another name, runs `tools/release_package.py`, and verifies the archive is `<package_id>.zip` with the single root `<package_id>/`, that `archive_name_audit.py` passes on it, and that the tool warns about the folder-name difference. Requirement: REQ-REL-002.

TEST-RPT-001 No tracked runtime reports
: `python tools/repo_health_audit.py` verifies `.gitignore` ignores `reports/*.txt` and, in a git clone, that `git ls-files` lists no top-level `reports/*.txt`. Requirement: REQ-RPT-001.

TEST-MAN-001 Manifest freshness check
: `python tools/manifest_update.py --check` exits 0 only when the committed manifest equals a fresh render; `run_all_audits.py` runs it last. Requirement: REQ-MAN-001.

TEST-RPT-002 Delivery documents cite the canonical report
: `python tools/repo_health_audit.py` verifies the template exists, every file in `report_template_citers` (config) cites it, and no other document has a package-report title without citing it. Requirement: REQ-RPT-002.

TEST-PROF-001 Personal-reference and profile-phrase scan
: `python tools/package_structure_audit.py` runs the personal-reference scan extended with third-person profile patterns (a pronoun followed by a habit or preference verb, "the user" followed by a preference verb, and similar; the list is `PROFILE_PHRASE_PATTERNS` in the tool) over every tracked Markdown file; `.gitignore` lists `USER_PROFILE.md`. Requirement: REQ-PROF-001.

TEST-DOC-004 Fence parity
: `python tools/package_structure_audit.py` counts fence lines per Markdown file: odd counts FAIL unless listed in `fence_parity_pending` (WARN), and a listed file that is already balanced FAILs so the list cannot go stale. Requirement: REQ-DOC-004.

TEST-ENTRY-001 Entry file size, identity, and content
: `python tools/edition_audit.py` checks size, header identity and status, the absence of other package_id tokens, both GENERATED regions, the mode names, and the requirements-source path; its reference check covers every cited path; `tests/smoke_test.py` checks presence. Requirement: REQ-ENTRY-001.

TEST-ENTRY-002 Pointer files present and small
: `python tools/edition_audit.py` checks each declared pointer for presence, size, header, and the string `AGENTS.md`; `python tools/build_editions.py --check` checks it is fresh. Requirement: REQ-ENTRY-002.

TEST-ENTRY-003 Generated freshness and the hand-edit negative case
: `python tools/build_editions.py --check` compares every generated target with a fresh render; `tests/smoke_test.py` edits the `rules` region in a copy of the tree and requires the check to exit 1 naming `docs/001_AISOP_CORE_RULES.md`, and validates `docs/index.json` (every document, documented keys, tier-then-path order). Requirement: REQ-ENTRY-003.

TEST-ENTRY-004 Cold-agent test (manual)
: Manual, per release (one tool from Phase 1, two tools from Phase 4): run the prompt in a fresh clone with no other context; record tool and version, date, tool-call count, the minute-5 report, files opened, and a PASS/FAIL verdict in the log; `tools/edition_audit.py` warns when the log for the current package_id is missing. Requirement: REQ-ENTRY-004.

TEST-ED-001 Tier and summary keys
: `python tools/package_structure_audit.py` requires both keys and validates them; `tests/smoke_test.py` deletes `tier:` from one header in a copy of the tree and requires the audit to exit 1 naming that file. Requirement: REQ-ED-001.

TEST-ED-002 Edition budgets and the Method Kit self-audit
: `python tools/build_editions.py --check` stages every edition in memory and fails on a budget or `max_files` breach or a duplicate Chat Kit basename; `tests/smoke_test.py` stages the Method Kit to a folder and requires `run_all_audits.py` to pass inside it. Budgets since REV-003 Phase 2 (DECISION-014): Card 8,192, Chat Kit 122,880 (40 files), Method Kit 524,288 bytes (raised from 409,600). Requirement: REQ-ED-002.

TEST-ED-003 Card budget, rules block, and labels
: `python tools/build_editions.py --check` measures the rendered card; `python tools/edition_audit.py` measures the rules block, checks Normative status, and compares the card's fifteen report labels with the template's. Requirement: REQ-ED-003.

TEST-LINK-001 Reference resolution
: `python tools/edition_audit.py` resolves references in the tree being audited; `python tools/build_editions.py --check` resolves them inside each lower staged edition, honouring edition markers and the planning and history lists in `config/editions.json`. Requirement: REQ-LINK-001.

TEST-BEG-001 Beginner documents, glossary coverage, and Chat Kit contents
: `python tools/edition_audit.py` checks the size caps and glossary coverage; `tests/smoke_test.py` stages the Chat Kit and compares its files with EDITION_INFO.md, rejects documents above tier 1, and confirms AISOP's own changelog and limitations are absent. The scripted cold-chat session (GATE-2 of the REV-003 gameplan) is manual and owner-run. Requirement: REQ-BEG-001.

TEST-TPL-001 Template parity, placeholders, and caps
: `python tools/edition_audit.py` resolves every `derived_from`, compares template headings with the SOP's Required sections, rejects concrete REQ/FEAT/TEST IDs in templates, and checks the caps; `python tools/build_editions.py --check` confirms the manual checklist matches the CHECKS table. Requirement: REQ-TPL-001.

TEST-EX-001 Example registration and lite audit
: `python tools/package_structure_audit.py` fails on an unregistered folder under `examples/` or a registered root without its identity; `tests/smoke_test.py` runs `python tools/aisop_check.py --root examples/hello_aisop --run` and requires SUMMARY: PASS. Requirement: REQ-EX-001.

TEST-ED-004 Edition zips: naming, EDITION_INFO, reproducible content
: `tests/smoke_test.py` builds the release assets twice into temporary folders, requires identical content checksums, and checks each zip's single root and EDITION_INFO.md; `python tools/release_package.py --edition all` runs `archive_name_audit.py` on each zip it writes. Requirement: REQ-ED-004.

TEST-REL-003 Release workflow order
: `python tools/repo_health_audit.py` verifies that `.github/workflows/release.yml` runs on `v*` tags, checks the tag against the configured version, and runs `run_all_audits.py` before `build_editions.py zips`. Requirement: REQ-REL-003.
