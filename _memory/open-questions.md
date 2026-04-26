---
name: Open Design Questions
description: Unresolved architectural questions awaiting Raja's input — answers drive Phase 2 build
type: project
---

These map to ARCHITECTURE.md Section 6. Answer here to unblock builds.

## Q1 | Skill decay — should stale skills reduce match score?
Options: A (hard cutoff at 5yr), B (decay function), C (no decay)
Recommendation: B (decay function)
**Raja's answer**: [TO-FILL]

## Q2 | JD parsing — regex (now) or LLM for required/preferred split?
Options: A (binary, current), B (LLM via Claude API, ~$0.01/JD), C (heuristic section detection)
Recommendation: C first, then B at scale
**Raja's answer**: [TO-FILL]

## Q3 | Single profile or per-cluster overlays?
Options: A (single + narrative), B (per-cluster files), C (weight multipliers in roles-graph)
Recommendation: C (focus_bonus multipliers)
**Raja's answer**: [TO-FILL — defaulting to C until told otherwise]

## Q4 | NetworkX for multi-hop graph traversal?
Main payoff: "shortest learning path to role X" via graph BFS
Effort: ~2 hrs
**Raja's answer**: [TO-FILL]

## Q5 | Claude API in the automated pipeline?
Options: A (manual only), B (full API), C (hybrid: regex screens, Claude narrates ≥60% roles)
Recommendation: C
**Raja's answer**: [TO-FILL]

## Q6 | Missing skill domains?
Current: hardware, embedded, systems, backend, frontend, AI/ML, legal tech, fintech, leadership
**Raja's answer**: [TO-FILL — any domains missing?]

## Q7 | Missing role clusters?
Current 14: silicon_engineer, soc_architect, ai_hardware_engineer, eda_engineer,
firmware_engineer, ai_engineer, ml_engineer, ml_infra_engineer, systems_engineer,
backend_engineer, legal_tech_engineer, fintech_engineer, staff_engineer
**Raja's answer**: [TO-FILL — any missing? e.g. Solutions Architect, TPM, DevRel?]

## Q8 | Geographies — any to add?
Current: Switzerland, UK, Germany, Netherlands, India
**Raja's answer**: [TO-FILL — France? Singapore? UAE? US with sponsorship?]
