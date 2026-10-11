---
document_id: DOC-100
title: "Release Versioning and Zip Handoff SOP"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-100
normative_status: Normative
tier: 2
summary: "Package naming, release procedure, and how GitHub releases and zip handoff stay aligned."
source: "AISOP REV-002 GitHub practice-space update"
---


# Release Versioning and Zip Handoff SOP

## Purpose

Keep GitHub releases and old-school zip trading aligned, for every edition.

## Naming

Package names follow:

```text
yyyymmdd_00_short-description
```

This package's name is the `package_id` in `config/package_metadata.json` and in every document header. A release produces, under `dist/`:

```text
<package_id>.zip            unpacks to <package_id>/            (Full edition)
<package_id>_method.zip     unpacks to <package_id>_method/     (Method Kit)
<package_id>_chatkit.zip    unpacks to <package_id>_chatkit/    (Chat Kit)
AISOP_CARD.md                                                   (Card)
EDITIONS_CHECKSUMS.txt      content and file checksums per edition
```

## Release procedure

1. When the identity changes, run `python tools/bump_release.py --package-id <yyyymmdd_00_name> --version <X.Y.Z>`, then `python tools/build_editions.py all`, and commit that alone (it changes only `package_id`, `version`, and generated files).
2. Update the changelog and the revisions of touched documents; update requirements and traceability if needed.
3. Run `python tools/build_editions.py all`, then `python tools/run_all_audits.py`; both must pass.
4. Run the cold-agent test (TEST-ENTRY-004) and commit its log as `reports/baseline/cold_agent_test_<package_id>.txt`, with a `baseline_<revision>_*` snapshot of the audit run.
5. Tag the commit `v<version>` (the tag must equal `version` in config) and push the tag. `.github/workflows/release.yml` checks the tag, runs every audit, builds the assets only after a green run, checks each archive, and attaches the assets to the release.
6. Manual fallback when the workflow cannot run: `python tools/run_all_audits.py`, `python tools/build_editions.py zips`, then `gh release create v<version> dist/* --title "AISOP v<version>" --notes-file <notes>`.
7. Verify: download each zip, run `python tools/archive_name_audit.py <zip>`, and compare the file's sha256 with `EDITIONS_CHECKSUMS.txt`.

For a direct handoff without a release, `python tools/release_package.py --edition all` writes the same assets and runs the archive check on each zip.

## Zip handoff rule

A recipient should be able to unzip the package, read `README_START_HERE.md` (and `EDITION_INFO.md`), run the audits where the edition ships them, and understand whether the package is safe to use for their intended purpose.

## GitHub release rule

A GitHub release corresponds to an audited package state and includes release notes, known limitations, safety, security and license status, and the edition assets above. Content checksums let anyone rebuild the same tag and get the same member files; the zip files' own checksums are for download integrity only.
