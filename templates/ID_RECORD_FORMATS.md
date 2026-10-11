---
document_id: DOC-TPL-ID-FORMATS
title: "ID Record Formats"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-TPL-ID-FORMATS
normative_status: Informative
tier: 1
summary: "The record shapes for requirements, features, tests, risks, debts, decisions, questions, and limitations, stated once."
source: "REV-003 Phase 2 template"
---

# ID Record Formats

Every important item gets a stable ID. Never renumber or reuse one: a changed item keeps its ID with new text; a retired one is marked Superseded. `XXX` is a short area code (for example `UI`, `DATA`, `PKG`); `NNN` is a three-digit number.

## Requirement

```text
REQ-XXX-NNN
Title: <short title>
Requirement: <one testable sentence using "shall">
Rationale: <why>
Priority: Must | Should | Could
Status: Proposed | Accepted | Implemented | Deferred | Rejected | Superseded
Verification: TEST-XXX-NNN
```

## Acceptance test

```text
TEST-XXX-NNN
Linked requirement: REQ-XXX-NNN
Type: Automated | Manual
Command or steps: <exact command, or numbered steps>
Expected result: <what PASS looks like>
Status: Planned | Implemented
```

## Feature

```text
FEAT-NNN
Name: <short name>
Description: <what the user can do>
Status: Current | Planned | Removed | Superseded
Preserve: Yes | No
Verification: TEST-XXX-NNN
```

## Risk, debt, decision, question

```text
RISK-NNN      Risk: <what could go wrong> | Likelihood | Impact | Mitigation | Owner
DEBT-NNN      Debt: <shortcut taken> | Why | Cost if left | Plan to repay
DECISION-NNN  Decision: <what was decided> | Options considered | Why | Date | Revisit when
QUESTION-NNN  Question: <what is unknown> | Blocks | Who answers | Due
```

## Limitation

```text
LIMIT-NNN
Title: <short title>
Description: <what does not work or was not tested>
Impact: <who is affected, workaround>
Status: Current | Resolved
```
