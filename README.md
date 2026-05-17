---
document_id: DOC-000-GITHUB-README
title: "AISOP GitHub Repository README"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-GITHUB-README
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# AISOP Seed

This repository is a space of practices as well as a package seed.

AISOP is a self-describing seed package for AI-assisted product development. It supports two compatible workflows:

1. **Old-school zip-package trading** for local experiments, offline review, and direct handoff.
2. **GitHub-hosted practice exploration** where branches, issues, releases, and audit trails become part of the development method.

The repository is intentionally both a working example and a teaching artifact. It does not only prepare a package for GitHub; it documents how to convert a local zip-based package into a GitHub-ready, auditable, safer, collaborative project.

## Start here

Read `README_START_HERE.md` first for the package workflow. Then read:

- `docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md`
- `docs/090_GITHUB_REPOSITORY_BOOTSTRAP_SOP.md`
- `docs/100_RELEASE_VERSIONING_AND_ZIP_HANDOFF_SOP.md`
- `docs/110_SECURITY_AND_SAFETY_BASELINE_SOP.md`
- `docs/120_CONTRIBUTION_REVIEW_AND_ISSUE_WORKFLOW_SOP.md`

## Local audit commands

```bash
python tools/run_all_audits.py
python tools/release_package.py
```

Generated reports are written to `reports/`. Release archives are written to `dist/`.

## Repository concept

`main` should represent the stable reference seed. Branches may represent explored practices, variants, hardware families, GUI stacks, domain examples, or safety classes. A useful branch should explain its tradeoffs, linked requirements, audit status, and release notes.

## License status

This seed includes `LICENSE_DECISION_REQUIRED.md`. Do not publish as an open-source repository until the license decision is resolved.
