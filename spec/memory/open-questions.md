---
name: Open Design Questions
description: Unresolved questions awaiting input — answers drive what Claude builds next
type: project
---

## Architecture questions (from ARCHITECTURE.md Section 6)

### Q1 | Skill decay — should stale skills reduce match score?
Options: A (hard cutoff at 5yr), B (decay function), C (no decay, trust self-assessment)
Recommendation: B — `decay(y) = 1.0 if y≤2, 0.8 if y≤5, 0.6 if y≤10, 0.4 if y>10`
**Answer**: [TO-FILL]

### Q2 | JD parsing — regex now or LLM for required/preferred split?
Options: A (binary, current), B (Claude API ~$0.01/JD), C (heuristic section detection)
Recommendation: C first, then B at scale (50+ JDs/week)
**Answer**: [TO-FILL]

### Q3 | Single profile or per-cluster overlays?
Decision already made: AD-03 → Option C (focus_bonus multipliers). Defaulting.
**Answer**: Using Option C — no action needed unless you disagree.

### Q4 | NetworkX for multi-hop graph traversal?
Payoff: "shortest learning path to role X" via BFS through skill implies graph
Effort: ~2 hrs to implement
**Answer**: [TO-FILL — yes/no]

### Q5 | Claude API in the automated pipeline?
Options: A (manual only), B (full API), C (hybrid: regex screens, Claude narrates ≥60% roles)
Recommendation: C
**Answer**: [TO-FILL]

---

## Profile + targeting questions

### Q6 | Which domains are your deepest? (from profile/domains.md)
The 10 domains are listed. Which 3 do you have the most professional depth in?
This determines the primary pitch angle and which lesson plans to prioritize.
**Answer**: [TO-FILL]

### Q7 | Missing skill domains?
Ontology currently covers: hardware, embedded, systems, backend, frontend, AI/ML, legal tech, fintech, leadership, computer_vision, edge_ai.
Any domains missing that appear in your target JDs?
**Answer**: [TO-FILL — signal processing? quantum? biotech? automotive AUTOSAR?]

### Q8 | Missing role clusters?
Current 14 role clusters. Missing any? (Solutions Architect, TPM, DevRel, Pre-sales Engineer, Quant Researcher?)
**Answer**: [TO-FILL]

### Q9 | Geographies to add?
Current: Switzerland, UK, Germany, Netherlands, India.
**Answer**: [TO-FILL — France? Singapore? UAE? US with sponsorship? Remote-global?]

---

## Execution questions

### Q10 | Which lesson plan to start first?
Options: LP-001 (RAG — highest JD frequency), LP-003 (cocotb — opens OS contribution), LP-007 (legal NLP — rarest differentiator), LP-013 (video analytics — unusual cross)
Recommendation: LP-001 if AI engineer is primary target; LP-003 if hardware roles are primary
**Answer**: [TO-FILL]

### Q11 | Content channel priority?
Decision already made: AD-12 (LinkedIn first, Medium second, YouTube third).
**Sub-question**: What's your comfort level with video? If low, skip YouTube for now.
**Answer**: [TO-FILL]

### Q12 | Open source project priority?
Tier 1 options: cocotb (hardware+Python), LangChain (AI, large audience), OpenLane (EDA, small pool).
Pick one to go deep in for 3+ months.
**Answer**: [TO-FILL]
