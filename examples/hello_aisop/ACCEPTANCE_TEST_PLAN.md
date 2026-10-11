---
document_id: DOC-EX-TESTS
title: "hello_aisop: Acceptance Test Plan"
version: 0.1.0
revision: REV-001
status: DRAFT
last_updated: 2026-10-11
package_id: 20261011_00_hello_aisop
machine_reference_prefix: DOC-EX-TESTS
normative_status: Informative
tier: 1
summary: "How each hello_aisop requirement is checked."
source: "AISOP worked example"
---

# Acceptance Test Plan

TEST-CNT-001
Linked requirement: REQ-CNT-001
Command: `python hello_aisop.py --smoke-test`
Expected result: `PASS two lines`, `PASS file round trip`, and `SUMMARY: PASS`.
Status: Implemented

TEST-DIAG-001
Linked requirement: REQ-DIAG-001
Command: `python hello_aisop.py --version` and `python hello_aisop.py --diagnostics`
Expected result: the version line; the Python version, platform, and `SUMMARY: PASS`.
Status: Implemented
