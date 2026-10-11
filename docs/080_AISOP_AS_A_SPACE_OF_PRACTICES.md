---
document_id: DOC-080
title: "AISOP as a Space of Practices"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-080
normative_status: Normative
tier: 2
summary: "Why the repository is a practice space: branches as experiments, the practice loop, required branch notes."
source: "AISOP REV-002 GitHub practice-space update"
---


# AISOP as a Space of Practices

AISOP treats a repository as more than a storage location. A repository is a practice space: a visible, branchable, testable record of competing ways to move from idea to working product.

## Core idea

The package should always do two jobs at once:

1. provide a working seed package; and
2. teach the method used to create, audit, revise, branch, release, and improve that seed package.

This means a future user can inspect the package as an artifact and also learn how to construct a similar artifact.

## Practice-space loop

```text
local idea
  -> monolithic planning document
  -> prototype
  -> audited zip package
  -> GitHub repository
  -> practice branch
  -> review/audit
  -> tagged release
  -> downloadable zip handoff
  -> improved seed
```

## Branches as experiments

Branches may explore different practices:

- documentation-heavy product development;
- hardware-control safety discipline;
- offline zip-only handoff;
- GUI application structure;
- teaching/learning examples;
- solo-maker MVP workflow;
- team review workflow;
- strict regulated-development approximation.

A branch is useful when it states its tradeoffs and provides audit evidence.

## Required branch notes

A serious practice branch should include:

- purpose;
- scope;
- new or changed requirements;
- expected user;
- safety/security/licensing impact;
- audit command results;
- known limitations;
- merge or archive recommendation.

## Acceptance

A practice-space update is acceptable when a user can understand both what the package is and how the package was made.
