---
document_id: DOC-166
title: "Editions and Tiers SOP"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-166
normative_status: Normative
tier: 2
summary: "How one source tree builds four editions: tiers, budgets, generated files and regions, edition markers, staging, release assets, and which tool owns which check."
source: "REV-003 Phase 1; extracted from docs/300 sections 5-7"
---

# Editions and Tiers SOP

## 1. Purpose

AISOP ships as four editions built from one source tree, each matched to a reader's tools and context budget. This SOP is Normative: it binds anyone who adds a document, changes a tier or budget, edits a generated file, or cuts a release. Facts that change (budgets, openers, file lists) live only in `config/editions.json`; this document states the rules.

## 2. Terms

- **Tier**: the integer `tier` (0-3) in a document's header; the lowest edition that includes it.
- **Edition**: a delivery of AISOP. Editions are cumulative: each holds every tier up to its own, so higher editions are strict supersets with the same file names and IDs.
- **GENERATED file or region**: content written by `tools/build_editions.py` (or `tools/manifest_update.py`). It starts with a banner naming its source. Edit the source, never the generated text.
- **Edition marker**: the text `(chat kit edition)`, `(method edition)`, or `(full edition)` on a line, alone or after a comma inside parentheses. It says the files cited on that line ship from that edition upward.

## 3. The editions

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

## 4. Membership

1. A Markdown document with a header belongs to every edition whose tier is at least its `tier`.
2. Other files join through the `include` globs of an edition in `config/editions.json`; higher editions inherit lower editions' globs. The Full edition includes everything.
3. The Card is one rendered file, `AISOP_CARD.md`, built from `docs/001_AISOP_CORE_RULES.md`.
4. Every staged zip edition gains a generated `EDITION_INFO.md` (edition name, root folder, reading order, opener, exact file list) and regenerates its own `docs/index.json`, `docs/000_DOCUMENTATION_INDEX.md`, and `PACKAGE_MANIFEST.md` when it ships them. That is why `python tools/run_all_audits.py` passes inside an unzipped Method Kit as well as in the repository.
5. `AGENTS.md` and the pointer files are tier 2: they are for agentic tools, which start at the Method Kit. Their rules block still comes from the tier-0 `docs/001`. The gameplan (`docs/300`, full edition) gives `AGENTS.md` tier 0 in section 8.1 but lists it only in the Method Kit in section 5.1; this SOP follows section 5.1, because the Chat Kit has no audit tools for the protocol to run.

## 5. Choosing a tier

- Tier 0: only `docs/001`. Nothing else competes for the card's 8 KB.
- Tier 1: what a chat-only beginner needs to apply the method by hand: short guides, templates, the worked example, the profile template, the license notice.
- Tier 2: the full method, governance, controlled records, and tooling, for agentic tools and maintainers.
- Tier 3: domain guides (`docs/010`, `docs/055`, `docs/170-290`), planning records such as `docs/300`, source notes, and baseline evidence (full edition).

When an edition nears its budget, raise the tier of a document; do not raise the budget. A budget change needs a CHANGELOG entry and a changed acceptance text. Never maintain a condensed copy of a document in another folder or tier: if a long document needs a short form, split it into two source documents with different tiers.

## 6. Generated files and regions

| Generated | Source | Tool |
|---|---|---|
| `AGENTS.md` region `rules` | the `AISOP:RULES` block in `docs/001` | `build_editions.py entry` |
| `AGENTS.md` region `commands` | `commands` in `config/editions.json` | `build_editions.py entry` |
| `docs/001` region `card-opener` | `openers.card` | `build_editions.py entry` |
| this document's region `editions-table` | `editions` and `openers` | `build_editions.py entry` |
| `docs/004` region `editions-table` | `editions` and `openers` | `build_editions.py entry` |
| `README.md` region `chooser` | `editions`, `openers`, `repository_url`, `package_id` | `build_editions.py entry` |
| `README_START_HERE.md` regions `openers` and `reading-order` | `openers`; `entry_read_order` and document summaries | `build_editions.py entry` and `index` |
| `templates/MANUAL_AUDIT_CHECKLIST.md` | the `CHECKS` table in `tools/aisop_check.py` | `build_editions.py entry` |
| `CLAUDE.md`, `GEMINI.md` | `pointer_files` | `build_editions.py entry` |
| `docs/index.json`, `docs/000_DOCUMENTATION_INDEX.md` | every document-control header | `build_editions.py index` |
| `PACKAGE_MANIFEST.md` | the package tree | `manifest_update.py` (run by `build_editions.py all`) |
| `dist/*` (not committed) | the whole tree | `build_editions.py zips` |

After editing any source, run `python tools/build_editions.py all`, then `python tools/run_all_audits.py`. Generated committed files carry no timestamps and no exact byte counts, so `python tools/build_editions.py --check` gives the same answer on every machine.

## 7. References and edition markers

- Every relative Markdown link and every backticked path that starts with one of the folders docs, tools, templates, or examples must resolve in the full tree, and inside each staged edition unless the line carries a marker for a higher edition. `docs/NNN` and `docs/NNN-MMM` shorthand resolve when a document with that number exists.
- This per-edition resolution is also the cross-tier rule: a tier-1 document that cites a tier-2 file without a marker fails in the Chat Kit. It is implemented once, in `build_editions.py --check`, and not repeated elsewhere.
- Write a downstream project's own paths with a leading `./` (for example `./tools/diagnostic_harness.py`), so they are not read as AISOP paths.
- Planning records (`link_check.planning_records`) describe proposed paths and are not checked. History records (`link_check.history_records`, the changelog and workplan) are checked in the full tree only.
- Fenced code blocks are examples and are not checked.

## 8. Budgets

Byte budgets are the enforced truth; token counts are estimates (roughly bytes divided by four). The check warns at `warn_fraction` (75%) and fails at 100%, listing the five largest files. The Card has its own budget and its rules block is capped (`card.rules_block_budget_bytes`) so `AGENTS.md`, which embeds the rules, stays under `agents_file.budget_bytes`. Pointer files stay under `pointer_budget_bytes`. The Chat Kit also has `max_files`, and its basenames must be unique so its files can be uploaded one by one; files inside registered example packages are exempt and are uploaded in a separate message.

## 9. Release assets

`python tools/build_editions.py zips` writes, under `dist/`: `<package_id>.zip`, `<package_id>_method.zip`, `<package_id>_chatkit.zip`, `AISOP_CARD.md`, and `EDITIONS_CHECKSUMS.txt`. Each zip unpacks to a single folder named like the zip (REQ-PKG-001), with members sorted and fixed timestamps. The checksum file lists, per edition, a content checksum (sha256 over the sorted members, each fed as length-prefixed path and data) that a rebuild of the same tag reproduces, and the file's own sha256 for download integrity only, because compressed bytes depend on the zlib build.

## 10. Repository layout

```text
AGENTS.md, CLAUDE.md, GEMINI.md     agent entry file (hand-written) and generated pointers
README.md, README_START_HERE.md     landing page and first file to read
config/editions.json                editions, budgets, openers, pointer list, link-check lists
config/package_metadata.json        package identity, required files, audit lists
docs/001-004                        card and beginner documents (tiers 0-1)
docs/005-166                        requirements, method, governance (tier 2; 020 and 050 are tier 1)
docs/170-290, docs/300+             domain guides and planning records (tier 3)
docs/index.json                     generated machine-readable map of every document
templates/, examples/               fill-in forms and the worked example (tier 1)
tools/, tests/                      standard-library audits, generators, smoke test
reports/baseline/                   committed audit evidence (tier 3); reports/*.txt are runtime output
dist/                               build output, git-ignored
```

## 11. Which tool owns which check

Each check lives in exactly one tool (PRIN-010 in `docs/300`, full edition).

| Check | Owner |
|---|---|
| Required files and folders; complete headers incl. `tier` and `summary`; unique `document_id`; personal-reference and profile scan; code-fence parity; example-package registration | `tools/package_structure_audit.py` |
| Required repository files and content checks; license; CI default branch; canonical report citations; release workflow order; untracked runtime reports | `tools/repo_health_audit.py` |
| Generated files fresh; edition budgets, `max_files`, unique basenames; references resolve inside each edition | `tools/build_editions.py --check` |
| References resolve in the tree; `AGENTS.md` size, identity and status; rules-block cap; pointer files; card labels equal the report template's; header `package_id` consistency; template parity and placeholder IDs; ID citations in tiers 0-1; glossary coverage; size caps; cold-agent log and superseded-tier warnings | `tools/edition_audit.py` |
| Manifest matches the tree | `tools/manifest_update.py --check` |
| Index valid and complete; negative cases (an edited generated region, a missing `tier`) make the audits fail; the Method Kit passes its own audits; Chat Kit contents; the example's lite audit; edition zips reproduce; release from a renamed folder | `tests/smoke_test.py` |
