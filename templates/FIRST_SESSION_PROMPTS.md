---
document_id: DOC-TPL-PROMPTS
title: "First Session Prompts"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-TPL-PROMPTS
normative_status: Informative
tier: 1
summary: "Three prompts to copy for a first project: plan this, prototype this, package and report."
source: "REV-003 Phase 2 template"
---

# First Session Prompts

Copy one prompt at a time and replace the `<...>` parts. Each step is in `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md`.

## 1. Plan this

```text
Follow the AISOP rules you were given. My idea: <one or two sentences>.
Ask me up to five questions about users, target computer, and must-have
features. Then write a Concept Brief Lite using
CONCEPT_BRIEF_TEMPLATE.md, and list the must-have features with FEAT IDs (FEAT- plus a three-digit
number, starting at 001). Do not write code yet.
```

## 2. Prototype this

```text
Using the concept brief above, write one Python file in the numbered
sections of docs/050, like examples/hello_aisop/hello_aisop.py. It must
support --version, --smoke-test and --diagnostics. Target: <computer,
operating system, Python version>. Standard library only unless I agree.
Give me the complete file and the exact commands to run it.
```

## 3. Package and report

```text
Turn this into a package named <yyyymmdd>_00_<short_name> with
README_START_HERE.md, CHANGELOG.md, FEATURE_INVENTORY.md,
ACCEPTANCE_TEST_PLAN.md and KNOWN_LIMITATIONS.md (use the templates).
Then give me the fifteen-field final package report.
```
