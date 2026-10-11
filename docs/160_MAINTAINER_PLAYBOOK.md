---
document_id: DOC-160
title: "Maintainer Playbook"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-160
normative_status: Normative
tier: 2
summary: "Maintainer routines: triage, branch decisions, release decisions, deprecation."
source: "AISOP REV-002 GitHub practice-space update"
---


# Maintainer Playbook

## Weekly or release-cycle routine

- Review open issues.
- Triage safety/security/licensing concerns first.
- Run all audits before release.
- Check whether branch experiments should merge, continue, or archive.
- Confirm known limitations still match reality.

## Branch decisions

A practice branch may be:

- merged into the default branch;
- kept as a named example;
- archived with notes;
- split into a separate project;
- rejected with rationale.

## Release decisions

Before publishing a release:

- verify license status;
- verify safety status;
- verify audit reports;
- verify zip/root-folder naming;
- run `python tools/build_editions.py all`, which also regenerates the manifest, then `python tools/run_all_audits.py`;
- review the edition budgets reported by `python tools/build_editions.py --check`; raise a document's tier rather than a budget (`docs/166_EDITIONS_AND_TIERS_SOP.md`);
- run the cold-agent test (TEST-ENTRY-004) and commit its log as `reports/baseline/cold_agent_test_<package_id>.txt`;
- write release notes.

## Editing generated content

`AGENTS.md` regions, the pointer files, the documentation indexes, and the manifest are generated. Edit their sources (`docs/001`, `config/editions.json`, document headers), never the generated text; the failure message of `python tools/build_editions.py --check` names the source.

## Deprecation

When retiring a practice, preserve enough notes for future users to understand why it was retired and what replaced it.
