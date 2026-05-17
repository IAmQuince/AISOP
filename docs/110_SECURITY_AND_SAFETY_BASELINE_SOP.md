---
document_id: DOC-110
title: "Security and Safety Baseline SOP"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-110
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Security and Safety Baseline SOP

## Purpose

Prevent a package from appearing production-ready before security, safety, and licensing gates are understood.

## Required checks

- Run local secret scan.
- Review safety class.
- Confirm license status.
- Review dependency manifests if present.
- Confirm no private data is included in examples or reports.
- Confirm hardware-control code has safe startup, shutdown, and fault behavior before live use.

## Unsafe publication conditions

Do not publish as product-ready when:

- license status is unresolved;
- secrets or private data are present;
- hardware-control hazards are undocumented;
- tests do not run;
- generated package name does not match internal folder;
- release notes omit known limitations.

## Human review

AI-generated or AI-modified packages must receive human review before controlling real hardware, publishing open source, or being used as a public product basis.
