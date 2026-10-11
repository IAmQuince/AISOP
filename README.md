---
document_id: DOC-000-GITHUB-README
title: "AISOP"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-000-GITHUB-README
normative_status: Informative
tier: 2
summary: "GitHub landing page: what AISOP is, which edition to download, and how agents and maintainers start."
source: "AISOP REV-002 GitHub practice-space update"
---

# AISOP

AISOP is a set of working procedures for building software with an AI assistant without losing features, decisions, or context between sessions. The project's memory lives in files (a package) that carry their own requirements, feature list, tests, and history, so any person or AI tool can pick the work up cold. This repository is both the method and a working example of it.

## Choose your edition

<!-- GENERATED:BEGIN chooser | by tools/build_editions.py from config/editions.json and config/package_metadata.json; edit the source, not this region -->
| If you use | Get | Size budget | Then type |
|---|---|---|---|
| Any chat product, including free plans and custom-instruction boxes. | **Card**: [AISOP_CARD.md](https://github.com/IAmQuince/AISOP/releases/latest/download/AISOP_CARD.md) | 8,192 bytes | Use the AISOP card above as your operating rules. Reply with the AISOP version it names and the word ORIENT, then ask me for my idea. |
| Chat-only plans with file upload but no filesystem or shell; beginners. | **Chat Kit**: [20261011_00_aisop_chatkit.zip](https://github.com/IAmQuince/AISOP/releases/latest/download/20261011_00_aisop_chatkit.zip) | 122,880 bytes, at most 40 files | I have uploaded the AISOP Chat Kit. Read EDITION_INFO.md, then README_START_HERE.md, then the card. Work in ORIENT or APPLY mode only and never ask for a file that EDITION_INFO.md does not list. Reply with: the AISOP version and package_id, the files you can see, the word ORIENT, and the question 'what is your idea?'. |
| Agentic tools with a filesystem (Claude Code, Codex CLI, Cursor, Copilot agents, Gemini CLI); practitioners who want the full method and audit tooling without the domain guides. | **Method Kit**: [20261011_00_aisop_method.zip](https://github.com/IAmQuince/AISOP/releases/latest/download/20261011_00_aisop_method.zip) | 524,288 bytes | Read AGENTS.md and follow its first-five-minutes protocol. |
| Maintainers, contributors, and projects that need the domain guides. | **Full**: `git clone https://github.com/IAmQuince/AISOP.git` or [20261011_00_aisop.zip](https://github.com/IAmQuince/AISOP/releases/latest/download/20261011_00_aisop.zip) | unbudgeted | Read AGENTS.md and follow its first-five-minutes protocol. |
<!-- GENERATED:END chooser -->

The download links work from the first tiered release (v0.3.0) on the GitHub Releases page. Until then, clone the repository, or build the files yourself with `python tools/build_editions.py zips` (they land in `dist/`).

New to AI coding? Start with `docs/002_BEGINNERS_GUIDE_TO_AI_AGENTS.md`. The editions are explained in `docs/004_EDITIONS_AND_UPGRADE_PATH.md`. Every package starts with `README_START_HERE.md`.

## For coding agents

Open the folder in your agentic tool and type: "Read AGENTS.md and follow its first-five-minutes protocol." `AGENTS.md` is the binding entry file. Claude Code and Gemini CLI load it through `CLAUDE.md` and `GEMINI.md`; Codex CLI, Cursor, and GitHub Copilot's coding agent read `AGENTS.md` directly.

## For maintainers

```bash
python tools/run_all_audits.py            # every audit; --quiet for the summary only
python tools/build_editions.py all        # regenerate generated files after editing a source
python tools/build_editions.py --check    # generated files fresh, editions within budget
python tools/build_editions.py zips       # release assets into dist/
```

Runtime reports go to `reports/` (git-ignored); release files go to `dist/`. `docs/166_EDITIONS_AND_TIERS_SOP.md` explains tiers and generated files; `docs/160_MAINTAINER_PLAYBOOK.md` covers releases.

## What is inside

- `docs/001`-`docs/004`: the card, beginner's guide, glossary, and editions guide.
- `docs/005`-`docs/166`: requirements, the method (concept, plan, prototype, migrate, package), and governance.
- `templates/` and `examples/hello_aisop/`: fill-in forms and a complete small package.
- `tools/` and `tests/`: standard-library audits and the edition builder.
- `docs/170`-`docs/290`: domain guides (hardware and data acquisition, quality control, embedded boards, MIDI, networking, interfaces), in the Full edition only (full edition).

## Repository concept

This repository is a space of practices as well as a package seed: branches can explore practices, variants, hardware families, or safety classes, and a useful branch states its tradeoffs, linked requirements, audit status, and release notes (`docs/080_AISOP_AS_A_SPACE_OF_PRACTICES.md`). Old-school zip trading and GitHub use stay equally supported. The default branch is `master` (recorded as `default_branch` in `config/package_metadata.json`); CI runs on pushes to `master` or `main` and on every pull request.

## License

AISOP is released under the MIT License; see `LICENSE.txt` and `NOTICE.md`.
