---
document_id: DOC-000-FEATURE-INVENTORY
title: "Feature Inventory"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-FEATURE-INVENTORY
normative_status: Informative
tier: 2
summary: "Every FEAT-* capability of this package, with status and verification; update it before changing behaviour."
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
Description: Adds a machine-readable document-control header to each markdown document. Extended in REV-003: code-fence parity is audited (TEST-DOC-004).
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
Description: Stores audit and smoke-test reports under `reports/`. Extended in REV-003: runtime `reports/*.txt` are git-ignored; committed evidence lives in `reports/baseline/` (TEST-RPT-001).
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
: Adds root repository files, `.github/` templates, CI workflow stubs, and repository bootstrap documentation. Extended in REV-003: CI runs on the configured default branch (`master`) as well as `main` and pull requests (TEST-CI-002).

FEAT-011 AISOP practice-space doctrine
: Documents GitHub branches, issues, pull requests, and releases as mechanisms for exploring and comparing practices.

FEAT-012 Dual zip/GitHub release workflow
: Preserves local zip-package handoff while preparing for GitHub tags and downloadable releases.

FEAT-013 Security and safety baseline
: Adds security policy, safety classification, local secret scan, and release-gate language.

FEAT-014 License and attribution decision gate
: Adds explicit license-decision blocking file and attribution/notice workflow. Status: Superseded by FEAT-030 in REV-003 (the MIT license was adopted and the blocking file removed).

FEAT-015 Repository health audit
: Adds a runnable audit for GitHub/community/repository-readiness files.

FEAT-016 Release packaging tool
: Adds deterministic release zip generation and dry-run verification. Extended in REV-003: the archive root comes from `package_id`, not the clone folder name (TEST-REL-002).

FEAT-017 AI agent handoff protocol
: Adds explicit rules for handing the package to AI without feature loss or interface drift.

FEAT-018 Contribution and review workflow
: Adds issue templates, pull request checklist, and contribution SOP.

FEAT-019 Expanded requirements traceability
: Adds requirements and tests covering GitHub readiness, release discipline, safety, security, and licensing.

## REV-003 Feature Additions

FEAT-030 Resolved MIT license and NOTICE consistency
: `LICENSE.txt` (MIT) is the resolved license, named as `license_file` in `config/package_metadata.json` and in `NOTICE.md`; the repository-health audit checks that the three agree. Supersedes FEAT-014. Verification: TEST-LIC-001.

FEAT-031 Checked package manifest
: `tools/manifest_update.py` renders `PACKAGE_MANIFEST.md` from config and the shared file walk and verifies it with `--check` inside `run_all_audits.py`. Verification: TEST-MAN-001.

FEAT-032 Canonical final package report
: `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` is the single fifteen-field delivery report, cited by `AGENTS.md`, `docs/020`, `050`, `060`, `070`, and `165`. Verification: TEST-RPT-002.

FEAT-033 Person-neutral operating instructions and profile template
: `docs/020` rewritten in the second person; preferences moved to `templates/USER_PROFILE_TEMPLATE.md` (six questions plus a fictional example); local `USER_PROFILE.md` git-ignored. Verification: TEST-PROF-001.

FEAT-034 Agent-first entry layer
: `AGENTS.md` (first-five-minutes protocol, modes, hard rules, delivery) with generated `CLAUDE.md` and `GEMINI.md` pointers, and a per-release cold-agent test. Verification: TEST-ENTRY-001.

FEAT-035 Single-source generator
: `tools/build_editions.py` (entry, index, all, zips, stage, --check) with `tools/_aisop_editions.py` and `tools/_aisop_generators.py` renders every generated file and region from one source each. Verification: TEST-ENTRY-003.

FEAT-036 Tiered editions from one tree
: Header `tier` keys and `config/editions.json` define four cumulative editions (Card, Chat Kit, Method Kit, Full) with byte budgets, openers, and file rules; no document is copied. Verification: TEST-ED-001.

FEAT-037 AISOP card
: `docs/001_AISOP_CORE_RULES.md`: the core rules, minimum package, ID discipline, and fifteen report labels in under 8 KB, usable in any chat with no tooling, and the source of the rules in `AGENTS.md`. Verification: TEST-ED-003.

FEAT-039 Edition-aware link checking
: Links and backticked repository paths are resolved in the tree and in every staged edition, with `(chat kit edition)`, `(method edition)`, and `(full edition)` markers for deliberate cross-tier citations. Verification: TEST-LINK-001.

FEAT-041 Beginner on-ramp
: `docs/002` (five-step first project with checks), `docs/003` glossary, `docs/004` editions guide, and the Chat Kit edition built from them. Verification: TEST-BEG-001.

FEAT-040 Templates for every stage
: Fill-in templates (concept brief, planning document, intake documents, ID record formats, handoff bundle, first-session prompts, final package report, user profile) and a generated manual audit checklist. Verification: TEST-TPL-001.

FEAT-042 Worked example and lite audit
: `examples/hello_aisop/` (a complete minimal package with a numbered-section script and the docs/050 flags) and `tools/aisop_check.py`, the single-file checker users copy into their own packages. Verification: TEST-EX-001.

FEAT-038 Multi-edition release flow
: `build_editions.py zips` and `release_package.py --edition all` write the Card, Chat Kit, Method Kit and Full assets with EDITIONS_CHECKSUMS.txt; `bump_release.py` moves the package identity; `.github/workflows/release.yml` publishes them on a `v*` tag after a green audit. Verification: TEST-ED-004.
