---
document_id: DOC-000-WORKPLAN-CURRENT-RUN
title: "Workplan Current Run"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-WORKPLAN-CURRENT-RUN
normative_status: Informative
source: "Generalized AI-assisted coding SOP source text"
---

# Workplan Current Run

RUN-001
Run name: 20260502_01_ai_sop_reference_package
Date: 2026-05-02
Purpose: Convert the generalized SOP markdown seed into a self-describing example package with document control, machine-referenceable requirements, feature inventory, acceptance tests, audit tooling, and smoke-test tooling.

## Scope

This run changes package structure and metadata only. It does not rewrite all long-form technical reference content.

## Completed Changes

- Added document-control metadata to markdown documents.
- Added package-level machine-referenceable requirements.
- Added feature inventory.
- Added acceptance test plan.
- Added known limitations.
- Added current workplan.
- Added machine-readable requirement catalog JSON.
- Added package metadata JSON.
- Expanded audit and smoke-test tooling.
- Generated reports.

## Out of Scope

- Full editorial rewrite of every technical guide.
- Conversion to DOCX/PDF.
- Building a runnable application beyond package validation tools.
- Verifying every third-party installer/link in the reference guides.

## Next Recommended Run

Perform a human editorial pass and decide whether to keep the long technical reference guides as one package or split them into a smaller public-facing starter edition plus an expanded technical appendix.

## REV-002 Workplan: GitHub Practice-Space Upgrade

### Objective

Convert the package from a local-only SOP seed into a dual-use artifact: a GitHub-ready repository and a self-documenting guide for making zip-based packages GitHub-ready.

### Phases

1. Preserve REV-001 baseline audit reports.
2. Rename package identity to `20260516_00_seed`.
3. Add GitHub/community/repository files.
4. Add practice-space and GitHub bootstrap SOP documents.
5. Expand requirements, feature inventory, tests, and traceability.
6. Add audits and release packaging tools.
7. Run all audits and generate release zip.

### Acceptance

- Existing package audit passes.
- Smoke test passes.
- Repository-health audit passes.
- Secret scan completes.
- Release dry run passes.
- Final package zip has matching zip basename and internal root folder.
