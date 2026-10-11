---
document_id: DOC-002
title: "Beginner's Guide to AI Agents"
version: 0.3.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20261011_00_aisop
machine_reference_prefix: DOC-002
normative_status: Informative
tier: 1
summary: "For people new to AI coding: chat versus agent, why files beat memory, which edition to pick, and a five-step first project with checks."
source: "REV-003 Phase 2 (docs/300 section 9.1)"
---

# Beginner's Guide to AI Agents

You have an idea for a small program and an AI assistant that can write code. This guide gets you from that idea to a working, checked, packaged first project, and explains the few habits that keep the AI from losing your work between sessions. No programming background is assumed; words in *italics* are in `docs/003_GLOSSARY.md`.

## 1. Chat or agent?

- A **chat** assistant answers messages. It sees only what you type, paste, or upload into the conversation. You copy its code into files and run them yourself.
- An **agent** (for example Claude Code, Codex CLI, Cursor, or Gemini CLI) works inside a folder on your computer. It can read and write files and run commands, so it can run its own tests.

Both work with AISOP. A chat needs you to carry files back and forth; an agent carries them itself but needs the rules file `AGENTS.md` (in the Method Kit).

## 2. What a context window means for you

The AI's *context window* is its working memory for one conversation. Two consequences matter:

1. It forgets everything when the conversation ends. A new chat starts from zero.
2. In a long conversation, early details get pushed out or blurred. The AI may "remember" an older version of your code and quietly drop a feature.

## 3. Give the AI files, not memories

So AISOP keeps the project's memory in files: a *package* folder holding the code, a list of what it does (`FEATURE_INVENTORY.md`), how to check it (`ACCEPTANCE_TEST_PLAN.md`), what changed (`CHANGELOG.md`), and what does not work yet (`KNOWN_LIMITATIONS.md`). At the start of every session you hand the AI the current files, and at the end it hands you updated files plus a short report. Nothing important lives only in the chat.

## 4. Which edition to pick

| You have | Pick | What you do |
|---|---|---|
| Any chat, even a free one, no file upload | Card | Paste `docs/001_AISOP_CORE_RULES.md` (the card) into the chat or its custom instructions. |
| A chat that accepts file uploads | Chat Kit | Upload the Chat Kit zip, or its files, and paste its opener. |
| An agentic coding tool | Method Kit | Unzip it, open the folder in the tool, and type: "Read AGENTS.md and follow its first-five-minutes protocol." |

`docs/004_EDITIONS_AND_UPGRADE_PATH.md` lists every edition with its size and exact opener.

## 5. Your first project in five steps

Each step says what you say, what the AI should produce, how you know it worked, and what to do if it did not. The prompts are in `templates/FIRST_SESSION_PROMPTS.md`.

### Step 1: Start the session

- **You say:** the opener for your edition (section 4), word for word.
- **The AI should:** reply with the AISOP version, the word ORIENT (a *mode* where it only looks and changes nothing), and ask for your idea. With the Chat Kit it also lists the files it can see.
- **It worked if:** the reply names an AISOP version.
- **If not:** start a new chat, paste the card or upload the files again, then the opener. Do not explain AISOP in your own words; let the files do it.

### Step 2: Plan it

- **You say:** prompt 1, "Plan this", with your idea in one or two sentences.
- **The AI should:** ask a few questions (who uses it, on which computer, what it must do), then write a short concept brief from `templates/CONCEPT_BRIEF_TEMPLATE.md` that lists the must-have features with numbered FEAT IDs. No code yet.
- **It worked if:** every section of the brief is filled in, and you agree with the feature list.
- **If not:** say "Fill every section of the concept brief template and list the features with FEAT IDs." Correct anything wrong now; it is cheaper than after coding.

> **Before step 3: running what the AI gives you.**
> 1. Install Python from python.org (tick "Add python.exe to PATH" on Windows).
> 2. Open a terminal: Command Prompt or PowerShell on Windows, Terminal on macOS and Linux.
> 3. Type `python --version` (or `python3 --version`) and press Enter. You should see a version number.
> 4. Make a folder named `yyyymmdd_00_your_idea` (today's date, for example `20261011_00_note_counter`) and save the AI's file there.
> 5. In the terminal, go to that folder (`cd` followed by the folder path) and run `python your_file.py --smoke-test`.
>
> Stuck? Ask the AI: "How do I run this Python file on my computer? I use <Windows, macOS, or Linux>." Some chat products can also run Python for you.

### Step 3: Build a first version

- **You say:** prompt 2, "Prototype this", with your computer and Python version filled in.
- **The AI should:** give one complete Python file, organised in numbered sections like `examples/hello_aisop/hello_aisop.py`, supporting `--version`, `--smoke-test`, and `--diagnostics`, plus the exact commands to run it.
- **It worked if:** `python your_file.py --smoke-test` ends with `SUMMARY: PASS`.
- **If not:** paste the whole error output back and say "Give me the corrected complete file." Never accept a fragment such as "the rest is unchanged".

### Step 4: Package it

- **You say:** prompt 3, "Package and report".
- **The AI should:** give `README_START_HERE.md`, `CHANGELOG.md`, `FEATURE_INVENTORY.md`, `ACCEPTANCE_TEST_PLAN.md`, and `KNOWN_LIMITATIONS.md` for your folder, then the fifteen-field final package report.
- **It worked if:** `python aisop_check.py --root your_folder` (copy `tools/aisop_check.py` from the kit) prints `SUMMARY: PASS`. Without Python, go through `templates/MANUAL_AUDIT_CHECKLIST.md` by hand.
- **If not:** paste the checker's output back; it names each missing piece.

### Step 5: Come back later

- **You say:** in a new chat, give the card or kit again, upload your package folder's files, and describe the one change you want.
- **The AI should:** read the files first, restate the current features, propose the smallest step, and end with the final package report.
- **It worked if:** the report's "Feature removals" line says None (or names a removal you asked for).
- **If not:** point it at core rule 2 in the card: inventory before change.

## 6. Five mistakes beginners make

1. **Letting the AI work from memory.** Re-upload the current files every session.
2. **Asking for everything at once.** One step, one check, then the next.
3. **Accepting partial files.** Ask for the complete file every time.
4. **Skipping the smoke test.** Run it, and paste the output back when it fails.
5. **Not noticing a lost feature.** Read the "Feature removals" line of every report and compare with your feature inventory.

## 7. Where to go next

- `docs/020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md`: the full instructions the AI follows.
- `templates/README.md`: which template to use at each stage.
- `examples/hello_aisop/`: a complete small package to copy the shape of.
- `docs/003_GLOSSARY.md` for words, and `docs/004_EDITIONS_AND_UPGRADE_PATH.md` for editions.
