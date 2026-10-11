---
document_id: DOC-TPL-CONCEPT
title: "Concept Brief Template (Lite)"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-TPL-CONCEPT
normative_status: Informative
tier: 1
summary: "A one-page concept brief to fill in before any code is written."
derived_from: DOC-030
source: "REV-003 Phase 2 template"
---

# Concept Brief (Lite)

The short form of `docs/030` (method edition). Use the full brief for anything with hardware, legacy systems, data that is costly to lose or safety-relevant, or refactoring. A small personal tool that keeps one simple data file can use this form; describe the file under "Constraints and safety".

## Project identity
Name: <short name>  Package name: <yyyymmdd_00_short-description>  Owner: <you>

## In plain words
<Two or three sentences: what it does and for whom.>

## Users and workflows
<Who uses it, and the three to five things they do, step by step.>

## Must-have features
<List them. These become FEAT- IDs in the feature inventory.>

## Out of scope for now
<What this run will not do.>

## Target environment
<Computer, operating system, language version, offline or online, hardware attached.>

## Constraints and safety
<Dependencies allowed, data that must not be lost, anything that moves or switches power.>

## Success looks like
<How you will check it works. These become TEST- IDs.>

## Open questions
<QUESTION-001 ... things to settle before coding.>

## Boundaries for this run
<Exactly what the AI may build or change in the next run, and what it must not touch.>
