---
document_id: DOC-300
title: "AISOP Expansion Gameplan (REV-003): Tiered Editions and Agent-First Entry"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-300
normative_status: Informative
tier: 3
summary: "Planning record for REV-003: tiered editions from one tree, agent-first entry, beginner on-ramp, and release flow."
topics: [planning, editions, roadmap]
source: "REV-003 planning run: corpus audit of all reference documents, three judged architecture proposals, and a five-lens adversarial review of the draft"
---

# AISOP Expansion Gameplan (REV-003)

## 0. Document Control

| Field | Value |
|---|---|
| Status | Proposed. Nothing in this plan is implemented yet. |
| Decision owner | Repository maintainer |
| Shape | Adapted from `docs/040_MONOLITHIC_PLANNING_DOCUMENT_SOP.md`: one planning document now, with an extraction plan (section 17) naming which sections later become SOPs, config, and tools. Sections 2, 13, 14 and 17 map to 040's Executive Summary, Risk Register, Decision Log plus Open Questions, and Extraction Plan. |
| Revision counter | This document's `revision` counts its own content changes (REV-001 draft, REV-002 after review) and is independent of the program name "REV-003". |
| How it was produced | (1) Every document under `docs/` was read in full and classified for audience, tier placement, reusable templates, stale or personal content, and agent-facing rules. (2) Three independent architecture proposals were written from a beginner-first, an agent-first, and a maintainer-first lens. (3) Three independent judges scored all proposals; the maintainer-first skeleton won unanimously and the beginner and agent conveniences that cost files rather than mechanisms were grafted onto it. (4) The resulting draft was reviewed by five adversarial critics (beginner, agent operator, maintainer, fact-checker, completeness) whose serious findings were each challenged by an independent skeptic; the confirmed findings are folded into this revision. |
| Normative weight | Informative until the owner approves it; approved items then land as `REQ-*` / `FEAT-*` / `TEST-*` entries in the controlled documents (section 12). |
| Supersedes | The "Next Recommended Run" paragraph in `WORKPLAN_CURRENT_RUN.md`. |

## 1. Executive Summary

AISOP already contains the method. What it lacks is a way in that matches the reader's tooling. This plan turns the single repository into **one source tree that produces four editions**, each matched to a context budget and a kind of user, without ever maintaining a second copy of any document:

```text
Tier 0  CARD        one file, <= 8 KB    paste into any chat                   (free / limited plans)
Tier 1  CHAT KIT    zip, <= 120 KB       upload into a chat session            (chat-only plans)
Tier 2  METHOD KIT  zip, <= 400 KB       full method + tools, no domain guides (agentic tools, lean)
Tier 3  FULL        git clone / zip      everything, navigated by map          (agentic tools, maintainers)
```

Membership is one integer in the document-control header every file already carries (`tier:`), budgets and openers live in one JSON file, and a single standard-library script builds the editions and refuses to build if anything drifted. An agent pointed at the repository URL auto-loads an `AGENTS.md` under 8 KB that states what is normative, what to read first, which mode it is in, and how to report; Claude Code and Gemini CLI reach the same file through a pointer, and tools that read `AGENTS.md` natively need nothing else.

The work is six phases. **Phase 0, in five independently mergeable slices, makes the existing audits green and gives agents a landing file.** Phases 0 and 1 together already deliver the owner's core ask: a link that an agent can be handed. Phases 2 to 5 add the beginner on-ramp, the release flow, cold-agent validation, and the optional domain packs.

## 2. Goals and Non-Goals

### 2.1 Goals (owner's statement, restated as outcomes)

| ID | Goal | Measured by |
|---|---|---|
| GOAL-001 | Multiple avenues into AISOP: a zip for lower-tier chat subscriptions and a structured local folder for higher-tier agentic subscriptions. | Four editions built from one tree, each within its budget, each with its own start-here file and opener. |
| GOAL-002 | AISOP serves people who are just beginning with AI agents. | The scripted cold-chat session (GATE-2) completes steps 1-3 of the beginner path with zero interventions, using only the Chat Kit and its opener. |
| GOAL-003 | Handing someone the repository link is enough for their agent to get up to speed quickly. | TEST-ENTRY-004: a cold agent given only the URL reaches a running audit and states the normative rule correctly in at most six tool calls (defined in Phase 1, first run in one tool; two tools and a per-release cadence from Phase 4). |
| GOAL-004 | The package keeps demonstrating the discipline it teaches. | Every new rule lands as REQ/FEAT/TEST with a traceability row; `run_all_audits.py` passes on a fresh clone of any folder name. |

### 2.2 Non-goals for REV-003

- No editorial rewrite of the ~500 KB of domain technical guides (docs/170-290). They receive header keys, a TL;DR, fence repair, and the removal of chat residue only.
- No new dependencies. Build and audit tooling stays Python standard library; CI plumbing may use a GitHub Action to attach release assets, with a documented manual fallback.
- No second repository, no branch per edition, no wiki as a source of truth.
- No renumbering of existing `docs/NNN` files and no deletion of existing REQ/FEAT/TEST IDs.

## 3. Current Baseline

### 3.1 What exists

- ~28,000 lines of Markdown (~750 KB of prose; the 2.3 MB repository size includes `.git` and reports). Every document carries a nine-key document-control header. Requirements, features, and tests use `REQ-*`, `FEAT-*`, `TEST-*` IDs tied together by a traceability matrix and a JSON catalog (22 requirements, 19 features, 22 tests). Twenty-four documents carry `normative_status: Normative` (`docs/005`, the ten governance SOPs `080-165`, and thirteen root files); the core-method SOPs `020-070` and the domain guides are Informative.
- Core method: `docs/020-070` (operating instructions, concept brief, planning document SOP, prototype SOP and example, migration SOP, zip review and handoff SOP). Governance: `docs/080-165` (ten short SOPs). Domain reference: `docs/010` and `docs/170-290` (fifteen long guides on Windows setup, compatibility, DAQ, QC, embedded platforms, pygame, MIDI, LabJack, I2C, Android, networking, GUI design).
- Stdlib tooling: eight audit/release scripts under `tools/` (archive name, manifest, package structure, release, repo health, requirements trace, run-all, secret scan), one smoke test, CI that runs `tools/run_all_audits.py`.
- GitHub state: default branch `master`; no tags, no releases, no issues; two open Dependabot pull requests (#4, #5) whose `audit` check is red because of DRIFT-001 below.

### 3.2 Drift register (verified by running the audits on this clone)

| ID | Drift | Effect today |
|---|---|---|
| DRIFT-001 | `LICENSE_DECISION_REQUIRED.md` was deleted and MIT `LICENSE.txt` added, but the literal filename or the gate it describes survives in `tools/package_structure_audit.py`, `tools/repo_health_audit.py`, `config/package_metadata.json`, `docs/005` (REQ-LIC-001), `ACCEPTANCE_TEST_PLAN.md` (TEST-LIC-001), `REQUIREMENTS_TRACEABILITY_MATRIX.md`, `PACKAGE_MANIFEST.md`, `README.md`, `docs/140` (L41), `KNOWN_LIMITATIONS.md` (prose: "includes a license decision gate"), and three committed `reports/*.txt`. | `run_all_audits.py` FAILS on every clone and every PR. |
| DRIFT-002 | `tools/release_package.py` hard-codes the expected root folder `20260516_00_seed`; a GitHub clone is named `AISOP`. | Release dry run FAILS in any clone. |
| DRIFT-003 | `.github/workflows/ci.yml` triggers on push to `main`; the default branch is `master`. (`package_audit.yml` and `release_dry_run.yml` are manual-only today, which is not a defect.) | CI never runs on pushes to the default branch (only on PRs). |
| DRIFT-004 | Seven `reports/*.txt` are committed and rewritten with a new timestamp on every audit run. `PACKAGE_MANIFEST.md` is also stale (hashes for three files changed by the commit that added this plan, and a row for the deleted license file) because nothing verifies it. | Every audit run dirties the tree; agents and contributors commit noise; the manifest silently lags. |
| DRIFT-005 | `docs/020` is a lightly cleaned personal system prompt: it describes one specific person in the third person and states personal preferences (UI colour scheme, legacy-target defaults) as universal rules, while its own line 16 claims to be project-neutral. | Contradicts the beginner audience; the personal-reference scan only catches names. |
| DRIFT-006 | No agent-native entry file exists (`AGENTS.md`, `CLAUDE.md`, or equivalent). | An agent handed the link has no deterministic first file. |
| DRIFT-007 | Seven long documents have an unclosed code fence near the top (`060` L145, `170` L78, `180` L107, `185` L54, `190` L70, `195` L47, `200` L47), so roughly 86-98% of each renders as one code block on GitHub and inside chat uploads. Each of the seven contains exactly one fence line: the source conversion lost every other fence, so the domain guides (`170-195`) hold hundreds of lines of unfenced code that a single closing fence will not make readable. Most long docs also end with an orphan line that is the heading of the next document in the original source, plus leftover chat-reply fragments. | The largest single barrier to the chat-upload avenue; models read these files as code, not prose. |
| DRIFT-008 | The method documents disagree with each other and with the repository on names: three different package-report formats (`020` ten items, `070` section 18 fifteen items, `070` section 21 checklist), `FEATURE-nnn` vs `FEAT-*`, `ACCEPT-nnn` vs `TEST-*`, `tools/package_smoke_test.py` and `tools/diagnostic_harness.py` (do not exist) vs `tests/smoke_test.py`, `test_reports/` vs `reports/`, `project/logging.py` (shadows the stdlib) vs `logging_utils.py`, four sentences in `docs/270` corrupted by citation-tool residue, a real `os.rename` Windows bug in `docs/055`, and a per-project `docs/` numbering that reuses AISOP's own numbers with different meanings. | An agent following one SOP emits IDs and filenames the audits do not recognise. |

### 3.3 Corpus classification (summary; full table in section 10)

- **Must-read for an agent applying AISOP to a new project:** `020`, `030`, `040`, `050`, `060`, `070` (and the governance SOPs when modifying AISOP itself).
- **Starter-worthy but long:** `030` (658 lines), `040` (855), `060` (1098), `070` (812) are forms and checklists interleaved with worked examples from one legacy project. Their reusable skeletons (about sixty distinct templates were identified) are what a beginner actually needs.
- **Domain packs, never in the lower tiers:** `010`, `170-290`. They group naturally into seven packs (section 10.3).
- **Genuinely short core docs that already fit a chat kit:** `050` (10.7 KB) and a generalized `020` (~12 KB).

## 4. Design Principles

| ID | Principle | Consequence |
|---|---|---|
| PRIN-001 | One tree. A fact is edited in exactly one place. | No condensed copies, no `docs-lite/`, no branch per edition. Budgets, openers and fixed file lists live only in `config/editions.json`; where a hand-written document must show them, it shows a GENERATED region. |
| PRIN-002 | File-granular tiers. A document is in an edition or it is not. | No section-level transclusion markers inside normative prose (the judges identified markers as the most likely future drift source). Short tiers come from short documents. |
| PRIN-003 | Generated means checked. Every generated file or region is produced by a stdlib script with a `--check` mode that `run_all_audits.py` and CI run. | Hand-editing a generated file turns CI red with a message naming the source to edit. This includes `PACKAGE_MANIFEST.md`, which today has no check. |
| PRIN-004 | Byte budgets are the enforced truth; token counts are estimates. | Budgets in `config/editions.json`; the audit WARNs at 75% and FAILs at 100%, listing the largest offenders. Policy: raise the tier of a document, not the budget; a budget change needs a CHANGELOG entry and a changed acceptance text. |
| PRIN-005 | Normative vs informative is defined once and stated to agents. | *Normative* = binding on anyone modifying this package (procedure or policy). Only `docs/005` and `requirements_catalog.json` define `REQ-*` requirements; a Normative header never makes a document a requirements source. *Informative* = reference; when `AGENTS.md` routes an agent to an Informative SOP for a step, the agent follows that SOP's steps for that step, and `docs/001` and `docs/005` win on conflict. Domain guides are informative, never requirements. |
| PRIN-006 | Both avenues stay first-class. | Every release ships zips whose basename equals the internal root; the clone folder name is a working-copy convention and the package_id is the handoff identity. |
| PRIN-007 | Every new rule is traceable. | New behaviour = REQ + FEAT + TEST + matrix row, in the same change. |
| PRIN-008 | Gates are maintainer-runnable. | No acceptance gate depends on outside volunteers; dogfood sessions are owner-run, scripted, and logged under `reports/baseline/`. |
| PRIN-009 | Nothing is deleted, only superseded. | IDs are marked Superseded/Rejected; `docs/NNN` numbers never change; superseded planning documents move to tier 3. |
| PRIN-010 | One check, one owner. | Each audit rule is implemented in exactly one tool (ownership table in section 7.4); two tools never test the same thing. |

## 5. The Four Editions

### 5.1 Edition table

| Tier | Name | Audience | Delivery form | Hard budget | Contents (cumulative) | How a human starts | How the AI enters |
|---|---|---|---|---|---|---|---|
| 0 | **Card** | Anyone with any chat product, including free tiers and custom-instruction boxes; also the rules block every agent entry embeds. | `AISOP_CARD.md` (release asset, rendered from `docs/001_AISOP_CORE_RULES.md`); also shown in README under "copy this". | 8,192 bytes for the card; its rules block <= 4,096 bytes so `AGENTS.md` has room (section 8.1). | What AISOP is (three sentences); the practice-space loop in one diagram; the core rules (about twelve, imperative); the minimum package skeleton and the naming rule; the ID discipline in one paragraph; the delivery report's fifteen field labels inline (about 300 bytes) with the sentence "the full template is `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` (Chat Kit and above)"; a two-line "words used here" footnote (feature inventory, CHANGELOG entry, package skeleton); the card-only opener; where the next tier is. | Copy the card into the chat's system prompt or first message, then type the card-only opener and describe the idea. No download, no Python. | The chat model receives the card as instructions; it must ask for or inspect current files, produce a feature inventory before changing code, deliver complete files plus a CHANGELOG entry, end with the fifteen-field report, and name the AISOP version it follows. |
| 1 | **Chat Kit** | Chat-only subscriptions with upload but no filesystem or shell; beginners who want prompts and templates rather than tooling. | `<package_id>_chatkit.zip` on every release, unpacking to `<package_id>_chatkit/`; also usable as a flat set of individually uploaded files (unique basenames, `max_files` budget). | 122,880 bytes of text; per-item caps in section 9; projected ~102 KB (section 9.6). | Card; `README_START_HERE.md` (edition-aware); `docs/002` beginners guide; `docs/003` glossary; `docs/004` editions and upgrade path; generalized `docs/020`; `docs/050`; `templates/` (section 9.2); `examples/hello_aisop/` (section 9.3); `tools/aisop_check.py`; `LICENSE.txt`, `NOTICE.md`; generated `EDITION_INFO.md` (exact file list, this edition's reading order, the opener, "there are no audit tools to run in this edition"). Deliberately excludes AISOP's own `CHANGELOG.md` and `KNOWN_LIMITATIONS.md` (they describe this package, not the user's) and `docs/000_USER_GUIDE_OVERVIEW.md` (tier 2). | Download the zip from the latest release, upload it (or its files), paste the Chat Kit opener (section 9.4), then use the "plan this" prompt from `templates/FIRST_SESSION_PROMPTS.md`. | Reads `EDITION_INFO.md` first (so it never asks for a file the kit lacks), then `README_START_HERE.md`, then the card; replies with the acknowledgment the opener demands (version, package_id, files seen, the word ORIENT or APPLY, "what is your idea?"). Operates in ORIENT or APPLY only; `EDITION_INFO.md` says MODIFY-AISOP needs the Method Kit. |
| 2 | **Method Kit** | Agentic tools (Claude Code, Codex CLI, Cursor, Copilot agents, Gemini CLI) with a filesystem; practitioners who want the full method and audit tooling but not ~500 KB of domain guides; offline reviewers. | `<package_id>_method.zip` on every release, unpacking to `<package_id>_method/`; or the clone with tier-3 files ignored. | 409,600 bytes of all shipped files. Measured on commit `d112f2a`: ~253 KB on the revised contents below (257,624 bytes of root files, `docs/000-165` without `010`, `055` and `300`, tools, tests, requirements, config, `.github`, `src/README.md`, `reports/README.md`, minus `reports/baseline/`); projected ~350 KB (85%) after Phase 2 (section 9.6). DECISION-014 covers the case where the projection is exceeded. | Everything in tier 1; all root intake and governance files; `docs/000-070` in full except `010` and `055` (tier 3); `docs/080-166`; `requirements/`, `config/`, `tools/`, `tests/`, `reports/README.md`; `.github/`; `AGENTS.md` and pointer files; `docs/index.json`. `reports/baseline/` is tier 3. | Unzip or clone, open the folder in the agentic tool, type the Method/Full opener printed in README: "Read AGENTS.md and follow its first-five-minutes protocol." | `AGENTS.md` auto-loads (or its pointer does). Runs the audits, reads `README_START_HERE.md` and the tier 0-1 part of the index, chooses a mode, loads that mode's reading set. |
| 3 | **Full** | Higher-tier agentic subscriptions, maintainers, contributors, and anyone whose project touches the domain guides. | The GitHub repository (branches = practices, tags = audited states) and `<package_id>.zip` unpacking to `<package_id>/`. | Unbudgeted on disk; budgeted in use: `AGENTS.md` forbids loading domain guides wholesale and allows one per task, chosen from the index summaries. | Everything in tier 2; `docs/010`, `docs/055`, `docs/170-290` with `summary`, `topics`, and a TL;DR; `docs/300` and later planning records; `docs/999`; `reports/baseline/`; git history and practice branches. | `git clone`, same opener as tier 2. README says when this tier is worth it and that it is not the beginner path. | Same protocol as tier 2; DOMAIN-LOOKUP reads exactly one guide, TL;DR first. |

### 5.2 Upgrade path

Higher tiers are strict supersets with identical file names and IDs. `docs/004` states this and tells each tier what the next one adds. Moving from the Method Kit to Full is a `git clone`; nothing has to be re-learned. Every lower-tier artifact carries one line: "the full documents win on conflict" and a `derived_from` pointer where applicable, so a chat model has a citation target instead of inventing a parent SOP.

### 5.3 Edition zip identity

Edition zips unpack to `<package_id>_<edition>/` (for example `20261101_00_aisop_chatkit/`), which satisfies both `archive_name_audit.py` (root equals zip stem) and the `yyyymmdd_00_short-description` naming rule of `docs/100`. Every header inside keeps the base `package_id`; `EDITION_INFO.md` records `edition`, `root_folder` and `base_package_id`; `aisop_check.py --root` accepts the `_<edition>` suffix.

## 6. Repository Layout After REV-003

```text
AISOP/                                  clone folder name is irrelevant; package_id lives in config/
|-- AGENTS.md                           HAND (<= 8,192 B, full document-control header, Normative, tier 0)
|                                       with two GENERATED regions: rules (from docs/001), commands (from editions.json)
|-- CLAUDE.md                           pointer (<= 1 KB): header + "@AGENTS.md" import + one sentence
|-- GEMINI.md                           pointer (same shape); other tools read AGENTS.md natively (section 8.2)
|-- .github/
|   |-- workflows/ci.yml                push: [master, main] + pull_request
|   |-- workflows/package_audit.yml     gains a push trigger on [master, main] (manual-only today)
|   |-- workflows/release.yml           NEW: on tag v*: audits -> build editions -> attach assets
|   |-- ISSUE_TEMPLATE/first_session_report.yml   NEW: beginner feedback channel (not a gate; optional)
|   `-- (existing templates, dependabot, release_dry_run)
|-- README.md                           HAND with a GENERATED chooser region (tiers, budgets, openers from editions.json)
|-- README_START_HERE.md                HAND, edition-aware (Phase 2): "which edition am I holding?", reading order
|                                       with (method edition) markers on tier-2 entries, commands under a marked heading
|-- CHANGELOG.md  FEATURE_INVENTORY.md  ACCEPTANCE_TEST_PLAN.md  KNOWN_LIMITATIONS.md
|-- WORKPLAN_CURRENT_RUN.md             gains a "## Decision Log" section (Phase 0)
|-- REQUIREMENTS_TRACEABILITY_MATRIX.md HAND (generation deferred; DECISION-011)
|-- PACKAGE_MANIFEST.md                 GENERATED by tools/manifest_update.py; gains --check (Phase 0)
|-- CONTRIBUTING.md SECURITY.md SAFETY.md SUPPORT.md NOTICE.md CODE_OF_CONDUCT.md CITATION.cff LICENSE.txt
|-- USER_PROFILE.md                     LOCAL, gitignored: the owner's (or any user's) real profile
|-- config/
|   |-- package_metadata.json           package_id, version, license_file, default_branch, required files/dirs
|   |                                   (dist removed), example_packages list; audits read lists from here
|   `-- editions.json                   NEW: editions, tier cutoffs, byte budgets, max_files, fixed file lists,
|                                       opener strings, pointer-file list
|-- requirements/requirements_catalog.json
|-- docs/
|   |-- index.json                      GENERATED: path, document_id, title, size_class, tier, normative_status,
|   |                                   topics, summary, read_order (ordered by tier then path; no exact byte counts)
|   |-- 000_DOCUMENTATION_INDEX.md      GENERATED from headers, grouped by tier
|   |-- 000_USER_GUIDE_OVERVIEW.md      tier 2
|   |-- 001_AISOP_CORE_RULES.md         tier 0  NEW, HAND, Normative, <= 8 KB (rules block <= 4 KB)
|   |-- 002_BEGINNERS_GUIDE_TO_AI_AGENTS.md   tier 1  NEW
|   |-- 003_GLOSSARY.md                 tier 1  NEW
|   |-- 004_EDITIONS_AND_UPGRADE_PATH.md     tier 1  NEW (tier table and openers are a GENERATED region)
|   |-- 005_PRODUCT_REQUIREMENTS.md     tier 2
|   |-- 010_WINDOWS_...                 tier 3 (reclassified as domain reference; file not renamed)
|   |-- 020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md   tier 1 (generalized in Phase 0)
|   |-- 030, 040, 060, 070              tier 2 (core method; content unchanged beyond hygiene)
|   |-- 050_MONOLITHIC_PROTOTYPE_CODE_SOP.md  tier 1
|   |-- 055_MONOLITHIC_PROTOTYPE_CODE_EXAMPLE.md  tier 3 (34 KB code example; Method Kit keeps 050 + a pointer)
|   |-- 080 ... 165                     tier 2 (governance)
|   |-- 166_EDITIONS_AND_TIERS_SOP.md   tier 2  NEW, Normative: tiers, budgets, generated files, release assets
|   |-- 170 ... 290                     tier 3 (domain guides; header keys + TL;DR + fence/residue repair only)
|   |-- 300_AISOP_EXPANSION_GAMEPLAN_REV003.md   this document, tier 3 (planning records are Full-only)
|   `-- 999_SOURCE_CLEANUP_NOTES.md     tier 3
|-- templates/                          NEW, HAND, tier 1; each carries derived_from: DOC-0xx; see 9.2 for caps
|   |-- README.md                       the stage table: stage -> one template -> SOP (section 8.1 item 6)
|   |-- USER_PROFILE_TEMPLATE.md        fill-in fields + one labelled fictional example
|   |-- CONCEPT_BRIEF_TEMPLATE.md       derived_from DOC-030 (the "Concept Brief Lite")
|   |-- PLANNING_DOCUMENT_TEMPLATE.md   derived_from DOC-040 (heading parity audited; optional sections marked)
|   |-- README_START_HERE_TEMPLATE.md  CHANGELOG_TEMPLATE.md  FEATURE_INVENTORY_TEMPLATE.md
|   |-- KNOWN_LIMITATIONS_TEMPLATE.md   FINAL_PACKAGE_REPORT_TEMPLATE.md   AGENT_HANDOFF_BUNDLE_TEMPLATE.md
|   |-- MANUAL_AUDIT_CHECKLIST.md       GENERATED from the CHECKS table in tools/aisop_check.py
|   |-- FIRST_SESSION_PROMPTS.md        plan this / prototype this / package and report, each < 20 lines
|   `-- ID_RECORD_FORMATS.md            the REQ/RISK/DEBT/DECISION/QUESTION record formats, stated once
|-- examples/
|   `-- hello_aisop/                    NEW, tier 1: complete minimal package, registered in config (section 9.5)
|       |-- README_START_HERE.md        header carries package_role: example and the example's own package_id
|       |-- 000_PLANNING_DOCUMENT.md CHANGELOG.md FEATURE_INVENTORY.md ACCEPTANCE_TEST_PLAN.md KNOWN_LIMITATIONS.md
|       |-- hello_aisop.py              ~80 lines; --version, --smoke-test, --diagnostics (the docs/050 names)
|       `-- tools/README.md             "copy ../../tools/aisop_check.py here" (no duplicate script in the kit)
|-- tools/
|   |-- _aisop_common.py                NEW: the one frontmatter parser (inline list form; 4,096-byte header window)
|   |-- build_editions.py               NEW: entry | index | zips | all | --check (owns generated freshness,
|   |                                        per-edition budgets, per-edition link resolution)
|   |-- edition_audit.py                NEW: tree-level link resolution, cross-tier link rule, template parity,
|   |                                        ID citation, pointer checks, size caps, example-package registration,
|   |                                        package_id consistency, cold-log WARN
|   |-- bump_release.py                 NEW: rewrite package_id and version in every header from config
|   |                                        (never revision or last_updated)
|   |-- aisop_check.py                  NEW: single-file lite audit for downstream packages (<= 10 KB)
|   |-- release_package.py              CHANGED: thin wrapper over build_editions zips; root from config
|   |-- run_all_audits.py               CHANGED: sys.executable; new audits; --quiet (SUMMARY block only)
|   |-- manifest_update.py              CHANGED: header values from config; --check
|   `-- package_structure_audit.py  repo_health_audit.py  requirements_trace_audit.py  secret_scan_lite.py
|       archive_name_audit.py           (CHANGED to read lists from config; skip dist/ and git-ignored files;
|                                        fence parity; tier/summary keys; profile-phrase patterns)
|-- tests/
|   |-- smoke_test.py                   extended: index.json valid, AGENTS.md present, negative cases (section 7.4)
|   `-- test_new_project.py             Phase 4, optional
|-- reports/
|   |-- README.md                       states that *.txt are runtime output and baseline/ is committed evidence
|   |-- baseline/                       committed per release, tier 3, incl. cold_agent_test_<package_id>.txt
|   `-- *.txt                           gitignored
|-- src/README.md
`-- dist/                               gitignored: <pid>.zip <pid>_method.zip <pid>_chatkit.zip AISOP_CARD.md EDITIONS_CHECKSUMS.txt
```

Optional, later-phase paths not shown above: `templates/monolithic_prototype_template.py` (Phase 5; exercised by the smoke test, not by heading parity), `templates/project_seed/` and `tools/new_project.py` (Phase 4, only if needed), `examples/<pack>/` (Phase 5), `skills/aisop/SKILL.md` (Phase 5, only if the owner uses a tool that loads skills).

## 7. Single-Source Mechanism

### 7.1 Two new header keys

Every Markdown document gains `tier: N` (0-3; the lowest tier that includes it; inclusion is cumulative) and `summary: "one line, <= 200 characters"`. Domain guides additionally gain `topics: [a, b]` in the inline bracket form. The existing parser splits each line on the first colon and strips quotes; it moves into `tools/_aisop_common.py`, which also splits inline lists on commas and raises the closing-`---` search window from 1,200 to 4,096 bytes. A missing `tier` or `summary` is a structure-audit FAIL. Every `.md` outside `.github/` (pointers, templates, examples, `reports/README.md`) carries the full header; the structure audit's walk skips `dist/` and git-ignored files.

### 7.2 One manifest

`config/editions.json` is the only place that holds, per edition: name, tier cutoff, hard byte budget, `max_files`, fixed non-document files (root governance files, `tools/`, `tests/`, `requirements/`, `config/`, `templates/`, `examples/`, `.github/`), zip suffix, the opener string, and the pointer-file list. `config/package_metadata.json` keeps `required_root_files`, `required_directories`, and `example_packages` for the structure audit; `editions.json` references them by name rather than repeating them.

### 7.3 One generator

`tools/build_editions.py` (stdlib: `json`, `re`, `hashlib`, `zipfile`, `pathlib`) with subcommands:

| Subcommand | Produces | Committed? |
|---|---|---|
| `entry` | The GENERATED regions inside `AGENTS.md` (rules block from `docs/001`; commands from `editions.json`), the pointer files, the chooser region in `README.md`, the tier table and openers in `docs/004`, and `templates/MANUAL_AUDIT_CHECKLIST.md` from the `CHECKS` table in `tools/aisop_check.py`. | Yes. |
| `index` | `docs/index.json` and `docs/000_DOCUMENTATION_INDEX.md` from headers, ordered by tier then path. | Yes. |
| `zips` | `dist/<pid>.zip`, `<pid>_method.zip`, `<pid>_chatkit.zip`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt`, and an `EDITION_INFO.md` inside each zip. Members are written with `writestr` and a fixed `ZipInfo` (date from `config.last_updated`, `external_attr` fixed), sorted by path. | No (gitignored; attached to releases). |
| `--check` | Regenerates everything in memory, exits 1 on any difference from the committed files, stages every edition in memory and FAILs on a budget or `max_files` breach or on an unresolved path inside an edition (section 7.4), writing nothing. | Runs inside `run_all_audits.py` and CI. |

`PACKAGE_MANIFEST.md` stays with `tools/manifest_update.py` (header values read from config; `--check` added in Phase 0) and is regenerated last, after `build_editions.py all`, because it hashes the generated files. Generated committed files contain no timestamps or exact byte counts, so `--check` is deterministic and a one-line edit elsewhere does not turn CI red. Each generated file or region starts with a banner: `GENERATED by tools/<script>.py from <source>; edit the source, not this file`.

Reproducibility is claimed on content, not on the zip container: `EDITIONS_CHECKSUMS.txt` carries, per edition, the sha256 of the sorted concatenation of member paths and contents, which a local rebuild on the same tag reproduces; the zip file's own sha256 is listed separately for download integrity only, because compressed bytes depend on the zlib build.

### 7.4 Audits that fail loudly (ownership table)

| Check | Owner | Notes |
|---|---|---|
| Header completeness incl. `tier` (0-3) and `summary`; duplicate `document_id`; personal-reference and profile-phrase scan; fence parity (every `docs/*.md` has an even number of lines starting with ` ``` `); walk skips `dist/` and git-ignored files; registered example roots audited for completeness with their own `package_id` | `package_structure_audit.py` | Existing tool, extended. |
| Required repository files and content checks (reads lists from config) | `repo_health_audit.py` | Existing tool, extended. |
| Generated freshness of every committed generated file and region; per-edition byte totals vs budget (WARN 75%, FAIL 100%, five largest files listed); `max_files` and unique-basename rule for the Chat Kit; inside each staged edition, every relative link and backticked repo path resolves unless the citing line carries `(method edition)` or `(full edition)` | `build_editions.py --check` | One generator, one staging pass. |
| In the full tree every relative link and backticked `docs/`, `tools/`, `templates/`, `examples/` path resolves; cross-tier rule (a tier-t document may not link a tier>t document as required reading without the marker); template heading parity (`templates/*.md` H2 list equals the `## Required sections` list in the SOP named by `derived_from`); ID citation (every `REQ-*`/`FEAT-*`/`TEST-*` cited in a tier <= 1 document under `docs/` or at the root exists in `docs/005`, `FEATURE_INVENTORY.md`, or `ACCEPTANCE_TEST_PLAN.md` respectively; `templates/` excluded and limited to placeholder forms `REQ-XXX-NNN` / `FEAT-NNN` / `TEST-XXX-NNN`; registered example roots excluded); `AGENTS.md` <= 8,192 bytes including both regions, header `package_id`/`version` equal config, body contains no other package_id-shaped token, Normative; `docs/001` rules block <= 4,096 bytes; pointer files <= 1 KB with merged front matter and the string `AGENTS.md`; card label list equals the report template's label list; glossary covers every ID family (first token before the first hyphen) occurring in a tier <= 2 document plus the seeded term list; every header `package_id` equals config except inside registered example roots; WARN when no cold-agent log exists for the current package_id; WARN when a document with status Superseded/Rejected is not tier 3 | `edition_audit.py` | New tool. |
| `PACKAGE_MANIFEST.md` matches the tree | `manifest_update.py --check` | Phase 0. |
| `docs/index.json` valid and lists every document; `AGENTS.md` present; negative cases: copy the tree to a temp dir, (a) alter one GENERATED region, (b) delete `tier:` from one header, assert the audit exits 1 and its message names the source file | `tests/smoke_test.py` | Scripted, so the negative gates are re-run every time. |

### 7.5 Hand-written vs generated (explicit list)

- **Hand-written:** every `docs/*.md` except the two index files; all root intake and governance documents (their GENERATED regions excepted); `templates/` except `MANUAL_AUDIT_CHECKLIST.md`; `examples/`; `config/*.json`; `requirements_catalog.json`; all tools; `AGENTS.md` outside its two regions, including its header.
- **Generated and committed:** the regions in `AGENTS.md`, `README.md`, `docs/004`, `README_START_HERE.md`; pointer files; `templates/MANUAL_AUDIT_CHECKLIST.md`; `docs/index.json`; `docs/000_DOCUMENTATION_INDEX.md`; `PACKAGE_MANIFEST.md`.
- **Generated and not committed:** everything under `dist/`; `reports/*.txt`.

## 8. Agent Entry Design

### 8.1 `AGENTS.md` (hand-written, <= 8,192 bytes including both regions, sections fixed)

`AGENTS.md` carries the full document-control header (`document_id: DOC-AGENTS`, `normative_status: Normative`, `tier: 0`) and is itself listed in the binding set, so its protocol, modes, hard rules, and delivery shape bind by the plan's own rule. The header is the identity; the prose repeats no package_id or version. Measured against a draft written to this section, the non-rules content is about 3.4 KB, which with a 4 KB rules block leaves roughly 700 bytes of headroom under the cap.

1. **Identity:** "This file is Normative. Two regions are GENERATED; edit their sources (`docs/001`, `config/editions.json`)."
2. **What this repository is** (three sentences) and the two avenues.
3. **NORMATIVE vs INFORMATIVE:** the PRIN-005 definition, verbatim, plus: "`docs/010`, `docs/055` and `docs/170-290` are informative reference, never requirements."
4. **Core rules** (GENERATED from `docs/001`, so the card, the Chat Kit, and the entry file cannot disagree).
5. **First-five-minutes protocol** (section 8.3).
6. **Mode selector and reading sets.** Select the mode by what the task will change. Nothing changes (orientation, questions, review): **ORIENT**, no reading beyond the protocol's own reads. Files outside this tree change: **APPLY**. Files inside this tree change: **MODIFY-AISOP** (`docs/165`, `160`, `166`, `120`; must run `build_editions.py --check` and the audits before delivering; must update CHANGELOG, FEATURE_INVENTORY, requirements, and traceability when behaviour changes). **DOMAIN-LOOKUP** is additive, not exclusive: append it to any mode when the task needs one of `docs/170-290`, report it as e.g. "APPLY + DOMAIN-LOOKUP (docs/185)", read index summaries first, open exactly one guide, TL;DR first. In APPLY, read the one template for the current stage, not the folder (table mirrored in `templates/README.md`):

   | Stage | Single template | SOP opened only at that stage |
   |---|---|---|
   | concept | `templates/CONCEPT_BRIEF_TEMPLATE.md` | `docs/030` |
   | plan | `templates/PLANNING_DOCUMENT_TEMPLATE.md` | `docs/040` |
   | prototype | `examples/hello_aisop/hello_aisop.py` as the pattern | `docs/050` |
   | migrate | `templates/AGENT_HANDOFF_BUNDLE_TEMPLATE.md` | `docs/060` |
   | package | `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` | `docs/070` |

   The agent states the chosen mode back to the user in one sentence before touching files.
7. **Commands** (GENERATED): `python tools/run_all_audits.py [--quiet]`, `python tools/build_editions.py --check`, `python tools/release_package.py --dry-run`.
8. **Hard rules:** never hand-edit a GENERATED region or file; never delete a REQ/FEAT/TEST ID (mark Superseded); bump `revision` and `last_updated` on every touched controlled document; keep tooling stdlib; every new document's header is complete including `tier` and `summary`; zip basename equals internal root; never read `docs/185` or `docs/195` (60+ KB each) in full unless asked.
9. **User profile rule:** if `USER_PROFILE.md` exists at the root, read it; otherwise, in APPLY only, ask the six profile questions from `templates/USER_PROFILE_TEMPLATE.md` before planning code.
10. **Delivery:** end every substantial task with the fifteen-field final package report (`templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`), the `run_all_audits.py --quiet` result, and, when code changed, the diagnostic command the user can run and paste back. A zip is delivered only when the user asked for a handoff (`docs/070`).

The repository map does **not** live in `AGENTS.md` (embedding it overflows every proposed cap). It lives in `docs/index.json`, ordered by tier so the protocol can read only the leading tier 0-1 records.

### 8.2 Pointer files (only for tools the owner can test; list in `editions.json`)

| Tool | File | Shape | Why |
|---|---|---|---|
| Claude Code | `CLAUDE.md` | document-control header, `@AGENTS.md` import line, one sentence ("Read AGENTS.md before doing anything, then follow its first-five-minutes protocol.") | Honours `@` imports, so `AGENTS.md` is inlined. |
| Gemini CLI | `GEMINI.md` | same shape | Same. |
| Codex CLI, Cursor, Copilot coding agent | none by default | These tools read `AGENTS.md` natively per their current documentation (verify in Phase 1); a pointer would load it twice. | If a pointer is ever needed, `.cursor/rules/aisop.mdc` has ONE front-matter block holding Cursor's own keys (`description`, `globs`, `alwaysApply: true`) merged with the document-control keys, and `.github/copilot-instructions.md` carries the header inside an HTML comment with no `@` line. |

Each pointer is <= 1 KB, cannot drift (it names the file, nothing else), and is audited for the string `AGENTS.md` and its header.

### 8.3 First-five-minutes protocol

| Minute | Action | Tokens (est.) |
|---|---|---|
| 0-1 | `AGENTS.md` auto-loads; confirm the package_id and version from its header. | ~2k |
| 1-2 | Run `python tools/run_all_audits.py --quiet`. PASS: trust the tree. FAIL: report the failing tool verbatim and stop structural work until understood (a red audit on a fresh clone is a bug to report, not to work around). If you cannot run commands, say so in the minute-5 report, apply `templates/MANUAL_AUDIT_CHECKLIST.md` by hand, and do not claim the tree is audited. | ~0.5k |
| 2-3 | Read `README_START_HERE.md`; read the leading tier 0-1 records of `docs/index.json` (they come first). | ~2k |
| 3-4 | Select the mode (8.1 item 6); load that mode's reading set; read `USER_PROFILE.md` if present (ask the profile questions only in APPLY). | ~2-4k |
| 4-5 | Report back in the fixed shape: AISOP version loaded, audit result (or "could not run"), mode chosen, files read, files intentionally not read, first proposed acceptance-gated step. | ~0.5k |

Budget to competence: roughly 8-10k tokens and five to six tool calls. The minute-5 report is the artifact TEST-ENTRY-004 checks; its expected content for the prompt "Get up to speed on AISOP" is mode ORIENT, the normative rule as 8.1 item 3 states it (only `docs/005` and the catalog define `REQ-*`; governance SOPs bind process; domain guides are informative), and no domain guide opened.

### 8.4 Machine-readable index

`docs/index.json`: one record per document with `path`, `document_id`, `title`, `size_class` (S < 8 KB, M < 24 KB, L < 48 KB, XL), `tier`, `normative_status`, `topics`, `summary`, and `read_order` for the entry path; ordered by tier then path. Exact byte counts are computed by the audits at run time, not committed, so the index does not go stale on every edit. An agent decides whether to open a 60 KB guide from the record, not from the file.

## 9. Beginner On-Ramp (Chat Kit content)

### 9.1 New short documents (hand-written, tier 0-1)

| File | Budget | Content |
|---|---|---|
| `docs/001_AISOP_CORE_RULES.md` | <= 8 KB; rules block <= 4 KB | The card. Distilled from `020` (core principles, feature-preservation rule), `070` (golden rule, minimal per-run checklist, what-not-to-do), `050` (freeze-before-refactor sequence), `060` (phase gate), `165` (handoff bundle), `080` (loop). Includes the fifteen report labels inline, the card-only opener, and the "words used here" footnote. Normative. |
| `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md` | <= 12 KB | What an agent is versus a chat; what a context window means in practice; why you give the agent files, not memories; which tier to pick; a five-step first project, each step with "what you say / what the AI should produce / how you know it worked / what to do if it did not"; a "Before step 2: running what the AI gives you" box (install Python from python.org, open a terminal, `python --version`, save the file into your `yyyymmdd_00_<idea>` folder, run it with `--smoke-test`, with the fallback "ask the AI how to run this on my computer" or run it inside a chat product that executes Python); the five mistakes beginners make. |
| `docs/003_GLOSSARY.md` | <= 6 KB | Every ID family used in tier <= 2 documents (REQ, FEAT, TEST, DOC, REV, LIMIT, RISK, DEBT, DECISION, QUESTION, GOAL, PRIN, DRIFT, GATE, PHASE), every document-control field, and the seeded term list: mode, ORIENT, APPLY, MODIFY-AISOP, DOMAIN-LOOKUP, normative, informative, monolithic prototype, feature inventory, intake document, document-control header, system prompt / custom instructions, context window, drift, package_id, edition, tier, practice space, golden baseline, diagnostic harness, handoff bundle, acceptance gate. ID families found only in tier-3 documents (`RULE-*`, `LESSON-*`, `ACCEPT-*`, `THREAD-RULE-*`, ...) are listed in `docs/index.json` `topics` instead. |
| `docs/004_EDITIONS_AND_UPGRADE_PATH.md` | <= 5 KB | The four tiers with budgets and openers (GENERATED region from `editions.json`), what each adds, that higher tiers are strict supersets, how zips relate to the repository and releases, the clone-name vs package_id convention, and, from Phase 2, per chat product the owner tested: whether a zip attaches, whether files are read whole or on demand, and the per-message file cap. |

### 9.2 Templates (tier 1; `templates/` total <= 24 KB, each <= 4 KB, `ID_RECORD_FORMATS.md` <= 6 KB)

Extracted from the long SOPs (section 10.2 lists the sources) and audited for heading parity against a `## Required sections` list added to `docs/040` and `docs/070`; `PLANNING_DOCUMENT_TEMPLATE.md` marks the sections a small project may answer with "Not needed for this project: <one-line reason>". Includes `CONCEPT_BRIEF_TEMPLATE.md` (the "Concept Brief Lite"), `FIRST_SESSION_PROMPTS.md` (three prompts under 20 lines each: plan this / prototype this / package and report), and `MANUAL_AUDIT_CHECKLIST.md`, which is GENERATED from the `CHECKS` table inside `tools/aisop_check.py` so the by-hand path and the script cannot diverge. The manual result shape is a table `TEST-ID | PASS/FAIL/SKIP | evidence`; that table is the step-3 "how you know it worked" artifact for users who cannot run Python. The standard AI prompts in `docs/270` sections 10-12 and `docs/290` section 27 seed the prompt file.

### 9.3 Worked example (`examples/hello_aisop/`, <= 8 KB)

One ~80-line script with the numbered sections from `docs/050` and the flags `docs/050` names (`--version`, `--smoke-test`, `--diagnostics`), a planning document at hello-world scale (so the "plan this" prompt has a model to imitate), and the five intake documents. It passes `tools/aisop_check.py --root examples/hello_aisop` and is the fixture `tests/smoke_test.py` runs the lite audit against. It ships no copy of the script (the kit has `tools/aisop_check.py` one level up); its `tools/README.md` says where to copy it from. A chat model imitates a concrete package far better than it follows prose, so nothing imitable in the example may be AISOP-only (no marker files).

### 9.4 Openers (single source: `editions.json`; rendered into README, `docs/004`, `EDITION_INFO.md`)

- **Card-only:** "Use the AISOP card above as your operating rules. Reply with the AISOP version it names and the word ORIENT, then ask me for my idea."
- **Chat Kit:** "I have uploaded the AISOP Chat Kit. Read EDITION_INFO.md, then README_START_HERE.md, then the card. Work in ORIENT or APPLY mode only and never ask for a file that EDITION_INFO.md does not list. Reply with: the AISOP version and package_id, the files you can see, the word ORIENT, and the question 'what is your idea?'." The model's reply is the tier-1 "loaded" artifact, the chat-side counterpart of the minute-5 report.
- **Method Kit / Full:** "Read AGENTS.md and follow its first-five-minutes protocol."

### 9.5 Lite audit and example-package rule

`tools/aisop_check.py` (<= 10 KB, stdlib only) audits a *downstream* package: the five intake documents exist with complete document-control headers, the zip basename equals the root folder when given a zip, a script with the `docs/050` flags is present, and every relative link resolves; `--explain` prints the same `CHECKS` table for humans. The Chat Kit root is an edition of AISOP, not a user package: the lite audit is shipped in it, not run on it.

Example packages are registered in `config/package_metadata.json` (`example_packages: ["examples/hello_aisop"]`) and their `README_START_HERE.md` header carries `package_role: example` and the example's own `package_id`; both are required (an unregistered root or a registered root without the key is a structure-audit FAIL). Inside a registered root, headers must be complete, `package_id` must equal the header's own value, `document_id` values use the prefix `DOC-EX-*` so they stay globally unique, and the example's own REQ/FEAT/TEST IDs are checked only by `aisop_check.py` inside that root.

### 9.6 Chat Kit arithmetic (measured or capped, bytes)

Card 8,192 + `docs/002` 12,288 + `docs/003` 6,144 + `docs/004` 5,120 + generalized `docs/020` ~12,000 + `docs/050` 10,746 + `README_START_HERE.md` ~4,000 + `LICENSE.txt` 1,200 + `NOTICE.md` 640 + `EDITION_INFO.md` ~2,000 + `templates/` <= 24,576 + `examples/hello_aisop/` <= 8,192 + `tools/aisop_check.py` <= 10,240 = ~105,000 bytes, about 85% of 122,880. Method Kit projection: ~253 KB today plus `docs/001-004` and `166` (<= 37 KB), `AGENTS.md` and pointers (~10 KB), `docs/index.json` (~8 KB), `config/editions.json` (~2 KB), `templates/` (<= 24 KB), `examples/` (<= 8 KB), and five new tools (~35 KB): ~377 KB, about 92% of 409,600; moving `docs/055` to tier 3 (already done above) is what keeps it there. DECISION-014 applies if Phase 2 lands above 90%.

### 9.7 Feedback channel

`.github/ISSUE_TEMPLATE/first_session_report.yml`: which tier, which tool, what the AI produced, pasted `aisop_check` output or the filled manual checklist. It is a channel, not a gate (PRIN-008), and optional for tier 0-1 users who have no GitHub account.

## 10. Corpus Reorganization Map

### 10.1 Placement of every existing document

| Document | Tier | Pack | Action in REV-003 |
|---|---|---|---|
| `000_DOCUMENTATION_INDEX` | 2 | - | Becomes generated. |
| `000_USER_GUIDE_OVERVIEW` | 2 | - | Header keys; light beginner wording pass. |
| `005_PRODUCT_REQUIREMENTS` | 2 | - | New REQ entries; REQ-LIC-001 rewritten under the same ID. |
| `010_WINDOWS_SOFTWARE_DOWNLOAD...` | 3 | windows-hardware-workstation | Reclassified as domain reference (no rename); residue removal. |
| `020_AI_COLLABORATION_OPERATING_INSTRUCTIONS` | 1 | - | Generalized to second person; profile moved to template (Phase 0). |
| `030_CONCEPT_DEVELOPMENT_AND_REQUIREMENTS_BRIEF` | 2 | - | Headings and fences; `CONCEPT_BRIEF_TEMPLATE.md` extracted. |
| `040_MONOLITHIC_PLANNING_DOCUMENT_SOP` | 2 | - | Headings; `## Required sections` list; extraction-target numbering reconciled (DRIFT-008). |
| `050_MONOLITHIC_PROTOTYPE_CODE_SOP` | 1 | - | `logging.py` -> `logging_utils.py` (content fix, revisioned); pointer block to 055/060. |
| `055_MONOLITHIC_PROTOTYPE_CODE_EXAMPLE` | 3 | - | Fix the `os.rename` Windows bug (content fix, revisioned); drop Python 2 branches; later move code to `templates/monolithic_prototype_template.py` run by the smoke test. |
| `060_MONOLITH_TO_PACKAGE_MIGRATION_SOP` | 2 | - | Close the fence at L145; remove chat preamble and duplicate H1; `## Required sections`. |
| `070_ZIP_PACKAGE_REVIEW_AND_HANDOFF_SOP` | 2 | - | Headings; canonical report format decision; `test_reports/` -> `reports/`; empty appendix stubs removed. |
| `080-165` governance | 2 | - | Header keys; `100`, `150`, `160`, `165` gain edition/release/agent paragraphs; `165` rewritten to defer to `AGENTS.md` (Phase 1). |
| `170_COMPATIBILITY_LESSONS_LEARNED` | 3 | legacy-and-embedded-compat | Fence repair and re-fencing (Phase 5); generic LESSON-GEN entries and checklists later lifted to a tier-2 compatibility discipline doc. |
| `180`, `185` | 3 | hardware-daq | Fence repair and re-fencing; remove chat residue; label project-specific examples as examples (Phase 5). |
| `190`, `195` | 3 | inline-qc-defect-traceability | Fence repair and re-fencing; remove stray MIDI paragraph; label domain examples (Phase 5). |
| `200_FILE_DOWNLOAD_INSTALLATION...` | 3 (trimmed beginner section later tier 1) | windows-hardware-workstation | Close fence L47 (Phase 0); orphan line; the "installing one of our ZIP packages" procedure promoted into `README_START_HERE_TEMPLATE`. |
| `205_PYTHON_LIBRARY_REFERENCE...` | 3 | python-environment-profiles | Describes an environment bundle that does not exist: rewrite as "proposed, not shipped" or implement later. |
| `210`, `250`, `260` | 3 | embedded-platforms | Orphan lines; dated API notes; `260` owns I2C. |
| `220`, `240`, `270`, `290` | 3 | simulation-games, audio-midi, android-pydroid, gui-design | Orphan lines; `270` has four sentences corrupted by citation-tool residue to repair (content fix, revisioned). |
| `280_NETWORKING...` | 3 | networking-and-remote-devices | Truncated mid-sentence at L727: finish or delete the ping-sweep section. |
| `300` (this plan) | 3 | - | Planning record; tier 3 from the start. |
| `999_SOURCE_CLEANUP_NOTES` | 3 | - | Header keys. |

### 10.2 Template extraction backlog (sources, cited by heading once Phase 0 hygiene lands)

Roughly sixty reusable skeletons exist inside the long SOPs. The Phase 2 set and their sources: planning document skeleton (`040` "Minimal Template"); ID record formats (`030` requirement blocks and `040` per-section record formats, stated once, with the illustrative IDs replaced by the placeholder forms `REQ-XXX-NNN` / `FEAT-NNN` / `TEST-XXX-NNN`); implementation-boundaries block (`030` "Implementation Boundaries for This Run"); pre-code checklist (`030` section 21 and `040` section 9, merged); package folder layout and package identity intake form (`070` sections 2-3); workplan scope block (`070` section 10); CHANGELOG entry standard (`070` section 13); final package report (`070` section 18); minimal per-run checklist (`070` section 21); transfer plan (`060` "005_MONOLITH_TO_PACKAGE_TRANSFER_PLAN"); phase-gate checklist (`060` section 19); handoff bundle (`165`). Domain-pack templates (channel map, wiring card, diagnostic report script, adapter interface) are Phase 5.

### 10.3 Domain packs (Phase 5, optional, one PR per guide)

windows-hardware-workstation (`010`, `200`), legacy-and-embedded-compat (`170`), hardware-daq (`180`, `185`), inline-qc-defect-traceability (`190`, `195`), embedded-platforms (`210`, `250`, `260`), application guides (`220`, `240`, `270`, `290`), networking (`280`). Each pack can later get a one-page brief assembled from its existing `RULE-*` / `THREAD-RULE-*` blocks and definition-of-done checklist, and its embedded code moved to `examples/<pack>/`.

## 11. Phases

Effort is given in maintainer sessions of about four hours. Each phase is one or more practice branches (`practice/rev003-<slice>`) with branch notes per `docs/080`; a slice merges as soon as its mini-gate passes, so `master` goes green early and stays green.

### PHASE-0: Make the clone green and give agents a landing file (5 slices, ~6-8 sessions)

**0a. License gate and CI branch (1 session; green `master` at the end).**
1. DRIFT-001: remove every live reference to the license-decision gate (the files listed in 3.2); rewrite REQ-LIC-001 as "a resolved license file named in `config/package_metadata.json` and a NOTICE.md consistent with it" (same ID); TEST-LIC-001 checks `LICENSE.txt` contains "MIT License"; update the matrix, README, NOTICE, `docs/140`, KNOWN_LIMITATIONS (it no longer states that no license has been selected), FEATURE_INVENTORY (FEAT-014 marked Superseded by FEAT-030 "Resolved MIT license and NOTICE consistency").
2. DRIFT-003: `ci.yml` push branches become `[master, main]`; `package_audit.yml` additionally gains a push trigger on those branches; document the default branch in README (DECISION-001). Add REQ-CI-002 / TEST-CI-002 (`ci.yml` `on.push.branches` contains the configured `default_branch`).
3. Merge or close the two Dependabot pull requests once CI is green.

Mini-gate: `run_all_audits.py` PASS on a clone named `AISOP` except for the release dry run; GitHub Actions green on `master`.

**0b. Release root, reports, manifest (1 session).**
4. DRIFT-002: `release_package.py` reads `package_id` from config, stages into a temp directory named `<package_id>` (full) or `<package_id>_<edition>` (editions, Phase 3), WARNs when the clone folder differs; `--name` override. Remove `dist` from `required_directories` in `config/package_metadata.json`. `run_all_audits.py` spawns `sys.executable`. Add REQ-REL-002 / TEST-REL-002.
5. DRIFT-004: gitignore `reports/*.txt` and `USER_PROFILE.md`, `git rm --cached` the seven runtime reports, keep `reports/README.md` and `reports/baseline/`; snapshot current outputs as `reports/baseline/baseline_rev003_*`; add REQ-RPT-001 / TEST-RPT-001.
6. `manifest_update.py` reads header values from config and gains `--check`, wired into `run_all_audits.py` as the last step; regenerate `PACKAGE_MANIFEST.md`. Add REQ-MAN-001 / TEST-MAN-001.

Mini-gate: full `run_all_audits.py` PASS; `git status --porcelain` empty after the run.

**0c. Interim entry file and canonical report (1 session).**
7. DRIFT-006: hand-written interim `AGENTS.md` (<= 4 KB, full document-control header so the structure audit passes, Normative, marked INTERIM and replaced in Phase 1) and a `CLAUDE.md` pointer: what the repo is, run the audits first, read `README_START_HERE.md`, the PRIN-005 rule, do not load `docs/170-290` wholesale, never delete IDs.
8. DRIFT-008 (DECISION-003): declare the `docs/070` section 18 fifteen-field report canonical, reference it from `docs/020`, `050`, `060`, `165`, and `AGENTS.md`, create `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`. Add REQ-RPT-002 / TEST-RPT-002 (grep: those documents cite the template; no other report-format heading remains).
9. Add a `## Decision Log` section to `WORKPLAN_CURRENT_RUN.md` holding the answered items from section 14.

**0d. Operating instructions (1-2 sessions; writing).**
10. DRIFT-005: rewrite `docs/020` in the second person with no biography; move every personal preference into `templates/USER_PROFILE_TEMPLATE.md` as fill-in fields plus one clearly labelled fictional example; add third-person-profile regexes to the personal-reference scan; add REQ-PROF-001 / TEST-PROF-001.

**0e. Source hygiene (1-2 sessions; two commits).**
11. Mechanical commit: close the fences in `docs/060` (L145) and `docs/200` (L47); delete the orphan trailing lines in every document; delete the two stray old-filename lines and the duplicate H1s. The commit must satisfy a scripted rule: `git diff -U0 <parent>..<commit> -- docs/` contains only added lines that are exactly a fence and removed lines; no modified line pairs. `docs/170-195` are re-fenced in Phase 5 (one PR per guide), because a single closing fence leaves hundreds of code lines as unfenced prose.
12. Content commit (revisioned): repair the four corrupted sentences in `docs/270`; fix the `os.rename` bug in `docs/055`; `project/logging.py` -> `logging_utils.py` in `050`/`055`; remove the chat-reply fragments.
13. Add the fence-parity check to `package_structure_audit.py` with REQ-DOC-004 / TEST-DOC-004.
14. Bump revisions on touched documents; CHANGELOG REV-003 Phase 0 entry; WORKPLAN run entry; regenerate `PACKAGE_MANIFEST.md`.

Gate GATE-0: on a fresh `git clone` into a folder named `AISOP` and into a folder with any other name, `python tools/run_all_audits.py` prints `SUMMARY: PASS` and `git status --porcelain` is empty afterwards; GitHub Actions green on the default branch; `grep -rl LICENSE_DECISION_REQUIRED --exclude-dir=.git --exclude-dir=reports --exclude=300_*.md --exclude=CHANGELOG.md --exclude=WORKPLAN_CURRENT_RUN.md .` returns nothing; the personal-reference scan passes with the new patterns; the fence-parity check passes for `docs/060` and `docs/200` and lists the five domain guides as the only remaining WARN entries until Phase 5 closes them; `requirements_trace_audit` passes with the revised and new IDs.

### PHASE-1: Single-source scaffold, real agent entry, machine-readable index (6-8 sessions)

Tasks: write `docs/001_AISOP_CORE_RULES.md`; add `tier:` and `summary:` to every header (scripted pass, summaries hand-reviewed) and to `REQUIRED_FRONTMATTER_KEYS`; review `normative_status` on the root files with the owner (NOTICE, SUPPORT, CODE_OF_CONDUCT, README, README_START_HERE, KNOWN_LIMITATIONS, FEATURE_INVENTORY are candidates for Informative; `manifest_update.py` emits Informative); write `config/editions.json`; implement `tools/_aisop_common.py`, `tools/build_editions.py` (`entry`, `index`, `--check`; `zips` stubbed), `tools/edition_audit.py`; switch `package_structure_audit.py` and `repo_health_audit.py` to read their lists from config; add `--quiet` to `run_all_audits.py` and wire in the new checks; extend `tests/smoke_test.py` with the index check and the two negative cases; write the real `AGENTS.md` and generate the pointer files (delete the interim files); generate `docs/index.json` and `docs/000_DOCUMENTATION_INDEX.md`; write `docs/166_EDITIONS_AND_TIERS_SOP.md`; rewrite `docs/165` to keep the handoff-bundle list and defer agent duties to `AGENTS.md` sections 5-10 by reference; update `docs/160`, `150`; define TEST-ENTRY-004 (prompt, expected report content per 8.3, log file `reports/baseline/cold_agent_test_<package_id>.txt`) and run it once in one tool; add REQ-ENTRY-001..004, REQ-ED-001..003, REQ-LINK-001 with tests and FEAT entries; `CONTRIBUTING.md` and the PR template gain "`python tools/build_editions.py --check` and `python tools/run_all_audits.py` pass" (with `all` documented as the way to regenerate first).

Gate GATE-1: `run_all_audits.py` PASS including `build_editions.py --check`, `edition_audit.py`, `manifest_update.py --check`; the smoke test's negative cases pass (altering a generated region or deleting `tier:` makes the audit exit 1 naming the source); `AGENTS.md` <= 8,192 bytes with every backticked path existing; `docs/001` rules block <= 4,096 bytes; `build_editions.py --check` reports the staged Method Kit total and headroom; `index.json` lists 100% of documents; the first TEST-ENTRY-004 log shows the agent reaching the audits within six calls, reporting mode ORIENT, stating that only `docs/005` and the catalog define `REQ-*` while Normative governance files bind process, and opening no domain guide.

### PHASE-2: Beginner on-ramp and Chat Kit content (8-12 sessions; writing dominates)

Tasks: write `docs/002`, `003`, `004`; write `templates/` (section 9.2) with `derived_from` keys, add `## Required sections` lists to `docs/040` and `docs/070`, add `templates/README.md` with the stage table; implement template heading parity, the cross-tier marker rule, the ID-citation check, the Chat Kit `max_files` and unique-basename rules, and the glossary rule in `edition_audit.py` / `build_editions.py --check` per the ownership table; write `tools/aisop_check.py` with its `CHECKS` table and generate `MANUAL_AUDIT_CHECKLIST.md` from it; build `examples/hello_aisop/` and register it (section 9.5); set `docs/050` and `docs/020` to tier 1 and confirm the Chat Kit is under budget by dry build; rewrite `README.md` with the GENERATED chooser region and `README_START_HERE.md` as the edition-aware intake (section 6); for each chat product the owner can test (at least one), record whether a `.zip` attaches, whether attached files are read whole or on demand, and the per-message file cap, in `docs/004` and `KNOWN_LIMITATIONS.md` (resolves QUESTION-001); add `first_session_report.yml`; add REQ-BEG-001, REQ-TPL-001, REQ-EX-001 and tests; update KNOWN_LIMITATIONS (lower tiers are lossy, full documents win).

Gate GATE-2: `build_editions.py --check` and `edition_audit.py` PASS with the Chat Kit under 122,880 bytes and `max_files`, zero unmarked cross-tier links from tier <= 1 documents, template parity green, glossary rule green; `build_editions.py zips --edition chatkit --dry-run` lists only tier <= 1 files plus fixed files, equal to `EDITION_INFO.md`, with no root `CHANGELOG.md` / `KNOWN_LIMITATIONS.md`, and every path cited inside the staged kit resolves or is marked; `aisop_check.py --root examples/hello_aisop` prints `SUMMARY: PASS`; the scripted cold-chat session passes: the owner types only (a) the Chat Kit opener verbatim, (b) the prompts verbatim, (c) one sentence of idea; any other message is a logged intervention; the session completes steps 1-3 of `docs/002` with zero interventions and the model never asks for a file the kit lacks; the log, with each intervention listed as a `docs/002` failure-branch item to add, is committed under `reports/baseline/`.

### PHASE-3: Multi-edition release flow (4-6 sessions)

Tasks: finish `build_editions.py zips` (section 7.3: `EDITION_INFO.md`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt` with content checksums, fixed `ZipInfo`, edition root folders per 5.3); `release_package.py --edition all` delegates and runs `archive_name_audit` per archive; implement `tools/bump_release.py` (rewrites `package_id` and `version` only); move `package_id` to the new identity (DECISION-004) in one dedicated commit with audits before and after; add `.github/workflows/release.yml` (tag `v*` -> audits -> build -> attach `dist/*`; `gh release upload` documented as the manual fallback); update `docs/100` and `docs/160`; add REQ-ED-004, REQ-REL-003 and tests; commit `reports/baseline/` snapshots; cut `v0.3.0`; README links point at latest-release asset URLs.

Gate GATE-3: pushing a `v*` tag yields a release with exactly `<pid>.zip`, `<pid>_method.zip`, `<pid>_chatkit.zip`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt`; `archive_name_audit` passes on every downloaded zip; each zip's sha256 matches the download line of the checksum file; a local `build_editions.py zips` on the same tag reproduces the content checksums; `run_all_audits.py` PASS before and after `bump_release.py`.

### PHASE-4: Cold-agent validation and the application layer (4-6 sessions plus ~1 hour per release)

Tasks: extend TEST-ENTRY-004 to two different agentic tools per release, with the log committed under `reports/baseline/` and `edition_audit` WARNing when it is missing for the current package_id. Optionally (only if the Phase 2 session shows beginners stalling at scaffolding): `templates/project_seed/`, `tools/new_project.py` (copies the seed into a validated `yyyymmdd_00_description` folder, writes the new project's `AGENTS.md` from the card, runs `aisop_check.py`), `tests/test_new_project.py`, REQ-SEED-001. Update `docs/160` with the quarterly routine (run audits, re-run the cold-agent test on current tool versions, review budgets, prune nothing without a Superseded entry).

Gate GATE-4: two logged cold-agent runs with the required report shape for the current package_id; if the scaffold shipped, `tests/test_new_project.py` passes inside `run_all_audits.py` (scaffold into a temp dir, lite audit PASS, bad name rejected).

### PHASE-5: Domain packs and the worked practice branch (optional, parallelizable, one PR per guide)

Tasks: for each of `docs/170`, `180`, `185`, `190`, `195`: re-fence every code block (the single-closer fix is not enough), remove chat residue, add `## TL;DR` and `topics`, generalize first-person-plural voice and label project-specific examples as examples; the same TL;DR/topics pass for `docs/010` and the other domain guides; decide the `RULE-*` namespace (register in the document-control conventions or rename); move embedded code to `examples/<pack>/` over time; create an "AISOP applied" practice branch (a tiny real project seeded from the templates with its own REQ/FEAT/TEST) linked from `docs/002`; `templates/monolithic_prototype_template.py` run by the smoke test; skills packaging of the card (`skills/aisop/SKILL.md` carrying both the skill loader keys and the document-control keys) only if the owner uses a tool that loads skills.

Gate GATE-5: fence parity passes for every `docs/*.md` with no WARN entries; `index.json` shows `summary` and `topics` for 100% of documents; the practice branch passes `run_all_audits.py` on its own tree; the TEST-ENTRY-004 re-run on the tag shows the agent did not open a domain guide for a non-domain task.

## 12. Proposed Requirements, Features, and Tests

Proposed IDs; registered in `docs/005`, `ACCEPTANCE_TEST_PLAN.md`, `FEATURE_INVENTORY.md`, the matrix, and the catalog in the phase that implements them (each new ID is five hand-written rows until DECISION-011 is revisited). Existing IDs are never renumbered; REQ-LIC-001 keeps its ID with new text.

| Requirement | Statement (short) | Test | Feature | Phase |
|---|---|---|---|---|
| REQ-LIC-001 (rewritten) | License file named in config present; NOTICE consistent. | TEST-LIC-001 (rewritten) | FEAT-014 Superseded by FEAT-030 "Resolved MIT license and NOTICE consistency" | 0a |
| REQ-CI-002 | CI runs on the configured default branch and on pull requests. | TEST-CI-002 | FEAT-010 (extended) | 0a |
| REQ-REL-002 | Release root derives from `package_id`, never from the clone folder name; edition roots are `<package_id>_<edition>`. | TEST-REL-002 | FEAT-016 (extended) | 0b |
| REQ-RPT-001 | Runtime reports are not committed; baseline snapshots are committed per release. | TEST-RPT-001 (`git ls-files` shows no `reports/*.txt`) | FEAT-008 (extended) | 0b |
| REQ-MAN-001 | `PACKAGE_MANIFEST.md` is verified against the tree by `manifest_update.py --check` in `run_all_audits.py`. | TEST-MAN-001 | FEAT-031 | 0b |
| REQ-RPT-002 | One canonical final package report format (fifteen fields), referenced by every SOP that mentions delivery. | TEST-RPT-002 (grep) | FEAT-032 | 0c |
| REQ-PROF-001 | Operating instructions contain no personal biography; the user profile is a template plus an optional local file. | TEST-PROF-001 (extended personal-reference scan) | FEAT-033 | 0d |
| REQ-DOC-004 | Every `docs/*.md` has balanced code fences. | TEST-DOC-004 | FEAT-003 (extended) | 0e |
| REQ-ENTRY-001 | `AGENTS.md` exists, is Normative with a full header, <= 8,192 bytes, cites only existing paths, states the normative rule and the mode selector. | TEST-ENTRY-001 | FEAT-034 | 1 |
| REQ-ENTRY-002 | Pointer files exist for the declared tools and reference `AGENTS.md`. | TEST-ENTRY-002 | FEAT-034 | 1 |
| REQ-ENTRY-003 | Generated regions, pointer files, and `docs/index.json` are fresh (`--check`). | TEST-ENTRY-003 | FEAT-035 | 1 |
| REQ-ENTRY-004 | Cold-agent protocol verified manually per release; transcript kept with the expected report content. | TEST-ENTRY-004 (manual) | FEAT-034 | 1 (one tool), 4 (two tools) |
| REQ-ED-001 | Every document declares `tier` and `summary`. | TEST-ED-001 | FEAT-036 | 1 |
| REQ-ED-002 | Editions declared in `config/editions.json` with byte budgets, `max_files`, and openers; built by one stdlib tool. | TEST-ED-002 | FEAT-036 | 1 |
| REQ-ED-003 | `docs/001` <= 8 KB with a rules block <= 4 KB; its report labels equal the template's; it is the single source of the core rules. | TEST-ED-003 | FEAT-037 | 1 |
| REQ-ED-004 | Every edition zip obeys the naming rule, contains `EDITION_INFO.md`, and reproduces its content checksums. | TEST-ED-004 | FEAT-038 | 3 |
| REQ-LINK-001 | Every relative link and backticked repo path resolves in the tree, and in each staged edition except on lines marked for a higher edition. | TEST-LINK-001 | FEAT-039 | 1 |
| REQ-TPL-001 | Templates declare `derived_from`, keep heading parity with their SOP, and use placeholder IDs only. | TEST-TPL-001 | FEAT-040 | 2 |
| REQ-BEG-001 | Beginner guide, glossary, and editions guide exist within their budgets; the glossary covers every ID family in tier <= 2 and the seeded terms. | TEST-BEG-001 | FEAT-041 | 2 |
| REQ-EX-001 | Registered example packages pass the lite audit inside their root and carry their own identity per section 9.5. | TEST-EX-001 | FEAT-042 | 2 |
| REQ-REL-003 | Release assets are built only from a green audit run of the tagged commit. | TEST-REL-003 | FEAT-038 | 3 |
| REQ-SEED-001 (optional) | Scaffold output passes the lite audit and the naming rule. | TEST-SEED-001 | FEAT-043 | 4 |

## 13. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | Contributors or agents hand-edit a generated file or region; the edit is lost or the file drifts. | High | Medium | GENERATED banner naming the source; `--check` in CI; MODIFY-AISOP mode requires `--check` before delivery; PR template checkbox names `--check`. |
| RISK-002 | Budget creep: each helpful document is set to a low tier until an edition no longer fits. | Medium | High | WARN at 75%, FAIL at 100% listing the largest offenders; policy "raise the tier, not the budget"; a budget change needs a CHANGELOG entry and a changed acceptance text; section 9.6 projections re-measured at every gate. |
| RISK-003 | File-level tiering feels coarse and tempts condensed copies (the classic drift source). | Medium | High | Accepted deliberately: short tier-1 documents and templates carry the method; if a long SOP truly needs a short form, split it into two source documents with different tiers. |
| RISK-004 | `AGENTS.md` goes semantically stale (protocol says X, `docs/165` says Y) even though its paths and size pass. | Medium | High | Rules region generated from `docs/001`; `docs/165` defers to `AGENTS.md` by reference; TEST-ENTRY-004 per release with an expected report content. |
| RISK-005 | Agent-tool conventions change and a pointer stops being auto-loaded, or a native reader starts double-loading. | Medium | Low | `AGENTS.md` is tool-agnostic; pointers exist only for tested tools; README gives the fallback sentence that works in any tool; KNOWN_LIMITATIONS records it. |
| RISK-006 | Generalizing `docs/020` strips the opinionated voice that made it effective for the owner. | Low | Medium | Nothing is deleted: preferences move to the profile template as a labelled example, and the owner's own gitignored `USER_PROFILE.md` restores the behaviour locally. |
| RISK-007 | The package_id rename touches ~60 headers and masks real edits. | Medium | Medium | One dedicated commit produced by `bump_release.py` (which never touches `revision` or `last_updated`), audits before and after, nothing else in that commit. |
| RISK-008 | Token estimates (bytes/4) mislead for some models or chat products; a "fits in chat" claim fails. | Medium | Medium | Bytes are the hard number; WARN at 75%; the Chat Kit sits near 85% by arithmetic (9.6); the Phase 2 and Phase 4 logged sessions catch real failures; KNOWN_LIMITATIONS states the approximation. |
| RISK-009 | Manual tests (cold-agent, cold-chat) get skipped under time pressure. | High | Medium | Release-gate items in `docs/100` and `docs/160`; the log file is committed per package_id; `edition_audit` WARNs when it is missing. |
| RISK-010 | Scope creep: domain-pack work, skills, and the scaffold delay the simpler goal. | High | Medium | Phases 0 and 1 alone deliver the core ask; Phases 4-5 items are explicitly optional and parallelizable; Phase 0 is sliced so `master` goes green in the first session. |
| RISK-011 | Source hygiene accidentally changes meaning in a normative SOP. | Low | High | The mechanical commit (0e task 11) must satisfy a scripted diff rule; content fixes are a separate, revisioned commit. |
| RISK-012 | Clone folder `AISOP` vs package_id root confuses zip traders. | Low | Low | `release_package.py` prints both names; `docs/004` and README explain the convention in one sentence; `archive_name_audit` remains the proof. |
| RISK-013 | The maintainer's time (a few hours a month) stretches the calendar so far that the interim `AGENTS.md` and half-done tiers become the de facto state. | High | Medium | Phase 0 slices merge independently; the interim entry file is honest about its status; Phase 1 is the only slice that must land before the link is advertised. |

## 14. Decisions Needed From the Owner

Each has a recommendation; the plan proceeds on the recommendation unless the owner says otherwise. Answered items move to the `## Decision Log` in `WORKPLAN_CURRENT_RUN.md`.

| ID | Decision | Recommendation | Why |
|---|---|---|---|
| DECISION-001 | Default branch: keep `master` or rename to `main`. | Keep `master` for now; CI runs on both. Rename later if ever, before external links accumulate. | Zero-risk now; a rename is reversible plumbing. |
| DECISION-002 | Which agentic tools get pointer files. | `CLAUDE.md` and `GEMINI.md`; none for tools that read `AGENTS.md` natively; the list is one line in `editions.json`. | An untested pointer is drift waiting to happen; a redundant one double-loads. |
| DECISION-003 | Canonical final package report. | The `docs/070` section 18 fifteen-field format; the card states the labels inline; `AGENTS.md` references the template. | Removes a documented contradiction; a tier-0 user has no template file. |
| DECISION-004 | New package identity and when to bump. | `yyyymmdd_00_aisop` at the first tiered release (Phase 3), not in Phase 0. | Keeps Phase 0 small; the bump is one scripted commit. |
| DECISION-005 | Where the owner's real profile lives. | Gitignored `USER_PROFILE.md`; the tracked template carries a fictional example only. | Nothing personal in the tree; nothing lost locally. |
| DECISION-006 | `docs/010` and `docs/055` tier. | Tier 3 for both. | `010` is a Windows lab-instrument install guide; `055` is a 34 KB code example that `050` already describes; both would push the Method Kit over 90%. |
| DECISION-007 | Chat Kit target and delivery. | 120 KB text; ships as a zip and must also work as a flat set of individually uploaded files; the card covers products without upload; per-product facts recorded in Phase 2. | Not every chat product accepts a zip; the flat form costs only a unique-basename rule. |
| DECISION-008 | Worked example flavour. | Neutral `hello_aisop` (a small file-processing utility) for Phase 2; a DAQ-flavoured example can be a Phase 5 practice branch. | Beginners should not meet hardware safety on day one. |
| DECISION-009 | GitHub Action for release-asset upload. | Yes, as CI plumbing; `gh release upload` documented as the manual fallback. | The stdlib rule is about package tooling, not CI. |
| DECISION-010 | Domain guides: stay in place with `tier: 3`, or move to `docs/reference/`. | Stay in place. | No broken links or bookmarks; tier tags already hide them from lower editions. |
| DECISION-011 | Generate the traceability matrix from the catalog. | Defer until after Phase 3, then revisit: each new ID currently costs five hand-written rows. | It forces a catalog schema migration unrelated to tiers. |
| DECISION-012 | Normative status of the core-method SOPs and the root files. | Promote `docs/001` and `AGENTS.md` to Normative; leave `030`-`070` Informative with `docs/001` as the binding method summary; review the thirteen Normative root files in Phase 1 and demote the ones that are not procedure or policy. | Agents get one binding method summary alongside the existing Normative governance set, and the Normative label regains its meaning. |
| DECISION-013 | Manual acceptance testing per release. | Two cold-agent runs and one scripted cold-chat run, logged; roughly one hour. | Without it the entry layer rots silently. |
| DECISION-014 | Method Kit headroom. | Keep 409,600 bytes; if the Phase 2 dry build lands above 90%, raise the budget to 524,288 bytes through the RISK-002 process rather than thinning the kit. | The projection in 9.6 is 92% before any trimming; a deliberate raise beats silent creep. |
| QUESTION-001 | Which chat products and plans does the intended lower-tier audience actually use, and do they allow zip upload? | Answered inside Phase 2 for every product the owner can test; recorded in `docs/004`. | - |
| QUESTION-002 | Which agentic tools does the owner use today? | Determines the pointer list and the TEST-ENTRY-004 tool pair. | - |

## 15. What Not To Do

- Do not hand-maintain condensed or "lite" versions of any SOP, in any folder; split the source instead.
- Do not add section-level transclusion markers to normative prose.
- Do not write a long `AGENTS.md`; if it does not fit in 8 KB it belongs in `docs/166` or the index, never in `docs/165` (which defers to `AGENTS.md`).
- Do not embed the repository map or exact byte counts in `AGENTS.md` or `docs/index.json`.
- Do not implement the same check in two tools (section 7.4 is the ownership table).
- Do not commit `dist/` or regenerated `reports/*.txt` again; do not let audits write into tracked files.
- Do not let any phase gate depend on outside volunteers.
- Do not make domain guides normative or put any of them into the Chat Kit or Method Kit.
- Do not renumber or rename existing `docs/NNN` files or any REQ/FEAT/TEST ID; extend, supersede, rewrite text under the same ID.
- Do not adopt mkdocs, Sphinx, pandoc, PyYAML, Jinja, pre-commit frameworks, or any non-stdlib dependency for building or auditing.
- Do not rename the default branch as a prerequisite for anything.
- Do not rewrite the tier-3 guides for tone as part of this program; TL;DR additions and re-fencing are one PR per guide.
- Do not describe any specific person in the third person in any tracked document.
- Do not make AISOP itself depend on git, a terminal, or Python at tier 0-1: the card must work with zero tooling, every template and checklist must be usable by hand, and the manual checklist must be generated from the lite audit so the two cannot diverge. Running the user's own prototype is the user's program, not AISOP tooling; `docs/002` tells a beginner the minimum needed to run it.
- Do not ship anything imitable in the worked example that a real package should not contain.

## 16. Effort and Sequencing Summary

| Phase | Delivers | Sessions (~4 h) | Depends on |
|---|---|---|---|
| 0a-0e | Green audits in any clone; CI on the default branch; clean tree after audits; manifest checked; generalized `020`; interim `AGENTS.md`; canonical report; readable `060`/`200` | 6-8 | - (0a-0e merge independently) |
| 1 | Tier headers, editions manifest, build/audit tools, real `AGENTS.md`, index, `docs/165` rewrite, first cold-agent log | 6-8 | 0 |
| 2 | Beginner documents, templates, prompts, worked example, lite audit, edition-aware intake and README, per-product upload facts, Chat Kit under budget | 8-12 | 1 |
| 3 | Reproducible zips, checksums, `bump_release`, new package_id, release workflow, `v0.3.0` | 4-6 | 2 |
| 4 | Two-tool cold-agent validation per release; optional scaffold | 4-6 + ~1 h/release | 1 (validation), 2 (scaffold) |
| 5 | Domain-guide re-fencing and TL;DRs, generalization, example branch, optional skills | open-ended, parallel | 1 |

Minimum viable delivery for GOAL-003 is Phases 0 and 1: 12-16 sessions. Phases 0-4 total roughly 28-40 sessions. At four sessions a month that is three to four months for the minimum and seven to ten months for Phases 0-4; the slicing of Phase 0 exists so that `master` is green and usable from the first session onward.

## 17. Extraction Plan

When approved, sections of this plan move to their permanent homes and this document is marked Superseded (not deleted) with a dated note; it is tier 3 from the start.

| Section of this plan | Extracts to | Phase |
|---|---|---|
| 3.2 Drift register | `CHANGELOG.md` REV-003 Phase 0 entries; `WORKPLAN_CURRENT_RUN.md` | 0 |
| 5, 7 | `docs/166_EDITIONS_AND_TIERS_SOP.md` (Normative) and `config/editions.json` | 1 |
| 6 | `docs/166` "Repository layout" section | 1 |
| 8 | `AGENTS.md`; `docs/165` (agent duties by reference) | 1 |
| 9 | `docs/001-004`, `templates/`, `examples/hello_aisop/`, `config/editions.json` (openers) | 1-2 |
| 10 | `docs/000_DOCUMENTATION_INDEX.md` tier column (generated); Phase 5 issue list | 1, 5 |
| 11 | Branch notes per `docs/080` on each `practice/rev003-<slice>` branch | each |
| 12 | `docs/005`, `ACCEPTANCE_TEST_PLAN.md`, `FEATURE_INVENTORY.md`, `REQUIREMENTS_TRACEABILITY_MATRIX.md`, `requirements_catalog.json` | each |
| 13 | `KNOWN_LIMITATIONS.md` (LIMIT-005..007) and `docs/160` maintainer playbook | 1-4 |
| 14 | `## Decision Log` section in `WORKPLAN_CURRENT_RUN.md` (created in 0c) | 0 |
| 15 | `docs/166` and `CONTRIBUTING.md` | 1 |
