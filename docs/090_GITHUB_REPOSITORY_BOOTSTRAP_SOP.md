---
document_id: DOC-090
title: "GitHub Repository Bootstrap SOP"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-090
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# GitHub Repository Bootstrap SOP

## Purpose

Convert an audited zip package into a GitHub-ready repository while preserving zip handoff compatibility.

## Inputs

- audited local package folder;
- passing `python tools/run_all_audits.py` result;
- license decision or explicit license-decision gate;
- safety/security status.

## Procedure

1. Confirm the package root folder name matches the intended repository/archive basename.
2. Initialize the repository from the package root.
3. Commit the package exactly as an audited baseline.
4. Add or verify `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SAFETY.md`, and license-status files.
5. Add `.github/` issue templates, pull-request template, workflows, and Dependabot configuration.
6. Run `python tools/run_all_audits.py`.
7. Create a bootstrap issue or project board for license, safety, roadmap, and branch practices.
8. Create the first tag only after the release dry run passes.

## Repository settings checklist

- Enable branch protection or rulesets for `main` when collaboration begins.
- Require passing status checks before merge.
- Require pull request review for non-trivial changes.
- Enable secret scanning/push protection when available.
- Define who may publish releases.
- Decide whether discussions, wiki, projects, or pages are in scope.

## Output

A repository that remains usable as a local zip package and as a GitHub-hosted practice space.
