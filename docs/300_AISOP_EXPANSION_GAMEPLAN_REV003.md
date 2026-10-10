---
document_id: DOC-300
title: "AISOP Expansion Gameplan (REV-003): Tiered Editions and Agent-First Entry"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-10-10
package_id: 20260516_00_seed
machine_reference_prefix: DOC-300
normative_status: Informative
source: "REV-003 planning run: corpus audit of all reference documents plus three judged architecture proposals"
---

# AISOP Expansion Gameplan (REV-003)

## 0. Document Control

| Field | Value |
|---|---|
| Status | Proposed. Nothing in this plan is implemented yet. |
| Decision owner | Repository maintainer |
| Shape | Follows `docs/040_MONOLITHIC_PLANNING_DOCUMENT_SOP.md`: one planning document now, with an extraction plan (section 17) naming which sections later become SOPs, config, and tools. |
| How it was produced | (1) Every document under `docs/` was read in full and classified for audience, tier placement, reusable templates, stale or personal content, and agent-facing rules. (2) Three independent architecture proposals were written from a beginner-first, an agent-first, and a maintainer-first lens. (3) Three independent judges scored all proposals on beginner usability, agent time-to-competence, drift resistance, maintenance cost, doctrine compatibility, and implementation risk. The maintainer-first skeleton won unanimously; the beginner and agent conveniences that cost files rather than mechanisms were grafted onto it, and every fatal flaw the judges found is resolved in this document. |
| Normative weight | Informative until the owner approves it; approved items then land as `REQ-*` / `FEAT-*` / `TEST-*` entries in the controlled documents (section 12). |
| Supersedes | The "Next Recommended Run" paragraph in `WORKPLAN_CURRENT_RUN.md` (split into a starter edition plus a technical appendix). |

## 1. Executive Summary

AISOP already contains the method. What it lacks is a way in that matches the reader's tooling. This plan turns the single repository into **one source tree that produces four editions**, each matched to a context budget and a kind of user, without ever maintaining a second copy of any document:

```text
Tier 0  CARD        one file, <= 8 KB    paste into any chat                 (free / limited plans)
Tier 1  CHAT KIT    zip, <= 120 KB       upload into a chat session           (chat-only plans)
Tier 2  METHOD KIT  zip, <= 400 KB       full method + tools, no domain guides (agentic tools, lean)
Tier 3  FULL        git clone / zip      everything, navigated by map          (agentic tools, maintainers)
```

Membership is one integer in the document-control header every file already carries (`tier:`), budgets live in one JSON file, and a single standard-library script builds the editions and refuses to build if anything drifted. An agent pointed at the repository URL auto-loads an `AGENTS.md` under 8 KB that states what is normative, what to read first, which of three modes it is in, and how to report; every other agent tool reaches the same file through a three-line pointer.

The work is six phases. **Phase 0 (one to two days) makes the existing audits green and gives agents a landing file today.** Phases 0 and 1 together already deliver the owner's core ask: a link that an agent can be handed. Phases 2 to 5 add the beginner on-ramp, the release flow, cold-agent validation, and the optional domain packs.

## 2. Goals and Non-Goals

### 2.1 Goals (owner's statement, restated as outcomes)

| ID | Goal | Measured by |
|---|---|---|
| GOAL-001 | Multiple avenues into AISOP: a zip for lower-tier chat subscriptions and a structured local folder for higher-tier agentic subscriptions. | Four editions built from one tree, each within its budget, each with its own start-here file. |
| GOAL-002 | AISOP serves people who are just beginning with AI agents. | A plain-language beginner path with failure branches, paste-ready prompts, a worked example package, and a glossary, all inside the Chat Kit. |
| GOAL-003 | Handing someone the repository link is enough for their agent to get up to speed quickly. | A cold agent given only the URL reaches a running audit and a correct statement of what is normative in at most six tool calls (TEST-ENTRY-004). |
| GOAL-004 | The package keeps demonstrating the discipline it teaches. | Every new rule lands as REQ/FEAT/TEST with a traceability row; `run_all_audits.py` passes on a fresh clone of any folder name. |

### 2.2 Non-goals for REV-003

- No editorial rewrite of the 500 KB of domain technical guides (docs/170-290). They receive header keys, a TL;DR, and the removal of chat residue only.
- No new dependencies. Build and audit tooling stays Python standard library; CI plumbing may use a GitHub Action to attach release assets, with a documented manual fallback.
- No second repository, no branch per edition, no wiki as a source of truth.
- No renumbering of existing `docs/NNN` files and no deletion of existing REQ/FEAT/TEST IDs.

## 3. Current Baseline

### 3.1 What exists

- ~28,000 lines of Markdown (~750 KB of prose; the 2.3 MB repository size includes `.git` and reports). Every document carries a nine-key document-control header. Requirements, features, and tests use `REQ-*`, `FEAT-*`, `TEST-*` IDs tied together by a traceability matrix and a JSON catalog (22 requirements, 19 features, 22 tests).
- Core method: `docs/020-070` (operating instructions, concept brief, planning document SOP, prototype SOP and example, migration SOP, zip review and handoff SOP). Governance: `docs/080-165` (ten short SOPs). Domain reference: `docs/010` and `docs/170-290` (fifteen long guides on Windows setup, compatibility, DAQ, QC, embedded platforms, pygame, MIDI, LabJack, I2C, Android, networking, GUI design).
- Stdlib tooling: seven audit/release scripts under `tools/`, one smoke test, CI that runs `tools/run_all_audits.py`.
- GitHub state: default branch `master`; no tags, no releases, no issues; two open Dependabot pull requests whose CI is red because of DRIFT-001 below.

### 3.2 Drift register (verified by running the audits on this clone)

| ID | Drift | Effect today |
|---|---|---|
| DRIFT-001 | `LICENSE_DECISION_REQUIRED.md` was deleted and MIT `LICENSE.txt` added, but `tools/package_structure_audit.py`, `tools/repo_health_audit.py`, `config/package_metadata.json`, REQ-LIC-001 / TEST-LIC-001, the traceability matrix, `README.md`, and `KNOWN_LIMITATIONS.md` still require or describe the license gate. | `run_all_audits.py` FAILS on every clone and every PR. |
| DRIFT-002 | `tools/release_package.py` hard-codes the expected root folder `20260516_00_seed`; a GitHub clone is named `AISOP`. | Release dry run FAILS in any clone. |
| DRIFT-003 | `.github/workflows/ci.yml` triggers on push to `main`; the default branch is `master`. | CI never runs on pushes to the default branch (only on PRs). |
| DRIFT-004 | `reports/*.txt` are committed and rewritten with a new timestamp on every audit run. | Every audit run dirties the tree; agents and contributors commit noise. |
| DRIFT-005 | `docs/020` is a lightly cleaned personal system prompt: it describes one specific person in the third person and states personal preferences (UI colour scheme, legacy-target defaults) as universal rules, while its own line 16 claims to be project-neutral. | Contradicts the beginner audience; the personal-reference scan only catches names. |
| DRIFT-006 | No agent-native entry file exists (`AGENTS.md`, `CLAUDE.md`, or equivalent). | An agent handed the link has no deterministic first file. |
| DRIFT-007 | Six long documents have an unclosed code fence near the top (`060` L145, `170` L78, `180` L107, `185` L54, `190` L70, `195` L47), so 90-95% of each renders as one code block on GitHub and inside chat uploads; most long docs also end with an orphan line that is the heading of the next document in the original source, plus leftover chat-reply fragments. | The largest single barrier to the chat-upload avenue; models read these files as code, not prose. |
| DRIFT-008 | The method documents disagree with each other and with the repository on names: three different package-report formats (`020` ten items, `070` section 18 fifteen items, `070` section 21 checklist), `FEATURE-nnn` vs `FEAT-*`, `ACCEPT-nnn` vs `TEST-*`, `tools/package_smoke_test.py` and `tools/diagnostic_harness.py` (do not exist) vs `tests/smoke_test.py`, `test_reports/` vs `reports/`, `project/logging.py` (shadows the stdlib) vs `logging_utils.py`, and a per-project `docs/` numbering that reuses AISOP's own numbers with different meanings. | An agent following one SOP emits IDs and filenames the audits do not recognise. |

### 3.3 Corpus classification (summary; full table in section 10)

- **Must-read for an agent applying AISOP to a new project:** `020`, `030`, `040`, `050`, `060`, `070` (and the governance SOPs when modifying AISOP itself).
- **Starter-worthy but long:** `030` (658 lines), `040` (855), `060` (1098), `070` (812) are forms and checklists interleaved with worked examples from one legacy project. Their reusable skeletons (about 60 distinct templates were identified) are what a beginner actually needs.
- **Domain packs, never in the lower tiers:** `010`, `170-290`. They group naturally into seven packs (section 10.3).
- **Genuinely short core docs that already fit a chat kit:** `050` (11 KB) and a generalized `020` (~12 KB).

## 4. Design Principles

| ID | Principle | Consequence |
|---|---|---|
| PRIN-001 | One tree. A fact is edited in exactly one place. | No condensed copies, no `docs-lite/`, no branch per edition. |
| PRIN-002 | File-granular tiers. A document is in an edition or it is not. | No section-level transclusion markers inside normative prose (the judges identified markers as the most likely future drift source). Short tiers come from short documents. |
| PRIN-003 | Generated means checked. Every generated file is produced by one stdlib script and verified by `--check` in `run_all_audits.py` and CI. | Hand-editing a generated file turns CI red with a message naming the source to edit. |
| PRIN-004 | Byte budgets are the enforced truth; token counts are estimates. | Budgets in `config/editions.json`; audit fails listing the largest offenders. Policy: raise the tier of a document, not the budget. |
| PRIN-005 | Normative vs informative is stated explicitly to agents. | Binding = `docs/005` + `requirements_catalog.json` + documents whose header says `normative_status: Normative`. Domain guides are informative, never requirements. |
| PRIN-006 | Both avenues stay first-class. | Every release ships zips whose basename equals the internal root; the clone folder name is a working-copy convention and the package_id is the handoff identity. |
| PRIN-007 | Every new rule is traceable. | New behaviour = REQ + FEAT + TEST + matrix row, in the same change. |
| PRIN-008 | Gates are maintainer-runnable. | No acceptance gate depends on outside volunteers; dogfood sessions are owner-run and logged under `reports/baseline/`. |
| PRIN-009 | Nothing is deleted, only superseded. | IDs are marked Superseded/Rejected; `docs/NNN` numbers never change. |

## 5. The Four Editions

### 5.1 Edition table

| Tier | Name | Audience | Delivery form | Hard budget | Contents (cumulative) | How a human starts | How an agent enters |
|---|---|---|---|---|---|---|---|
| 0 | **Card** | Anyone with any chat product, including free tiers and custom-instruction boxes; also the rule block every agent entry embeds. | `AISOP_CARD.md` (release asset, rendered from `docs/001_AISOP_CORE_RULES.md`); also shown in README under "copy this". | 8,192 bytes for the card; the rules block itself <= 5 KB so `AGENTS.md` has room. | What AISOP is (three sentences); the practice-space loop in one diagram; the core rules (about twelve, imperative); the minimum package skeleton and the naming rule; the ID discipline in one paragraph; the delivery report format by reference; where the next tier is. | Copy the card into the chat's system prompt or first message, then describe the idea. No download, no Python. | The chat model receives the card as instructions; it must ask for or inspect current files, produce a feature inventory before changing code, deliver complete files plus a CHANGELOG entry, and name the AISOP version it follows. |
| 1 | **Chat Kit** | Chat-only subscriptions with upload but no filesystem or shell; beginners who want prompts and templates rather than tooling. | `<package_id>_chatkit.zip` on every release. | 122,880 bytes of text (target 90-100 KB). | Card; `README_START_HERE.md`; `docs/002` beginners guide (<= 12 KB, five steps each with "what you say / what the AI should produce / how you know it worked / what to do if it did not"); `docs/003` glossary; `docs/004` editions and upgrade path; generalized `docs/020`; `docs/050`; `templates/` (user profile, planning document, README_START_HERE, CHANGELOG, FEATURE_INVENTORY, KNOWN_LIMITATIONS, final package report, handoff bundle, manual audit checklist keyed to TEST-* IDs, first-session prompts); `examples/hello_aisop/` (complete tiny package the model can imitate); `tools/aisop_check.py` (one stdlib file, `--explain` prints the checklist so a model that cannot run Python applies it by hand); `LICENSE.txt`, `NOTICE.md`; generated `EDITION_INFO.md`. Deliberately excludes AISOP's own CHANGELOG and KNOWN_LIMITATIONS (they describe this package, not the user's). | Download the zip from the latest release, upload it, paste the one-line opener printed in README, then pick prompt 01. | Reads `EDITION_INFO.md` (exact file list, so it never asks for a file the kit lacks), then `README_START_HERE.md`, then the card. Operates in APPLY mode only; `EDITION_INFO.md` says MODIFY-AISOP needs the Method Kit. |
| 2 | **Method Kit** | Agentic tools (Claude Code, Codex CLI, Cursor, Copilot agents, Gemini CLI) with a filesystem; practitioners who want the full method and audit tooling but not ~500 KB of domain guides; offline reviewers. | `<package_id>_method.zip` on every release, or the clone with tier-3 files ignored. | 409,600 bytes of text (measured today: ~270 KB). | Everything in tier 1; all root intake and governance files; `docs/000-070` in full; `docs/080-166`; `requirements/`, `config/`, `tools/`, `tests/`, `reports/README.md` + `reports/baseline/`; `.github/`; `AGENTS.md` and pointer files; `docs/index.json`. | Unzip or clone, open the folder in the agentic tool, type the opener printed in README ("Read AGENTS.md and follow its first-five-minutes protocol"). | `AGENTS.md` auto-loads (or its pointer does). Runs the audits, reads `README_START_HERE.md` and the tier 0-1 part of the index, chooses a mode, loads that mode's reading set. |
| 3 | **Full** | Higher-tier agentic subscriptions, maintainers, contributors, and anyone whose project touches the domain guides. | The GitHub repository (branches = practices, tags = audited states) and `<package_id>.zip`. | Unbudgeted on disk; budgeted in use: `AGENTS.md` forbids loading domain guides wholesale and allows one per task, chosen from the index summaries. | Everything in tier 2; `docs/010` and `docs/170-290` with `summary`, `topics`, and a TL;DR; `docs/999`; git history and practice branches. | `git clone`, same opener as tier 2. README says when this tier is worth it and that it is not the beginner path. | Same protocol as tier 2; DOMAIN-LOOKUP mode reads exactly one guide, TL;DR first. |

### 5.2 Upgrade path

Higher tiers are strict supersets with identical file names and IDs. `docs/004` states this and tells each tier what the next one adds. Moving from the Method Kit to Full is a `git clone`; nothing has to be re-learned. Every lower-tier artifact carries one line: "the full documents win on conflict" and a `derived_from` pointer where applicable, so a chat model has a citation target instead of inventing a parent SOP.

## 6. Repository Layout After REV-003

```text
AISOP/                                  clone folder name is irrelevant; package_id lives in config/
|-- AGENTS.md                           HAND (<= 8 KB) with two GENERATED regions (rules, commands)
|-- CLAUDE.md                           pointer: header + "@AGENTS.md" import line + "read AGENTS.md first"
|-- GEMINI.md                           pointer (only generated for tools the owner actually uses)
|-- .cursor/rules/aisop.mdc             pointer with alwaysApply: true
|-- .github/
|   |-- copilot-instructions.md         pointer
|   |-- workflows/ci.yml                push: [master, main] + pull_request
|   |-- workflows/release.yml           NEW: on tag v*: audits -> build editions -> attach assets
|   |-- ISSUE_TEMPLATE/first_session_report.yml   NEW: beginner feedback channel (not a gate)
|   `-- (existing templates, dependabot, package_audit, release_dry_run)
|-- README.md                           HAND: "pick your avenue" chooser with the exact first prompt per tier
|-- README_START_HERE.md                HAND: universal intake; gains "which edition am I holding?"
|-- CHANGELOG.md  FEATURE_INVENTORY.md  ACCEPTANCE_TEST_PLAN.md  KNOWN_LIMITATIONS.md  WORKPLAN_CURRENT_RUN.md
|-- REQUIREMENTS_TRACEABILITY_MATRIX.md HAND (generation deferred; see DECISION-011)
|-- PACKAGE_MANIFEST.md                 GENERATED (unchanged role)
|-- CONTRIBUTING.md SECURITY.md SAFETY.md SUPPORT.md NOTICE.md CODE_OF_CONDUCT.md CITATION.cff LICENSE.txt
|-- USER_PROFILE.md                     LOCAL, gitignored: the owner's (or any user's) real profile
|-- config/
|   |-- package_metadata.json           package_id, version, revision, license_file, default_branch,
|   |                                   required files/dirs (audits read from here, no duplicated lists)
|   `-- editions.json                   NEW: editions, tier cutoffs, byte budgets, fixed file lists, pointer list
|-- requirements/requirements_catalog.json
|-- docs/
|   |-- index.json                      GENERATED: path, bytes, est_tokens, tier, normative_status, topics, summary
|   |-- 000_DOCUMENTATION_INDEX.md      GENERATED from headers, grouped by tier
|   |-- 000_USER_GUIDE_OVERVIEW.md      tier 1
|   |-- 001_AISOP_CORE_RULES.md         tier 0  NEW, HAND, normative, <= 8 KB (rules block <= 5 KB)
|   |-- 002_BEGINNERS_GUIDE_TO_AI_AGENTS.md   tier 1  NEW
|   |-- 003_GLOSSARY.md                 tier 1  NEW
|   |-- 004_EDITIONS_AND_UPGRADE_PATH.md     tier 1  NEW
|   |-- 005_PRODUCT_REQUIREMENTS.md     tier 2
|   |-- 010_WINDOWS_...                 tier 3 (reclassified as domain reference; file not renamed)
|   |-- 020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md   tier 1 (generalized in Phase 0)
|   |-- 030, 040, 055, 060, 070         tier 2 (core method; content unchanged beyond hygiene)
|   |-- 050_MONOLITHIC_PROTOTYPE_CODE_SOP.md  tier 1
|   |-- 080 ... 165                     tier 2 (governance)
|   |-- 166_EDITIONS_AND_TIERS_SOP.md   tier 2  NEW, normative: tiers, budgets, generated files, release assets
|   |-- 170 ... 290                     tier 3 (domain guides; header keys + TL;DR + residue removal only)
|   |-- 300_AISOP_EXPANSION_GAMEPLAN_REV003.md   this document (tier 2)
|   `-- 999_SOURCE_CLEANUP_NOTES.md     tier 3
|-- templates/                          NEW, HAND, tier 1; each carries derived_from: DOC-0xx
|   |-- USER_PROFILE_TEMPLATE.md        fill-in fields + one labelled fictional example
|   |-- PLANNING_DOCUMENT_TEMPLATE.md   derived_from DOC-040 (heading parity audited)
|   |-- README_START_HERE_TEMPLATE.md  CHANGELOG_TEMPLATE.md  FEATURE_INVENTORY_TEMPLATE.md
|   |-- KNOWN_LIMITATIONS_TEMPLATE.md   FINAL_PACKAGE_REPORT_TEMPLATE.md   AGENT_HANDOFF_BUNDLE_TEMPLATE.md
|   |-- MANUAL_AUDIT_CHECKLIST.md       by-hand audits keyed to TEST-* IDs (for chat-only users)
|   |-- FIRST_SESSION_PROMPTS.md        plan this / prototype this / package and report, each < 20 lines
|   `-- ID_RECORD_FORMATS.md            the REQ/RISK/DEBT/DECISION/QUESTION record formats, stated once
|-- examples/
|   `-- hello_aisop/                    NEW, tier 1: complete minimal package with its own package_id
|       |-- README_START_HERE.md CHANGELOG.md FEATURE_INVENTORY.md ACCEPTANCE_TEST_PLAN.md KNOWN_LIMITATIONS.md
|       |-- hello_aisop.py              ~80 lines, --selfcheck, numbered sections per docs/050
|       `-- tools/aisop_check.py        identical to root tools/aisop_check.py (identity audited)
|-- tools/
|   |-- _aisop_common.py                NEW: the one frontmatter parser, shared by every tool
|   |-- build_editions.py               NEW: entry regions | index | zips | all | --check
|   |-- edition_audit.py                NEW: tier/summary keys, budgets, generated freshness, entry size,
|   |                                        cross-tier link rule, template heading parity, package_id consistency,
|   |                                        ID-citation check for tier<=1 docs
|   |-- link_audit.py                   NEW: every relative link and backticked repo path resolves (tree and each staged edition)
|   |-- bump_release.py                 NEW: rewrite package_id/version/last_updated in every header from config
|   |-- aisop_check.py                  NEW: single-file lite audit for downstream packages and the Chat Kit
|   |-- release_package.py              CHANGED: root from config, staged temp dir, --edition all, checksums
|   |-- run_all_audits.py               CHANGED: + new audits, + --quiet (SUMMARY block only, for agents)
|   `-- package_structure_audit.py  repo_health_audit.py  requirements_trace_audit.py  secret_scan_lite.py
|       archive_name_audit.py  manifest_update.py   (CHANGED to read lists from config)
|-- tests/
|   |-- smoke_test.py                   extended: builds every edition in memory, asserts budgets
|   `-- test_new_project.py             Phase 4, optional
|-- reports/
|   |-- README.md                       states that *.txt are runtime output and baseline/ is committed evidence
|   |-- baseline/                       committed per release, incl. cold_agent_test_<package_id>.txt
|   `-- *.txt                           gitignored
|-- src/README.md
`-- dist/                               gitignored: <pid>.zip <pid>_method.zip <pid>_chatkit.zip AISOP_CARD.md EDITIONS_CHECKSUMS.txt
```

## 7. Single-Source Mechanism

### 7.1 Two new header keys

Every Markdown document gains `tier: N` (0-3; the lowest tier that includes it; inclusion is cumulative) and `summary: "one line, <= 200 characters"`. The existing line-based header parser already handles new keys; it moves into `tools/_aisop_common.py` so every tool imports one parser. Domain guides additionally gain `topics: [...]`. A missing `tier` or `summary` is a structure-audit FAIL.

### 7.2 One manifest

`config/editions.json` declares, per edition: name, tier cutoff, hard byte budget, fixed non-document files (root governance files, `tools/`, `tests/`, `requirements/`, `config/`, `templates/`, `examples/`, `.github/`), zip suffix, and the pointer-file list. Changing what an edition contains means editing one integer in a header or one list in this file.

### 7.3 One generator

`tools/build_editions.py` (stdlib: `json`, `re`, `hashlib`, `zipfile`, `pathlib`) with subcommands:

| Subcommand | Produces | Committed? |
|---|---|---|
| `entry` | The two GENERATED regions inside `AGENTS.md` (rules block from `docs/001`; commands block from `editions.json`) and the pointer files. | Yes (tools auto-load them). |
| `index` | `docs/index.json` and `docs/000_DOCUMENTATION_INDEX.md` from headers. | Yes (humans browse the index on GitHub; agents read the JSON). |
| `zips` | `dist/<pid>.zip`, `_method.zip`, `_chatkit.zip`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt`, and an `EDITION_INFO.md` inside each zip. Fixed `ZipInfo` dates from `config.last_updated` so checksums are reproducible. | No (gitignored; attached to releases). |
| `--check` | Regenerates everything in memory and exits 1 on any difference from the committed files, writing nothing. | Runs inside `run_all_audits.py` and CI. |

Generated committed files contain no timestamps, so `--check` is deterministic. Each generated file (or region) starts with a banner: `GENERATED by tools/build_editions.py from <source>; edit the source, not this file`.

### 7.4 Audits that fail loudly

`tools/edition_audit.py` checks: tier/summary presence and range; per-edition byte totals vs budget (lists the five largest documents on failure); generated freshness; `AGENTS.md` <= 8,192 bytes and `docs/001` rules block <= 5,120 bytes; pointer files each <= 1 KB, carry a document-control header, and contain the string `AGENTS.md`; cross-tier link rule (a tier-t document may not link a tier>t document as required reading without an explicit `(method edition)` / `(full edition)` marker on that line); template heading parity (a template's H2 list equals the `## Required sections` list in the SOP named by its `derived_from`); every header's `package_id` equals config (except inside registered example packages, section 9.4); every `REQ-*`/`FEAT-*`/`TEST-*` cited in a tier <= 1 document exists in the catalog; a WARN when no cold-agent log exists for the current package_id.

`tools/link_audit.py` checks that every relative Markdown link and every backticked `docs/...`, `tools/...`, `templates/...` path resolves, across the tree and inside each staged edition (so a Chat Kit never references a file it does not contain).

### 7.5 Hand-written vs generated (explicit list)

- **Hand-written:** every `docs/*.md` except the two index files; all root intake and governance documents; `templates/`; `examples/`; `config/*.json`; `requirements_catalog.json`; all tools; the non-generated regions of `AGENTS.md`.
- **Generated and committed:** the two regions in `AGENTS.md`; pointer files; `docs/index.json`; `docs/000_DOCUMENTATION_INDEX.md`; `PACKAGE_MANIFEST.md`.
- **Generated and not committed:** everything under `dist/`; `reports/*.txt`.

## 8. Agent Entry Design

### 8.1 `AGENTS.md` (hand-written, <= 8 KB, sections fixed)

1. **Identity line:** AISOP version and package_id; "this file is the only thing an agent must read before acting; two regions are generated, edit their sources."
2. **What this repository is** (three sentences) and the two avenues.
3. **NORMATIVE vs INFORMATIVE:** binding = `docs/005` + `requirements_catalog.json` + any document with `normative_status: Normative`. `docs/010` and `docs/170-290` are informative reference, never requirements.
4. **Core rules** (GENERATED from `docs/001`, so the card, the Chat Kit, and the entry file cannot disagree).
5. **First-five-minutes protocol** (section 8.3).
6. **Modes and reading sets:** APPLY (user wants AISOP applied to their own project: `docs/001`, `templates/`, `docs/002` if they are new, then `040/050/060` only when that step is reached); MODIFY-AISOP (`docs/165`, `160`, `166`, `120`; must run `build_editions.py --check` and the audits before delivering; must update CHANGELOG, FEATURE_INVENTORY, requirements, and traceability when behaviour changes); DOMAIN-LOOKUP (read index summaries, open exactly one of `docs/170-290`, TL;DR first). The agent states the chosen mode back to the user in one sentence before touching files.
7. **Commands** (GENERATED): `python tools/run_all_audits.py [--quiet]`, `python tools/build_editions.py --check`, `python tools/release_package.py --dry-run`.
8. **Hard rules:** never hand-edit a GENERATED region or file; never delete a REQ/FEAT/TEST ID (mark Superseded); keep tooling stdlib; every new document's header is complete including `tier` and `summary`; zip basename equals internal root; never read `docs/185` or `docs/195` (60+ KB each) in full unless asked.
9. **User profile rule:** if `USER_PROFILE.md` exists at the root, read it; otherwise ask the six profile questions from `templates/USER_PROFILE_TEMPLATE.md` before planning code.
10. **Delivery:** end every substantial task with the canonical final package report (`templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`, see DECISION-003) and the `run_all_audits.py --quiet` result.

The repository map does **not** live in `AGENTS.md` (the judges showed that embedding it overflows every proposed cap). It lives in `docs/index.json`, which the protocol tells the agent to skim.

### 8.2 Pointer files

`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/aisop.mdc`, `.github/copilot-instructions.md` are generated three-line pointers: a document-control header, an `@AGENTS.md` import line where the tool supports imports, and the sentence "Read AGENTS.md before doing anything, then follow its first-five-minutes protocol." A pointer cannot drift; it costs at most one extra read. Only pointers for tools the owner can test are generated (QUESTION-002); the list is one line in `editions.json`.

### 8.3 First-five-minutes protocol

| Minute | Action | Tokens (est.) |
|---|---|---|
| 0-1 | `AGENTS.md` auto-loads; confirm the package_id and version it states. | ~2k |
| 1-2 | Run `python tools/run_all_audits.py --quiet`. PASS: trust the tree. FAIL: report the failing tool verbatim and stop structural work until understood (a red audit on a fresh clone is a bug to report, not to work around). | ~0.5k |
| 2-3 | Read `README_START_HERE.md`; skim `docs/index.json` entries with tier <= 1. | ~3k |
| 3-4 | Decide the mode from the user's request; load that mode's reading set; read `USER_PROFILE.md` or ask the profile questions. | ~2-4k |
| 4-5 | Report back in the fixed shape: AISOP version loaded, audit result, mode chosen, files read, files intentionally not read, first proposed acceptance-gated step. | ~0.5k |

Budget to competence: roughly 8-10k tokens and five to six tool calls. The minute-5 report is the artifact TEST-ENTRY-004 checks at each release.

### 8.4 Machine-readable index

`docs/index.json`: one record per document with `path`, `document_id`, `title`, `bytes`, `est_tokens` (bytes/4), `tier`, `normative_status`, `topics`, `summary`, and `read_order` for the entry path. An agent decides whether to open a 60 KB guide from the record, not from the file.

## 9. Beginner On-Ramp (Chat Kit content)

### 9.1 New short documents (hand-written, tier 0-1)

| File | Budget | Content |
|---|---|---|
| `docs/001_AISOP_CORE_RULES.md` | <= 8 KB; rules block <= 5 KB | The card. Distilled from `020` (core principles, feature-preservation rule), `070` (golden rule, minimal per-run checklist, what-not-to-do), `050` (freeze-before-refactor sequence), `060` (phase gate), `165` (handoff bundle), `080` (loop). Normative. |
| `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md` | <= 12 KB | What an agent is versus a chat; what a context window means in practice; why you give the agent files, not memories; which tier to pick; a five-step first project, each step with "what you say / what the AI should produce / how you know it worked / what to do if it did not"; the five mistakes beginners make. |
| `docs/003_GLOSSARY.md` | <= 6 KB | Every ID prefix, every document-control field, package_id, edition, tier, practice space, golden baseline, diagnostic harness, handoff bundle, acceptance gate. Audited: every ID prefix used in the tree has an entry. |
| `docs/004_EDITIONS_AND_UPGRADE_PATH.md` | <= 5 KB | The four tiers, budgets, what each adds, that higher tiers are strict supersets, how zips relate to the repository and releases, the clone-name vs package_id convention. |

### 9.2 Templates

Extracted from the long SOPs (section 10.2 lists the sources) and audited for heading parity against a `## Required sections` list added to `docs/040` and `docs/070`. Includes `FIRST_SESSION_PROMPTS.md` (three prompts under 20 lines each: plan this / prototype this / package and report) and `MANUAL_AUDIT_CHECKLIST.md` (each line keyed to the TEST-* it approximates, so chat-only users still practise the discipline). The standard AI prompts in `docs/270` sections 10-12 and `docs/290` section 27 are the clearest existing chat-workflow artifacts in the corpus and seed the prompt file.

### 9.3 Worked example

`examples/hello_aisop/`: one ~80-line script with `--selfcheck` and the numbered sections from `docs/050`, plus the five intake documents. It passes `tools/aisop_check.py` and is the fixture that `tests/smoke_test.py` runs the lite audit against. A chat model imitates a concrete package far better than it follows prose.

### 9.4 Example-package audit rule

`package_structure_audit.py` treats any directory containing `aisop_example.json` as an independent package: its headers must be complete, but its `package_id` is its own and it is excluded from the root package_id-consistency check. This resolves the conflict the judges found between "every header matches config" and "a worked example with its own identity".

### 9.5 Feedback channel

`.github/ISSUE_TEMPLATE/first_session_report.yml`: which tier, which tool, what the AI produced, pasted `aisop_check` output. It is a channel, not a gate (PRIN-008).

## 10. Corpus Reorganization Map

### 10.1 Placement of every existing document

| Document | Tier | Pack | Action in REV-003 |
|---|---|---|---|
| `000_DOCUMENTATION_INDEX` | 2 | - | Becomes generated. |
| `000_USER_GUIDE_OVERVIEW` | 1 | - | Header keys; light beginner wording pass. |
| `005_PRODUCT_REQUIREMENTS` | 2 | - | New REQ entries; REQ-LIC-001 rewritten under the same ID. |
| `010_WINDOWS_SOFTWARE_DOWNLOAD...` | 3 | windows-hardware-workstation | Reclassified as domain reference (no rename); residue removal. |
| `020_AI_COLLABORATION_OPERATING_INSTRUCTIONS` | 1 | - | Generalized to second person; profile moved to template (Phase 0). |
| `030_CONCEPT_DEVELOPMENT_AND_REQUIREMENTS_BRIEF` | 2 | - | Headings and fences; "Concept Brief Lite" extracted as a template. |
| `040_MONOLITHIC_PLANNING_DOCUMENT_SOP` | 2 | - | Headings; `## Required sections` list; extraction-target numbering reconciled (DRIFT-008). |
| `050_MONOLITHIC_PROTOTYPE_CODE_SOP` | 1 | - | `logging.py` -> `logging_utils.py`; pointer block to 055/060. |
| `055_MONOLITHIC_PROTOTYPE_CODE_EXAMPLE` | 2 | - | Fix the `os.rename` Windows bug; drop Python 2 branches; later move code to `templates/monolithic_prototype_template.py` run by the smoke test. |
| `060_MONOLITH_TO_PACKAGE_MIGRATION_SOP` | 2 | - | Close the fence at L145; remove chat preamble and duplicate H1; `## Required sections`. |
| `070_ZIP_PACKAGE_REVIEW_AND_HANDOFF_SOP` | 2 | - | Headings; canonical report format decision; `test_reports/` -> `reports/`; empty appendix stubs removed. |
| `080-165` governance | 2 | - | Header keys; `100`, `150`, `160`, `165` gain edition/release/agent paragraphs. |
| `170_COMPATIBILITY_LESSONS_LEARNED` | 3 | legacy-and-embedded-compat | Close fence L78; generic LESSON-GEN entries and checklists later lifted to a tier-2 compatibility discipline doc. |
| `180`, `185` | 3 | hardware-daq | Close fences; remove chat residue; label project-specific examples as examples. |
| `190`, `195` | 3 | inline-qc-defect-traceability | Close fences; remove stray MIDI paragraph; label domain examples. |
| `200_FILE_DOWNLOAD_INSTALLATION...` | 3 (trimmed beginner section later tier 1) | windows-hardware-workstation | Orphan line; the "installing one of our ZIP packages" procedure promoted into `README_START_HERE_TEMPLATE`. |
| `205_PYTHON_LIBRARY_REFERENCE...` | 3 | python-environment-profiles | Describes an environment bundle that does not exist: rewrite as "proposed, not shipped" or implement later. |
| `210`, `250`, `260` | 3 | embedded-platforms | Orphan lines; dated API notes; `260` owns I2C. |
| `220`, `240`, `270`, `290` | 3 | simulation-games, audio-midi, android-pydroid, gui-design | Orphan lines; `270` has four sentences corrupted by citation-tool residue to repair. |
| `280_NETWORKING...` | 3 | networking-and-remote-devices | Truncated mid-sentence at L727: finish or delete the ping-sweep section. |
| `999_SOURCE_CLEANUP_NOTES` | 3 | - | Header keys. |

### 10.2 Template extraction backlog (sources)

Roughly sixty reusable skeletons exist inside the long SOPs. The Phase 2 set and their sources: planning document skeleton (`040` L815-841); ID record formats (`030` L163-227 and `040` L190-580, stated once); implementation-boundaries block (`030` L518-541); pre-code checklist (`030` section 21 and `040` section 9, merged); package folder layout (`070` L46-103); package identity intake form (`070` L107-119); workplan scope block (`070` L410-434); CHANGELOG entry standard (`070` L552-578); final package report (`070` L706-752); minimal per-run checklist (`070` L784-802); transfer plan (`060` L163-224); phase-gate checklist (`060` L788-800); handoff bundle (`165`). Domain-pack templates (channel map, wiring card, diagnostic report script, adapter interface) are Phase 5.

### 10.3 Domain packs (Phase 5, optional, one PR per guide)

windows-hardware-workstation (`010`, `200`), legacy-and-embedded-compat (`170`), hardware-daq (`180`, `185`), inline-qc-defect-traceability (`190`, `195`), embedded-platforms (`210`, `250`, `260`), application guides (`220`, `240`, `270`, `290`), networking (`280`). Each pack can later get a one-page brief assembled from its existing `RULE-*` / `THREAD-RULE-*` blocks and definition-of-done checklist, and its embedded code moved to `examples/<pack>/`.

## 11. Phases

Each phase is one practice branch (`practice/rev003-phase-N`) with branch notes per `docs/080`, merged only when its gate passes. Effort is maintainer time; phases 0 and 1 are the minimum viable delivery.

### PHASE-0: Make the clone green and give agents a landing file (1-2 days)

Tasks:
1. **License gate (DRIFT-001):** remove every `LICENSE_DECISION_REQUIRED.md` reference; rewrite REQ-LIC-001 as "a resolved license file named in `config/package_metadata.json` and a NOTICE.md consistent with it" (same ID); TEST-LIC-001 checks `LICENSE.txt` contains "MIT License"; update the matrix, README, NOTICE, KNOWN_LIMITATIONS, FEATURE_INVENTORY (FEAT-014 marked Superseded).
2. **Release root (DRIFT-002):** `release_package.py` reads `package_id` from config, stages into a temp directory named `package_id`, WARNs (not FAILs) when the clone folder differs; `--name` override. Add REQ-REL-002 / TEST-REL-002.
3. **CI branch (DRIFT-003):** `ci.yml` and `package_audit.yml` on `[master, main]`; document the default branch in README (DECISION-001).
4. **Reports (DRIFT-004):** gitignore `reports/*.txt`, `git rm --cached` the seven runtime reports, keep `reports/README.md` and `reports/baseline/`; snapshot current outputs as `reports/baseline/baseline_rev003_*`; add REQ-RPT-001 / TEST-RPT-001.
5. **Operating instructions (DRIFT-005):** rewrite `docs/020` in the second person with no biography; move every personal preference into `templates/USER_PROFILE_TEMPLATE.md` as fill-in fields plus one clearly labelled fictional example; add third-person-profile regexes to the personal-reference scan; gitignore `USER_PROFILE.md`; add REQ-PROF-001 / TEST-PROF-001.
6. **Interim entry file (DRIFT-006):** hand-written `AGENTS.md` (<= 4 KB, marked INTERIM, replaced in Phase 1) and a `CLAUDE.md` pointer: what the repo is, run the audits first, read `README_START_HERE.md`, do not load `docs/170-290` wholesale, never delete IDs, normative vs informative rule.
7. **Canonical report format (DRIFT-008, DECISION-003):** declare one final package report format in `docs/070` and reference it from `docs/020`; create `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`.
8. **Source hygiene (DRIFT-007, mechanical only, separate commit):** close the six unclosed fences; delete orphan trailing lines and chat-reply fragments; fix the duplicate H1s and the two stray old-filename lines; repair the four corrupted sentences in `docs/270`; fix the `os.rename` bug in `docs/055`; `project/logging.py` -> `logging_utils.py` in `050`/`055`. No prose rewriting.
9. Bump revisions on touched documents; CHANGELOG REV-003 Phase 0 entry; WORKPLAN run entry; regenerate `PACKAGE_MANIFEST.md`; merge or close the two Dependabot pull requests once CI is green.

Gate GATE-0: on a fresh `git clone` into a folder named `AISOP` and into a folder with any other name, `python tools/run_all_audits.py` prints `SUMMARY: PASS` and `git status --porcelain` is empty afterwards; the GitHub Actions run on the default branch is green; `grep -r LICENSE_DECISION_REQUIRED` returns nothing; the personal-reference scan passes with the new patterns; `requirements_trace_audit` passes with the revised and new IDs; every `docs/*.md` renders with headings visible on GitHub (no document is one code block).

### PHASE-1: Single-source scaffold, real agent entry, machine-readable index (3-4 days)

Tasks: write `docs/001_AISOP_CORE_RULES.md`; add `tier:` and `summary:` to every header (scripted pass, summaries hand-reviewed) and to `REQUIRED_FRONTMATTER_KEYS`; write `config/editions.json`; implement `tools/_aisop_common.py`, `tools/build_editions.py` (`entry`, `index`, `--check`; `zips` stubbed), `tools/edition_audit.py`, `tools/link_audit.py`; add `--quiet` to `run_all_audits.py` and wire in the new audits; write the real `AGENTS.md` and generate the pointer files (delete the interim files); generate `docs/index.json` and `docs/000_DOCUMENTATION_INDEX.md`; write `docs/166_EDITIONS_AND_TIERS_SOP.md`; update `docs/165`, `160`, `150`; add REQ-ENTRY-001..003, REQ-ED-001..003, REQ-LINK-001 with tests and FEAT entries; `CONTRIBUTING.md` and the PR template gain "I ran `python tools/build_editions.py all`".

Gate GATE-1: `run_all_audits.py` PASS including `build_editions.py --check`, `edition_audit.py`, `link_audit.py`; deliberately hand-editing a generated region or omitting `tier:` from one document makes the audit fail with a message naming the source to edit; `AGENTS.md` <= 8,192 bytes with every backticked path existing; `docs/001` rules block <= 5,120 bytes; the smoke test confirms `index.json` is valid and lists 100% of documents; an owner-run cold-agent session in one tool reaches the audits within six calls and names `docs/005` as the only binding requirements source (logged under `reports/baseline/`).

### PHASE-2: Beginner on-ramp and Chat Kit content (4-6 days; writing dominates)

Tasks: write `docs/002`, `003`, `004`; write `templates/` with `derived_from` keys and add `## Required sections` lists to `docs/040` and `docs/070`; implement template heading parity, the cross-tier link rule, and the ID-citation check in `edition_audit.py`; write `templates/FIRST_SESSION_PROMPTS.md` and `MANUAL_AUDIT_CHECKLIST.md`; build `examples/hello_aisop/` with `aisop_example.json` and the example-package audit rule; write `tools/aisop_check.py` (`--explain`); set `docs/050` and `docs/020` to tier 1 and confirm the Chat Kit is under budget by dry build; rewrite `README.md` as the chooser with exact openers; add the "which edition am I holding?" section to `README_START_HERE.md`; add `first_session_report.yml`; add REQ-BEG-001, REQ-TPL-001, REQ-EX-001 and tests; update KNOWN_LIMITATIONS (lower tiers are lossy, full documents win).

Gate GATE-2: `edition_audit` PASS with the Chat Kit under 120 KB, zero unmarked cross-tier links from tier <= 1 documents, template parity green, glossary covering every ID prefix in the tree; `build_editions.py zips --edition chatkit --dry-run` lists only tier <= 1 files plus fixed files and no `CHANGELOG.md`/`KNOWN_LIMITATIONS.md` from the root; `aisop_check.py` run inside the staged Chat Kit root and inside `examples/hello_aisop/` prints `SUMMARY: PASS`; an owner-run cold chat session given only the dry-built Chat Kit and the README opener produces a planning document from the template without asking for a file the kit lacks (logged under `reports/baseline/`).

### PHASE-3: Multi-edition release flow (2-3 days)

Tasks: finish `build_editions.py zips` (`EDITION_INFO.md`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt`, fixed dates); `release_package.py --edition all` delegates and runs `archive_name_audit` per archive; implement `tools/bump_release.py`; move `package_id` to the new identity (DECISION-004) in one dedicated commit with audits before and after; `manifest_update.py` reads config; add `.github/workflows/release.yml` (tag `v*` -> audits -> build -> attach `dist/*`; `gh release upload` documented as the manual fallback); update `docs/100` and `docs/160`; add REQ-ED-004, REQ-REL-003, REQ-CI-002 and tests; commit `reports/baseline/` snapshots; cut `v0.3.0`; README links point at latest-release asset URLs.

Gate GATE-3: pushing a `v*` tag yields a release with exactly `<pid>.zip`, `<pid>_method.zip`, `<pid>_chatkit.zip`, `AISOP_CARD.md`, `EDITIONS_CHECKSUMS.txt`; `archive_name_audit` passes on every downloaded zip; sha256 of each asset matches the checksum file; rebuilding locally from the same tag reproduces identical checksums; `run_all_audits.py` PASS before and after `bump_release.py`.

### PHASE-4: Cold-agent validation and the application layer (2-3 days plus ~1 hour per release)

Tasks: define TEST-ENTRY-004 (manual, owner-run): a fresh session in at least two different agentic tools is given only the repository URL and "Get up to speed on AISOP"; its minute-5 report must contain version, audit result, mode, files read, files skipped, first step, and must not have opened any `docs/170-290` file; log to `reports/baseline/cold_agent_test_<package_id>.txt` per release; `edition_audit` WARNs when the log is missing for the current package_id. Optionally (only if the Phase 2 session shows beginners stalling at scaffolding): `templates/project_seed/`, `tools/new_project.py` (copies the seed into a validated `yyyymmdd_00_description` folder, writes the new project's `AGENTS.md` from the card, runs `aisop_check.py`), `tests/test_new_project.py`. Update `docs/160` with the quarterly routine (run audits, re-run the cold-agent test on current tool versions, review budgets, prune nothing without a Superseded entry).

Gate GATE-4: two logged cold-agent runs with the required report shape for the current package_id; if the scaffold shipped, `tests/test_new_project.py` passes inside `run_all_audits.py` (scaffold into a temp dir, lite audit PASS, bad name rejected).

### PHASE-5: Domain packs and the worked practice branch (optional, parallelizable, one PR per guide)

Tasks: add `## TL;DR` and `topics` to `docs/010` and `docs/170-290` (agent-drafted, human-reviewed); generalize first-person-plural voice and label project-specific examples as examples; register the `RULE-*` namespace in the document-control conventions or rename; move embedded code to `examples/<pack>/` over time; create an "AISOP applied" practice branch (a tiny real project seeded from the templates with its own REQ/FEAT/TEST) linked from `docs/002`; skills packaging of the card (`skills/aisop/SKILL.md` carrying both the skill loader keys and the document-control keys) only if the owner uses a tool that loads skills.

Gate GATE-5: `index.json` shows `summary` and `topics` for 100% of documents; the practice branch passes `run_all_audits.py` on its own tree; the TEST-ENTRY-004 re-run on the tag shows the agent did not open a domain guide for a non-domain task.

## 12. Proposed Requirements, Features, and Tests

Proposed IDs; registered in `docs/005`, `ACCEPTANCE_TEST_PLAN.md`, `FEATURE_INVENTORY.md`, and the matrix in the phase that implements them. Existing IDs are never renumbered; REQ-LIC-001 keeps its ID with new text.

| Requirement | Statement (short) | Test | Feature | Phase |
|---|---|---|---|---|
| REQ-LIC-001 (rewritten) | License file named in config present; NOTICE consistent. | TEST-LIC-001 (rewritten) | FEAT-014 Superseded by FEAT-030 | 0 |
| REQ-REL-002 | Release root derives from `package_id`, never from the clone folder name. | TEST-REL-002 | FEAT-016 (extended) | 0 |
| REQ-RPT-001 | Runtime reports are not committed; baseline snapshots are committed per release. | TEST-RPT-001 (`git ls-files` shows no `reports/*.txt`) | FEAT-008 (extended) | 0 |
| REQ-PROF-001 | Operating instructions contain no personal biography; the user profile is a template plus an optional local file. | TEST-PROF-001 (extended personal-reference scan) | FEAT-031 | 0 |
| REQ-RPT-002 | One canonical final package report format, referenced by every SOP. | TEST-RPT-002 | FEAT-032 | 0 |
| REQ-ENTRY-001 | `AGENTS.md` exists, <= 8,192 bytes, cites only existing paths, states the normative rule. | TEST-ENTRY-001 | FEAT-033 | 1 |
| REQ-ENTRY-002 | Pointer files exist for declared tools and reference `AGENTS.md`. | TEST-ENTRY-002 | FEAT-033 | 1 |
| REQ-ENTRY-003 | Generated regions and `docs/index.json` are fresh (`--check`). | TEST-ENTRY-003 | FEAT-034 | 1 |
| REQ-ENTRY-004 | Cold-agent protocol verified manually per release; transcript kept. | TEST-ENTRY-004 (manual) | FEAT-033 | 4 |
| REQ-ED-001 | Every document declares `tier` and `summary`. | TEST-ED-001 | FEAT-035 | 1 |
| REQ-ED-002 | Editions declared in `config/editions.json` with byte budgets; built by one stdlib tool. | TEST-ED-002 | FEAT-035 | 1 |
| REQ-ED-003 | `docs/001` <= 8 KB with a rules block <= 5 KB; it is the single source of the core rules. | TEST-ED-003 | FEAT-036 | 1 |
| REQ-ED-004 | Every edition zip obeys the naming rule, contains `EDITION_INFO.md`, and is reproducible. | TEST-ED-004 | FEAT-037 | 3 |
| REQ-LINK-001 | Every relative link and backticked repo path resolves, in the tree and in each edition. | TEST-LINK-001 | FEAT-038 | 1 |
| REQ-TPL-001 | Templates declare `derived_from` and keep heading parity with their SOP. | TEST-TPL-001 | FEAT-039 | 2 |
| REQ-BEG-001 | Beginner guide, glossary, and editions guide exist within their budgets; glossary covers every ID prefix. | TEST-BEG-001 | FEAT-040 | 2 |
| REQ-EX-001 | Worked example package passes the lite audit and carries its own package identity under the example-package rule. | TEST-EX-001 | FEAT-041 | 2 |
| REQ-REL-003 | Release assets are built only from a green audit run of the tagged commit. | TEST-REL-003 | FEAT-037 | 3 |
| REQ-CI-002 | CI runs on the default branch and on pull requests. | TEST-CI-002 | FEAT-010 (extended) | 0 |
| REQ-SEED-001 (optional) | Scaffold output passes the lite audit and the naming rule. | TEST-SEED-001 | FEAT-042 | 4 |

## 13. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | Contributors or agents hand-edit a generated file or region; the edit is lost or the file drifts. | High | Medium | GENERATED banner naming the source; `--check` in CI; MODIFY-AISOP mode requires `--check` before delivery; PR template checkbox. |
| RISK-002 | Chat Kit budget creep: each helpful document is set to tier 1 until the kit no longer fits a chat context. | Medium | High | Budget failure lists the largest offenders; policy "raise the tier, not the budget"; a budget change needs a CHANGELOG entry and a changed acceptance text. |
| RISK-003 | File-level tiering feels coarse and tempts condensed copies (the classic drift source). | Medium | High | Accepted deliberately: short tier-1 documents and templates carry the method; if a long SOP truly needs a short form, split it into two source documents with different tiers. |
| RISK-004 | `AGENTS.md` goes semantically stale (protocol says X, `docs/165` says Y) even though its paths and size pass. | Medium | High | Rules region generated from `docs/001`; TEST-ENTRY-004 manual run per release; `docs/165` references the protocol by pointer rather than restating it. |
| RISK-005 | Agent-tool conventions (`CLAUDE.md`, `.cursor/rules`, Copilot, Gemini, skills) change and a pointer stops being auto-loaded. | Medium | Low | `AGENTS.md` is tool-agnostic; a pointer is three lines; README gives the fallback sentence that works in any tool; KNOWN_LIMITATIONS records it. |
| RISK-006 | Generalizing `docs/020` strips the opinionated voice that made it effective for the owner. | Low | Medium | Nothing is deleted: preferences move to the profile template as a labelled example, and the owner's own gitignored `USER_PROFILE.md` restores the behaviour locally. |
| RISK-007 | The package_id rename touches ~60 headers and masks real edits. | Medium | Medium | One dedicated commit produced by `bump_release.py`, audits before and after, nothing else in that commit. |
| RISK-008 | Token estimates (bytes/4) mislead for some models or chat products; a "fits in chat" claim fails. | Medium | Medium | Bytes are the hard number; budgets leave 25-30% headroom; the Phase 2 and Phase 4 logged sessions catch real failures; KNOWN_LIMITATIONS states the approximation. |
| RISK-009 | Manual tests (cold-agent, cold-chat) get skipped under time pressure. | High | Medium | Release-gate items in `docs/100` and `docs/160`; the log file is committed per package_id; `edition_audit` WARNs when it is missing. |
| RISK-010 | Scope creep: domain-pack work, skills, and the scaffold delay the simpler goal. | High | Medium | Phases 0 and 1 alone deliver the core ask; Phases 4-5 items are explicitly optional and parallelizable. |
| RISK-011 | Source hygiene (Phase 0 task 8) accidentally changes meaning in a normative SOP. | Low | High | Mechanical-only rule; separate commit; diff reviewed for prose changes; no sentence rewritten. |
| RISK-012 | Clone folder `AISOP` vs package_id root confuses zip traders. | Low | Low | `release_package.py` prints both names; `docs/004` and README explain the convention in one sentence; `archive_name_audit` remains the proof. |

## 14. Decisions Needed From the Owner

Each has a recommendation; the plan proceeds on the recommendation unless the owner says otherwise.

| ID | Decision | Recommendation | Why |
|---|---|---|---|
| DECISION-001 | Default branch: keep `master` or rename to `main`. | Keep `master` for now; CI runs on both. Rename later if ever, before external links accumulate. | Zero-risk now; a rename is reversible plumbing. |
| DECISION-002 | Which agentic tools get pointer files. | Generate pointers only for tools the owner can test (at minimum `CLAUDE.md`); the list is one line in `editions.json`. | An untested pointer is drift waiting to happen. |
| DECISION-003 | Canonical final package report: `070` section 18 (15 fields) or `020`'s 10 items. | Adopt the 15-field format as canonical; the card and `AGENTS.md` reference the template rather than restating a shorter form. | Removes a documented contradiction; the SOP already carries it. |
| DECISION-004 | New package identity and when to bump. | `yyyymmdd_00_aisop` at the first tiered release (Phase 3), not in Phase 0. | Keeps Phase 0 small; the bump is one scripted commit. |
| DECISION-005 | Where the owner's real profile lives. | Gitignored `USER_PROFILE.md`; the tracked template carries a fictional example only. | Nothing personal in the tree; nothing lost locally. |
| DECISION-006 | `docs/010` tier. | Tier 3 (domain reference). | It is a Windows lab-instrument install guide with no AI-collaboration content. |
| DECISION-007 | Chat Kit target and budget. | 120 KB text; assume current web chat products with file upload; the card covers products without upload. | Leaves headroom under common upload limits; validated by the Phase 2 session. |
| DECISION-008 | Worked example flavour. | Neutral `hello_aisop` (a small file-processing utility) for Phase 2; a DAQ-flavoured example can be a Phase 5 practice branch. | Beginners should not meet hardware safety on day one. |
| DECISION-009 | GitHub Action for release-asset upload. | Yes, as CI plumbing; `gh release upload` documented as the manual fallback. | The stdlib rule is about package tooling, not CI. |
| DECISION-010 | Domain guides: stay in place with `tier: 3`, or move to `docs/reference/`. | Stay in place. | No broken links or bookmarks; tier tags already hide them from lower editions. |
| DECISION-011 | Generate the traceability matrix from the catalog. | Defer until after Phase 3. | It forces a catalog schema migration unrelated to tiers. |
| DECISION-012 | Core-method SOPs (`030`, `040`, `060`, `070`) become Normative. | Promote `docs/001` to Normative now; leave the long SOPs Informative with `docs/001` as the binding summary. | Agents get one binding source without turning 3,000 lines of prose into requirements. |
| DECISION-013 | Manual acceptance testing per release. | Two cold-agent runs and one cold-chat run, logged; roughly one hour. | Without it the entry layer rots silently. |
| QUESTION-001 | Which chat products and plans does the intended lower-tier audience actually use, and do they allow zip upload? | Answer sets the Chat Kit budget and whether the worked example fits. | - |
| QUESTION-002 | Which agentic tools does the owner use today? | Determines the pointer list and the TEST-ENTRY-004 tool pair. | - |

## 15. What Not To Do

- Do not hand-maintain condensed or "lite" versions of any SOP, in any folder; split the source instead.
- Do not add section-level transclusion markers to normative prose.
- Do not write a long `AGENTS.md`; if it does not fit in 8 KB it belongs in `docs/165`, `docs/166`, or the index.
- Do not embed the repository map in `AGENTS.md`; it lives in `docs/index.json`.
- Do not commit `dist/` or regenerated `reports/*.txt` again.
- Do not let any phase gate depend on outside volunteers.
- Do not make domain guides normative or put any of them into the Chat Kit or Method Kit.
- Do not renumber or rename existing `docs/NNN` files or any REQ/FEAT/TEST ID; extend, supersede, rewrite text under the same ID.
- Do not adopt mkdocs, Sphinx, pandoc, PyYAML, Jinja, pre-commit frameworks, or any non-stdlib dependency for building or auditing.
- Do not rename the default branch as a prerequisite for anything.
- Do not rewrite the tier-3 guides for tone as part of this program; TL;DR additions are additive and one PR per guide.
- Do not describe any specific person in the third person in any tracked document.
- Do not require git, a terminal, or Python from tier 0 or tier 1 users; the card must work with zero tooling and `aisop_check.py` must explain itself for models that cannot execute it.

## 16. Effort and Sequencing Summary

| Phase | Delivers | Effort | Depends on |
|---|---|---|---|
| 0 | Green audits in any clone; CI on the default branch; clean tree after audits; generalized `020`; interim `AGENTS.md`; readable SOPs | 1-2 days | - |
| 1 | Tier headers, editions manifest, build/audit/link tools, real `AGENTS.md`, index | 3-4 days | 0 |
| 2 | Beginner documents, templates, prompts, worked example, lite audit, README chooser, Chat Kit under budget | 4-6 days | 1 |
| 3 | Reproducible zips, checksums, `bump_release`, new package_id, release workflow, `v0.3.0` | 2-3 days | 2 |
| 4 | Cold-agent validation per release; optional scaffold | 2-3 days + 1 h/release | 1 (validation), 2 (scaffold) |
| 5 | Domain-pack TL;DRs, generalization, example branch, optional skills | open-ended, parallel | 1 |

Minimum viable delivery for GOAL-003 is Phases 0 and 1 (about one week). Total for Phases 0-4 is roughly 12-18 maintainer days.

## 17. Extraction Plan

When approved, sections of this plan move to their permanent homes and this document is marked Superseded (not deleted) with a dated note.

| Section of this plan | Extracts to | Phase |
|---|---|---|
| 3.2 Drift register | `CHANGELOG.md` REV-003 Phase 0 entry; `WORKPLAN_CURRENT_RUN.md` | 0 |
| 5, 7 | `docs/166_EDITIONS_AND_TIERS_SOP.md` (normative) and `config/editions.json` | 1 |
| 8 | `AGENTS.md`; `docs/165` (protocol by reference) | 1 |
| 9 | `docs/001-004`, `templates/`, `examples/hello_aisop/` | 1-2 |
| 10 | `docs/000_DOCUMENTATION_INDEX.md` tier column (generated); Phase 5 issue list | 1, 5 |
| 11 | Branch notes per `docs/080` on each `practice/rev003-phase-N` branch | each |
| 12 | `docs/005`, `ACCEPTANCE_TEST_PLAN.md`, `FEATURE_INVENTORY.md`, `REQUIREMENTS_TRACEABILITY_MATRIX.md`, `requirements_catalog.json` | each |
| 13 | `KNOWN_LIMITATIONS.md` (LIMIT-005..007) and `docs/160` maintainer playbook | 1-4 |
| 14 | Decision log entries in `WORKPLAN_CURRENT_RUN.md` once answered | 0 |
| 15 | `docs/166` and `CONTRIBUTING.md` | 1 |
