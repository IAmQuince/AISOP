---
document_id: DOC-000-SECURITY
title: "Security Policy"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-SECURITY
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Security Policy

## Supported status

This package is a reference seed. Security handling depends on the project that adopts it. A downstream project should define supported versions before public release.

## Reporting vulnerabilities

Report suspected vulnerabilities through a private maintainer channel when available. Do not publish secrets, credentials, exploit details, or private data in public issues.

## No-secrets rule

Never commit API keys, passwords, tokens, private keys, instrument credentials, customer data, or confidential test data. Run:

```bash
python tools/secret_scan_lite.py
```

This local scan is only a preflight. Public GitHub repositories should also enable the platform's security features where appropriate.

## Security release gate

Before public release, complete:

- license decision;
- secret scan;
- dependency review if dependency manifests exist;
- safety classification for hardware/control/data projects;
- release manifest/hash regeneration.
