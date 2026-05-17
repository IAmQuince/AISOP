---
document_id: DOC-160
title: "Maintainer Playbook"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-160
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Maintainer Playbook

## Weekly or release-cycle routine

- Review open issues.
- Triage safety/security/licensing concerns first.
- Run all audits before release.
- Check whether branch experiments should merge, continue, or archive.
- Confirm known limitations still match reality.

## Branch decisions

A practice branch may be:

- merged into main;
- kept as a named example;
- archived with notes;
- split into a separate project;
- rejected with rationale.

## Release decisions

Before publishing a release:

- verify license status;
- verify safety status;
- verify audit reports;
- verify zip/root-folder naming;
- regenerate manifest;
- write release notes.

## Deprecation

When retiring a practice, preserve enough notes for future users to understand why it was retired and what replaced it.
