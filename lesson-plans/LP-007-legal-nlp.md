# LP-007 | Legal NLP: Contract Analysis Techniques

**Domain**: Legal Tech × AI  
**Priority**: P1 — your rarest differentiator; few engineers have both LLM depth + legal domain knowledge  
**Effort**: 3–5 days  
**STATUS**: TODO

---

## Why this matters

The combination of LLM engineering + legal domain understanding is extremely rare.
Most legal tech engineers come from legal (and lack engineering depth) or from software
(and lack domain understanding). Your position bridges both.

This lesson plan builds the domain vocabulary and technical patterns for legal AI,
turning a domain gap into a differentiator.

Gap closed: `legal_ai`, `compliance_automation`, `nlp` in `profile/my-profile.yaml`

---

## Learning objectives

- [ ] Understand the structure of legal documents (contracts, clauses, schedules)
- [ ] Know the standard clause types: indemnification, limitation of liability, termination, IP ownership, confidentiality
- [ ] Apply NLP techniques: clause extraction, named entity recognition (parties, dates, obligations)
- [ ] Build a contract analysis pipeline using LLMs + structured extraction
- [ ] Handle the reliability requirements of legal AI (citation, uncertainty, audit trail)
- [ ] Understand the regulatory context: GDPR, UK AI Act, EU AI Act (for compliance)

---

## Resources

### Day 1 — Legal domain vocabulary
- [ ] Read: "Understanding Contract Structure" — any legal primer or LegalZoom articles
- [ ] Read: Wikipedia articles on: indemnification, force majeure, IP assignment, NDA, SLA
- [ ] Exercise: Read 3 real public contracts (government contracts are public domain):
  - Find via: contracts.open.fda.gov or search "contract template PDF"
  - Label each clause by type manually — builds intuition

### Day 2 — Legal NLP foundations
- [ ] Read: "Legal NLP" chapter in any accessible NLP resource
- [ ] Explore: spaCy's legal models (en_legal_ner_trf) — demo and try it
- [ ] Read: "CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review" — cuad-data.com
  - This is the key dataset for contract understanding. Download and explore it.

### Day 3 — LLM-based contract analysis
- [ ] Build: A contract clause extractor using Claude API
  - Input: paste a contract text
  - Output: JSON with clause type + clause text + confidence
  - Prompt design: few-shot examples are critical here
- [ ] Test: Run it on 5 different contracts. Where does it fail?

### Day 4 — Compliance automation
- [ ] Read: GDPR Article 28 (processor agreements) — understand what a DPA must contain
- [ ] Build: A GDPR compliance checker
  - Input: a Data Processing Agreement (DPA) PDF
  - Output: checklist of required clauses vs. found clauses + risk flags
- [ ] Note: this is the pattern used by ComplyAdvantage, Clausematch, etc.

### Day 5 — Evidence artifact
- [ ] Polish `legal-contract-agent` or `compliance-checker` repo
- [ ] Document the design decisions: why LLM over rule-based, how you handle uncertainty
- [ ] Stub Medium article: "Building an LLM-powered GDPR compliance checker"

---

## Evidence artifact

**Repo**: `compliance-checker` — GDPR/contract compliance tool
**What it proves**: Domain understanding + engineering depth + LLM application in regulated context

---

## Done criteria

- [ ] Can explain 10 standard contract clause types without looking them up
- [ ] Working compliance checker on real documents (not toy examples)
- [ ] GitHub repo live with example output
- [ ] Can answer in interview: "How do you handle hallucination risk in legal AI?"
- [ ] `profile/my-profile.yaml`: `legal_ai: PROFICIENT, compliance_automation: PROFICIENT`

---

## Cross-domain connections

- Contract clause extraction ↔ RTL signal extraction from specifications
- Compliance checking ↔ DRC (Design Rule Check) in physical design
- Audit trail requirement ↔ DFT / silicon traceability

Document these in `second-brain/connections.md`.

---

## STATUS: TODO
