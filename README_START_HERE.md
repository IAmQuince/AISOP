---
document_id: DOC-000-README
title: "AI-Assisted Coding SOP Reference Package"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-README
normative_status: Informative
tier: 1
summary: "First file to read in any AISOP package: purpose, reading order, and how to check the package."
source: "Generalized AI-assisted coding SOP source text"
---

# AI-Assisted Coding SOP Reference Package

This package is a cleaned, generalized, self-describing reference package for AI-assisted software planning, prototyping, packaging, diagnostics, and platform-specific development workflows.

It is intentionally structured like the type of code package it recommends. The package includes root-level intake documents, a documentation library, machine-referenceable requirements, a feature inventory, acceptance tests, audit tooling, smoke-test tooling, reports, and placeholder source folders.

## Start Here

Read these files in order:

1. `README_START_HERE.md`
2. `CHANGELOG.md`
3. `FEATURE_INVENTORY.md`
4. `docs/005_PRODUCT_REQUIREMENTS.md` (method edition)
5. `ACCEPTANCE_TEST_PLAN.md`
6. `KNOWN_LIMITATIONS.md`
7. `docs/000_DOCUMENTATION_INDEX.md` (method edition)

## Intended Use

Use this package as:

- a seed for AI-assisted coding workflows;
- a reference example for package structure;
- a lightweight demonstration of machine-referenceable requirements;
- a documentation starter for future code projects;
- a handoff artifact that can be reviewed by a human or AI agent without hidden chat context.

## Quick Commands

Run the structure audit:

```bash
python tools/package_structure_audit.py
```

Run the smoke test:

```bash
python tests/smoke_test.py
```

Generated reports are written to `reports/`.

## Package Rules

- The zip filename and internal top-level folder name should match.
- Every markdown document should include document-control metadata.
- Normative package requirements should use stable `REQ-*` IDs.
- Feature inventory entries should use stable `FEAT-*` IDs.
- Acceptance tests should use stable `TEST-*` IDs and link back to requirements.
- Personal source-specific wording should remain generalized.

## Current Status

Status: Draft reference package.

This is a structured seed, not a finished production application.

## REV-002 GitHub and Practice-Space Update

This revision keeps local zip handoff as a first-class workflow while adding a GitHub-ready repository layer.

The package now demonstrates and documents the transition:

```text
local zip package -> audited package -> GitHub repository -> practice branch -> tagged release -> downloadable zip package
```

For the practice-space concept, read `docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md` (method edition).
For repository bootstrapping, read `docs/090_GITHUB_REPOSITORY_BOOTSTRAP_SOP.md` (method edition).
For release and zip handoff, read `docs/100_RELEASE_VERSIONING_AND_ZIP_HANDOFF_SOP.md` (method edition).

Additional commands:

```bash
python tools/run_all_audits.py
python tools/release_package.py
```
