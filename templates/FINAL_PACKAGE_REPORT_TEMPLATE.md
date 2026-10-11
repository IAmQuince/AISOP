---
document_id: DOC-TPL-FINAL-REPORT
title: "Final Package Report Template"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-TPL-FINAL-REPORT
normative_status: Informative
tier: 1
summary: "The canonical fifteen-field report an AI or person gives at the end of every package delivery or substantial change."
derived_from: DOC-070
source: "Extracted from docs/070 section 18 (canonical per DECISION-003)"
---

# Final Package Report Template

This is the one report format AISOP uses at the end of a delivery. It comes from `docs/070_ZIP_PACKAGE_REVIEW_AND_HANDOFF_SOP.md` section 18 (method edition); the full documents win on conflict. Copy the block, fill every field, and write `None` or `Not applicable` rather than deleting a field.

## Report

```text
Package:                          <zip name, or repository + branch/commit>
Internal folder:                  <top-level folder inside the zip; must equal the zip basename>
Based on:                         <previous package, tag, or commit this run started from>
Purpose:                          <one sentence: what this run was for>
Changed files:                    <every file added, changed, or removed>
Unchanged important files:        <files a reviewer might expect to change but did not>
Tests run:                        <exact commands>
Test results:                     <PASS/FAIL per command, pasted, not paraphrased>
Known limitations:                <what still does not work or was not checked>
Risks:                            <what could go wrong because of this change>
Debt added:                       <shortcuts taken, with where they are recorded>
Debt resolved:                    <debt items closed by this run>
Feature removals:                 <None intended / list with the approval reference>
Broad refactor performed? yes/no: <no / yes with the reason>
Next recommended step:            <the smallest safe next step>
```

## Rules

- Fill the fields from the files and the command output, not from memory.
- `Test results` quotes the tool output; a claim without output is reported as "not run".
- When a field does not apply, say so; an empty field reads as "forgotten".
- When code changed, add the diagnostic command the user can run and paste back.

## Example (fictional)

```text
Package:                          20261011_00_csv_tidy.zip
Internal folder:                  20261011_00_csv_tidy
Based on:                         20261004_00_csv_tidy
Purpose:                          Add a --dry-run flag to the CSV clean-up script.
Changed files:                    csv_tidy.py, CHANGELOG.md, FEATURE_INVENTORY.md, ACCEPTANCE_TEST_PLAN.md
Unchanged important files:        README_START_HERE.md (run instructions still correct)
Tests run:                        python csv_tidy.py --smoke-test
Test results:                     SUMMARY: PASS (4 checks)
Known limitations:                Files over 1 GB not tested.
Risks:                            Low; the flag only skips the final write.
Debt added:                       None.
Debt resolved:                    DEBT-002 (hard-coded output path).
Feature removals:                 None.
Broad refactor performed? yes/no: no
Next recommended step:            Add a --diagnostics report section for file encodings.
```
