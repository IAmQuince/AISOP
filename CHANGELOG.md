---
document_id: DOC-000-CHANGELOG
title: "Changelog"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-10
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-CHANGELOG
normative_status: Informative
source: "Generalized AI-assisted coding SOP source text"
---

# Changelog

## 0.1.0 / REV-001 / 2026-05-02

- Converted the markdown seed into a self-describing example package.
- Added document-control metadata to markdown documents.
- Added root-level `FEATURE_INVENTORY.md`.
- Added root-level `ACCEPTANCE_TEST_PLAN.md`.
- Added root-level `KNOWN_LIMITATIONS.md`.
- Added root-level `WORKPLAN_CURRENT_RUN.md`.
- Added root-level `REQUIREMENTS_TRACEABILITY_MATRIX.md`.
- Added `docs/005_PRODUCT_REQUIREMENTS.md` as the authoritative requirement list.
- Added `requirements/requirements_catalog.json` for machine-readable requirement indexing.
- Added `config/package_metadata.json`.
- Expanded package audit tooling.
- Added smoke-test tooling.
- Generated audit and smoke-test reports.

## 0.0.1 / REV-000 / 2026-05-02

- Initial cleaned generalized markdown seed package.

## 0.2.0 / REV-002 - 2026-05-16

### Added

- GitHub-ready repository substrate: `README.md`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.github/` templates, CI workflows, and Dependabot configuration.
- Practice-space doctrine explaining AISOP as a branchable, auditable space of practices rather than only a static package.
- Security, safety, support, contribution, attribution, and license-decision documents.
- Release-package tooling to preserve old-school zip handoff while supporting GitHub releases.
- Repository-health, traceability, archive-name, secret-scan, manifest-update, and all-audits tools.
- Baseline REV-001 audit reports preserved under `reports/baseline/`.

### Changed

- Package identity updated to `20260516_00_seed`.
- Package version updated from `0.1.0` to `0.2.0`.
- Touched existing controlled documents updated to `REV-002`.
- README workflow updated to describe both zip handoff and GitHub repository use.
- Requirement catalog expanded for repository, CI, release, safety, security, license, and governance requirements.

### Risk notes

- License remains intentionally unresolved and is treated as a release gate.
- GitHub repository settings such as branch protection cannot be fully enforced from files alone and require maintainer setup.
- Local secret scan is a lightweight preflight, not a complete security review.

## Unreleased / REV-003 planning - 2026-10-10

### Added

- `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`: proposed plan for tiered editions built from one source tree, an agent-first entry file, a beginner on-ramp, a multi-edition release flow, and the Phase 0 drift fixes that must land first. Revised once (REV-002) after a five-lens adversarial review. Planning document only; no structure changes in this entry.
- Index and workplan entries pointing at the gameplan.

### Changed

- `PACKAGE_MANIFEST.md` regenerated for the files touched by this entry; the header constants in `tools/manifest_update.py` bumped to match (revision, last_updated). Reading those values from `config/package_metadata.json` is scheduled for Phase 0 of the gameplan.

### Known drift recorded (not yet fixed)

- `run_all_audits.py` currently fails: the license-decision gate was removed on GitHub but the audits, metadata, and requirements still expect it; `release_package.py` hard-codes the seed root folder name; CI triggers on `main` while the default branch is `master`; runtime reports are committed. All are scheduled for Phase 0 of the gameplan.

## Unreleased / REV-003 Phase 0 - 2026-10-11

Executes Phase 0 of `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`. Slices were developed as separate commits on one working branch (the session could push to a single branch only), not as separate `practice/rev003-*` branches.

### 0a. License gate and CI branch

- DRIFT-001: retired every live reference to the deleted license-decision gate. REQ-LIC-001 and TEST-LIC-001 rewritten under the same IDs: the license file named by `license_file` in `config/package_metadata.json` (`LICENSE.txt`, MIT) must exist and `NOTICE.md` must name it. FEAT-014 marked Superseded by FEAT-030. `README.md`, `NOTICE.md`, `KNOWN_LIMITATIONS.md`, `CITATION.cff` (license field), and `docs/140` updated.
- DRIFT-003: `ci.yml` now runs on pushes to `master` and `main`; `package_audit.yml` gained the same push trigger. Default branch recorded as `default_branch` in config and documented in `README.md` (DECISION-001). Added REQ-CI-002 / TEST-CI-002, checked by `repo_health_audit.py`.
