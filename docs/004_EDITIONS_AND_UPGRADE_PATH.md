---
document_id: DOC-004
title: "Editions and Upgrade Path"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-004
normative_status: Informative
tier: 1
summary: "The four AISOP editions, their sizes and openers, what each adds, and how zips, releases, and the repository relate."
source: "REV-003 Phase 2 (docs/300 sections 5 and 9.1)"
---

# Editions and Upgrade Path

AISOP comes in four editions built from the same files. Pick the smallest one your tools can use; move up when you need more.

<!-- GENERATED:BEGIN editions-table | by tools/build_editions.py from config/editions.json; edit the source, not this region -->
| Tier | Edition | Budget | Delivery | Audience |
|---|---|---|---|---|
| 0 | Card | 8,192 bytes | AISOP_CARD.md (release asset; rendered from docs/001_AISOP_CORE_RULES.md) | Any chat product, including free plans and custom-instruction boxes. |
| 1 | Chat Kit | 122,880 bytes, at most 40 files | <package_id>_chatkit.zip, or its files uploaded individually | Chat-only plans with file upload but no filesystem or shell; beginners. |
| 2 | Method Kit | 524,288 bytes | <package_id>_method.zip, or a clone with tier-3 files ignored | Agentic tools with a filesystem (Claude Code, Codex CLI, Cursor, Copilot agents, Gemini CLI); practitioners who want the full method and audit tooling without the domain guides. |
| 3 | Full | unbudgeted | git clone, or <package_id>.zip | Maintainers, contributors, and projects that need the domain guides. |

Openers (the first message to the AI):

- **Card:** Use the AISOP card above as your operating rules. Reply with the AISOP version it names and the word ORIENT, then ask me for my idea.
- **Chat Kit:** I have uploaded the AISOP Chat Kit. Read EDITION_INFO.md, then README_START_HERE.md, then the card. Work in ORIENT or APPLY mode only and never ask for a file that EDITION_INFO.md does not list. Reply with: the AISOP version and package_id, the files you can see, the word ORIENT, and the question 'what is your idea?'.
- **Method Kit:** Read AGENTS.md and follow its first-five-minutes protocol.
- **Full:** Read AGENTS.md and follow its first-five-minutes protocol.
<!-- GENERATED:END editions-table -->

## What each edition adds

- **Card:** the core rules, the minimum package, ID rules, and the report fields, in one file you paste into a chat.
- **Chat Kit:** the card plus this guide, the beginner's guide, the glossary, the operating instructions, the prototype SOP, the templates, the worked example, and the package checker `tools/aisop_check.py`.
- **Method Kit:** everything above plus the full method SOPs, governance, requirements, `AGENTS.md`, and the audit tools. Its audits pass inside the unzipped folder.
- **Full:** everything, including the domain guides (hardware, data acquisition, quality control, embedded boards, networking, interfaces), planning records, and audit history.

Higher editions are strict supersets: same file names, same IDs, nothing to re-learn. Lower editions are shortened on purpose; the full documents win on conflict.

## Zips, releases, and the repository

Each release on the project's GitHub Releases page carries `AISOP_CARD.md` and three zips: `<package_id>_chatkit.zip`, `<package_id>_method.zip`, and `<package_id>.zip` (Full). Each zip unpacks to one folder with the same name as the zip, and `EDITION_INFO.md` inside lists every file it holds. A `git clone` gives you the Full edition in a folder usually named `AISOP`; the folder name does not matter, because the identity is the `package_id` in the headers.

## Chat products and uploads

Whether a chat product accepts a zip, reads attached files whole or on demand, and how many files it takes per message changes between products and plans. Results from the owner's own tests are recorded here as they are made.

| Product and plan | Zip upload | Files read | Files per message |
|---|---|---|---|
| Not yet tested (QUESTION-001) | - | - | - |

If a product rejects the zip, upload the Chat Kit files one by one (their names are unique), sending the `examples/` files in a separate message. If it takes no files at all, use the Card.
