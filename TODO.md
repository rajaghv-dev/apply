# Priority To-Do List

Last updated: 2026-04-26  
Format: each item is a discrete action, owner is always Raja unless noted.

---

## P0 — BLOCKERS (system produces zero value without these)

Everything below this line is blocked until P0 is done.

- [ ] **P0-1 | Fill `profile/my-profile.yaml`**
  Fill in skill levels (EXPERT / PROFICIENT / FAMILIAR) and `last_used` year.
  You don't need evidence links yet — just levels.
  Even filling 10 skills unlocks the matcher.
  _Effort: 20–30 min_

- [ ] **P0-2 | Answer `profile/questionnaire.md` Sections A + C**
  Section A = who you are (location, work auth, years of XP, status).
  Section C = target role titles (top 3), IC vs. mgmt, geography priority.
  These two sections unlock: LinkedIn headline, gap analysis framing, role matching.
  _Effort: 15 min_

---

## P1 — HIGH VALUE (do this week)

- [ ] **P1-1 | Run matcher on 3 real JDs**
  Find 3 JDs from LinkedIn/Naukri/jobs.ch for your top target role cluster.
  Save each as a `.txt` file in `gap-analysis/jobs/`.
  Run: `pip install pyyaml && python tools/matcher.py --jd gap-analysis/jobs/jd1.txt`
  Review the match% and gap list.
  _Effort: 30 min_
  _Unlocks: first real gap actions, first real "why me" bullets_

- [ ] **P1-2 | Pull LinkedIn baseline (5 min)**
  - SSI score: linkedin.com/sales/ssi → paste number in `profile/linkedin.md`
  - Profile views (last 7 days): LinkedIn Analytics → paste
  - InMails received (last 30 days): LinkedIn notifications → count
  - Search appearances (last week): LinkedIn Analytics → paste
  - Current headline: copy-paste into `profile/linkedin.md`
  _Effort: 5 min_
  _Unlocks: LinkedIn optimization (currently flying blind)_

- [ ] **P1-3 | Inventory existing public evidence**
  Go through: GitHub, LinkedIn posts, publications, patents, conference talks, blog posts.
  Fill in `evidence/projects.md` with everything that already exists.
  _Effort: 20 min_
  _Unlocks: know what evidence is already there vs. what needs to be built_

- [ ] **P1-4 | Fill `profile/skills.md` (human-readable view)**
  After doing P0-1, copy levels into `profile/skills.md` table and add evidence notes.
  This is the version Claude reads to write LinkedIn copy and "why me" pitches.
  _Effort: 10 min (after P0-1)_

- [ ] **P1-5 | Answer Architecture Review Questions**
  Read `ARCHITECTURE.md` Section 6 (Open Design Questions) and Section 11 (Review Questions).
  Answer the 8 questions — even brief answers (1–2 sentences each) are enough.
  Your answers determine Phase 2 build priorities.
  _Effort: 20 min_

---

## P2 — IMPORTANT (do this month)

- [ ] **P2-1 | Set up LinkedIn saved searches**
  Use the 5 templates in `job-sources/search-strategy.md` (Tier 1 section).
  Set each as a LinkedIn Job Alert (email or push, weekly frequency).
  _Effort: 15 min_

- [ ] **P2-2 | Fill `network/contacts.md`**
  For each target company in the table, mark: warm / cold / none.
  For warm contacts: send referral request this week (template in file).
  _Effort: 20 min_

- [ ] **P2-3 | Run LinkedIn optimization session**
  After P0-2 + P1-2: paste answers in chat with prompt from `prompts.md` LinkedIn template.
  Output: 3 headline variants, optimized about section, 5 skills to pin.
  Apply on LinkedIn. Re-measure SSI after 2 weeks.
  _Effort: 30 min (Claude session)_

- [ ] **P2-4 | Answer `profile/questionnaire.md` remaining sections (D–G)**
  Section D = LinkedIn current state (URL, headline, SSI).
  Section E = evidence inventory (GitHub, publications).
  Section F = network at target companies.
  Section G = differentiators (the "rare combo" narrative).
  _Effort: 30 min_

- [ ] **P2-5 | Add skill decay to matcher.py**
  Implement Option B decay from `ARCHITECTURE.md` Q1:
  decay(y) = 1.0 if y ≤ 2, else 0.8 if y ≤ 5, else 0.6 if y ≤ 10, else 0.4
  Apply to `direct_score` only (not implied — implied is already discounted).
  Add decay note to gap report output.
  _Effort: 1 hr (Claude session — say "implement skill decay in matcher.py")_

- [ ] **P2-6 | Add LLM JD parsing (required vs. preferred split)**
  Implement Option C from `ARCHITECTURE.md` Q2 first (heuristic section detection).
  If that's insufficient: Option B (Claude API call per JD).
  Weight required skills 2×, preferred 1× in match% calculation.
  _Effort: 2 hrs_

- [ ] **P2-7 | Build `tools/job-scraper.py`**
  See `job-sources/scraping.md` for full design.
  Phase 1: Adzuna API + Reed API (both free, both open).
  Phase 2: Add Playwright for 5 company career pages (Synopsys, Cadence, ARM, Qualcomm, Google).
  Output: `job-tracker/new-this-week.md`
  _Effort: 3–4 hrs_
  _Say: "build the job scraper" to start this_

- [ ] **P2-8 | First real application**
  After P1-1 + P1-3: pick the role with the highest match% from the JD analysis.
  Complete `gap-analysis/jobs/[company]-[role].md` fully (gap table + why me + outreach plan).
  Apply. Update `job-tracker/applications.md`.
  _Effort: 1 hr_

---

## P3 — PHASE 2 ARCHITECTURE (next sprint)

Decide yes/no on each based on your answers to Architecture Review Questions.

- [ ] **P3-1 | NetworkX multi-hop inference** (`ARCHITECTURE.md` Q4)
  Load YAML → build DiGraph → BFS from current skills → find role reachability.
  Main output: "shortest learning path to [role]" sorted by transfer efficiency.
  _Say: "implement NetworkX graph traversal" to build_

- [ ] **P3-2 | Domain focus bonus in matcher** (`ARCHITECTURE.md` Q3)
  Add `focus_bonus: {domain: multiplier}` to roles-graph.yaml.
  Hardware-focused JD → hardware skills weighted 1.2× in match%.
  _Effort: 1 hr_

- [ ] **P3-3 | Claude API in pipeline** (`ARCHITECTURE.md` Q5)
  Hybrid: regex screens (free), Claude API narrates for ≥60% match roles.
  Outputs: gap narrative + "why me" bullets + LinkedIn post idea per role.
  _Effort: 2–3 hrs_

- [ ] **P3-4 | LinkedIn analytics log**
  Create `linkedin/analytics-log.md` — weekly record: SSI, views, InMails, post impressions.
  After 8 weeks: correlation between activity changes and InMail volume.
  _Effort: 15 min to create; 5 min/week to fill_

- [ ] **P3-5 | Resume cluster generation**
  Generate 5 role-cluster resumes from `profile/my-profile.yaml` + `ontology/roles-graph.yaml`.
  Each resume emphasizes the skills most valued by that cluster.
  ATS keyword density check against the cluster's top JDs.
  _Effort: 1 hr per cluster (Claude session)_

- [ ] **P3-6 | ESCO ontology mapping**
  Map Raja's skills to ESCO standard IDs.
  Enables: EU job portal compatibility, standardized skill vocabulary for CH/UK/EU applications.
  Download ESCO JSON-LD → add esco_id field to skills-graph.yaml nodes.
  _Effort: 3 hrs_

- [ ] **P3-7 | Market scan (20 JDs → frequency table)**
  Pull 20 real JDs for each target role cluster.
  Tag every requirement → fill `profile/market-scan.md` frequency table.
  Output: ranked list of skills by JD frequency (what the market actually wants).
  _Effort: 2 hrs_
  _Say: "run market scan for [role cluster]" to start_

---

## Someday / If-needed

- [ ] Salary intelligence auto-pull (Glassdoor / Levels.fyi scraping)
- [ ] Offer comparison model (total comp calculator)
- [ ] LinkedIn SSI correlation dashboard (matplotlib, weekly cron)
- [ ] Neo4j graph DB migration (only if YAML becomes unwieldy at >200 skills)
- [ ] GitHub Actions: weekly scraper run + auto-commit to job-tracker/

---

## Done

- [x] Repo created and pushed to GitHub (github.com/rajaghv-dev/apply)
- [x] Directory structure: profile/, gap-analysis/, evidence/, job-sources/, ontology/, tools/, network/, interview/, resume/, learning/, job-tracker/
- [x] Ontology: skills-graph.yaml (45+ nodes), roles-graph.yaml (14 clusters), domains.yaml (8 domains + unique bridges)
- [x] Matcher: tools/matcher.py (synonym extraction + weighted scoring + report)
- [x] Job sources: company-careers.md, aggregators.md, search-strategy.md, scraping.md
- [x] System gap analysis: gaps-and-improvements.md (10 gaps, 5 improvements)
- [x] Architecture: ARCHITECTURE.md (full system design + 6 open questions + 8 review questions)
- [x] Profile stubs: skills.md, linkedin.md, domains.md, questionnaire.md, my-profile.yaml, market-scan.md
- [x] Supporting modules: network/contacts.md, interview/prep.md, resume/README.md, learning/roadmap.md
- [x] Session protocol: context.md + sessions.md cold-start system
- [x] Memory in repo: _memory/ dir with all Claude context
