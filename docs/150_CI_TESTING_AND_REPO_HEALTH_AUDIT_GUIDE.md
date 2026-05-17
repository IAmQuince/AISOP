---
document_id: DOC-150
title: "CI Testing and Repo Health Audit Guide"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-150
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# CI Testing and Repo Health Audit Guide

## Local command

```bash
python tools/run_all_audits.py
```

## What it checks

- package structure;
- required GitHub repository files;
- required GitHub workflow files;
- smoke test basics;
- requirements traceability basics;
- obvious secret patterns;
- release package dry run.

## CI principle

CI should call the same commands a local zip recipient can run. Avoid CI-only magic that makes the GitHub path diverge from zip handoff.

## Report handling

Reports should be copy/pasteable and written to `reports/`. They should state PASS/FAIL clearly and identify missing files or broken links.
