---
document_id: DOC-EX-PLAN
title: "hello_aisop: Planning Document"
version: 0.1.0
revision: REV-001
status: DRAFT
last_updated: 2026-10-11
package_id: 20261011_00_hello_aisop
machine_reference_prefix: DOC-EX-PLAN
normative_status: Informative
tier: 1
summary: "The plan for hello_aisop at hello-world scale, one short answer per required section."
source: "AISOP worked example"
---

# hello_aisop Planning Document

## 0. Document Control
Header above. Owner: the user. Status: approved for version 0.1.0.
## 1. Executive Summary
A tool that prints line, word, and character counts for one text file.
## 2. Concept Recap
The user wants quick counts for notes without opening an editor.
## 3. User Workflows
Run `python hello_aisop.py notes.txt` and read one line of output.
## 4. Current Baseline / Prototype State
None; this is the first version.
## 5. Functional Requirements
REQ-CNT-001: print lines, words, and characters for one UTF-8 file. REQ-DIAG-001: offer --version, --smoke-test, and --diagnostics.
## 6. Non-Functional Requirements
Standard library only; Python 3, written to stay Python 2.7 compatible.
## 7. Data and Persistence Model
Not needed for this project: nothing is stored.
## 8. UI / UX Model
One output line: `notes.txt: 12 lines, 80 words, 450 characters`.
## 9. Architecture Direction
One file with numbered sections, ready to split later.
## 10. Module Boundary Plan
Not needed for this project: one file.
## 11. File and Folder Structure Plan
The five intake documents, this plan, `hello_aisop.py`, and `tools/`.
## 12. Routes / APIs / Interfaces
Command line only: a path, or one of the three flags.
## 13. Diagnostics and Testing Plan
`--smoke-test` checks known texts and a temporary file; `--diagnostics` adds the environment.
## 14. Risk Register
RISK-001: non-UTF-8 files raise an error; recorded in `KNOWN_LIMITATIONS.md`.
## 15. Technical Debt Register
None yet.
## 16. Decision Log
DECISION-001: no third-party libraries.
## 17. Open Questions
QUESTION-001: should counts ignore blank lines? Not for 0.1.0.
## 18. Implementation Phases
Phase 1: counting and the three flags (done).
## 19. Acceptance Criteria
TEST-CNT-001 and TEST-DIAG-001 in `ACCEPTANCE_TEST_PLAN.md` pass.
## 20. Packaging and Handoff Requirements
Zip as `20261011_00_hello_aisop.zip` with the same top folder; end with the final package report.
## 21. Extraction Plan
Not needed for this project: the plan stays one file.
## 22. Appendices
None.
