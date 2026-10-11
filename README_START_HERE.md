---
document_id: DOC-000-README
title: "AISOP: Start Here"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-000-README
normative_status: Informative
tier: 1
summary: "First file to read in any AISOP edition: which edition you hold, the reading order, the package rules, and how to check the package."
source: "Generalized AI-assisted coding SOP source text"
---

# AISOP: Start Here

AISOP is a set of working procedures for building software with an AI assistant without losing features or context between sessions. This package is structured the way it recommends your own packages to be: intake documents, machine-referenceable requirements, a feature inventory, acceptance tests, and audit tools.

## Which edition am I holding?

- If `EDITION_INFO.md` sits next to this file, it names your edition, gives its reading order, and lists every file it contains.
- If there is no `EDITION_INFO.md`, you have a clone of the repository: the Full edition.

The first message to give your AI, per edition:

<!-- GENERATED:BEGIN openers | by tools/build_editions.py from config/editions.json; edit the source, not this region -->
- **Chat Kit** (folder `20261011_00_aisop_chatkit/`): "I have uploaded the AISOP Chat Kit. Read EDITION_INFO.md, then README_START_HERE.md, then the card. Work in ORIENT or APPLY mode only and never ask for a file that EDITION_INFO.md does not list. Reply with: the AISOP version and package_id, the files you can see, the word ORIENT, and the question 'what is your idea?'."
- **Method Kit** (folder `20261011_00_aisop_method/`): "Read AGENTS.md and follow its first-five-minutes protocol."
- **Full** (folder `20261011_00_aisop/`, or a git clone): "Read AGENTS.md and follow its first-five-minutes protocol."
<!-- GENERATED:END openers -->

## Reading order

<!-- GENERATED:BEGIN reading-order | by tools/build_editions.py from entry_read_order in config/editions.json and document summaries; edit the source, not this region -->
1. `AGENTS.md`: Entry file for coding agents: what is binding, the first-five-minutes protocol, modes and reading sets, hard rules, and the delivery shape (method edition).
2. `docs/001_AISOP_CORE_RULES.md`: The AISOP card: what AISOP is, the core rules, the minimum package, ID discipline, and the fifteen-field delivery report.
3. `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md`: For people new to AI coding: chat versus agent, why files beat memory, which edition to pick, and a five-step first project with checks.
4. `docs/020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md`: Operating instructions for the AI assistant: collaboration style, coding principles, feature preservation, diagnostics, delivery.
5. `templates/README.md`: Which template to use at each stage of a project, and what each one is for.
6. `examples/hello_aisop/README_START_HERE.md`: Start here: what hello_aisop does, how to run and test it, and what must not break.
7. `docs/050_MONOLITHIC_PROTOTYPE_CODE_SOP.md`: SOP for a single-file prototype that stays disciplined: numbered sections, --smoke-test, --diagnostics, safe state.
8. `docs/003_GLOSSARY.md`: Short definitions of AISOP's terms, modes, header fields, and every ID family used in tiers 0-2.
9. `docs/004_EDITIONS_AND_UPGRADE_PATH.md`: The four AISOP editions, their sizes and openers, what each adds, and how zips, releases, and the repository relate.
10. `docs/005_PRODUCT_REQUIREMENTS.md`: The authoritative list of REQ-* requirements for this package; the only requirements source besides the JSON catalog (method edition).
11. `docs/000_DOCUMENTATION_INDEX.md`: Generated map of every AISOP document by tier, with status, size class, and a one-line summary (method edition).
<!-- GENERATED:END reading-order -->

## Package rules

- The zip filename and the internal top-level folder name match.
- Every Markdown document carries a document-control header.
- Requirements use stable `REQ-*` IDs, features `FEAT-*`, acceptance tests `TEST-*`, each test linked to a requirement.
- No ID is renumbered or deleted; retired items are marked Superseded.
- Wording stays general; nothing personal is committed (a local `USER_PROFILE.md` stays on your machine).

## Checking this package

These commands come with the Method Kit and the Full edition (method edition): `python tools/run_all_audits.py --quiet` runs every audit, and `python tools/build_editions.py --check` confirms the generated files and edition budgets. Reports are written to `reports/`.

To check your own package, copy `tools/aisop_check.py` into it and run `python tools/aisop_check.py --root .`; without Python, use `templates/MANUAL_AUDIT_CHECKLIST.md`.

## Status

Draft reference package (see the `status` field in the header), not a finished product. The practice-space idea, repository bootstrap, and release handoff are described in `docs/080`, `docs/090`, and `docs/100` (method edition).
