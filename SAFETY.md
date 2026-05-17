---
document_id: DOC-000-SAFETY
title: "Safety Baseline"
version: 0.2.0
revision: REV-001
status: DRAFT-REFERENCE
last_updated: 2026-05-16
package_id: 20260516_00_seed
machine_reference_prefix: DOC-000-SAFETY
normative_status: Normative
source: "AISOP REV-002 GitHub practice-space update"
---


# Safety Baseline

AISOP-generated projects may touch software-only workflows, hardware control, electrical systems, heating, pressure, fluids, motion, lab instrumentation, chemistry, or user data. Safety classification is required before a project is treated as product-ready.

## Safety classes

- `SAFE-CLASS-0`: documentation or analysis only.
- `SAFE-CLASS-1`: local software tool with no physical output control.
- `SAFE-CLASS-2`: reads sensors or instruments but does not command hazardous outputs.
- `SAFE-CLASS-3`: commands power, motion, heat, pressure, fluid, chemical, or test equipment.
- `SAFE-CLASS-4`: safety-critical, regulated, public-facing, or human-impacting system.

## Mandatory rules for controlled hardware

- Default outputs to safe state on startup, fault, and shutdown.
- Include emergency stop or equivalent disable pathway when physical risk exists.
- Log commands, setpoints, measured values, faults, and shutdown events.
- Separate simulation/demo mode from live-control mode.
- Require human review before connecting new code to live equipment.

## Safety handoff requirement

Every downstream product should include a safety note explaining its class, hazards, mitigations, and remaining limitations.
