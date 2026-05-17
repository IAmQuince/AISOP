---
document_id: DOC-README-TESTS
title: "Tests"
version: 0.2.0
revision: REV-002
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-README-TESTS
normative_status: Informative
source: "Generalized AI-assisted coding SOP source text"
---

# Tests

This folder contains the package smoke test.

Run:

```bash
python tests/smoke_test.py
```

## REV-002 Test Additions

REV-002 keeps script-based tests and audits dependency-light. Run `python tools/run_all_audits.py` for the current combined diagnostic harness.
