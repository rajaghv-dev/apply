# Priority To-Do List

Last updated: 2026-04-26 (Session 7)
Format: P0 = nothing works without this | P1 = do this week | P2 = this month | P3 = next sprint

---

## P0 — BLOCKERS

Nothing below produces real value until both of these are done.

- [ ] **P0-1 | Fill `profile/my-profile.yaml`**
  Add EXPERT / PROFICIENT / FAMILIAR + `last_used` year for every skill you have.
  Start with the 10 you're most confident about — that's enough to unlock the matcher.
  File: `profile/my-profile.yaml` (all skill slots pre-written, just fill the values)
  _Effort: 20–30 min_
  _Unlocks: matcher.py, gap analysis, role matching, evidence prioritization_

- [ ] **P0-2 | Fill `profile/questionnaire.md` Sections A + C**
  Section A: location, work authorization, years of XP, current status, start date
  Section C: top 3 target role titles, IC vs. mgmt, geography priority, comp range
  _Effort: 15 min_
  _Unlocks: LinkedIn headline, role framing, application strategy_

---

## P1 — HIGH VALUE (this week)

- [ ] **P1-1 | Pick one lesson plan and start it**
  Recommended first: **LP-001** (RAG pipeline, 5 days) — highest JD frequency, feeds GP-01
  Or: **LP-003** (cocotb, 5 days) — opens OS contribution to cocotb immediately
  File: `lesson-plans/LP-001-rag-pipeline.md` or `lesson-plans/LP-003-cocotb.md`
  Process: follow the daily schedule, check off objectives, build the artifact
  _Effort: 5 days part-time_
  _Unlocks: first evidence artifact, first content piece, first OS contribution target_

- [ ] **P1-2 | Run matcher on 3 real JDs** _(after P0-1)_
  Get 3 JDs from LinkedIn/Naukri/jobs.ch for your top target role.
  Save as `.txt` in `gap-analysis/jobs/`
  Run: `pip install pyyaml && python tools/matcher.py --jd gap-analysis/jobs/jd1.txt`
  _Effort: 30 min_
  _Unlocks: real gap list, first "why me" bullets, application decisions_

- [ ] **P1-3 | Pull LinkedIn baseline (5 min)**
  SSI: linkedin.com/sales/ssi
  Profile views + InMails + Search appearances: LinkedIn Analytics
  Paste into: `profile/linkedin.md` Current State section
  _Effort: 5 min_
  _Unlocks: LinkedIn optimization baseline — can't improve what you don't measure_

- [ ] **P1-4 | Inventory existing public evidence**
  GitHub repos, LinkedIn posts, publications, patents, talks, blog posts — anything public
  Fill: `evidence/platform-tracker.md` and `evidence/projects.md`
  _Effort: 20 min_
  _Unlocks: know what already exists before building more_

- [ ] **P1-5 | Write first LinkedIn post**
  Pick from `content/ideas.md` quick posts (Q01–Q12) — any of them, 30 min
  Use the Bridge post template in `content/linkedin-posts.md`
  Suggested first: Q12 "Why I track my learning in a GitHub repo" (links to this repo)
  _Effort: 30 min_
  _Unlocks: LinkedIn algorithm warmup, profile activity signal_

- [ ] **P1-6 | Fill `profile/skills.md` (human-readable view)** _(after P0-1)_
  Copy levels from my-profile.yaml → skills.md table, add evidence notes
  _Effort: 10 min_

- [ ] **P1-7 | Answer Architecture Review Questions**
  Read `ARCHITECTURE.md` Section 6 (6 open design questions)
  Read `_memory/open-questions.md` (Q1–Q11)
  Even 1-sentence answers per question unblock Phase 2 build decisions
  _Effort: 20 min_

---

## P2 — IMPORTANT (this month)

### Profile & Matching
- [ ] **P2-1 | Answer `profile/questionnaire.md` sections D–G**
  D: LinkedIn state (URL, headline, SSI) | E: evidence inventory
  F: network at target companies | G: differentiators
  _Effort: 30 min_

- [ ] **P2-2 | Run LinkedIn optimization session**
  After P0-2 + P1-3: start Claude session with LinkedIn prompt template from `prompts.md`
  Output: 3 headline variants, optimized About, 5 pinned skills
  Apply on LinkedIn, re-measure SSI after 2 weeks
  _Effort: 30 min_

- [ ] **P2-3 | Set up LinkedIn saved searches**
  Use 5 templates in `job-sources/search-strategy.md` Tier 1 section
  Set each as a LinkedIn Job Alert (weekly email)
  _Effort: 15 min_

- [ ] **P2-4 | Fill `network/contacts.md`**
  For each target company: warm / cold / none
  Warm contacts: send referral request using template in same file
  _Effort: 20 min_

### Lesson Plans — complete the index
- [ ] **P2-5 | Write LP-004** (OpenLane: open source chip design flow) — 5–7 days
- [ ] **P2-6 | Write LP-005** (MLOps: experiment tracking + model serving) — 5–7 days
- [ ] **P2-7 | Write LP-006** (Kubernetes for ML engineers) — 3–5 days
- [ ] **P2-8 | Write LP-008** (Financial risk modeling) — 3–5 days
- [ ] **P2-9 | Write LP-009** (RISC-V architecture + ISA) — 5–7 days
- [ ] **P2-10 | Write LP-010** (Distributed systems: consensus + replication) — 7–10 days
- [ ] **P2-11 | Write LP-011** (MLIR: ML compiler infrastructure) — 7–10 days
- [ ] **P2-12 | Write LP-012** (Systolic arrays + neural network accelerators) — 7–10 days
- [ ] **P2-13 | Write LP-014** (Prompt engineering + evaluation) — 2–3 days
- [ ] **P2-14 | Write LP-015** (Cloud: AWS/GCP for engineers) — 5–7 days
  _Say "write lesson plan LP-00N" to Claude to generate each_

### Matcher improvements
- [ ] **P2-15 | Add skill decay** (`ARCHITECTURE.md` Q1)
  Decay function: 1.0 if ≤2yr, 0.8 if ≤5yr, 0.6 if ≤10yr, 0.4 if >10yr
  Apply to direct_score only. Report decay note in gap output.
  _Say: "implement skill decay in matcher.py"_

- [ ] **P2-16 | Add required/preferred JD section detection** (`ARCHITECTURE.md` Q2)
  Heuristic: detect "Required:", "Must have:", "Nice to have:" headers
  Weight required 2×, preferred 1× in match%
  _Say: "implement JD section detection in matcher.py"_

### Content + Open Source
- [ ] **P2-17 | Make first open source contribution**
  Target: cocotb or LangChain (Tier 1 in `open-source/targets.md`)
  Start with docs or a good-first-issue
  Log in `open-source/log.md`

- [ ] **P2-18 | Publish first Medium article**
  Suggested: B01 "RTL timing ↔ distributed latency" or C06 "How I use AI for job search"
  Follow pipeline in `content/pipeline.md`

- [ ] **P2-19 | First real application**
  After P1-2: highest match% role from JD analysis
  Complete `gap-analysis/jobs/[company]-[role].md` fully
  Log in `job-tracker/applications.md`
  _Effort: 1 hr_

### Build tools
- [ ] **P2-20 | Build `tools/job-scraper.py`**
  Design in `job-sources/scraping.md`
  Phase 1: Adzuna + Reed APIs (free)
  Phase 2: Playwright for 5 company pages
  _Say: "build the job scraper"_

---

## P3 — ALL COMPLETE ✓

All planned code is done. Remaining work is data entry (profile) and content production.

---

## Someday / If-needed

- [ ] Salary intelligence: Glassdoor / Levels.fyi auto-pull
- [ ] Offer comparison model: total comp calculator (base + equity + bonus)
- [ ] LinkedIn SSI correlation dashboard (matplotlib)
- [ ] Neo4j migration (only if skills graph > 500 nodes)
- [ ] Conference talk: propose a talk on the hardware×AI bridge at a relevant venue

---

## Done ✓

### Infrastructure
- [x] Repo created, git initialized, pushed to GitHub (`github.com/rajaghv-dev/apply`)
- [x] `_memory/` directory — all Claude memory in repo, nothing local-only
- [x] Cold-start protocol: context.md + sessions.md (2-file full context)
- [x] Naming: removed personal names from all headings

### Core system
- [x] Ontology: `skills-graph.yaml` (45+ skill nodes, synonyms, weighted implies edges)
- [x] Ontology: `roles-graph.yaml` (14 role clusters, title synonyms, bridge bonuses)
- [x] Ontology: `domains.yaml` (10 domains, cross-domain bridge weights, 4 unique bridges)
- [x] Matcher: `tools/matcher.py` — decay + section detection + domain focus bonus (×1.15)
- [x] Pathfinder: `tools/pathfinder.py` — NetworkX Dijkstra multi-hop learning path
- [x] Narrator: `tools/narrator.py` — Claude API (Haiku, prompt-cached) gap narrative
- [x] Scraper: `tools/job-scraper.py` — Adzuna/Reed/Remotive/Playwright → new-this-week.md
- [x] Log: `tools/log-linkedin.py` — append weekly SSI/views/inmails/searches snapshot
- [x] Dashboard: `tools/ssi-dashboard.py` — matplotlib 2×2 LinkedIn trend chart
- [x] Resume: `tools/resume-gen.py` — cluster-specific resume stubs per role
- [x] Market scan: `tools/market-scan.py` — batch JD skill frequency table
- [x] ESCO map: `tools/esco-map.py` — map skills to EU standard ESCO URIs
- [x] Salary: `tools/salary-pull.py` — curated 2025 benchmarks + optional LinkedIn scrape
- [x] Offers: `tools/offer-compare.py` — total comp + CoL-adjusted comparison table
- [x] Tests: `tests/` — 81 tests, 100% passing (pytest)
- [x] `requirements.txt` — pyyaml, requests, playwright, networkx, anthropic, matplotlib, pytest
- [x] `.github/workflows/weekly-scraper.yml` — Monday 08:00 UTC cron + manual trigger

### Job sources
- [x] `job-sources/company-careers.md` — 50+ direct career URLs (CH, UK, EU, India)
- [x] `job-sources/aggregators.md` — 30+ boards by region + specialist boards (semicon, AI, legal, fintech)
- [x] `job-sources/search-strategy.md` — weekly routine, LinkedIn saved search templates, cold DM
- [x] `job-sources/scraping.md` — scraping vs API analysis, cost table, recommended free setup

### Profile stubs (built, need filling)
- [x] `profile/my-profile.yaml` — machine-readable (all slots pre-built, values empty)
- [x] `profile/skills.md` — human-readable skills table (empty)
- [x] `profile/linkedin.md` — LinkedIn copy (empty)
- [x] `profile/domains.md` — 10 vertical domains with target roles, companies, evidence slots
- [x] `profile/questionnaire.md` — 7-section question set (A–G)
- [x] `profile/market-scan.md` — JD keyword frequency + salary benchmark template

### Second brain
- [x] `second-brain/README.md` — system design + flywheel diagram
- [x] `second-brain/knowledge-map.md` — 15 documented cross-domain bridges with content angles
- [x] `second-brain/learning-log.md` — protocol + resource library per domain
- [x] `second-brain/insights.md` — 5 durable cross-domain principles
- [x] `second-brain/connections.md` — bridge registry (published / unpublished)

### Content engine
- [x] `content/README.md` — flywheel, content types ROI table, 4 pillars, cadence targets
- [x] `content/pipeline.md` — IDEA→PUBLISHED workflow, weekly schedule, quality checklists
- [x] `content/ideas.md` — 50+ ideas: Bridge (13), Tutorial (13), Landscape (9), Career (8), LinkedIn quick (12)
- [x] `content/medium.md` — 12 articles tracked, article template, Medium setup checklist
- [x] `content/linkedin-posts.md` — post queue, 4 post templates, hashtag clusters
- [x] `content/youtube.md` — 10 videos tracked, production template, start-here guide

### Lesson plans
- [x] `lesson-plans/README.md` — 15-plan index with effort, priority, status
- [x] LP-001: RAG pipeline (5 days, daily schedule, done criteria)
- [x] LP-002: LLM agents + tool use (5 days)
- [x] LP-003: cocotb Python hardware verification (5 days)
- [x] LP-007: Legal NLP + contract analysis (5 days)
- [x] LP-013: Video analytics + edge CV (7 days)
- [ ] LP-004, 005, 006, 008, 009, 010, 011, 012, 014, 015 — stubs in index, full files not yet written

### Open source
- [x] `open-source/README.md` — contributor → maintainer path
- [x] `open-source/targets.md` — Tier 1 (cocotb, LangChain, OpenLane), Tier 2, Tier 3, own projects
- [x] `open-source/log.md` — contribution tracker (empty, ready to fill)
- [x] `open-source/maintainer-roadmap.md` — 18-month path per project

### GitHub projects
- [x] `github-projects/README.md` — pipeline + project index
- [x] `github-projects/ideas.md` — 8 project specs (GP-01 through GP-08) with tech stack + done criteria

### Evidence
- [x] `evidence/platform-tracker.md` — all-platform registry (ready to fill)
- [x] `evidence/projects.md` — skill → proof map (one entry: this repo)

### Supporting modules
- [x] `network/contacts.md` — contact map + referral template
- [x] `interview/prep.md` — STAR bank, technical deep-dives, company research template
- [x] `resume/README.md` — 5-cluster strategy + ATS checklist
- [x] `learning/roadmap.md` — gap → learning plan template
- [x] `gap-analysis/template.md` — reusable JD analysis template
- [x] `job-tracker/applications.md` — pipeline tracker
