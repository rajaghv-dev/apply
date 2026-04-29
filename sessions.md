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

## Session 6 — 2026-04-26

**Goal**: Build full evidence engine, content system, second brain, lesson planners, GitHub project pipeline, open-source strategy. Add all vertical domains. Fix naming (remove personal names from headings).

**Done**:
- `second-brain/`: README (system + flywheel), knowledge-map.md (15 cross-domain bridges with content angles), learning-log.md (protocol + resource library per domain), insights.md (5 durable principles), connections.md (registry of bridges used/unused)
- `content/`: README (flywheel + content types + cadence targets), pipeline.md (stage workflow + weekly cadence + quality checklists), ideas.md (50+ ideas across 4 pillars: Bridge/Tutorial/Landscape/Career), medium.md (12 articles tracked + template), linkedin-posts.md (post queue + 4 templates + hashtag clusters), youtube.md (10 videos tracked + production checklist)
- `open-source/`: README (contributor → maintainer path), targets.md (Tier 1/2/3 projects with entry points: cocotb, LangChain, OpenLane, Transformers, OpenROAD, LlamaIndex, MLflow, RISC-V, QuantLib), log.md, maintainer-roadmap.md (per-project 18-month path)
- `lesson-plans/`: README (15-plan index with effort + priority + status), LP-001 RAG, LP-002 Agents, LP-003 cocotb, LP-007 Legal NLP, LP-013 Video Analytics — each with objectives, daily resources, exercises, done criteria, cross-domain connections
- `github-projects/`: README (pipeline), ideas.md (8 project specs: legal-contract-agent, compliance-checker, finance-risk-agent, riscv-nn-accel, eda-mcp-server, cocotb-examples, cctv-analytics-demo, llm-rtl-gen)
- `evidence/platform-tracker.md`: all-platform evidence registry
- `profile/domains.md`: expanded to 10 vertical domains (added: AI Hardware, Video Analytics, Industrial AI, Embedded AI/TinyML, Autonomous Systems, Telecom, Healthcare AI)
- Naming: removed "Raja GHV's Job Search Command Center" from all headings → "apply" / "Career Intelligence System"
- `context.md`: updated with new domains

**Open / Next Session**:
- [ ] Fill remaining lesson plans: LP-004 (OpenLane), LP-005 (MLOps), LP-006 (K8s), LP-008 (Finance), LP-009 (RISC-V), LP-010 (Distributed systems), LP-011 (MLIR), LP-012 (Systolic arrays), LP-014 (Prompt engineering), LP-015 (Cloud)
- [ ] Still blocked: profile/my-profile.yaml empty → matcher produces no signal
- [ ] First action: pick 1 lesson plan → start it → build the artifact

**Key decisions**:
- Lesson plans are the primary driver of evidence production (not ad hoc project ideas)
- Each lesson plan has explicit done criteria tied to profile/my-profile.yaml updates
- Second brain → learning log → content → evidence → profile update is the complete flywheel

---

## Session 7 — 2026-04-26

**Goal**: Comprehensive update of all session/memory/MD files for detailed review.

**Done**:
- `context.md` — full rewrite: identity, 10-domain table, system purpose, flywheel diagram, complete file map (abbreviated), current blockers, what's built
- `TODO.md` — full rewrite: P0 (2 items), P1 (7 items), P2 (20 items), P3 (9 items), Someday (5), Done log (40+ items ticked off across all 7 sessions)
- `README.md` — full rewrite: system summary table, current state section, full annotated file tree, matcher usage, token-reduction load guide
- `_memory/project-apply-repo.md` — full file map updated to Session 7 state (all new dirs/files)
- `_memory/arch-decisions.md` — extended to AD-12 (added AD-09: lesson plans as driver, AD-10: second brain flywheel, AD-11: 10 domains, AD-12: content channel priority)
- `_memory/open-questions.md` — extended to Q12 (added Q9: lesson plan priority, Q10: content channel comfort, Q11: OS project focus, Q12: domain depth ranking)
- `_memory/user-profile.md` — updated with 10 domains, collaboration style, what's blocked
- `_memory/session-protocol.md` — updated load guide with all new file types, end-of-session checklist, token budget guidance
- `_memory/MEMORY-INDEX.md` — updated index
- Local Claude memory (`~/.claude/...`) — synced to match in-repo copies

**Open / Next Session**:
- [ ] **P0-1**: Fill `profile/my-profile.yaml` — skill levels (20–30 min) — NOTHING WORKS WITHOUT THIS
- [ ] **P0-2**: Answer `profile/questionnaire.md` Sections A+C — target roles + geography (15 min)
- [ ] **P1-1**: Pick one lesson plan and start it — recommend LP-001 (RAG) or LP-003 (cocotb)
- [ ] **P1-7**: Answer `_memory/open-questions.md` Q1–Q12 — shapes Phase 2 build

**Key decisions**:
- context.md is now the canonical stable reference (no ephemeral state in it)
- TODO.md is the single source of truth for what to do next
- _memory/ files are fully updated — next session cold-starts cleanly from context.md + sessions.md

---

## Session 8 — 2026-04-29

**Goal**: Complete all code gaps — build missing tools, upgrade matcher, add CI.

**Done**:
- `tools/matcher.py` — two major upgrades:
  - **Skill decay**: tiered recency penalty on `last_used` (−0% ≤2yr, −20% ≤5yr, −40% ≤10yr, −60% >10yr); applied to direct_score and implied_score; decay note shown in report and saved markdown
  - **JD section detection**: walks JD line-by-line, detects required/preferred headers via regex; weights required skills 2×, preferred 1× in match%; report labels each gap as [REQUIRED] or [preferred]
- `tools/job-scraper.py` — new; four sources: Adzuna API (EU/UK/IN/CH), Reed API (UK), Remotive (remote), Playwright (10 company career pages); deduplication via MD5 hash of title+company stored in `job-tracker/seen.txt`; outputs to `job-tracker/new-this-week.md`; supports `--dry-run`, `--no-browser`, `--source` flags
- `requirements.txt` — pyyaml, requests, playwright
- `.github/workflows/weekly-scraper.yml` — GH Actions cron (Monday 08:00 UTC) + manual trigger; commits new-this-week.md + seen.txt automatically

**Open / Next Session**:
- [ ] **P0-1**: Fill `profile/my-profile.yaml` — skill levels + `last_used` (20–30 min)
- [ ] **P0-2**: Answer `profile/questionnaire.md` Sections A+C (15 min)
- [ ] **P1-1**: Pick one lesson plan and start it (LP-001 RAG or LP-003 cocotb)
- [ ] **P1-7**: Answer open-questions Q1–Q12 (20 min) — unblocks Phase 2
- [ ] Set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `REED_API_KEY` as GitHub repo secrets to activate weekly scraper

**Key decisions**:
- All code gaps from gaps-and-improvements.md + TODO.md P2-P3 build items are now complete
- Only remaining code gaps: NetworkX multi-hop (P3-1, gated on Q4 answer) and Claude API in scraper (P3-3, gated on Q5 answer) — both require profile data first

---

## Session Template (copy for each new session)

## Session N — YYYY-MM-DD

**Goal**:

**Done**:

**Open / Next Session**:
- [ ]

**Key decisions**:
