---
document_id: DOC-AGENTS
title: "AGENTS.md: AISOP Agent Entry File"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-AGENTS
normative_status: Normative
tier: 2
summary: "Entry file for coding agents: what is binding, the first-five-minutes protocol, modes and reading sets, hard rules, and the delivery shape."
source: "REV-003 Phase 1 (docs/300 section 8); replaces the Phase 0 interim file"
---

# AGENTS.md

## 1. Identity

This file is Normative: it binds any agent working in this tree. Two regions are GENERATED; edit their sources (`docs/001_AISOP_CORE_RULES.md`, `config/editions.json`), never the regions. The package identity and version are in the header above.

## 2. What this repository is

AISOP is a self-describing package of procedures for AI-assisted software work: plan, prototype, package, review, and hand off without losing features or context. It travels two ways: as zip packages traded between people and tools, and as a git repository. You hold either the Full tree or the Method Kit; `EDITION_INFO.md`, when present, says which.

## 3. Normative vs informative

*Normative* means binding on anyone modifying this package (procedure or policy). Only `docs/005_PRODUCT_REQUIREMENTS.md` and `requirements/requirements_catalog.json` define `REQ-*` requirements; a Normative header never makes a document a requirements source. *Informative* means reference: when this file routes you to an Informative SOP for a step, follow that SOP's steps for that step, and `docs/001` and `docs/005` win on conflict.
Domain guides are informative reference, never requirements: `docs/010`, `docs/055` and `docs/170-290` (full edition).

## 4. Core rules

<!-- GENERATED:BEGIN rules | by tools/build_editions.py from docs/001_AISOP_CORE_RULES.md; edit the source, not this region -->
1. **Files, not memory.** Work from the actual current files. Ask for them or inspect them before changing anything; never rewrite from memory.
2. **Inventory before change.** Before changing code, list the current features. Never remove or weaken a feature unless the user explicitly approves.
3. **Small, gated steps.** Make the smallest change that moves one step forward, with a stated way to check it. No broad rewrites unless asked.
4. **Freeze before refactor.** Keep a runnable baseline. Keep public interfaces stable or add compatibility shims.
5. **Evidence over claims.** State assumptions and uncertainty. Say what was not tested. Never invent results.
6. **Diagnostics ship with code.** Every serious change comes with a smoke test or diagnostic the user can run and paste back.
7. **Complete deliverables.** Deliver complete files, not fragments, and a CHANGELOG entry for every change.
8. **Stable IDs.** Requirements, features and tests get IDs (`REQ-`, `FEAT-`, `TEST-`). Never renumber or delete an ID; mark it Superseded.
9. **Current headers.** When you change a controlled document, update its revision and last-updated date.
10. **Matching names.** Packages are named `yyyymmdd_00_short-description`; a zip's name equals its top-level folder.
11. **Respect the target.** Confirm the language version, operating system and libraries before writing code; never assume modern defaults.
12. **Safe by default.** Anything that drives hardware starts safe, fails safe, and never acts automatically at startup.
13. **Gate the phases.** Concept, plan, prototype, package: move on only when the current phase's check passes.
14. **Report every delivery.** End each substantial reply with the fifteen-field final package report and name the AISOP version you follow.
<!-- GENERATED:END rules -->

## 5. First-five-minutes protocol

1. This file is loaded; note the package_id and version in its header.
2. Run `python tools/run_all_audits.py --quiet`; it writes only git-ignored `reports/*.txt` and temporary copies outside the tree, so it is safe in every mode. PASS: trust the tree. FAIL: report the failing tool verbatim and stop structural work; a red audit on a fresh copy is a bug to report, not to work around. If you cannot run commands, say so, apply `templates/MANUAL_AUDIT_CHECKLIST.md` by hand, and do not claim the tree is audited.
3. Read `README_START_HERE.md`, then the leading tier 0-1 records of `docs/index.json` (they come first).
4. Choose the mode (section 6), load its reading set, and read `USER_PROFILE.md` if it exists.
5. Report back: AISOP version loaded; audit result (or "could not run"); mode; the normative rule (section 3) in one sentence; files read; files intentionally not read; first proposed acceptance-gated step.

## 6. Modes and reading sets

Choose the mode by what the task will change, and state it in one sentence before touching files.

- **ORIENT**: nothing changes (orientation, questions, review). No reading beyond section 5.
- **APPLY**: files outside this tree change (the user's own project). Read `docs/020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md`, then only the one template for the current stage (table below; also in `templates/README.md`), and its SOP only when you reach that stage.
- **MODIFY-AISOP**: files inside this tree change. Read `docs/165`, `docs/160`, `docs/166`, `docs/120`. Run `python tools/build_editions.py --check` and the audits before delivering; update CHANGELOG, FEATURE_INVENTORY, requirements, and traceability when behaviour changes.
- **DOMAIN-LOOKUP** is additive: append it to any mode when the task needs a domain guide, and report it as "APPLY + DOMAIN-LOOKUP (docs/185)". Read the index summaries first, open exactly one guide, TL;DR first (full edition).

| Stage | Single template | SOP opened only at that stage |
|---|---|---|
| concept | `templates/CONCEPT_BRIEF_TEMPLATE.md` | `docs/030` |
| plan | `templates/PLANNING_DOCUMENT_TEMPLATE.md` | `docs/040` |
| prototype | `examples/hello_aisop/hello_aisop.py` as the pattern | `docs/050` |
| migrate | `templates/AGENT_HANDOFF_BUNDLE_TEMPLATE.md` | `docs/060` |
| package | `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` | `docs/070` |

## 7. Commands

<!-- GENERATED:BEGIN commands | by tools/build_editions.py from config/editions.json; edit the source, not this region -->
- `python tools/run_all_audits.py --quiet`: every audit; prints the SUMMARY block (drop --quiet for full output).
- `python tools/build_editions.py --check`: generated files fresh, edition budgets, links inside each edition.
- `python tools/build_editions.py all`: regenerate every generated file and region (then rerun the audits).
- `python tools/release_package.py --dry-run`: release naming check without writing a zip.
<!-- GENERATED:END commands -->

## 8. Hard rules

- Never hand-edit a GENERATED region or file; edit its named source, then run `python tools/build_editions.py all`.
- Never delete or renumber a `REQ-*`, `FEAT-*`, or `TEST-*` ID; mark it Superseded.
- Bump `revision` and `last_updated` in the header of every controlled document you change.
- Keep tooling Python standard library only.
- Every new document's header is complete, including `tier` and `summary`.
- A zip's basename equals its internal root folder.
- Never read `docs/185` or `docs/195` (over 60 KB each) in full unless asked (full edition).

## 9. User profile

If `USER_PROFILE.md` exists at the root, read it. Otherwise, in APPLY only, ask the six questions in `templates/USER_PROFILE_TEMPLATE.md` before planning code.

## 10. Delivery

End every substantial task with the fifteen-field final package report (`templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`), the `python tools/run_all_audits.py --quiet` result, and, when code changed, the diagnostic command the user can run and paste back. Deliver a zip only when the user asked for a handoff (`docs/070_ZIP_PACKAGE_REVIEW_AND_HANDOFF_SOP.md`).
