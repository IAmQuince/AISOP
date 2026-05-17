---
document_id: DOC-000-CONTRIBUTING
title: "Contribution Guide"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-CONTRIBUTING
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Contributing

AISOP contributions should preserve traceability and avoid feature loss.

## Required before opening a pull request

- Run `python tools/run_all_audits.py`.
- Update `CHANGELOG.md` for user-visible changes.
- Update document-control metadata for touched controlled documents.
- Update `requirements/requirements_catalog.json` when adding, changing, or retiring requirements.
- Update `ACCEPTANCE_TEST_PLAN.md` and `REQUIREMENTS_TRACEABILITY_MATRIX.md` when requirements or tests change.
- Explain whether the change affects zip handoff, GitHub workflow, safety, security, licensing, or release packaging.

## Branch style

Use branches to explore practices deliberately. Recommended branch names:

```text
practice/python-gui-seed
practice/hardware-control-safety
practice/offline-zip-handoff
example/labjack-daq
example/pydroid-android
fix/manifest-hash-drift
```

A branch should document what practice it explores, what risks it accepts, and what audit evidence it produces.

## Non-regression rule

Do not remove existing features, files, tests, or documented capabilities unless the pull request explicitly states the removal and explains the replacement or deprecation path.
