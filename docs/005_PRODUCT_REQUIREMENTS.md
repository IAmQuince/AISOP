---
document_id: DOC-005
title: "Product Requirements"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-005
normative_status: Normative
tier: 2
summary: "The authoritative list of REQ-* requirements for this package; the only requirements source besides the JSON catalog."
source: "Generalized AI-assisted coding SOP source text"
---

# Product Requirements

## Scope

This document is the authoritative machine-referenceable requirement list for this example package.

The long instructional guides in `docs/` are informative reference material unless a requirement in this file explicitly references them. This keeps the example package small while still illustrating how requirements should be captured, traced, tested, and audited.

## Requirement Status Values

- Proposed
- Accepted
- Implemented
- Deferred
- Rejected

## Machine-Referenceable Requirements

REQ-PKG-001
Title: Package naming match
Requirement: The zip filename and internal top-level folder name shall match.
Rationale: Matching names make package intake, auditing, and handoff less ambiguous.
Acceptance test: Open the zip and verify the top-level folder name equals the zip basename.
Priority: Must
Status: Implemented
Verification: TEST-PKG-001

REQ-PKG-002
Title: Start-here documentation
Requirement: The package shall include `README_START_HERE.md` at the root.
Rationale: A reviewer or AI agent needs a deterministic first file to read.
Acceptance test: Confirm the file exists and explains package purpose, usage, and audit commands.
Priority: Must
Status: Implemented
Verification: TEST-PKG-002

REQ-DOC-001
Title: Document control metadata
Requirement: Every markdown document shall include a machine-readable document-control header with document ID, title, version, revision, status, last-updated date, package ID, and normative status.
Rationale: The package itself should demonstrate the documentation discipline it recommends.
Acceptance test: Run `python tools/package_structure_audit.py` and verify all markdown files pass the metadata check.
Priority: Must
Status: Implemented
Verification: TEST-DOC-001

REQ-DOC-002
Title: Machine-referenceable requirements
Requirement: Every normative package requirement shall have a stable ID using the `REQ-*` pattern.
Rationale: Requirements must be traceable across acceptance tests, feature inventory, workplans, and audit reports.
Acceptance test: Confirm this document contains no unnumbered normative requirements and that each `REQ-*` has a linked verification item.
Priority: Must
Status: Implemented
Verification: TEST-DOC-002

REQ-DOC-003
Title: Documentation index
Requirement: The package shall include a documentation index listing the major documents and their intended use.
Rationale: Reviewers should be able to navigate the package without hidden chat context.
Acceptance test: Confirm `docs/000_DOCUMENTATION_INDEX.md` exists and lists the package documents.
Priority: Must
Status: Implemented
Verification: TEST-DOC-003

REQ-FEAT-001
Title: Feature inventory
Requirement: The package shall include `FEATURE_INVENTORY.md` with stable `FEAT-*` IDs.
Rationale: Feature preservation depends on knowing what the package currently contains.
Acceptance test: Confirm each listed feature has an ID, description, status, and verification method.
Priority: Must
Status: Implemented
Verification: TEST-FEAT-001

REQ-TEST-001
Title: Acceptance test plan
Requirement: The package shall include `ACCEPTANCE_TEST_PLAN.md` with stable `TEST-*` IDs mapped to requirements.
Rationale: A requirement without a test is not enforceable.
Acceptance test: Confirm every Must requirement in this file has at least one mapped `TEST-*` item.
Priority: Must
Status: Implemented
Verification: TEST-TEST-001

REQ-AUDIT-001
Title: Structure audit tool
Requirement: The package shall include a runnable structure audit tool under `tools/`.
Rationale: The package should be self-checking and should generate copy/pasteable reports.
Acceptance test: Run `python tools/package_structure_audit.py` and confirm the report is written to `reports/package_structure_audit_report.txt`.
Priority: Must
Status: Implemented
Verification: TEST-AUDIT-001

REQ-SMOKE-001
Title: Smoke test
Requirement: The package shall include a runnable smoke test under `tests/`.
Rationale: The package should demonstrate the minimum test harness expected of future code packages.
Acceptance test: Run `python tests/smoke_test.py` and confirm the report is written to `reports/smoke_test_report.txt`.
Priority: Should
Status: Implemented
Verification: TEST-SMOKE-001

REQ-GEN-001
Title: Generalized wording
Requirement: The deliverable package shall not contain direct personal-name references from the source draft.
Rationale: The package is intended as a reusable consumer-facing seed, not a personal working note.
Acceptance test: Run the audit tool and confirm the personal-reference scan passes.
Priority: Must
Status: Implemented
Verification: TEST-GEN-001

REQ-LIMIT-001
Title: Known limitations
Requirement: The package shall include known limitations and make clear that it is an example seed, not a complete production application.
Rationale: The package should not overclaim completeness.
Acceptance test: Confirm `KNOWN_LIMITATIONS.md` exists and includes first-pass limitations.
Priority: Should
Status: Implemented
Verification: TEST-LIMIT-001

## Requirement Traceability Summary

The machine-readable requirement catalog is also stored at:

`requirements/requirements_catalog.json`

That JSON file is derived from the requirement list above and is intended as a simple example of machine-readable requirement indexing.

## REV-002 Product Requirements

REQ-REPO-001 GitHub-facing repository README
: The package shall include a root `README.md` suitable for GitHub visitors and shall direct users to the package start-here workflow.

REQ-REPO-002 Repository hygiene files
: The package shall include `.gitignore`, `.gitattributes`, and `.editorconfig`.

REQ-REPO-003 GitHub collaboration files
: The package shall include `.github/` issue templates, a pull request template, and baseline workflows.

REQ-CI-001 Local/CI audit parity
: The GitHub CI workflow shall call the same all-audits command available to zip-package recipients.

REQ-REL-001 Archive/root name match
: Release packaging shall verify that the zip basename and internal root folder name match.

REQ-SEC-001 Security policy
: The package shall include `SECURITY.md` defining reporting and no-secrets expectations.

REQ-SEC-002 Lightweight secret scan
: The package shall include a local secret-pattern scan that writes a copy/pasteable report.

REQ-SAFE-001 Safety baseline
: The package shall include `SAFETY.md` defining safety classes and baseline live-control rules.

REQ-LIC-001 Resolved license and notice consistency
: The package shall include the resolved license file named by `license_file` in `config/package_metadata.json`, and `NOTICE.md` shall name that license and file. (Rewritten in REV-003 under the same ID; the earlier license-decision gate was retired when the MIT license was adopted.)

REQ-GOV-001 Practice-space doctrine
: The package shall document AISOP as a branchable, auditable space of practices.

REQ-AI-001 AI agent handoff protocol
: The package shall include instructions for AI-assisted revision that require file inspection, revision updates, audit execution, and feature preservation.

## REV-003 Product Requirements

REQ-CI-002 CI on the default branch
: CI shall run on pushes to the default branch named by `default_branch` in `config/package_metadata.json` and on every pull request. Priority: Must. Status: Implemented. Verification: TEST-CI-002.

REQ-REL-002 Release root from package_id
: The release archive root and basename shall derive from `package_id` in `config/package_metadata.json`, never from the working-copy folder name; edition archives use `<package_id>_<edition>`. Priority: Must. Status: Implemented. Verification: TEST-REL-002.

REQ-RPT-001 Runtime reports not committed
: Runtime audit reports (`reports/*.txt`) shall be git-ignored and untracked; committed audit evidence lives under `reports/baseline/`, snapshotted per release. Priority: Must. Status: Implemented. Verification: TEST-RPT-001.

REQ-MAN-001 Manifest verified against the tree
: `PACKAGE_MANIFEST.md` shall be generated from the git-ignore-aware file list with header values from config, and `tools/manifest_update.py --check` shall run as the last step of `tools/run_all_audits.py`. Priority: Must. Status: Implemented. Verification: TEST-MAN-001.

REQ-RPT-002 One canonical final package report
: There shall be one final package report format, the fifteen fields of `docs/070` section 18, provided as `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`; every document that describes delivery shall cite that template rather than define its own format. Priority: Must. Status: Implemented. Verification: TEST-RPT-002.

REQ-PROF-001 No personal profile in operating instructions
: The AI operating instructions (`docs/020`) shall address the assistant in the second person and contain no biography or personal preference of a specific user; user-specific facts live in `templates/USER_PROFILE_TEMPLATE.md` (fill-in fields plus a labelled fictional example) and an optional git-ignored `USER_PROFILE.md`. Priority: Must. Status: Implemented. Verification: TEST-PROF-001.

REQ-DOC-004 Balanced code fences
: Every Markdown document shall have an even number of lines starting with a code fence, so no document renders as one unterminated code block; documents awaiting re-fencing are listed in `fence_parity_pending` in config and reported as warnings until fixed. Priority: Must. Status: Implemented. Verification: TEST-DOC-004.

REQ-ENTRY-001 Agent entry file
: `AGENTS.md` shall exist with a complete Normative document-control header, stay within `agents_file.budget_bytes` (8,192) including its GENERATED regions, cite only existing paths, name no package_id in its body, and state the normative rule and the mode selector (ORIENT, APPLY, MODIFY-AISOP, DOMAIN-LOOKUP). Priority: Must. Status: Implemented. Verification: TEST-ENTRY-001.

REQ-ENTRY-002 Pointer files
: A pointer file shall exist for each tool listed in `pointer_files` in `config/editions.json`; each is generated, carries a document-control header, names `AGENTS.md`, and stays within `pointer_budget_bytes`. Priority: Must. Status: Implemented. Verification: TEST-ENTRY-002.

REQ-ENTRY-003 Generated content is fresh
: Every GENERATED region and file (the `AGENTS.md` regions, pointer files, the card opener, the editions table, `docs/index.json`, `docs/000_DOCUMENTATION_INDEX.md`) shall equal a fresh render from its source, and a hand edit shall fail the audits with a message naming the source to edit. Priority: Must. Status: Implemented. Verification: TEST-ENTRY-003.

REQ-ENTRY-004 Cold-agent verification per release
: Before each release, a cold agent given only the repository and the prompt 'Get up to speed on AISOP' shall reach a running audit within six tool calls and deliver the first-five-minutes report with mode ORIENT, the normative rule stated correctly, and no domain guide opened; the transcript summary is kept as `reports/baseline/cold_agent_test_<package_id>.txt`. Priority: Must. Status: Implemented. Verification: TEST-ENTRY-004.

REQ-ED-001 Tier and summary in every header
: Every Markdown document outside `.github/` shall declare `tier` (0-3) and a one-line `summary` of at most 200 characters in its document-control header; domain guides also declare `topics`. Priority: Must. Status: Implemented. Verification: TEST-ED-001.

REQ-ED-002 Editions declared and built by one tool
: Editions shall be declared only in `config/editions.json` (tier cutoff, byte budget, `max_files`, include globs, opener) and staged by one standard-library tool; each staged edition shall stay within budget and the staged Method Kit shall pass its own audits. Priority: Must. Status: Implemented. Verification: TEST-ED-002.

REQ-ED-003 One source for the core rules
: `docs/001_AISOP_CORE_RULES.md` shall be the single source of the core rules: Normative, rendered as the card within `card.budget_bytes` (8,192), with a rules block within `card.rules_block_budget_bytes` (4,096) that is generated into `AGENTS.md`, and report labels equal to those of `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`. Priority: Must. Status: Implemented. Verification: TEST-ED-003.

REQ-LINK-001 References resolve in every edition
: Every relative Markdown link and every backticked path under the docs, tools, templates, or examples folders shall resolve in the tree, and in each staged edition except on lines carrying an edition marker for a higher edition; downstream-project paths are written with a leading `./`. Priority: Must. Status: Implemented. Verification: TEST-LINK-001.

REQ-BEG-001 Beginner on-ramp
: The package shall include a beginner's guide (`docs/002`, at most 12,288 bytes), a glossary (`docs/003`, at most 6,144 bytes) that defines every ID family used in tiers 0-2 and the seeded terms, and an editions guide (`docs/004`, at most 5,120 bytes); the staged Chat Kit shall contain only tier 0-1 documents plus its fixed files, exactly as its EDITION_INFO.md lists. Priority: Must. Status: Implemented. Verification: TEST-BEG-001.

REQ-TPL-001 Templates
: Templates under `templates/` shall declare `derived_from` when they come from an SOP, match the `## Required sections` list that SOP gives for them, use placeholder IDs only (`REQ-XXX-NNN`, `FEAT-NNN`, `TEST-XXX-NNN`), and stay within their size caps; `templates/MANUAL_AUDIT_CHECKLIST.md` is generated from the CHECKS table of `tools/aisop_check.py`. Priority: Must. Status: Implemented. Verification: TEST-TPL-001.

REQ-EX-001 Registered example package
: Example packages shall be registered in `example_packages` in `config/package_metadata.json`, declare `package_role: example` and their own `package_id` in their README_START_HERE.md, use `DOC-EX-` document IDs, and pass `tools/aisop_check.py` (the standard-library lite audit for downstream packages) including their own smoke test. Priority: Must. Status: Implemented. Verification: TEST-EX-001.
