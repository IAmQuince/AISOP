---
document_id: DOC-000-WORKPLAN-CURRENT-RUN
title: "Workplan Current Run"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-000-WORKPLAN-CURRENT-RUN
normative_status: Informative
tier: 2
summary: "Scope and status of the current and previous runs, plus the decision log for REV-003."
source: "Generalized AI-assisted coding SOP source text"
---

# Workplan Current Run

RUN-001
Run name: 20260502_01_ai_sop_reference_package
Date: 2026-05-02
Purpose: Convert the generalized SOP markdown seed into a self-describing example package with document control, machine-referenceable requirements, feature inventory, acceptance tests, audit tooling, and smoke-test tooling.

## Scope

This run changes package structure and metadata only. It does not rewrite all long-form technical reference content.

## Completed Changes

- Added document-control metadata to markdown documents.
- Added package-level machine-referenceable requirements.
- Added feature inventory.
- Added acceptance test plan.
- Added known limitations.
- Added current workplan.
- Added machine-readable requirement catalog JSON.
- Added package metadata JSON.
- Expanded audit and smoke-test tooling.
- Generated reports.

## Out of Scope

- Full editorial rewrite of every technical guide.
- Conversion to DOCX/PDF.
- Building a runnable application beyond package validation tools.
- Verifying every third-party installer/link in the reference guides.

## Next Recommended Run

Perform a human editorial pass and decide whether to keep the long technical reference guides as one package or split them into a smaller public-facing starter edition plus an expanded technical appendix.

Update 2026-10-10: that decision is now worked out in `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md` (tiered editions from one source tree). The next run is its Phase 0: make the audits green in any clone and add an interim agent entry file.

## REV-002 Workplan: GitHub Practice-Space Upgrade

### Objective

Convert the package from a local-only SOP seed into a dual-use artifact: a GitHub-ready repository and a self-documenting guide for making zip-based packages GitHub-ready.

### Phases

1. Preserve REV-001 baseline audit reports.
2. Rename package identity to `20260516_00_seed`.
3. Add GitHub/community/repository files.
4. Add practice-space and GitHub bootstrap SOP documents.
5. Expand requirements, feature inventory, tests, and traceability.
6. Add audits and release packaging tools.
7. Run all audits and generate release zip.

### Acceptance

- Existing package audit passes.
- Smoke test passes.
- Repository-health audit passes.
- Secret scan completes.
- Release dry run passes.
- Final package zip has matching zip basename and internal root folder.

## REV-003 Run: Expansion Gameplan Execution

RUN-003
Run name: 20261011_00_rev003_expansion_execution
Date: 2026-10-11
Purpose: Execute `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md`, phase by phase, keeping `run_all_audits.py` green after every slice.

### Status by phase

| Phase | Status | Evidence |
|---|---|---|
| 0a-0e | Done | GATE-0 local checks pass on fresh clones named `AISOP` and otherwise (`reports/baseline/baseline_rev003_phase0_run_all_audits_report.txt`). |
| 1 | Done | `run_all_audits.py` includes `edition_audit.py` and `build_editions.py --check`; negative cases in the smoke test; TEST-ENTRY-004 log under `reports/baseline/`. |
| 2 | Done except owner-run items | Automated GATE-2 parts pass (budgets, markers, parity, glossary, Chat Kit contents, example lite audit). A simulated cold-chat session completed docs/002 steps 1-3 with zero interventions, and its prototype passed its own smoke test (`reports/baseline/cold_chat_simulation_20261011_00_aisop.txt`). The real owner-run session and per-product facts (QUESTION-001) are pending. |
| 3 | Done except the tag | Edition zips, checksums, `bump_release.py`, `release.yml`; identity moved to `20261011_00_aisop` 0.3.0 in its own commit. Pushing the `v0.3.0` tag is the owner's step. |
| 4 | Partly done | TEST-ENTRY-004 passes on Claude Code (`reports/baseline/cold_agent_test_20261011_00_aisop.txt`), and a Method Kit run passed its audits inside the unzipped kit; the second tool is pending QUESTION-002; quarterly routine in `docs/160`. The optional scaffold was not built: the simulated beginner session did not stall at scaffolding. |
| 5 | Done except optional items | `docs/170`-`195` re-fenced; TL;DR and topics for every domain guide; RULE namespace settled (EXEC-010). Not done: the "AISOP applied" practice branch (this run could push one branch only), a runnable prototype template (templates/monolithic_prototype_template.py), and skills packaging (QUESTION-002). |

### Owner actions

1. Review the branch and merge it into `master`; CI on the pull request is the first GitHub run of the new audits (GATE-0 "Actions green on the default branch").
2. Decide the two Dependabot pull requests (`actions/checkout` and `actions/setup-python` major bumps) once CI is green; the workflows currently pin `@v4` and `@v5`.
3. Cut the first tiered release: confirm `version` 0.3.0 in config, set `date-released` in `CITATION.cff`, then `git tag v0.3.0 && git push origin v0.3.0`. `release.yml` publishes the assets; check them per `docs/100` (GATE-3).
4. Run the scripted cold-chat session in a real chat product (GATE-2) and record upload facts in `docs/004` (QUESTION-001).
5. Name the agentic tools you use (QUESTION-002): it sets the pointer files and the second tool for TEST-ENTRY-004.
6. Confirm or override the adopted decisions above, especially DECISION-012 (six root files demoted), EXEC-003 (`AGENTS.md` tier 2), DECISION-014 (Method Kit budget raised), and the move of `docs/000_USER_GUIDE_OVERVIEW.md` to tier 3. The Method Kit is near its budget; further growth needs another re-tier or budget decision.

## Decision Log

Decisions from `docs/300_AISOP_EXPANSION_GAMEPLAN_REV003.md` section 14. The plan proceeds on each recommendation unless the owner says otherwise; "Adopted (recommendation)" means the recommendation was applied during execution and stands until the owner overrides it.

| ID | Decision | Status | Applied as |
|---|---|---|---|
| DECISION-001 | Default branch | Adopted (recommendation) | Keep `master`; CI runs on `master` and `main`; `default_branch` in config (0a). |
| DECISION-002 | Pointer files | Adopted (recommendation) | `CLAUDE.md` and `GEMINI.md`; none for tools that read `AGENTS.md` natively. |
| DECISION-003 | Canonical final package report | Adopted (recommendation) | `docs/070` section 18, fifteen fields; template `templates/FINAL_PACKAGE_REPORT_TEMPLATE.md` (0c). |
| DECISION-004 | New package identity | Adopted (recommendation) | `yyyymmdd_00_aisop` at the first tiered release (Phase 3), not in Phase 0. |
| DECISION-005 | Owner's real profile | Adopted (recommendation) | Git-ignored `USER_PROFILE.md`; tracked template carries a fictional example only (0b ignore rule, 0d template). |
| DECISION-006 | `docs/010` and `docs/055` tier | Adopted (recommendation) | Tier 3 for both. |
| DECISION-007 | Chat Kit target and delivery | Adopted (recommendation) | 120 KB text; zip plus flat upload; per-product facts pending owner tests (QUESTION-001). |
| DECISION-008 | Worked example flavour | Adopted (recommendation) | Neutral `hello_aisop` file-processing utility. |
| DECISION-009 | Release-asset upload in CI | Adopted (recommendation) | GitHub workflow on `v*` tags; `gh release upload` documented as the manual fallback. |
| DECISION-010 | Domain guide location | Adopted (recommendation) | Stay in place with `tier: 3`. |
| DECISION-011 | Generate the traceability matrix | Deferred (recommendation) | Revisit after Phase 3. |
| DECISION-012 | Normative status of method SOPs and root files | Adopted (recommendation) | `docs/001` and `AGENTS.md` Normative; `030`-`070` stay Informative; non-procedure root files demoted in Phase 1. |
| DECISION-013 | Manual acceptance testing per release | Adopted (recommendation) | Two cold-agent runs and one scripted cold-chat run, logged under `reports/baseline/`. |
| DECISION-014 | Method Kit headroom | Applied in Phase 2 | The Phase 2 dry build measured 473,970 bytes (116% of 409,600); budget raised to 524,288 bytes through the RISK-002 process (CHANGELOG entry, TEST-ED-002 text). |
| QUESTION-001 | Chat products and zip upload | Open (owner) | Needs the owner's own tests; recorded in the editions guide (docs/004) when answered. |
| QUESTION-002 | Agentic tools the owner uses | Open (owner) | Determines the pointer list and the TEST-ENTRY-004 tool pair. |

### Execution notes (REV-003)

- EXEC-001: Phase slices were developed as separate commits on one working branch, because the executing session could push to a single branch only. The plan's `practice/rev003-<slice>` branch names are not used for this run.
- EXEC-002: Document revisions follow the repository's existing convention: a controlled document touched during the REV-003 program carries `revision: REV-003` (as REV-002 did), with `last_updated` set to the change date.
- EXEC-003: `AGENTS.md` and the pointer files are tier 2. `docs/300` section 8.1 says tier 0, but section 5.1 lists `AGENTS.md` only in the Method Kit; tier 0 would put it into the Chat Kit, which has no audit tools for its protocol (`docs/166` section 4).
- EXEC-004: PRIN-010 (one check, one owner) wins over the section 7.4 table where they overlap: the cross-tier rule is the per-edition reference resolution in `build_editions.py --check`, and `edition_audit.py` resolves references only in the tree it audits.
- EXEC-005: The Chat Kit unique-basename rule exempts registered example packages (the worked example has its own README_START_HERE.md); EDITION_INFO.md tells flat uploaders to send the example in a separate message.
- EXEC-006: DECISION-012 applied: six root files demoted to Informative; `CODE_OF_CONDUCT.md` kept Normative because it is a conduct policy.
- EXEC-007: The worked example's cap is 12,288 bytes, not the 8,192 in `docs/300` section 9.3: complete document-control headers on its seven Markdown files cost about 3.3 KB on their own.
- EXEC-008: Template heading parity applies to the templates an SOP lists under `## Required sections` (`PLANNING_DOCUMENT_TEMPLATE.md` from `docs/040`, `README_START_HERE_TEMPLATE.md` from `docs/070`); other templates declare `derived_from` without a parity list, because one list per SOP cannot fit several different templates.
- EXEC-009: Coding agents launched with git worktrees create them under `.claude/worktrees/`, inside the tree; `.gitignore` now excludes that folder and every tool walks the tree through the shared git-ignore-aware walk.
- EXEC-010: The `RULE-*` namespace question in `docs/300` Phase 5 is settled as "keep and register": domain guides keep their local ID families (`RULE-<AREA>-`, `LESSON-`, `ACCEPT-<AREA>-`, `THREAD-RULE-`, and others), `docs/003` registers the namespaces, and each guide lists its families in `topics`. Renaming would rewrite tier-3 guides for no reader benefit.
