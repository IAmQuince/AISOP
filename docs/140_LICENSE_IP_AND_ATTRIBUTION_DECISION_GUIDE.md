---
document_id: DOC-140
title: "License IP and Attribution Decision Guide"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-140
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# License, IP, and Attribution Decision Guide

## Purpose

Force explicit decisions before public publication.

## License questions

- Who owns the code and documents?
- Is public reuse intended?
- Is commercial reuse allowed?
- Are patent, hardware, or safety implications relevant?
- Are third-party examples included?
- Are generated examples derived from proprietary material?

## Common release statuses

- `LICENSE-PENDING`: not ready for public reuse.
- `INTERNAL-ONLY`: may be shared privately inside the organization.
- `OPEN-SOURCE-READY`: license file and attribution are complete.
- `DUAL-LICENSE-REVIEW`: public/private terms need review.

## Required files

- `LICENSE` (or `LICENSE.txt`) after decision.
- `NOTICE.md` for attribution and copied content notes.
- Until the decision is made, a clearly named blocking file (for example `LICENSE_PENDING.md`) that says the work is not yet licensed for reuse.

## This repository

AISOP itself resolved this decision: it is released under the MIT License in `LICENSE.txt`, recorded as `license_file` in `config/package_metadata.json`, and named in `NOTICE.md`. REQ-LIC-001 checks that the three agree.
