---
document_id: DOC-130
title: "Product Launch Readiness Checklist"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-130
normative_status: Normative
tier: 2
summary: "Checklist to pass before calling a package release-ready."
source: "AISOP REV-002 GitHub practice-space update"
---


# Product Launch Readiness Checklist

A project derived from AISOP is not launch-ready until these gates are complete.

## Documentation

- README is accurate.
- Start-here guide is accurate.
- Requirements are machine-referenceable.
- Acceptance tests map to requirements.
- Known limitations are explicit.
- Changelog is current.

## Repository

- GitHub community files exist or are intentionally omitted with reason.
- CI passes.
- Branch protection/rulesets are considered.
- Release process is documented.

## Safety/security/license

- License is chosen.
- Attribution is complete.
- Secret scan passes.
- Safety class is assigned.
- Hardware/control risks are mitigated or blocked.

## Release

- Manifest is regenerated.
- Release dry run passes.
- Zip/internal-folder names match.
- Release notes include risks, mitigations, and limitations.
