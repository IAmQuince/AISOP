---
document_id: DOC-README-REPORTS
title: "Reports"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-README-REPORTS
normative_status: Informative
tier: 2
summary: "What the reports folder holds: runtime reports (not committed) and committed baseline evidence."
source: "Generalized AI-assisted coding SOP source text"
---

# Reports

Generated audit and smoke-test reports are written here at run time.

- `reports/*.txt` are runtime output. They are git-ignored (REQ-RPT-001) and rewritten on every run, so running the audits never dirties the working tree. Paste them into a conversation or issue as evidence; do not commit them.
- `reports/baseline/` is committed evidence: one snapshot per release or revision, named `baseline_<revision>_<report>.txt`. `baseline_rev002_run_all_audits_report.txt` is the REV-002 release run; `baseline_rev003_*` files record REV-003 gates (for example `baseline_rev003_phase0_run_all_audits_report.txt`, the GATE-0 run).

## REV-002 Reports

REV-002 adds these reports:

- `repo_health_audit_report.txt`
- `requirements_trace_audit_report.txt`
- `secret_scan_lite_report.txt`
- `release_dry_run_report.txt`
- `run_all_audits_report.txt`
- `baseline/baseline_rev001_package_structure_audit_report.txt`
- `baseline/baseline_rev001_smoke_test_report.txt`
