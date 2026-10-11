---
document_id: DOC-003
title: "Glossary"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-003
normative_status: Informative
tier: 1
summary: "Short definitions of AISOP's terms, modes, header fields, and every ID family used in tiers 0-2."
source: "REV-003 Phase 2 (docs/300 section 9.1)"
---

# Glossary

## Terms

- **Acceptance gate**: a check that must pass before work moves to the next step or phase.
- **Card**: `docs/001_AISOP_CORE_RULES.md`, the one-page rules any chat AI can follow.
- **Context window**: the AI's working memory for one conversation; it is lost when the chat ends.
- **Diagnostic harness**: a command (often `--diagnostics`) that prints a report you can paste back to the AI.
- **Document-control header**: the `---` block at the top of a document with its ID, version, and status.
- **Drift**: documents, code, and tools slowly disagreeing with each other.
- **Edition**: one of AISOP's four deliveries: Card, Chat Kit, Method Kit, Full.
- **Edition marker**: "(method edition)" on a line means the file it cites ships from that edition upward.
- **Feature inventory**: the list of everything the software does now that must not be lost.
- **GENERATED region**: text written by a tool from a named source; edit the source, never the region.
- **Golden baseline**: a frozen, runnable version used to prove later changes lost nothing.
- **Handoff bundle**: what you give an AI before it changes a package (`templates/AGENT_HANDOFF_BUNDLE_TEMPLATE.md`).
- **Informative**: reference material; it guides but does not bind.
- **Intake document**: one of the five files every package starts with: README_START_HERE, CHANGELOG, FEATURE_INVENTORY, ACCEPTANCE_TEST_PLAN, KNOWN_LIMITATIONS.
- **Mode**: what the AI may change in a session: ORIENT, APPLY, MODIFY-AISOP, plus DOMAIN-LOOKUP.
- **ORIENT**: look and explain; change nothing.
- **APPLY**: use AISOP on your own project.
- **MODIFY-AISOP**: change AISOP itself (Method Kit and above).
- **DOMAIN-LOOKUP**: read one domain guide for a task; added to another mode.
- **Monolithic prototype**: a first working program in one file, with numbered sections that can be split later.
- **Normative**: binding on anyone changing the package.
- **package_id**: a package's name and identity, `yyyymmdd_00_short-description`; the zip and its top folder use it.
- **Practice space**: the repository as a place to try and compare ways of working, one branch per practice.
- **Smoke test**: a quick self-check (`--smoke-test`) that ends with `SUMMARY: PASS` or `FAIL`.
- **System prompt / custom instructions**: standing instructions a chat product sends with every message; the card fits there.
- **Tier**: the lowest edition a document belongs to (0 Card, 1 Chat Kit, 2 Method Kit, 3 Full).

## Header fields

`document_id` stable document ID; `title`; `version` package version; `revision` program revision (REV-); `status`; `last_updated` date of the last change; `package_id`; `machine_reference_prefix` prefix for references into the document; `normative_status` Normative or Informative; `tier`; `summary` one line; `topics` (domain guides); `source` where the text came from; `derived_from` the document a template comes from; `package_role` set to example in example packages.

## ID families

| ID | Means | Where |
|---|---|---|
| `REQ-` | requirement | `docs/005` (method edition), `ID_RECORD_FORMATS` |
| `FEAT-` | feature | feature inventory |
| `TEST-` | acceptance test | acceptance test plan |
| `CHECK-` | lite-audit check | `tools/aisop_check.py` |
| `DOC-` | document ID | every header |
| `REV-` | revision of the package or program | headers, changelog |
| `LIMIT-` | known limitation | known limitations |
| `RISK-` | risk | risk register |
| `DEBT-` | technical debt | debt register |
| `DECISION-` | decision | decision log |
| `REJECTED-` | rejected option in a decision log | `docs/040` (method edition) |
| `QUESTION-` | open question | open questions |
| `GOAL-` | goal | planning documents |
| `PRIN-` | design principle | planning documents |
| `DRIFT-` | known drift to fix | `docs/300` drift register (full edition) |
| `GATE-` | phase gate | planning documents |
| `PHASE-` | implementation phase | planning documents |
| `RUN-` | one work run | workplan |
| `EXEC-` | execution note | workplan |
| `WORKFLOW-` | user workflow | planning documents |
| `DATA-` | data item or entity | planning documents |
| `UI-` | interface element | planning documents |
| `MODULE-` | planned module | planning documents |
| `IFACE-` | frozen public interface | `docs/040`, `docs/060` (method edition) |
| `SAFE-` | safety class (`SAFE-CLASS-0` to `4`) | `SAFETY.md` |
| `RULE-` | rule inside a domain guide, by area (`RULE-GUI-`, `RULE-LJ-`, ...) | domain guides (full edition) |
| `LESSON-` | compatibility lesson | `docs/170` (full edition) |
| `ACCEPT-` | acceptance item inside a domain guide; method documents use `TEST-` | domain guides (full edition) |

Domain guides keep their own local ID families; each guide lists them in the `topics` of its header (and so in `docs/index.json`, method edition).
