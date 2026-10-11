---
document_id: DOC-000-KNOWN-LIMITATIONS
title: "Known Limitations"
version: 0.2.0
revision: REV-003
status: DRAFT-REFERENCE
last_updated: 2026-10-11
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-KNOWN-LIMITATIONS
normative_status: Informative
tier: 2
summary: "What this package does not do or has not verified, stated so nobody over-claims it."
source: "Generalized AI-assisted coding SOP source text"
---

# Known Limitations

LIMIT-001
Title: First-pass reference package
Description: This package is a structured reference seed, not a finished production application.
Impact: The package demonstrates expected structure and documentation patterns but does not ship an executable product beyond audit/smoke-test tools.
Status: Current

LIMIT-002
Title: Informative technical guides
Description: Most long technical guides in `docs/` are informative reference material. The authoritative package requirements are centralized in `docs/005_PRODUCT_REQUIREMENTS.md`.
Impact: Future projects should create their own project-specific requirements rather than treating every sentence in the reference guides as normative.
Status: Current

LIMIT-003
Title: Manual editorial review still recommended
Description: The source text was cleaned and generalized, but a human editorial pass is still recommended before public distribution.
Impact: Tone and wording may still need refinement for a specific audience.
Status: Current

LIMIT-004
Title: No external dependency validation
Description: The package does not download or validate the current status of all third-party tools described in the guides.
Impact: Users should verify installer sources and package versions when applying the instructions.
Status: Current

LIMIT-005
Title: Edition budgets are bytes; token counts are estimates
Description: Edition and card budgets are enforced in bytes. Token counts (roughly bytes divided by four) vary by model and chat product, so "fits in a chat" is an estimate until a logged session confirms it.
Impact: A product with a small context or upload limit may still truncate the Chat Kit. The audit warns at 75% of each budget.
Status: Current

LIMIT-006
Title: Agent entry depends on tool conventions
Description: `AGENTS.md` is tool-agnostic. Pointer files exist only for Claude Code (`CLAUDE.md`) and Gemini CLI (`GEMINI.md`); other agentic tools are expected to read `AGENTS.md` natively, which can change between tool versions.
Impact: If a tool stops auto-loading the entry file, type the Method Kit opener: "Read AGENTS.md and follow its first-five-minutes protocol." The cold-agent test (TEST-ENTRY-004) is manual and covers one tool per release until Phase 4 adds a second.
Status: Current

LIMIT-007
Title: Lower editions are lossy
Description: The Card and the Chat Kit leave out most of the method and all domain guides by design. Lines that cite a file from a higher edition are marked "(method edition)" or "(full edition)".
Impact: A chat model using a lower edition can only follow what it was given; the full documents win on conflict.
Status: Current

## REV-002 Known Limitations

- The package is released under the MIT License (`LICENSE.txt`). Third-party material referenced by the domain guides keeps its own license; review it before redistribution (see `NOTICE.md`).
- GitHub branch protection, secret scanning, repository visibility, and release permissions require maintainer configuration outside the file tree.
- The local secret scan is intentionally lightweight and does not replace GitHub security features or professional security review.
- CI workflows are provided as baseline examples and may need adjustment for downstream projects with dependencies.
- The package is a practice seed and teaching artifact, not a complete production product.
- Hardware-control safety rules are baseline doctrine only; downstream live-control projects need project-specific hazard review.
