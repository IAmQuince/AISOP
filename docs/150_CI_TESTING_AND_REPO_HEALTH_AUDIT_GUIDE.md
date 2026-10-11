---
document_id: DOC-150
title: "CI Testing and Repo Health Audit Guide"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-150
normative_status: Normative
tier: 2
summary: "What the audit commands check, how CI runs them, and how to read the reports."
source: "AISOP REV-002 GitHub practice-space update"
---


# CI Testing and Repo Health Audit Guide

## Local command

```bash
python tools/run_all_audits.py           # full output
python tools/run_all_audits.py --quiet   # one line per tool plus the SUMMARY block
```

The command runs every check with the current Python interpreter and passes in any clone, under any folder name, and inside an unzipped Method Kit.

## What it checks

- package structure, complete document-control headers (including `tier` and `summary`), code-fence parity, and the personal-reference scan (`tools/package_structure_audit.py`);
- required repository files, the license and NOTICE, the CI default branch, canonical report citations, and untracked runtime reports (`tools/repo_health_audit.py`);
- the agent entry layer and references in this tree (`tools/edition_audit.py`);
- generated files and regions are fresh, and every edition is within budget with its references resolving (`tools/build_editions.py --check`);
- the smoke test, including scripted negative cases on a copy of the tree (`tests/smoke_test.py`);
- requirements traceability (`tools/requirements_trace_audit.py`);
- obvious secret patterns (`tools/secret_scan_lite.py`);
- release naming (`tools/release_package.py --dry-run`);
- the package manifest matches the tree (`tools/manifest_update.py --check`, last because it hashes generated files).

`docs/166_EDITIONS_AND_TIERS_SOP.md` section 11 lists which tool owns each check; no check is implemented twice.

## CI principle

CI should call the same commands a local zip recipient can run. Avoid CI-only magic that makes the GitHub path diverge from zip handoff.

## Report handling

Reports are copy/pasteable, state PASS/FAIL clearly, and name the file to fix. They are written to `reports/*.txt` at run time and are not committed; committed evidence lives in `reports/baseline/`.

## When a generated file is stale

Edit the source the failure message names, then run `python tools/build_editions.py all` and the audits again. Never edit a GENERATED file or region by hand.
