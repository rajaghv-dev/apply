# Skills Ontology — Strategy & Design

## Why ontology matters here (especially for you)

A standard gap analysis is **flat**: JD says "FPGA" → your profile says nothing → marked GAP.

An ontology-powered gap analysis is **relational**: JD says "FPGA" → ontology knows RTL Design
implies 60% of FPGA competence → marked PARTIAL, not GAP, with a specific bridge action.

For a generalist with chip-to-app depth, this difference is enormous:
- Your skills span 6+ domains — a flat profile undersells the cross-domain transfer
- JDs use inconsistent terminology — ontology normalizes (RTL = HVL = hardware description)
- Your differentiator IS the rare cross-domain combination — ontology makes it arguable and quantifiable

---

## What an ontology does in this system

### 1. Skill bridging (partial credit on gaps)
```
You have:  RTL Design (EXPERT)
JD wants:  FPGA experience
Flat:      GAP
Ontology:  RTL → implies(0.6) FPGA → PARTIAL (save 3 weeks of learning)
```

### 2. Synonym normalization (don't miss matches)
```
JD says:   "HVL", "hardware description language", "digital design"
Your CV:   "Verilog", "RTL"
Flat:      no match found
Ontology:  all map to the same concept → MATCH
```

### 3. Implicit skill inference (enrich your profile automatically)
```
You state: "SoC Architecture"
Ontology infers you also likely know:
  - RTL (0.85), Timing Analysis (0.80), Power Domains (0.75), CDC (0.70)
Profile becomes richer without you listing every sub-skill manually.
```

### 4. Cross-domain bridge detection (your unfair advantage)
```
You have: RTL Design + LLM Integration
Ontology: these two together → maps to "AI Hardware / AI Chip Design" role cluster
          — a rare bridge fewer than 0.1% of candidates have
This surfaces role clusters you might not have thought to target.
```

### 5. Learning path optimization (shortest route to a role)
```
Target: Staff AI Platform Engineer
Missing: MLOps (GAP), Kubernetes (GAP), Distributed Training (GAP)
Ontology: Kubernetes → prerequisite of Distributed Training → learn K8s first
          Cloud systems knowledge (you have) → implies(0.5) Kubernetes → reduced effort
Result: ordered learning plan, not a flat todo list
```

### 6. Role cluster discovery (find titles you don't know to search for)
```
Your skill intersection: chip design ∩ ML ∩ systems software
Ontology role matches: "AI Accelerator Engineer", "ML Hardware Architect",
                       "Silicon ML Engineer", "Hardware-Aware ML Researcher"
→ titles you'd never search for but are perfect fits
```

---

## Architecture

```
ontology/
├── README.md               ← this file
├── skills-graph.yaml       ← skill nodes, synonyms, implies edges, domain membership
├── roles-graph.yaml        ← role nodes, required/preferred skill clusters
├── domains.yaml            ← domain taxonomy, cross-domain bridge weights
└── tools/
    └── matcher.py          ← JD text → extract skills → score against profile
```

### Data model

**Skill node:**
```yaml
rtl_design:
  label: RTL Design
  synonyms: [Verilog, VHDL, SystemVerilog, RTL, HVL, hardware description]
  domain: hardware
  level_descriptors:
    EXPERT: "Designed production silicon at full SoC scale"
    PROFICIENT: "Designed and verified blocks in a real tapeout"
    FAMILIAR: "Wrote RTL for learning or small FPGAs"
  implies:           # skills you get partial credit for if you have this one
    - digital_logic: 0.90
    - timing_analysis: 0.75
    - fpga_design: 0.55
    - hardware_verification: 0.60
  required_by:       # role clusters that list this as required
    - silicon_engineer
    - asic_designer
    - soc_architect
```

**Role node:**
```yaml
staff_silicon_engineer:
  label: Staff Silicon Engineer
  skill_requirements:
    required:
      rtl_design: EXPERT
      soc_architecture: PROFICIENT
      timing_closure: PROFICIENT
    preferred:
      dft: PROFICIENT
      ml_hardware: FAMILIAR
  domain_clusters: [hardware, embedded]
  title_synonyms: [Principal RTL Engineer, Senior ASIC Architect, Staff Hardware Engineer]
```

**Domain bridge:**
```yaml
hardware:
  bridges_to:
    embedded: 0.70      # hardware people often know embedded
    ai_hardware: 0.55   # chip designers crossing to AI silicon
    systems: 0.45
```

---

## Match scoring formula

```
For each JD requirement R:
  direct_score   = profile_level_score(R)           # 3=EXPERT, 2=PROFICIENT, 1=FAMILIAR, 0=none
  implied_score  = max(implies_weight(S→R) × profile_level_score(S) for all S you have)
  final_score(R) = max(direct_score, implied_score)

Match% = sum(final_score(R)) / sum(max_possible(R)) × 100

Apply if Match% ≥ 60%
Stretch if Match% 40–59% (apply + gap-close in parallel)
Skip if Match% < 40%
```

---

## Existing ontologies to leverage (don't build from scratch)

| Source | Coverage | Format | URL |
|--------|----------|--------|-----|
| ESCO (EU) | 13,890 occupations, skills | RDF, JSON-LD | esco.ec.europa.eu/en/download |
| O*NET (US) | Detailed occupational data | CSV, API | onetonline.org/developer |
| IEEE Taxonomy | Engineering/CS concepts | XML | standards.ieee.org |
| Wikidata | General tech concepts | SPARQL | wikidata.org |

**Strategy**: Use ESCO as the backbone (EU-relevant for your target markets), layer a
custom extension on top for the hardware/EDA/AI-hardware domain (under-represented in ESCO).

---

## Build plan (3 phases)

### Phase 1 — Static YAML (this session)
Hand-crafted skills graph for your 6 core domains.
Enough to power manual gap analysis with better accuracy.
No code needed — Claude reads it when doing analysis.

### Phase 2 — Matcher script (next session)
`tools/matcher.py`: paste JD text → extracts skill keywords →
scores against skills-graph.yaml → outputs match% + gap list.

### Phase 3 — Auto-enrichment (future)
Connect matcher to Adzuna/Indeed API → weekly auto-score all new JDs →
surface only those with Match% ≥ 60% in `job-tracker/new-this-week.md`.
