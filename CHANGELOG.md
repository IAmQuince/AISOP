---
document_id: DOC-000-CHANGELOG
title: "Changelog"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
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
