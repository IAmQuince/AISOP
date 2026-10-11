---
document_id: DOC-EX-TOOLS
title: "hello_aisop: Tools"
version: 0.1.0
revision: REV-001
status: DRAFT
last_updated: 2026-10-11
package_id: 20261011_00_hello_aisop
machine_reference_prefix: DOC-EX-TOOLS
normative_status: Informative
tier: 1
summary: "Where the package checker comes from and how to run it."
source: "AISOP worked example"
---

# Tools

Copy `aisop_check.py` from the AISOP package (its `tools/` folder) into this folder, then run from the package root:

```bash
python tools/aisop_check.py --root . --run
```

It checks the intake documents, headers, package identity, the diagnostic flags, IDs, the changelog, and links.
