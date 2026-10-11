---
document_id: DOC-TPL-USER-PROFILE
title: "User Profile Template"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-TPL-USER-PROFILE
normative_status: Informative
tier: 1
summary: "Six questions that tell the AI who it is working with; save the answers as a local, git-ignored USER_PROFILE.md."
derived_from: DOC-020
source: "REV-003 Phase 0d: personal preferences moved out of docs/020"
---

# User Profile Template

Your profile tells the AI who it is working with, so `docs/020_AI_COLLABORATION_OPERATING_INSTRUCTIONS.md` can stay the same for everyone. Copy this file to `USER_PROFILE.md` at your project root (it is git-ignored, so it never leaves your machine), replace each answer, and delete the example. In a chat product without files, paste your answers into the custom-instructions box.

## The six questions

1. **Experience:** How familiar are you with programming and with AI tools, and what is your field?
   Answer:
2. **Target environment:** Which computers, operating systems, language versions, and hardware must the code run on? Any offline, legacy, or locked-down machines?
   Answer:
3. **Kind of work:** What do you usually build (scripts, desktop tools, data logging, hardware control, web pages, games)?
   Answer:
4. **Deliverables:** How do you want finished work delivered (zip packages, git commits, single files), and how should runs be named?
   Answer:
5. **Communication and style:** How should the AI talk to you (brief or detailed, level of explanation), and what visual style do you want in interfaces?
   Answer:
6. **Hard constraints:** Dependencies you cannot install, safety-critical equipment, data that must never leave the machine, anything the AI must never do?
   Answer:

## Example profile (fictional, delete before use)

Written in the first person by an imaginary user, to show the level of detail that helps.

1. Experience: I am an engineer (physics, electrochemistry, controls, data acquisition, embedded systems). Treat me as a technical peer; skip the basics.
2. Target environment: Windows 10/11 desktops, Raspberry Pi, LabJack devices, Arduino/ESP32 boards, and some offline Windows XP machines running Python 2.7. Confirm the target before writing code.
3. Kind of work: practical tools for real lab workflows: device interfaces, sensors, local files, data logging, simulations, desktop interfaces.
4. Deliverables: a clean zip package at the end of each run, named `yyyymmdd_00_description`, with docs, tests, a diagnostic harness, and a changelog.
5. Communication and style: direct and concise, no praise. Interfaces in a dark navy/black theme with thin blue/cyan accents, compact controls, legends with real colour swatches, independently scrollable panels, no unnecessary horizontal scrolling.
6. Hard constraints: never lose existing features between iterations; standard library only on the legacy machines; hardware tools must start in a safe state and never actuate on startup.
