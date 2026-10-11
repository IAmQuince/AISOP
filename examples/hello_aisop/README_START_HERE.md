---
document_id: DOC-EX-README
title: "hello_aisop: Start Here"
version: 0.1.0
revision: REV-001
status: DRAFT
last_updated: 2026-10-11
package_id: 20261011_00_hello_aisop
machine_reference_prefix: DOC-EX-README
normative_status: Informative
tier: 1
summary: "Start here: what hello_aisop does, how to run and test it, and what must not break."
package_role: example
source: "AISOP worked example"
---

# hello_aisop

## What this is

A small command-line tool that counts the lines, words, and characters in a text file. It is a complete minimal AISOP package, small enough to read in one sitting.

## How to run it

```bash
python hello_aisop.py notes.txt
```

## How to test it

```bash
python hello_aisop.py --smoke-test     # expect SUMMARY: PASS
python hello_aisop.py --diagnostics    # paste this output back to your AI
python tools/aisop_check.py --root .   # after copying the checker, see tools/README.md
```

## What changed

See `CHANGELOG.md`. Version 0.1.0 is the first release.

## What must not break

FEAT-001 (counting) and FEAT-002 (self-check and diagnostics) in `FEATURE_INVENTORY.md`.

## Risks and limitations

See `KNOWN_LIMITATIONS.md`.

## Files that matter

- `hello_aisop.py`: the program, in the numbered sections of a disciplined single-file prototype.
- `000_PLANNING_DOCUMENT.md`: the plan, at hello-world scale.
- `FEATURE_INVENTORY.md` and `ACCEPTANCE_TEST_PLAN.md`: what exists and how it is checked.

## Next step

Add a `--json` output option (planned, not built).
