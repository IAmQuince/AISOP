---
document_id: DOC-TPL-START-HERE
title: "README_START_HERE Template"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-TPL-START-HERE
normative_status: Informative
tier: 1
summary: "The first file of every package: what it is, how to run and test it, and what must not break."
derived_from: DOC-070
source: "REV-003 Phase 2 template"
---

# <Project name>

## What this is
<One paragraph: what it does, for whom, and which version this is.>

## How to run it
<Exact commands, from unpacking the zip to the first result. For a zip: unzip it, check the top folder has the same name as the zip, open a terminal in that folder.>

## How to test it
<`python <script>.py --smoke-test` (expect SUMMARY: PASS) and `--diagnostics` (paste the output back to your AI).>

## What changed
<The latest CHANGELOG entry in one line.>

## What must not break
<The FEAT- IDs from FEATURE_INVENTORY.md that matter most.>

## Risks and limitations
<The top items from KNOWN_LIMITATIONS.md.>

## Files that matter
<The handful of files a reviewer should open first.>

## Next step
<The smallest safe next step.>
