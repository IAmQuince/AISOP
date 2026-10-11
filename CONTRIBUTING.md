---
document_id: DOC-000-CONTRIBUTING
title: "Contribution Guide"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-000-CONTRIBUTING
normative_status: Normative
tier: 2
summary: "What a contributor must run and update before opening a pull request."
source: "AISOP REV-002 GitHub practice-space update"
---


# Contributing

AISOP contributions should preserve traceability and avoid feature loss.

## Required before opening a pull request

- Run `python tools/build_editions.py all` to regenerate generated files and regions, then make sure `python tools/build_editions.py --check` and `python tools/run_all_audits.py` pass.
- Give every new Markdown document a complete document-control header, including `tier` and `summary` (`docs/166_EDITIONS_AND_TIERS_SOP.md`).
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
