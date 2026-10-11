---
document_id: DOC-000-WORKPLAN-CURRENT-RUN
title: "Workplan Current Run"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
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

### Phase 0 (complete)

- 0a license gate retired and CI on the default branch; 0b release root from config, runtime reports untracked, manifest checked; 0c interim `AGENTS.md` and canonical report; 0d person-neutral `docs/020`; 0e fences, orphan lines, content fixes, fence parity.
- Not done by this run (owner actions): merging or closing the Dependabot pull requests once CI is green on `master`.

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
| DECISION-014 | Method Kit headroom | Adopted (recommendation) | Keep 409,600 bytes; raise to 524,288 only through the RISK-002 process if the Phase 2 dry build exceeds 90%. |
| QUESTION-001 | Chat products and zip upload | Open (owner) | Needs the owner's own tests; recorded in the editions guide (docs/004) when answered. |
| QUESTION-002 | Agentic tools the owner uses | Open (owner) | Determines the pointer list and the TEST-ENTRY-004 tool pair. |

### Execution notes (REV-003)

- EXEC-001: Phase slices were developed as separate commits on one working branch, because the executing session could push to a single branch only. The plan's `practice/rev003-<slice>` branch names are not used for this run.
- EXEC-002: Document revisions follow the repository's existing convention: a controlled document touched during the REV-003 program carries `revision: REV-003` (as REV-002 did), with `last_updated` set to the change date.
- EXEC-003: `AGENTS.md` and the pointer files are tier 2. `docs/300` section 8.1 says tier 0, but section 5.1 lists `AGENTS.md` only in the Method Kit; tier 0 would put it into the Chat Kit, which has no audit tools for its protocol (`docs/166` section 4).
- EXEC-004: PRIN-010 (one check, one owner) wins over the section 7.4 table where they overlap: the cross-tier rule is the per-edition reference resolution in `build_editions.py --check`, and `edition_audit.py` resolves references only in the tree it audits.
- EXEC-005: The Chat Kit unique-basename rule exempts registered example packages (the worked example has its own README_START_HERE.md); EDITION_INFO.md tells flat uploaders to send the example in a separate message.
- EXEC-006: DECISION-012 applied: six root files demoted to Informative; `CODE_OF_CONDUCT.md` kept Normative because it is a conduct policy.
