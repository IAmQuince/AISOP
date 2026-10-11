---
document_id: DOC-000-README
title: "AISOP: Start Here"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
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
- **Chat Kit** (folder `20260516_00_seed_chatkit/`, or a git clone for Full): "I have uploaded the AISOP Chat Kit. Read EDITION_INFO.md, then README_START_HERE.md, then the card. Work in ORIENT or APPLY mode only and never ask for a file that EDITION_INFO.md does not list. Reply with: the AISOP version and package_id, the files you can see, the word ORIENT, and the question 'what is your idea?'."
- **Method Kit** (folder `20260516_00_seed_method/`, or a git clone for Full): "Read AGENTS.md and follow its first-five-minutes protocol."
- **Full** (folder `20260516_00_seed/`, or a git clone for Full): "Read AGENTS.md and follow its first-five-minutes protocol."
<!-- GENERATED:END openers -->

## Reading order

1. `docs/001_AISOP_CORE_RULES.md`: the card, the rules on one page.
2. `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md`: if you are new to AI coding.
3. `docs/020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md`: what the AI follows.
4. `templates/README.md`: which template to use at each stage.
5. `examples/hello_aisop/README_START_HERE.md`: a complete small package.
6. `AGENTS.md`: the entry file for coding agents (method edition).
7. `docs/005_PRODUCT_REQUIREMENTS.md` with `FEATURE_INVENTORY.md`, `ACCEPTANCE_TEST_PLAN.md`, and `CHANGELOG.md`: this package's own requirements and history (method edition).
8. `docs/000_DOCUMENTATION_INDEX.md`: every document by tier (method edition).

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
