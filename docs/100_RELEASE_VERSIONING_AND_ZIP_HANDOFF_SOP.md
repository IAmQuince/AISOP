---
document_id: DOC-100
title: "Release Versioning and Zip Handoff SOP"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-100
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Release Versioning and Zip Handoff SOP

## Purpose

Keep GitHub releases and old-school zip trading aligned.

## Naming

Package names should follow:

```text
yyyymmdd_00_short-description
```

For this package:

```text
20260516_00_seed.zip
20260516_00_seed/
```

## Release procedure

1. Update package metadata.
2. Update touched document revisions.
3. Update changelog.
4. Update requirements and traceability if needed.
5. Run all audits.
6. Regenerate manifest.
7. Run release package dry run.
8. Build the zip.
9. Verify archive/root-folder match.
10. Attach the zip to the release or trade it directly.

## Zip handoff rule

A recipient should be able to unzip the package, read `README_START_HERE.md`, run the audits, and understand whether the package is safe to use for their intended purpose.

## GitHub release rule

A GitHub release should correspond to an auditable package state and should include release notes, known limitations, and safety/security/license status.
