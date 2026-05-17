---
document_id: DOC-120
title: "Contribution Review and Issue Workflow SOP"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-120
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Contribution Review and Issue Workflow SOP

## Purpose

Use GitHub issues and pull requests to keep practice exploration traceable.

## Issue workflow

1. Open the closest issue template.
2. Identify package version and branch.
3. Link affected requirements, tests, features, or docs.
4. Classify safety/security/licensing impact.
5. Add reproduction steps or acceptance criteria.

## Pull request workflow

1. Keep changes scoped.
2. Update controlled document metadata for touched docs.
3. Update changelog and traceability.
4. Run all audits.
5. State non-regression impact.
6. Request review when safety/security/licensing is touched.

## Merge gate

A pull request should not merge when audits fail, requirements are untraced, release files are inconsistent, or feature loss is unexplained.
