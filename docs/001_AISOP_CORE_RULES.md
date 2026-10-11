---
document_id: DOC-001
title: "AISOP Core Rules (the Card)"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-001
normative_status: Normative
tier: 0
summary: "The AISOP card: what AISOP is, the core rules, the minimum package, ID discipline, and the fifteen-field delivery report."
source: "REV-003 Phase 1; distilled from docs/020, 050, 060, 070, 080 and 165"
---

# AISOP Core Rules

AISOP is a set of working rules for building software with an AI assistant without losing features, decisions, or context between sessions. Its central habit: the project's memory lives in files (a *package*) that carry their own requirements, feature list, tests, and history, so any person or AI can pick the work up cold. This card is the smallest form of AISOP: give it to any chat AI as its operating rules.

## The loop

```text
idea -> concept brief -> plan -> prototype -> freeze baseline -> package -> review
  ^                                                                         |
  +------- the next run starts from the package, never from memory ---------+
```

## Core rules

<!-- AISOP:RULES:BEGIN -->
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
14. **Report every delivery.** End each substantial reply with the fifteen-field report below and name the AISOP version you follow.
<!-- AISOP:RULES:END -->

## Minimum package

```text
yyyymmdd_00_short-description/
  README_START_HERE.md     what it is, how to run it, how to test it
  CHANGELOG.md             what changed, newest first
  FEATURE_INVENTORY.md     FEAT-001 ... what exists and must not be lost
  ACCEPTANCE_TEST_PLAN.md  TEST-... how each requirement is checked
  KNOWN_LIMITATIONS.md     what does not work yet
  main_script.py           supports --version, --smoke-test, --diagnostics
```

## IDs

A requirement is `REQ-<AREA>-<NNN>` (for example `REQ-UI-001`), a feature `FEAT-<NNN>`, and an acceptance test `TEST-<AREA>-<NNN>` that names the requirement it checks. Risks, debts, decisions and open questions use `RISK-`, `DEBT-`, `DECISION-` and `QUESTION-`. An ID is never reused: a changed requirement keeps its ID with new text, and a retired one is marked Superseded.

## Final package report (fifteen fields)

The same fields as `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` (chat kit edition), which adds guidance for each.

```text
Package:
Internal folder:
Based on:
Purpose:
Changed files:
Unchanged important files:
Tests run:
Test results:
Known limitations:
Risks:
Debt added:
Debt resolved:
Feature removals:
Broad refactor performed? yes/no:
Next recommended step:
```

## Using the card

Paste this card into your chat's custom instructions or first message, then send:

<!-- GENERATED:BEGIN card-opener | by tools/build_editions.py from config/editions.json; edit the source, not this region -->
> Use the AISOP card above as your operating rules. Reply with the AISOP version it names and the word ORIENT, then ask me for my idea.
<!-- GENERATED:END card-opener -->

Then describe your idea in a few sentences. The Chat Kit adds a beginner's guide, glossary, templates, and a worked example; the Method Kit adds the full method and audit tools for agentic coding tools. Both are on the project's releases page.

Words used here: a *feature inventory* is the list of everything the software does now that must not be lost; a *CHANGELOG entry* is a dated note of what changed and why; a *package skeleton* is the minimum folder shown above.
