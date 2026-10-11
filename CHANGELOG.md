---
document_id: DOC-000-CHANGELOG
title: "Changelog"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-CHANGELOG
normative_status: Informative
tier: 2
summary: "What changed in each AISOP revision, newest program entries last, including the REV-003 phases."
source: "Generalized AI-assisted coding SOP source text"
---

# Changelog

## 0.1.0 / REV-001 / 2026-05-02

- Converted the markdown seed into a self-describing example package.
- Added document-control metadata to markdown documents.
- Added root-level `FEATURE_INVENTORY.md`.
- Added root-level `ACCEPTANCE_TEST_PLAN.md`.
- Added root-level `KNOWN_LIMITATIONS.md`.
- Added root-level `WORKPLAN_CURRENT_RUN.md`.
- Added root-level `REQUIREMENTS_TRACEABILITY_MATRIX.md`.
- Added `docs/005_PRODUCT_REQUIREMENTS.md` as the authoritative requirement list.
- Added `requirements/requirements_catalog.json` for machine-readable requirement indexing.
- Added `config/package_metadata.json`.
- Expanded package audit tooling.
- Added smoke-test tooling.
- Generated audit and smoke-test reports.

## 0.0.1 / REV-000 / 2026-05-02

- Initial cleaned generalized markdown seed package.

## 0.2.0 / REV-002 - 2026-05-16

### Added

- GitHub-ready repository substrate: `README.md`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.github/` templates, CI workflows, and Dependabot configuration.
- Practice-space doctrine explaining AISOP as a branchable, auditable space of practices rather than only a static package.
- Security, safety, support, contribution, attribution, and license-decision documents.
- Release-package tooling to preserve old-school zip handoff while supporting GitHub releases.
- Repository-health, traceability, archive-name, secret-scan, manifest-update, and all-audits tools.
- Baseline REV-001 audit reports preserved under `reports/baseline/`.

### Changed

- Package identity updated to `20260516_00_seed`.
- Package version updated from `0.1.0` to `0.2.0`.
- Touched existing controlled documents updated to `REV-002`.
- README workflow updated to describe both zip handoff and GitHub repository use.
- Requirement catalog expanded for repository, CI, release, safety, security, license, and governance requirements.

### Risk notes

- License remains intentionally unresolved and is treated as a release gate.
- GitHub repository settings such as branch protection cannot be fully enforced from files alone and require maintainer setup.
- Local secret scan is a lightweight preflight, not a complete security review.

## Unreleased / REV-003 planning - 2026-10-10

### Added

- `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`: proposed plan for tiered editions built from one source tree, an agent-first entry file, a beginner on-ramp, a multi-edition release flow, and the Phase 0 drift fixes that must land first. Revised once (REV-002) after a five-lens adversarial review. Planning document only; no structure changes in this entry.
- Index and workplan entries pointing at the gameplan.

### Changed

- `PACKAGE_MANIFEST.md` regenerated for the files touched by this entry; the header constants in `tools/manifest_update.py` bumped to match (revision, last_updated). Reading those values from `config/package_metadata.json` is scheduled for Phase 0 of the gameplan.

### Known drift recorded (not yet fixed)

- `run_all_audits.py` currently fails: the license-decision gate was removed on GitHub but the audits, metadata, and requirements still expect it; `release_package.py` hard-codes the seed root folder name; CI triggers on `main` while the default branch is `master`; runtime reports are committed. All are scheduled for Phase 0 of the gameplan.

## Unreleased / REV-003 Phase 0 - 2026-10-11

Executes Phase 0 of `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`. Slices were developed as separate commits on one working branch (the session could push to a single branch only), not as separate `practice/rev003-*` branches.

### 0a. License gate and CI branch

- DRIFT-001: retired every live reference to the deleted license-decision gate. REQ-LIC-001 and TEST-LIC-001 rewritten under the same IDs: the license file named by `license_file` in `config/package_metadata.json` (`LICENSE.txt`, MIT) must exist and `NOTICE.md` must name it. FEAT-014 marked Superseded by FEAT-030. `README.md`, `NOTICE.md`, `KNOWN_LIMITATIONS.md`, `CITATION.cff` (license field), and `docs/140` updated.
- DRIFT-003: `ci.yml` now runs on pushes to `master` and `main`; `package_audit.yml` gained the same push trigger. Default branch recorded as `default_branch` in config and documented in `README.md` (DECISION-001). Added REQ-CI-002 / TEST-CI-002, checked by `repo_health_audit.py`.

### 0b. Release root, reports, manifest

- DRIFT-002: `tools/release_package.py` takes the archive root from `package_id` in config (REQ-REL-002 / TEST-REL-002), warns when the working-copy folder name differs, accepts `--name` and `--out`, and writes members sorted with fixed timestamps. `dist` removed from `required_directories`. `run_all_audits.py` spawns `sys.executable` and gained `--quiet`.
- New `tools/_aisop_common.py`: the shared front-matter parser, git-ignore-aware file walk (works without git, so zip recipients and clone users see the same file list), hashing, and deterministic zip writer.
- DRIFT-004: `reports/*.txt` and `USER_PROFILE.md` are git-ignored; the six individual runtime reports were untracked and the REV-002 combined run report preserved as `reports/baseline/baseline_rev002_run_all_audits_report.txt` (REQ-RPT-001 / TEST-RPT-001).
- `tools/manifest_update.py` reads header values from config, uses the shared file walk (so `reports/README.md` and `reports/baseline/` are now listed and git-ignored files never are), emits `normative_status: Informative`, and gained `--check`, which `run_all_audits.py` runs last (REQ-MAN-001 / TEST-MAN-001, FEAT-031).
- `tests/smoke_test.py` restructured into named checks; it now builds a release from a renamed copy of the tree in a temp directory.

### 0c. Interim entry file and canonical report

- DRIFT-006: added an interim `AGENTS.md` (Normative, full header, marked INTERIM; replaced in Phase 1) and a `CLAUDE.md` pointer that imports it.
- DRIFT-008 / DECISION-003: `docs/070` section 18 declared the canonical fifteen-field final package report; added `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md`; `docs/020` (ten-item list removed), `050` (new section 8), `060` (section 21 now extends the canonical report with transfer fields), `165`, `040`, and `AGENTS.md` cite it. REQ-RPT-002 / TEST-RPT-002 (FEAT-032), checked by `repo_health_audit.py` with the citer list in config.
- `WORKPLAN_CURRENT_RUN.md` gained a `## Decision Log` with every section-14 decision and two execution notes.

### 0d. Operating instructions

- DRIFT-005: `docs/020` rewritten in the second person (about 10.5 KB, down from 13.4 KB) with no biography; it now reads `USER_PROFILE.md` when present and otherwise asks the six questions in the new `templates/USER_PROFILE_TEMPLATE.md`, whose labelled fictional example keeps the earlier preferences (legacy targets, dark interface theme, zipped deliverables) available to anyone who wants them (RISK-006). The personal-reference scan gained third-person profile patterns. REQ-PROF-001 / TEST-PROF-001 (FEAT-033).

### 0e. Source hygiene

- Mechanical commit (deletions and exact fence lines only, verified with `git diff -U0`): closed the unclosed fences in `docs/060` and `docs/200`; removed the orphan next-document headings and chat-reply tails at the end of `docs/170`-`280`, the empty appendix stub in `docs/070`, the stale filename lines in `docs/010` and `docs/030`, and the duplicate H1s in `docs/060`, `185`, `190`, `195`.
- Content commit (revisioned): repaired the four sentences in `docs/270` corrupted by citation-tool residue and a split word; finished the truncated ping-sweep example in `docs/280`; fixed the `os.rename` overwrite bug on Windows in `docs/055` (uses `os.replace` where available); `project/logging.py` renamed to `logging_utils.py` in `docs/050` and `055` (the old name shadows the standard library); removed chat phrasing from `docs/030`, `070`, `185`, `190`; DRIFT-008 reconciled in the method documents (`FEATURE-nnn` to `FEAT-nnn`, `ACCEPT-nnn` to `TEST-XXX-nnn`, `test_reports/` to `reports/`, and a numbering note in `030`, `040`, `060`, `070` separating a project's own `docs/NNN` numbers from AISOP's); `docs/205` marked "proposed, not shipped".
- Added the fence-parity check to `package_structure_audit.py` (REQ-DOC-004 / TEST-DOC-004). The five domain guides that still need full re-fencing (`docs/170`, `180`, `185`, `190`, `195`) are listed in `fence_parity_pending` and reported as WARN until Phase 5.
- Revisions bumped on every touched document.

## Unreleased / REV-003 Phase 1 - 2026-10-11

### Added

- `docs/001_AISOP_CORE_RULES.md` (tier 0, Normative): the AISOP card, the single source of the core rules (REQ-ED-003, FEAT-037).
- `config/editions.json`: the four editions (Card, Chat Kit, Method Kit, Full) with tiers, byte budgets, `max_files`, include globs, openers, pointer list, commands, and link-check lists (REQ-ED-002, FEAT-036).
- `tools/build_editions.py` with `tools/_aisop_editions.py` and `tools/_aisop_generators.py`: `entry`, `index`, `all`, `zips`, `stage`, and `--check`. Staged editions get their own `EDITION_INFO.md`, index, and manifest, so the audits pass inside an unzipped Method Kit (REQ-ENTRY-003, FEAT-035).
- `tools/edition_audit.py`: references in the tree, `AGENTS.md` size/identity/status, the rules-block cap, pointer files, card labels versus the report template, header package_id consistency, and cold-agent-log and superseded-tier warnings (REQ-ENTRY-001/002, REQ-LINK-001, FEAT-034, FEAT-039).
- The real `AGENTS.md` (tier 2, Normative; sections per `docs/300` 8.1) with GENERATED `rules` and `commands` regions; generated `CLAUDE.md` and `GEMINI.md` pointers; generated `docs/index.json` and `docs/000_DOCUMENTATION_INDEX.md`.
- `docs/166_EDITIONS_AND_TIERS_SOP.md` (Normative): tiers, membership, generated content, edition markers, budgets, release assets, repository layout, and check ownership.
- TEST-ENTRY-004 (cold-agent test) defined; KNOWN_LIMITATIONS LIMIT-005 to LIMIT-007.

### Changed

- Every document header gained `tier` and `summary` (domain guides also `topics`); both keys are required (REQ-ED-001).
- Demoted to Informative (records and orientation, not procedure or policy): `NOTICE.md`, `SUPPORT.md`, `README.md`, `README_START_HERE.md`, `KNOWN_LIMITATIONS.md`, `FEATURE_INVENTORY.md`. `CODE_OF_CONDUCT.md` stays Normative as a conduct policy (DECISION-012).
- `package_structure_audit.py` and `repo_health_audit.py` read their lists from `config/package_metadata.json`; the structure audit uses the shared parser and the git-ignore-aware walk.
- `run_all_audits.py` runs `edition_audit.py` and `build_editions.py --check`.
- `tests/smoke_test.py`: index validity, two negative cases on a copy of the tree (a hand-edited GENERATED region; a deleted `tier:`), and a staged Method Kit that must pass its own audits.
- `docs/165` keeps the handoff bundle and defers agent duties to `AGENTS.md` sections 5-10; `docs/150`, `docs/160`, `CONTRIBUTING.md`, and the pull request template name `build_editions.py`.
- Tier-1 documents mark citations of tier-2 files "(method edition)"; downstream-project paths are written `./tools/...`.

### Deviations from docs/300 (recorded in the Decision Log)

- `AGENTS.md` is tier 2, not tier 0 (section 5.1 versus 8.1).
- The cross-tier rule is enforced once, by per-edition reference resolution in `build_editions.py --check`; `edition_audit.py` resolves references only in the tree it audits.
- The Chat Kit unique-basename rule exempts registered example packages.

### Known state

- The Method Kit is at about 96% of its 409,600-byte budget before Phase 2 content; DECISION-014 applies at the Phase 2 dry build.

## Unreleased / REV-003 Phase 2 - 2026-10-11

### Added

- Beginner on-ramp (REQ-BEG-001, FEAT-041): `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md` (chat versus agent, context windows, files over memory, which edition, a five-step first project with checks and failure branches, a "before you run code" box, five beginner mistakes), `docs/003_GLOSSARY.md` (terms, header fields, every ID family in tiers 0-2), and `docs/004_EDITIONS_AND_UPGRADE_PATH.md` (generated edition table and openers, upgrade path, chat-product facts pending owner tests).
- Templates (REQ-TPL-001, FEAT-040): concept brief (lite), planning document (23 sections, parity with `docs/040`), README_START_HERE (parity with `docs/070`), changelog, feature inventory, known limitations, agent handoff bundle, first-session prompts, ID record formats, an index with the one-template-per-stage table, and `MANUAL_AUDIT_CHECKLIST.md` generated from the lite audit's CHECKS table. `docs/040` and `docs/070` gained `## Required sections` lists.
- Worked example and lite audit (REQ-EX-001, FEAT-042): `examples/hello_aisop/` (a text-statistics utility with the `docs/050` sections and flags, plus its five intake documents and a hello-world-scale planning document), registered in `example_packages`; `tools/aisop_check.py` (eight checks, `--root` for a folder or zip, `--run`, `--explain`; Python 2.7/3 syntax).
- `.github/ISSUE_TEMPLATE/first_session_report.yml` (optional beginner feedback; not a gate).
- Audits: template parity, placeholder-only IDs in templates, ID citations in tier 0-1 documents, glossary coverage, and size caps (`edition_audit.py`); example-package registration (`package_structure_audit.py`); the example's lite audit and the Chat Kit contents check (`tests/smoke_test.py`).

### Changed

- `README.md` rewritten around a generated edition chooser with latest-release links and openers; `README_START_HERE.md` is edition-aware (which edition am I holding, generated openers, reading order with edition markers).
- `AGENTS.md` gained the one-template-per-stage table and the manual checklist as the no-commands fallback (7,761 of 8,192 bytes).
- Core rule 14 no longer says "the report below" (wrong once the rules are embedded in `AGENTS.md`); `AGENTS.md` step 2 says the audits only write git-ignored reports and temporary copies (findings from the first cold-agent runs).
- `repo_health_audit.py` and `secret_scan_lite.py` use the shared git-ignore-aware walk; `.gitignore` excludes `.claude/worktrees/`.
- KNOWN_LIMITATIONS LIMIT-008 (chat products untested) and LIMIT-009 (Python 2.7 paths untested).

### Budget change (DECISION-014, RISK-002 process)

- The Phase 2 dry build put the Method Kit at 473,970 bytes, 116% of its 409,600-byte budget. As DECISION-014 pre-approved, the budget is raised to 524,288 bytes in `config/editions.json`, and the TEST-ED-002 acceptance text records the new figures. The Chat Kit is at about 76% of 122,880 bytes with 32 of 40 files.

## Unreleased / REV-003 Phase 5 (part 1): domain-guide re-fencing - 2026-10-11

- `docs/170`, `180`, `185`, `190`, and `195` re-fenced, one guide per isolated change: every code sample, record template, folder tree, and diagram is now in a closed, language-tagged fence (17, 53, 42, 62, and 45 blocks), numbered section titles became Markdown headings (13, 59, 40, 66, and 44), and each guide gained a `## TL;DR`. `170`, `180`, and `185` gained one sentence saying their named projects or hardware are examples, not requirements. No other wording changed: a word-level comparison against the previous revision, excluding the TL;DR, shows zero removed words and only those label sentences added (21, 6, and 23 words; 0 for `190` and `195`).
- `fence_parity_pending` is now empty: every Markdown file has balanced fences (REQ-DOC-004 without exceptions).
- The `170` TL;DR names the downstream harness as `./tools/diagnostic_harness.py`.
