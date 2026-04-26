# Sessions Log

> **How to use**: Start each new Claude session by saying:
> "Read sessions.md and context.md, then continue from Session N."
> This loads ~2 files instead of replaying the full conversation.

---

## Session 1 — 2026-04-26

**Goal**: Bootstrap the job search repo and push to GitHub.

**Done**:
- Created repo structure: profile/, gap-analysis/, evidence/, linkedin/, job-tracker/, learning/
- Wrote context.md (stable background), sessions.md (this file), prompts.md
- Wrote profile stubs: skills.md, linkedin.md, domains.md
- Wrote gap-analysis/template.md, evidence/projects.md, learning/roadmap.md, job-tracker/applications.md
- Pushed to GitHub: https://github.com/rajaghv-dev/apply

**Open / Next Session**:
- [ ] Fill in LinkedIn profile copy in `profile/linkedin.md` — need: current headline, summary, top 3 roles targeted
- [ ] Add first real JD to `gap-analysis/jobs/` and run gap analysis
- [ ] Map at least 3 concrete evidence artifacts per skill cluster in `evidence/projects.md`
- [ ] Connect LinkedIn account details (URL, current headline)

**Key decisions**:
- Repo named `apply` on GitHub under rajaghv-dev
- Token-reduction strategy: context.md + sessions.md are the only two files needed to cold-start any session

---

## Session 2 — 2026-04-26

**Goal**: Add job sources — company career pages, aggregators, search strategy by region.

**Done**:
- Created `job-sources/company-careers.md` — Big Tech, EDA/Semicon, Research Labs, AI, Legal Tech, FinTech companies with direct career URLs; covers Switzerland, UK, Germany, EU, India
- Created `job-sources/aggregators.md` — global, Europe, Switzerland, UK, Germany/DACH, Netherlands, India, plus specialist boards (semiconductor, AI, legal tech, fintech)
- Created `job-sources/search-strategy.md` — weekly search routine (Tier 1/2/3), LinkedIn saved search templates per domain, keyword cheat sheet, location filter reference, cold outreach DM template
- Pushed to GitHub

**Open / Next Session**:
- [ ] Build job scraper / API tool to pull live listings into job-tracker (see P003 — user asked about scraping vs API costs)
- [ ] Fill in LinkedIn profile copy in `profile/linkedin.md`
- [ ] Add first real JD to `gap-analysis/jobs/` and run gap analysis
- [ ] Map evidence artifacts in `evidence/projects.md`

**Key decisions**:
- job-sources/ is a new top-level directory
- Aggregators split by region for fast lookup
- Semiconductor specialist boards included (IEEE, SemiEngineering, ChipDesignJobs, EETimes)

---

## Session 3 — 2026-04-26

**Goal**: Gap analysis of the system itself; identify what's missing to enable high-value job matching.

**Done**:
- Created `gaps-and-improvements.md` — full audit of 10 gaps (GAP-01 through GAP-10) + 5 system improvements, priority order table, and top 5 highest-leverage questions
- Created `profile/questionnaire.md` — structured question set (7 sections: identity, experience by domain, target roles, LinkedIn baseline, evidence inventory, network map, differentiators)
- Created `profile/market-scan.md` — template to run JD keyword frequency analysis + salary benchmarks
- Created `network/contacts.md` — contact map + referral outreach template
- Created `interview/prep.md` — STAR story bank, technical deep-dives by domain, company research template
- Created `resume/README.md` — resume cluster strategy + ATS checklist

**Open / Next Session**:
- [ ] HIGHEST PRIORITY: User to answer `profile/questionnaire.md` (even just Section A+C unlocks everything)
- [ ] Run market scan: pull 20 real JDs → fill `profile/market-scan.md`
- [ ] Pull LinkedIn baseline: SSI score, profile views, InMails → fill `profile/linkedin.md`
- [ ] Build the job scraper (`tools/job-scraper.py`)

**Key decisions**:
- Skill scoring upgraded to include recency + scale (not just level)
- Gap match score formula: (STRONG×3 + PARTIAL×1) / (total reqs × 3) × 100; target ≥60% before applying
- Resume strategy: clusters by domain, not one-size CV

---

## Session 4 — 2026-04-26

**Goal**: Design and build ontology layer for skill bridging + JD matching.

**Done**:
- Created `ontology/README.md` — full strategy: why ontology, 6 use cases, architecture, 3-phase build plan, existing ontologies to leverage (ESCO, O*NET)
- Created `ontology/skills-graph.yaml` — 45+ skill nodes with synonyms, implies edges (weighted), domain membership, level descriptors; covers hardware, embedded, systems, backend, frontend, AI/ML, legal tech, fintech, leadership
- Created `ontology/roles-graph.yaml` — 14 role clusters with required/preferred skills, title synonyms, target companies, geographies, bridge bonuses for rare cross-domain combos
- Created `ontology/domains.yaml` — domain taxonomy with cross-domain bridge weights + Raja's 4 unique bridge combos identified (hardware×AI, hardware×AI×systems, AI×legal, AI×fintech)
- Created `tools/matcher.py` — JD text → extracts skill keywords via synonym matching → scores against profile using direct + implied scores → outputs match%, STRONG/PARTIAL/GAP table, gap actions, role cluster suggestion, "why me" bullet drafts → saves to gap-analysis/jobs/
- Created `profile/my-profile.yaml` — machine-readable profile stub for matcher.py

**Open / Next Session**:
- [ ] BLOCKER: Fill `profile/my-profile.yaml` with actual skill levels (matcher is useless until then)
- [ ] Test matcher on a real JD: `python tools/matcher.py --jd path/to/jd.txt`
- [ ] Add `pyyaml` install note or requirements.txt

**Key decisions**:
- Ontology format: YAML (human-readable, Claude-readable, editable without tooling)
- implies edges are weighted (0.0–1.0); match score uses max(direct, implied) per skill
- Apply threshold: ≥60%; Stretch: 40–59%; Skip: <40%
- Raja's rarest bridge: hardware + AI + systems = "from transistor to transformer" — captured in domains.yaml unique_bridges

---

## Session 5 — 2026-04-26

**Goal**: Write full system architecture document + priority to-do list. Move all memory/context into repo (nothing on local machine only).

**Done**:
- Created `ARCHITECTURE.md` — 11-section architecture doc covering: system overview, full ASCII component diagram, data model (SkillNode/ProfileSkill/RoleNode/DomainNode/JD/Application), 5 processing flows, ontology graph properties (DAG, decay, domain bridges), 6 open design questions with options + recommendations, component status table, file dependency map, 4-phase build plan, tech choices rationale, 8 review questions for Raja
- Created `TODO.md` — prioritized to-do list (P0/P1/P2/P3 tiers)
- Moved Claude memory files into `_memory/` inside the repo (nothing left on local machine only)
- Updated `README.md` to include ARCHITECTURE.md and TODO.md references

**Open / Next Session**:
- [ ] Raja to review ARCHITECTURE.md — answer the 8 Review Questions
- [ ] Raja to answer `profile/questionnaire.md` — at minimum Section A + C (unlocks everything)
- [ ] Decide on Q2 (JD parsing: regex vs LLM) and Q4 (NetworkX graph traversal) before Phase 2 build

**Key decisions**:
- All state lives in Git — no local-machine-only files
- ARCHITECTURE.md is the canonical system reference; update it when design changes

---

## Session Template (copy for each new session)

## Session N — YYYY-MM-DD

**Goal**:

**Done**:

**Open / Next Session**:
- [ ]

**Key decisions**:
